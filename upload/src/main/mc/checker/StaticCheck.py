#1711679

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

    def calculateBinOp(self, left, right, op):
        if left is None or right is None:
            return None
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left // right
        elif op == '%':
            return left % right
        else:
            return None

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
        for fun in lstFunc:
            if fun.name != 'main':
                raise UnreachableFunction(fun.name)
        
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
        [isReturn, isBreak] = self.visit(ast.body, [c[0], c[1], False, ast, isReturn, isBreak])
        if isReturn is False and type(ast.returnType) is not VoidType:
            raise FunctionNotReturn(ast.name.name)

    #c[0]: list environment
    #c[1]: danh sach ham chua duoc goi
    #c[2]: boolean: true neu stmt nay nam trong 1 vong lap
    #c[3]: AST: kieu tra ve cua function
    #c[4]: boolean, true neu da goi return
    #c[5]: boolean, true neu da goi break/continue
    #return[0]: boolean, true neu da goi return
    #return[1]: boolean, true neu da goi break/continue

    def visitBlock(self, ast, c):
        isReturn = False
        isBreak = False
        for x in ast.member:
            if isinstance(x, Block):
                [isReturn, isBreak] = self.visit(x, [[[]] + c[0], c[1], c[2], c[3], isReturn, isBreak])
            elif isinstance(x, Decl):
                self.visit(x, [c, Variable()])
            elif isinstance(x, Expr) is False:
                [isReturn, isBreak] = self.visit(x, [c[0], c[1], c[2], c[3], isReturn, isBreak])
            else:
                if isReturn is True or isBreak is True:
                    raise UnreachableStatement(x)
                self.visit(x, c)
        if c[4] or c[5]:
            raise UnreachableStatement(ast)
        return [isReturn, isBreak]

    def visitId(self, ast, c):
        IsDecl = False
        sym = None
        for envi in c[0]:
            sym = self.lookup(ast.name, envi, lambda x: x.name)
            if sym is not None and type(sym.mtype) is not MType:
                IsDecl = True
                break
        if IsDecl is False:
            raise Undeclared(Identifier(), ast.name)
        else:
            return [sym.mtype, None]

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
            if self.checkType(sym.mtype.partype[i], param[i][0]) is False:
                raise TypeMismatchInExpression(ast)
        sym1 = self.lookup(ast.method.name, c[1], lambda x: x.name)
        if sym1 is not None:
            if sym1.name != c[3].name.name:
                c[1].remove(sym1)
        return [sym.mtype.rettype, None]

    def visitArrayCell(self, ast, c):
        arr = self.visit(ast.arr, c)
        idx = self.visit(ast.idx, c)
        if type(idx[0]) is not IntType:
            raise TypeMismatchInExpression(ast)
        if type(arr[0]) is not ArrayType and type(arr[0]) is not ArrayPointerType:
            raise TypeMismatchInExpression(ast)
        if idx[1] is not None and type(arr[0]) is ArrayType:
            if idx[1] < 0 or idx[1] >= arr[0].dimen:
                raise IndexOutOfRange(ast)
        return [arr[0].eleType, None]

    def visitBinaryOp(self, ast, c):
        left = self.visit(ast.left, c)
        right = self.visit(ast.right, c)
        if isinstance(ast.left, LHS) is False and ast.op == '=':
            raise NotLeftValue(ast)
        if type(left[0]) == type(right[0]):
            if type(left[0]) is BoolType:
                if ast.op in ['==', '!=', '&&', '||', '=']:
                    return [BoolType(), None]
            if type(left[0]) is IntType:
                if ast.op in ['+', '-', '*', '/', '%', '=']:
                    return [IntType(), self.calculateBinOp(left[1], right[1], ast.op)]
                elif ast.op in ['<', '<=', '>', '>=', '==', '!=']:
                    return [BoolType(), None]
            if type(left[0]) is FloatType:
                if ast.op in ['+', '-', '*', '/', '=']:
                    return [FloatType(), None]
                elif ast.op in ['<', '<=', '>', '>=']:
                    return [BoolType(), None]
            raise TypeMismatchInExpression(ast)
        else:
            if type(left[0]) is IntType and type(right[0]) is FloatType:
                if ast.op in ['+', '-', '*', '/']:
                    return [FloatType(), None]
                elif ast.op in ['<', '<=', '>', '>=']:
                    return [BoolType(), None]
            if type(left[0]) is FloatType and type(right[0]) is IntType:
                if ast.op in ['+', '-', '*', '/', '=']:
                    return [FloatType(), None]
                elif ast.op in ['<', '<=', '>', '>=']:
                    return [FloatType(), None]
            raise TypeMismatchInExpression(ast)

    def visitUnaryOp(self, ast, c):
        body = self.visit(ast.body, c)
        if type(body[0]) is BoolType and ast.op == '!':
            return [BoolType(), not body[1] if body[1] is not None else None]
        elif type(body[0]) is IntType and ast.op == '-':
            return [IntType(), -body[1] if body[1] is not None else None]
        elif type(body[0]) is FloatType and ast.op == '-':
            return [FloatType(), -body[1] if body[1] is not None else None]
        raise TypeMismatchInExpression(ast)

    def visitIf(self, ast, c):
        if c[4] or c[5]:
            raise UnreachableStatement(ast)
        expr = self.visit(ast.expr, c)
        if type(expr[0]) is not BoolType:
            raise TypeMismatchInStatement(ast)
        isReturn = False
        isBreak = False
        [isReturn, isBreak] = self.visit(ast.thenStmt, [c[0], c[1], c[2], c[3], isReturn, isBreak])
        if ast.elseStmt is not None:
            isReturn1 = False
            isBreak1 = False
            [isReturn1, isBreak1] = self.visit(ast.elseStmt, [c[0], c[1], c[2], c[3], isReturn1, isBreak1])
            return [isReturn and isReturn1, isBreak and isBreak1]
        return [False, False]

    def visitFor(self, ast, c):
        expr1 = self.visit(ast.expr1, c)
        expr2 = self.visit(ast.expr2, c)
        expr3 = self.visit(ast.expr3, c)
        isReturn = False
        isBreak = False
        [isReturn, isBreak] = self.visit(ast.loop, [c[0], c[1], True, c[3], isReturn, isBreak])
        #self.visit(ast.loop, c)
        if type(expr1[0]) is not IntType or type(expr3[0]) is not IntType or type(expr2[0]) is not BoolType:
            raise TypeMismatchInStatement(ast)
        if c[4] or c[5]:
            raise UnreachableStatement(ast)
        return [False, False]

    def visitDowhile(self, ast, c):
        isReturn = False
        isBreak = False
        for x in ast.sl:
            if isinstance(x, Block):
                [isReturn, isBreak] = self.visit(x, [[[]] + c[0], c[1], True, c[3], isReturn, isBreak])
            elif isinstance(x, Expr) is False:
                [isReturn, isBreak] = self.visit(x, [c[0], c[1], True, c[3], isReturn, isBreak])
            else:
                if isReturn is True or isBreak is True:
                    raise UnreachableStatement(x)
                self.visit(x, c)
        exp = self.visit(ast.exp, c)
        if type(exp[0]) is not BoolType:
            raise TypeMismatchInStatement(ast)
        if c[4] or c[5]:
            raise UnreachableStatement(ast)
        return [isReturn, False]

    def visitBreak(self, ast, c):
        if c[2] is False:
            raise BreakNotInLoop()
        if c[4] or c[5]:
            raise UnreachableStatement(ast)
        return [False, True]

    def visitContinue(self, ast, c):
        if c[2] is False:
            raise ContinueNotInLoop()
        if c[4] or c[5]:
            raise UnreachableStatement(ast)
        return [False, True]

    def visitReturn(self, ast, c):
        if ast.expr is not None:
            exp = self.visit(ast.expr, c)
            #if type(exp) != type(c[3].returnType):
            if self.checkType(c[3].returnType, exp[0]) is False:
                raise TypeMismatchInStatement(ast)
        elif type(c[3].returnType) is not VoidType:
            raise TypeMismatchInStatement(ast)
        if c[4] or c[5]:
            raise UnreachableStatement(ast)
        return [True, False]

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
        return [IntType(), ast.value]
    
    def visitFloatLiteral(self, ast, c):
        return [FloatType(), ast.value]

    def visitStringLiteral(self, ast, c):
        return [StringType(), ast.value]

    def visitBooleanLiteral(self, ast, c):
        return [BoolType(), ast.value]
