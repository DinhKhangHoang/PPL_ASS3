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

    def test_Undeclare_021(self):
        input = """void main(){
            a =a + 1;
        }"""
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input, expect, 421))
    
    def test_Undeclare_022(self):
        input = """int a;
        void main(int b){
            a = a + 1;
            b = 0;
            b - 1;
        }"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 422))

    def test_Undeclare_023(self):
        input = """int a, b;
        void main(){
            a = 1;
            a =a + 1;
            b = 0;
            b - 1;
            c[8];
        }"""
        expect = "Undeclared Identifier: c"
        self.assertTrue(TestChecker.test(input, expect, 423))

    def test_Undeclare_024(self):
        input = """int a, b;
        void main(){
            a = 1;
            a =a + 1;
            b - 1;
            int c[9];
            {
                c[2] = 7;
                c[2] = c[2] + 1;
            }
        }"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 424))

    def test_Undeclare_025(self):
        input = """int a, b;
        void main(){
            a = 1;
            a =a + 1;
            b - 1;
            int c[9];
            if(true){
                c[2] = 7;
                c[2] = c[2] + 1;
            }
            else{
                d = true;
            }
        }"""
        expect = "Undeclared Identifier: d"
        self.assertTrue(TestChecker.test(input, expect, 425))

    def test_Undeclare_026(self):
        input = """int a, b;
        void main(){
            a = 1;
            a =a + 1;
            b - 1;
            int c[9];
            if(true){
                c[2] = 7;
                c[2] = c[2] + 1;
            }
            else{
                boolean d;
                d = true;
                putIntLn(100);
            }
        }"""
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 426))

    def test_Undeclare_027(self):
        input = """int a, b;
        void main(){
            a = 1;
            a =a + 1;
            b - 1;
            int c[9];
            for(a = 0; a < 10; a = a + 1){
                if (true){
                    d = 10;
                }
            }
        }"""
        expect = "Undeclared Identifier: d"
        self.assertTrue(TestChecker.test(input, expect, 427))

    def test_Undeclare_028(self):
        input = """int a, b;
        void main(){
            a = 1;
            a =a + 1;
            b - 1;
            int c[9];
            for(a = 0; a < 10; a = a + 1){
                if (true){
                   do{
                       d = 1;
                   }while(false);
                }
            }
        }"""
        expect = "Undeclared Identifier: d"
        self.assertTrue(TestChecker.test(input, expect, 428))

    def test_Undeclare_029(self):
        input = """int a, b;
        void main(){
            a = 1;
            a =a + 1;
            b - 1;
            int c[9];
            for(a = 0; a < 10; a = a + 1){
                int d;
                if (true){
                   do{
                       d = 1;
                   }while(false);
                   (-e + b)*a/a;
                }
            }
        }"""
        expect = "Undeclared Identifier: e"
        self.assertTrue(TestChecker.test(input, expect, 429))

    def test_Undeclare_030(self):
        input = """int a, b;
        void main(){
            a = 1;
            a =a + 1;
            b - 1;
            int c[9];
            for(a = 0; a < 10; a = a + 1){
                int d;
                if (true){
                   do{
                       d = 1;
                   }while(false);
                   add(a, b);
                }
            }
        }"""
        expect = "Undeclared Function: add"
        self.assertTrue(TestChecker.test(input, expect, 430))

    
    

    