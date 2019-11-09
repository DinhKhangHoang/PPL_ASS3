#1711679

from MCVisitor import MCVisitor
from MCParser import MCParser
from AST import *

class ASTGeneration(MCVisitor):

    def visitProgram(self, ctx: MCParser.ProgramContext):
        #program  : (decl)+ EOF;
        def flatten(lst):
            if lst == []:
                return []
            return lst[0]+ flatten(lst[1:]) if type(lst[0]) == list else [lst[0]] + flatten(lst[1:])

        return Program(flatten([self.visit(x) for x in ctx.decl()]))

    def visitDecl(self, ctx:MCParser.DeclContext):
        #decl : vardecl | funcdecl;
        return self.visit(ctx.getChild(0))

    def visitVardecl(self, ctx:MCParser.VardeclContext):
        #vardecl: primitivetype listvar SEMI ;
        return [VarDecl(x[0], ArrayType(x[1], self.visit(ctx.primitivetype()))) if len(x)==2 else VarDecl(x[0], self.visit(ctx.primitivetype())) for x in self.visit(ctx.listvar())]

    def visitPrimitivetype(self, ctx:MCParser.PrimitivetypeContext):
        #primitivetype: BOOLEAN|INTTYPE|FLOATTYPE|STRING;
        if ctx.BOOLEAN():
            return BoolType()
        elif ctx.INTTYPE():
            return IntType()
        elif ctx.FLOATTYPE():
            return FloatType()
        else:
            return StringType()

    def visitListvar(self, ctx:MCParser.ListvarContext):
        #listvar: var (CM var)*;
        return [self.visit(x) for x in ctx.var()]
    
    def visitVar(self, ctx:MCParser.VarContext):
        #var: ID (LSB INTLIT RSB)?;
        if ctx.INTLIT():
            return [ctx.ID().getText(),int(ctx.INTLIT().getText())]
        else:
            return [ctx.ID().getText()]
    
    """chua chac"""
    def visitFuncdecl(self, ctx:MCParser.FuncdeclContext):
        #funcdecl: functype funcname LB listparam RB blockstmt;
        return FuncDecl(self.visit(ctx.funcname()), self.visit(ctx.listparam()), self.visit(ctx.functype()), self.visit(ctx.blockstmt()))
    
    def visitFunctype(self, ctx:MCParser.FuncnameContext):
        #functype : primitivetype | VOIDTYPE | arraypointertype;
        return VoidType() if ctx.VOIDTYPE() else self.visit(ctx.getChild(0))

    def visitArraypointertype(self, ctx:MCParser.ArraypointertypeContext):
        #arraypointertype: primitivetype LSB RSB;
        return ArrayPointerType(self.visit(ctx.primitivetype()))

    def visitFuncname(self, ctx:MCParser.FuncnameContext):
        #funcname: ID;
        return Id(ctx.ID().getText())

    def visitListparam(self, ctx:MCParser.ListparamContext):
        #listparam: (paradecl (CM paradecl)*)?;
        return [self.visit(x) for x in ctx.paradecl()]
    '''chua chac'''
    def visitParadecl(self, ctx:MCParser.ParadeclContext):
        #paradecl: primitivetype ID (LSB RSB)?;
        if ctx.LSB():
            return VarDecl(ctx.ID().getText(), ArrayPointerType(self.visit(ctx.primitivetype())))
        else:
            return VarDecl(ctx.ID().getText(), self.visit(ctx.primitivetype()))
    '''chua chac'''
    def visitBlockstmt(self, ctx:MCParser.BlockstmtContext):
        #blockstmt: LP (vardecl | stmt)* RP;
        def flatten(lst):
            if lst == []:
                return []
            return lst[0]+ flatten(lst[1:]) if type(lst[0]) == list else [lst[0]] + flatten(lst[1:])

        lstChild = [ctx.getChild(i) for i in range(ctx.getChildCount())]
        #lstBlockMember = lstChild[1:-1]
        return Block(flatten([self.visit(x) for x in lstChild[1:-1]]))

    def visitStmt(self, ctx:MCParser.StmtContext):
        #stmt: ifstmt | whilestmt | forstmt | breakstmt | continuestmt | returnstmt | exprstmt | blockstmt;
        return self.visit(ctx.getChild(0))

    def visitIfstmt(self, ctx:MCParser.IfstmtContext):
        #ifstmt : IF LB expr RB stmt (ELSE stmt)?;
        if len(ctx.stmt()) == 1:
            return If(self.visit(ctx.expr()), self.visit(ctx.stmt(0)))
        else:
            return If(self.visit(ctx.expr()), self.visit(ctx.stmt(0)), self.visit(ctx.stmt(1)))

    def visitWhilestmt(self, ctx:MCParser.WhilestmtContext):
        #whilestmt: DO stmt+ WHILE expr SEMI;
        return Dowhile([self.visit(x) for x in ctx.stmt()], self.visit(ctx.getChild(ctx.getChildCount()-2)))

    def visitForstmt(self, ctx:MCParser.ForstmtContext):
        #forstmt: FOR LB expr SEMI expr SEMI expr RB stmt;
        return For(self.visit(ctx.expr(0)), self.visit(ctx.expr(1)), self.visit(ctx.expr(2)), self.visit(ctx.stmt()))

    def visitBreakstmt(self, ctx:MCParser.BreakstmtContext):
        #breakstmt: BREAK SEMI;
        return Break()

    def visitContinuestmt(self, ctx:MCParser.ContinuestmtContext):
        #continuestmt: CONTINUE SEMI;
        return Continue()

    def visitReturnstmt(self, ctx:MCParser.ReturnstmtContext):
        #returnstmt: RETURN expr? SEMI;
        return Return(self.visit(ctx.expr()) if ctx.expr() else None)

    def visitExprstmt(self, ctx:MCParser.ExprstmtContext):
        #exprstmt: expr SEMI;
        return self.visit(ctx.expr())

    def visitExpr(self, ctx:MCParser.ExprContext):
        #expr :  expr1 (EQ | NEQ) expr1
        #       | <assoc=left> expr AND expr
        #       | <assoc=left> expr OR expr
        #       | <assoc=right> expr ASSIGN expr
        #       | expr1;
        if ctx.ASSIGN():
            return BinaryOp(ctx.ASSIGN().getText(), self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))
        elif ctx.OR():
            return BinaryOp(ctx.OR().getText(), self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))
        elif ctx.AND():
            return BinaryOp(ctx.AND().getText(), self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))
        elif ctx.EQ() or ctx.NEQ():
            return BinaryOp(ctx.getChild(1).getText(), self.visit(ctx.expr1(0)), self.visit(ctx.expr1(1)))
        else:
            return self.visit(ctx.expr1(0))
        
    def visitExpr1(self, ctx:MCParser.Expr1Context):
        #expr1:  expr2 (LT | LE | GT | GE) expr2
        #       | expr2;
        if ctx.getChildCount() == 3:
            return BinaryOp(ctx.getChild(1).getText(), self.visit(ctx.expr2(0)), self.visit(ctx.expr2(1)))
        else:
            return self.visit(ctx.expr2(0))

    def visitExpr2(self, ctx:MCParser.Expr2Context):
        #expr2:  operand LSB expr RSB
        #       | <assoc=right> (SUB | NOT) expr2
        #       | <assoc=left> expr2 (DIV | MUL | MOD) expr2
        #       | <assoc=left> expr2 (ADD | SUB) expr2
        #       | operand;
        if ctx.getChildCount() == 3:
            return BinaryOp(ctx.getChild(1).getText(), self.visit(ctx.expr2(0)), self.visit(ctx.expr2(1)))
        elif ctx.getChildCount() == 2:
            return UnaryOp(ctx.getChild(0).getText(), self.visit(ctx.expr2(0)))
        elif ctx.getChildCount() == 4:
            return ArrayCell(self.visit(ctx.operand()), self.visit(ctx.expr()))
        else:
            return self.visit(ctx.operand())

    def visitOperand(self, ctx:MCParser.OperandContext):
        #operand: LB expr RB | INTLIT | BOOLLIT | FLOATLIT | STRINGLIT | funcall | ID;
        if ctx.getChildCount() == 3:
            return self.visit(ctx.expr())
        elif ctx.funcall():
            return self.visit(ctx.funcall())
        elif ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.BOOLLIT():
            if ctx.BOOLLIT().getText() == "true":
                return BooleanLiteral(True)
            else:
                return BooleanLiteral(False)
        elif ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif ctx.STRINGLIT():
            return StringLiteral(ctx.STRINGLIT().getText())
        else:
            return Id(ctx.ID().getText())
    
    def visitFuncall(self, ctx:MCParser.FuncallContext):
        #funcall: ID LB listarg RB;
        return CallExpr(Id(ctx.ID().getText()), self.visit(ctx.listarg()))

    def visitListarg(self, ctx:MCParser.ListargContext):
        #listarg: (expr (CM expr)*)? ;
            return [self.visit(x) for x in ctx.expr()] if ctx.expr() else []