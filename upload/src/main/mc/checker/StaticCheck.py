
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
                return Symbol(decl.variable, [decl.varType.eleType, decl.varType.dimen], Variable())
            elif type(decl.varType) == ArrayPointerType:
                return Symbol(decl.variable, [decl.varType.eleType], Variable())
            else:
                return Symbol(decl.variable, decl.varType, Variable())
        elif type(decl) == FuncDecl:
            if type(decl.returnType) == ArrayPointerType:
                return Symbol(decl.name.name, MType([x.varType for x in decl.param],[decl.returnType.eleType]), Function())
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
        self.visit(ast.body, c)

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
        for envi in c[0]:
            if self.lookup(ast.name, envi, lambda x: x.name):
                IsDecl = True
                break
        if IsDecl is False:
            raise Undeclared(Identifier(), ast.name)

    def visitCallExpr(self, ast, c):
        IsDecl = False
        
        if self.lookup(ast.method.name, c[0][-1], lambda x: x.name):
            IsDecl = True
                
        if IsDecl is False:
            raise Undeclared(Function(), ast.method.name)
    
    def visitArrayCell(self, ast, c):
        self.visit(ast.arr, c)
        self.visit(ast.idx, c)

    def visitBinaryOp(self, ast, c):
        self.visit(ast.left, c)
        self.visit(ast.right, c)

    def visitUnaryOp(self, ast, c):
        self.visit(ast.body, c)

    def visitIf(self, ast, c):
        self.visit(ast.expr, c)
        self.visit(ast.thenStmt, c)
        if ast.elseStmt is not None:
            self.visit(ast.elseStmt, c)

    def visitFor(self, ast, c):
        self.visit(ast.expr1, c)
        self.visit(ast.expr2, c)
        self.visit(ast.expr3, c)
        self.visit(ast.loop, c)

    def visitDowhile(self, ast, c):
        for x in ast.sl:
            self.visit(x, c)
        self.visit(ast.exp, c)

    def visitBreak(self, ast, c):
        return Break()

    def visitContinue(self, ast, c):
        return Continue()

    def visitReturn(self, ast, c):
        if ast.exp is not None:
            self.visit(ast.exp, c)

    def visitArrayType(self, ast, c):
        return [ast.eleType, ast.dimen]

    def visitArrayPointerType(self, ast, c):
        return [ast.eleType]

    def visitStringType(self, ast, c):
        return StringType()
    
    def visitIntType(self, ast, c):
        return IntType()

    def visitFloatType(self, ast, c):
        return FloatType()
    
    def visitBoolType(self, ast, c):
        return BoolType()
    
    def visitIntLiteral(self,ast, c): 
        return ast.value
    
    def visitFloatLiteral(self, ast, c):
        return ast.value

    def visitStringLiteral(self, ast, c):
        return ast.value

    def visitBooleanLiteral(self, ast, c):
        return ast.value

    
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


    
