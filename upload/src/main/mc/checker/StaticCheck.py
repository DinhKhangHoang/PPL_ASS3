
"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *

class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
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
            return Symbol(decl.variable, decl.VarType)
        elif type(decl) == FuncDecl:
            return Symbol(decl.name.name, MType([x.VarType for x in decl.param],decl.ReturnType))

    def toLstSymbol(self, lstDecl, lstSym, kind, lstGlobal=None, lstFunc=None):
        for x in lstDecl:
            sym = self.convertToSymbol(x)
            res = self.lookup(sym.name, lstSym, lambda x: x.name)
            res1 = None
            if

    def visitProgram(self,ast, c): 
        #return [self.visit(x,c) for x in ast.decl]
        lstFunc = []
        lstGlobal = []
        self.toLstSymbol(ast.decl, lstGlobal, None, c, lstFunc)


    def visitFuncDecl(self,ast, c): 
        return list(map(lambda x: self.visit(x,(c,True)),ast.body.member)) 
    

    def visitCallExpr(self, ast, c): 
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
            return res.mtype.rettype

    def visitIntLiteral(self,ast, c): 
        return IntType()
    

