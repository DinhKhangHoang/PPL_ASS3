
"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce

class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

class Symbol:
    def __init__(self,name,mtype,kind = None, value = None):
        self.name = name
        self.mtype = mtype
        self.kind = kind
        self.value = value

class StaticChecker(BaseVisitor,Utils):

    global_envi = [
    Symbol("getInt",MType([],IntType())),
    Symbol("putIntLn",MType([IntType()],VoidType())),
    Symbol("putInt",MType([IntType()],VoidType())),
    Symbol("getFloat",MType([],FloatType())),
    Symbol("putFloat",MType([FloatType()],VoidType())),
    Symbol("putFloatLn",MType([FloatType()],VoidType())),
    Symbol("putBool",MType([BoolType()],VoidType())),
    Symbol("putBoolLn",MType([BoolType()],VoidType())),
    Symbol("putString",MType([StringType()],VoidType())),
    Symbol("putStringLn",MType([StringType()],VoidType())),
    Symbol("putLn",MType([],VoidType()))
    ]
            
    
    def __init__(self,ast):
        #print(ast)
        #print(ast)
        #print()
        self.ast = ast

    def check(self):
        return self.visit(self.ast,StaticChecker.global_envi)

    def convertToSymbol(self, decl):
        if type(decl) == VarDecl:
            if type(decl.varType) == ArrayType:
                return Symbol(decl.variable, ArrayType(decl.varType.dimen, decl.varType.eleType), Variable())
            elif type(decl.varType) == ArrayPointerType:
                return Symbol(decl.variable, ArrayPointerType(decl.varType.eleType), Variable())
            else:
                return Symbol(decl.variable, decl.varType, Variable())
        elif type(decl) == FuncDecl:
            if type(decl.returnType) == ArrayPointerType:
                return Symbol(decl.name.name, MType([x.varType for x in decl.param], ArrayPointerType(decl.returnType.eleType)), Function())
            return Symbol(decl.name.name, MType([x.varType for x in decl.param],decl.returnType), Function())

    def getGlobal(self, lstDecl, lstGlobal, c, lstFunc):
        for x in lstDecl:
            sym = self.convertToSymbol(x)
            res = self.lookup(sym.name, c, lambda x: x.name)
            if res is None:
                res1 = self.lookup(sym.name, lstGlobal, lambda x: x.name)
                if res1 is None:
                    lstGlobal.insert(0, sym)
                    if isinstance(sym.mtype, MType):
                        lstFunc.insert(0,sym)
                elif type(sym.mtype) == MType:
                    raise Redeclared(Function(), sym.name)
                else:
                    raise Redeclared(Variable(), sym.name)
            else:
                if type(sym.mtype) == MType:
                    raise Redeclared(Function(), sym.name)
                else:
                    raise Redeclared(Variable(), sym.name)


    def checkEntryPoint(self, lstFunc):
        if self.lookup("main", lstFunc, lambda x: x.name) is None:
            raise NoEntryPoint()

    def checkType(self, left, right):
        if type(left) == type(right):
            if type(left) is ArrayPointerType:
                if type(left.eleType) == type(right.eleType):
                    return True
                else:
                    return False
            return True
        elif type(left) is FloatType and type(right) is IntType:
            return True
        elif type(left) is ArrayPointerType and type(right) is ArrayType:
            if type(left.eleType) == type(right.eleType):
                return True
            else:
                return False
        else:
            return False

    def visitProgram(self,ast, c): 
        #return [self.visit(x,c) for x in ast.decl]
        lstFunc = []
        lstenvi = [[]]
        self.getGlobal(ast.decl, lstenvi[0], c, lstFunc)
        self.checkEntryPoint(lstenvi[0])
        lstenvi[0] += c
        
        for x in ast.decl:
            if isinstance(x, FuncDecl):
                self.visit(x, [[[]] + lstenvi, lstFunc])
        
    def visitVarDecl(self, ast, c):
        if self.lookup(ast.variable, c[0][0][0], lambda x: x.name):
            if isinstance(c[1], Parameter):
                raise Redeclared(Parameter(), ast.variable)
            else:
                raise Redeclared(Variable(), ast.variable)
        c[0][0][0].insert(0, Symbol(ast.variable, self.visit(ast.varType, c), Variable()))
        
    def visitFuncDecl(self,ast, c): 
        for x in ast.param:
            self.visit(x, [c, Parameter()])
        isReturn = False
        isBreak = False
        self.visit(ast.body, [c[0], c[1], False, ast, isReturn, isBreak])

    #c[0]: list environment
    #c[1]: danh sach ham chua duoc goi
    #c[2]: boolean: true neu stmt nay nam trong 1 vong lap
    #c[3]: AST: kieu tra ve cua function
    #c[4]: boolean, true neu da goi return
    #c[5]: boolean, true neu da goi break/continue
    #return[0]: boolean, true neu da goi return
    #return[1]: boolean, true neu da goi break/continue

    def visitBlock(self, ast, c):
        for x in ast.member:
            if isinstance(x, Block):
                self.visit(x, [[[]] + c[0]] + c[1:])
            elif isinstance(x, Decl):
                self.visit(x, [c, Variable()])
            else:
                self.visit(x, c)

    def visitId(self, ast, c):
        IsDecl = False
        sym = None
        for envi in c[0]:
            sym = self.lookup(ast.name, envi, lambda x: x.name)
            if sym is not None:
                IsDecl = True
                break
        if IsDecl is False:
            raise Undeclared(Identifier(), ast.name)
        else:
            return sym.mtype

    def visitCallExpr(self, ast, c):
        param = [self.visit(x, c) for x in ast.param]
        sym = self.lookup(ast.method.name, c[0][-1], lambda x: x.name)
        if sym is None:
            raise Undeclared(Function(), ast.method.name)
        if type(sym.mtype) is not MType:
            raise Undeclared(Function(), ast.method.name)
        if len(sym.mtype.partype) != len(param):
            raise TypeMismatchInExpression(ast)
        for i in range(len(sym.mtype.partype)):
            if self.checkType(sym.mtype.partype[i], param[i]) is False:
                raise TypeMismatchInExpression(ast)
        return sym.mtype.rettype

    def visitArrayCell(self, ast, c):
        arr = self.visit(ast.arr, c)
        idx = self.visit(ast.idx, c)
        if type(idx) is not IntType:
            raise TypeMismatchInExpression(ast)
        if type(arr) is not ArrayType and type(arr) is not ArrayPointerType:
            raise TypeMismatchInExpression(ast)
        return arr.eleType

    def visitBinaryOp(self, ast, c):
        left = self.visit(ast.left, c)
        right = self.visit(ast.right, c)
        if type(left) == type(right):
            if type(left) is BoolType:
                if ast.op in ['==', '!=', '&&', '||', '=']:
                    return BoolType()
            if type(left) is IntType:
                if ast.op in ['+', '-', '*', '/', '%', '=']:
                    return IntType()
                elif ast.op in ['<', '<=', '>', '>=', '==', '!=']:
                    return BoolType()
            if type(left) is FloatType:
                if ast.op in ['+', '-', '*', '/', '=']:
                    return FloatType()
                elif ast.op in ['<', '<=', '>', '>=']:
                    return BoolType()
            raise TypeMismatchInExpression(ast)
        else:
            if type(left) is IntType and type(right) is FloatType:
                if ast.op in ['+', '-', '*', '/']:
                    return FloatType()
                elif ast.op in ['<', '<=', '>', '>=']:
                    return BoolType()
            if type(left) is FloatType and type(right) is IntType:
                if ast.op in ['+', '-', '*', '/', '=']:
                    return FloatType()
                elif ast.op in ['<', '<=', '>', '>=']:
                    return FloatType()
            raise TypeMismatchInExpression(ast)

    def visitUnaryOp(self, ast, c):
        body = self.visit(ast.body, c)
        if type(body) is BoolType and ast.op == '!':
            return BoolType()
        elif type(body) is IntType and ast.op == '-':
            return IntType()
        elif type(body) is FloatType and ast.op == '-':
            return FloatType()
        raise TypeMismatchInExpression(ast)

    def visitIf(self, ast, c):
        expr = self.visit(ast.expr, c)
        self.visit(ast.thenStmt, c)
        if ast.elseStmt is not None:
            self.visit(ast.elseStmt, c)
        if type(expr) is not BoolType:
            raise TypeMismatchInStatement(ast)

    def visitFor(self, ast, c):
        expr1 = self.visit(ast.expr1, c)
        expr2 = self.visit(ast.expr2, c)
        expr3 = self.visit(ast.expr3, c)
        self.visit(ast.loop, c)
        if type(expr1) is not IntType or type(expr3) is not IntType or type(expr2) is not BoolType:
            raise TypeMismatchInStatement(ast)

    def visitDowhile(self, ast, c):
        for x in ast.sl:
            if isinstance(x, Block):
                self.visit(x, [[[]] + c[0]] + c[1:])
            else:
                self.visit(x, c)
        exp = self.visit(ast.exp, c)
        if type(exp) is not BoolType:
            raise TypeMismatchInStatement(ast)

    def visitBreak(self, ast, c):
        return Break()

    def visitContinue(self, ast, c):
        return Continue()

    def visitReturn(self, ast, c):
        if ast.expr is not None:
            exp = self.visit(ast.expr, c)
            #if type(exp) != type(c[3].returnType):
            if self.checkType(c[3].returnType, exp) is False:
                raise TypeMismatchInStatement(ast)
        elif type(c[3].returnType) is not VoidType:
            raise TypeMismatchInStatement(ast)

    def visitArrayType(self, ast, c):
        return ArrayType(ast.dimen, ast.eleType)

    def visitArrayPointerType(self, ast, c):
        return ArrayPointerType(ast.eleType)

    def visitStringType(self, ast, c):
        return StringType()
    
    def visitIntType(self, ast, c):
        return IntType()

    def visitFloatType(self, ast, c):
        return FloatType()
    
    def visitBoolType(self, ast, c):
        return BoolType()
    
    def visitIntLiteral(self,ast, c): 
        return IntType()
    
    def visitFloatLiteral(self, ast, c):
        return FloatType()

    def visitStringLiteral(self, ast, c):
        return StringType()

    def visitBooleanLiteral(self, ast, c):
        return BoolType()

    
    """def visitCallExpr(self, ast, c): 
        at = [self.visit(x,(c[0],False)) for x in ast.param]
        
        res = self.lookup(ast.method.name,c[0],lambda x: x.name)
        if res is None or not type(res.mtype) is MType:
            raise Undeclared(Function(),ast.method.name)
        elif len(res.mtype.partype) != len(at):
            if c[1]:
                raise TypeMismatchInStatement(ast)
            else:
                raise TypeMismatchInExpression(ast)
        else:
            return res.mtype.rettype"""


    
