import unittest
from TestUtils import TestChecker
from AST import *

class CheckSuite(unittest.TestCase):
    
    def test_Redeclare_Var_001(self):
        """Simple program: int main() {} """
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("main"), [], VoidType(),
                            Block([])),
                        VarDecl("a", IntType())])
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,401))
    
    def test_Redeclare_Var_002(self):
        input = Program([VarDecl("a", IntType()),
                        VarDecl("b", IntType()),
                        FuncDecl(Id("main"), [], VoidType(), Block([])),
                        VarDecl("b", IntType())])
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input,expect,402))

    def test_Redeclare_Func_003(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("putIntLn"), [], VoidType(), Block([])),
                        FuncDecl(Id("main"), [], VoidType(), Block([])),
                        VarDecl("b", IntType())])
        expect = "Redeclared Function: putIntLn"
        self.assertTrue(TestChecker.test(input,expect,403))

    def test_Redeclare_Func_004(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("putFloatLn"), [], VoidType(), Block([])),
                        FuncDecl(Id("main"), [], VoidType(), Block([])),
                        VarDecl("b", IntType())])
        expect = "Redeclared Function: putFloatLn"
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_Redeclare_Var_005(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("main"), [], VoidType(),
                            Block([VarDecl("b", IntType()),
                                VarDecl("b", IntType())])),
                        VarDecl("b", IntType())])
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input,expect,405))

    def test_Redeclare_Var_006(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("main"), [], VoidType(),
                            Block([VarDecl("b", IntType()),
                                VarDecl("b", IntType())]))])
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_Redeclare_Var_007(self):
        input = Program([VarDecl("a", IntType()), 
                        FuncDecl(Id("main"), [], VoidType(),
                            Block([VarDecl("b", IntType()),
                                Block([VarDecl("b", IntType())])]))])
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,407))

    def test_Redeclare_Var_008(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("main"), [], VoidType(),
                            Block([VarDecl("c", IntType()),
                                Block([VarDecl("b", IntType()),
                                    VarDecl("b", IntType())])]))])
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input,expect,408))

    def test_Redeclare_Var_009(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("main"), [], VoidType(),
                            Block([VarDecl("c", IntType()),
                                Block([VarDecl("b", IntType()),
                                    VarDecl("d", IntType())]),
                                Block([VarDecl("e", IntType()),
                                    VarDecl("e", IntType())])]))])
        expect = "Redeclared Variable: e"
        self.assertTrue(TestChecker.test(input,expect,409))

    def test_Redeclare_Var_010(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("main"), [], VoidType(),
                            Block([VarDecl("c", IntType()),
                                Block([VarDecl("b", IntType()),
                                    VarDecl("d", IntType())]),
                                Block([VarDecl("e", IntType()),
                                    VarDecl("f", IntType())]),
                                VarDecl("c", IntType())]))])
        expect = "Redeclared Variable: c"
        self.assertTrue(TestChecker.test(input,expect,410))

    def test_Redeclare_Var_011(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("main"), [], VoidType(),
                            Block([VarDecl("c", IntType()),
                                Block([VarDecl("b", IntType()),
                                    VarDecl("c", IntType()),
                                    VarDecl("d", IntType())]),
                                Block([VarDecl("e", IntType()),
                                    VarDecl("f", IntType())]),
                                ]))])
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,411))

    def test_Redeclare_Var_012(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("main"), [], VoidType(),
                            Block([VarDecl("c", IntType()),
                                Block([VarDecl("b", IntType()),
                                    VarDecl("d", IntType())]),
                                VarDecl("c", IntType()),
                                Block([VarDecl("e", IntType()),
                                    VarDecl("f", IntType())]),
                                ]))])
        expect = "Redeclared Variable: c"
        self.assertTrue(TestChecker.test(input,expect,412))

    def test_Redeclare_Var_013(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("main"), [], VoidType(),
                            Block([VarDecl("c", IntType()),
                                Block([VarDecl("b", IntType()),
                                    Block([VarDecl("g", IntType()),
                                        VarDecl("b", IntType()),
                                        VarDecl("g", IntType())]),
                                    VarDecl("d", IntType())]),
                                Block([VarDecl("e", IntType()),
                                    VarDecl("f", IntType())]),
                                ]))])
        expect = "Redeclared Variable: g"
        self.assertTrue(TestChecker.test(input,expect,413))

    def test_Redeclare_Var_014(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("main"), [], VoidType(),
                            Block([VarDecl("g", IntType()),
                                Block([VarDecl("b", IntType()),
                                    Block([VarDecl("g", IntType()),
                                        VarDecl("b", IntType()),
                                        VarDecl("g", IntType())]),
                                    VarDecl("d", IntType())]),
                                Block([VarDecl("e", IntType()),
                                    VarDecl("f", IntType())]),
                                ]))])
        expect = "Redeclared Variable: g"
        self.assertTrue(TestChecker.test(input,expect,414))

    def test_Redeclare_Param_015(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("main"), [VarDecl("g", IntType()), VarDecl("g", IntType())], VoidType(),
                            Block([VarDecl("g", IntType()),
                                Block([VarDecl("b", IntType()),
                                    Block([VarDecl("g", IntType()),
                                        VarDecl("b", IntType()),
                                        ]),
                                    VarDecl("d", IntType())]),
                                Block([VarDecl("e", IntType()),
                                    VarDecl("f", IntType())]),
                                ]))])
        expect = "Redeclared Parameter: g"
        self.assertTrue(TestChecker.test(input,expect,415))

    def test_Redeclare_Param_016(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("main"), [VarDecl("g", IntType())], VoidType(),
                            Block([VarDecl("g", IntType()),
                                Block([VarDecl("b", IntType()),
                                    Block([VarDecl("g", IntType()),
                                        VarDecl("b", IntType()),
                                        ]),
                                    VarDecl("d", IntType())]),
                                Block([VarDecl("e", IntType()),
                                    VarDecl("f", IntType())]),
                                ]))])
        expect = "Redeclared Variable: g"
        self.assertTrue(TestChecker.test(input,expect,416))

    def test_Redeclare_Param_017(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("main"), [VarDecl("g", IntType())], VoidType(),
                            Block([VarDecl("h", IntType()),
                                Block([VarDecl("b", IntType()),
                                    Block([VarDecl("g", IntType()),
                                        VarDecl("b", IntType()),
                                        ]),
                                    VarDecl("d", IntType())]),
                                Block([VarDecl("e", IntType()),
                                    VarDecl("f", IntType())]),
                                ]))])
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,417))

    def test_NoEntryPoint_018(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("hihihaha"), [VarDecl("g", IntType())], VoidType(),
                            Block([VarDecl("h", IntType()),
                                Block([VarDecl("b", IntType()),
                                    Block([VarDecl("g", IntType()),
                                        VarDecl("b", IntType()),
                                        ]),
                                    VarDecl("d", IntType())]),
                                Block([VarDecl("e", IntType()),
                                    VarDecl("f", IntType())]),
                                ]))])
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input,expect,418))

    def test_NoEntryPoint_019(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("fun"), [], VoidType(),
                            Block([]))])
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input,expect,419))

    def test_NoEntryPoint_020(self):
        input = Program([VarDecl("a", IntType()),
                        FuncDecl(Id("fun"), [], VoidType(),
                            Block([])),
                        FuncDecl(Id("bored"), [], VoidType(),
                            Block([]))])
                        
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input,expect,420))

    
    