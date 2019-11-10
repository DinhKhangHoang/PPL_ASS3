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
            a = 1;
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
            int b;
            b = -2;
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
        }
        """
        expect = "Undeclared Function: add"
        self.assertTrue(TestChecker.test(input, expect, 430))

    def test_TypeMissMatchInStmt_031(self):
        input = """int a, b;
        void main(){
            return 3;
        }
        """
        expect = "Type Mismatch In Statement: Return(IntLiteral(3))"
        self.assertTrue(TestChecker.test(input, expect, 431))

    def test_TypeMissMatchInStmt_032(self):
        input = """int a, b;
        void main(){
            a = 0;
            b = 8;
            float f;
            f = 7.8;
            if(f){

            }
        }
        """
        expect = "Type Mismatch In Statement: If(Id(f),Block([]))"
        self.assertTrue(TestChecker.test(input, expect, 432))

    def test_TypeMissMatchInStmt_033(self):
        input = """int a, b;
        void main(){
            a = 0;
            b = 8;
            float f;
            f = 7.8;
            if (a){

            }
            else{

            }
        }
        """
        expect = "Type Mismatch In Statement: If(Id(a),Block([]),Block([]))"
        self.assertTrue(TestChecker.test(input, expect, 433))

    def test_TypeMissMatchInStmt_034(self):
        input = """int a, b;
        void main(){
            a = 0;
            b = 8;
            float f;
            f = 7.8;
            do{
                boolean f;
                f = true;
            }
            while(f);
        }
        """
        expect = "Type Mismatch In Statement: Dowhile([Block([VarDecl(f,BoolType),BinaryOp(=,Id(f),BooleanLiteral(true))])],Id(f))"
        self.assertTrue(TestChecker.test(input, expect, 434))

    def test_TypeMissMatchInStmt_035(self):
        input = """int a, b;
        void main(){
            a = 0;
            b = 8;
            float f;
            f = 7.8;
            do{
                do{
                    f = f + 1;
                }while(f);
            }while(true);
        }
        """
        expect = "Type Mismatch In Statement: Dowhile([Block([BinaryOp(=,Id(f),BinaryOp(+,Id(f),IntLiteral(1)))])],Id(f))"
        self.assertTrue(TestChecker.test(input, expect, 435))

    def test_TypeMissMatchInStmt_036(self):
        input = """int a, b;
        void main(){
            a = 0;
            b = 8;
            float f;
            f = 7.8;
            do{
                do{
                    f = f + 1;
                }while(a);
            }while(true);
        }
        """
        expect = "Type Mismatch In Statement: Dowhile([Block([BinaryOp(=,Id(f),BinaryOp(+,Id(f),IntLiteral(1)))])],Id(a))"
        self.assertTrue(TestChecker.test(input, expect, 436))

    def test_TypeMissMatchInStmt_037(self):
        input = """int a, b;
        void main(){
            a = 0;
            b = 8;
            float f;
            f = 7.8;
            do{
                boolean f;
            }
            {
                boolean f;
            }while(f);
        }
        """
        expect = "Type Mismatch In Statement: Dowhile([Block([VarDecl(f,BoolType)]),Block([VarDecl(f,BoolType)])],Id(f))"
        self.assertTrue(TestChecker.test(input, expect, 437))

    def test_TypeMissMatchInStmt_038(self):
        input = """int a, b;
        void main(){
            a = 0;
            b = 8;
            float f;
            f = 7.8;
            int i;
            for(i = 0; i < 10; i = i + 1){
                boolean a;
                a = true;
                a + 1;
            }
        }
        """
        expect = "Type Mismatch In Expression: BinaryOp(+,Id(a),IntLiteral(1))"
        self.assertTrue(TestChecker.test(input, expect, 438))

    def test_TypeMissMatchInStmt_039(self):
        input = """int a, b;
        void main(){
            a = 0;
            b = 8;
            float f;
            f = 7.8;
            int i;
            for(i = 0; i - 7; i = i + 1){
                boolean a;
                a = true;
            }
        }
        """
        expect = "Type Mismatch In Statement: For(BinaryOp(=,Id(i),IntLiteral(0));BinaryOp(-,Id(i),IntLiteral(7));BinaryOp(=,Id(i),BinaryOp(+,Id(i),IntLiteral(1)));Block([VarDecl(a,BoolType),BinaryOp(=,Id(a),BooleanLiteral(true))]))"
        self.assertTrue(TestChecker.test(input, expect, 439))

    def test_TypeMissMatchInStmt_040(self):
        input = """int a, b;
        void main(){
            a = 0;
            b = 8;
            float f;
            f = 7.8;
            float i;
            for(i = 0; i < 10; i = i + 1){
                boolean a;
                a = true;
            }
        }
        """
        expect = "Type Mismatch In Statement: For(BinaryOp(=,Id(i),IntLiteral(0));BinaryOp(<,Id(i),IntLiteral(10));BinaryOp(=,Id(i),BinaryOp(+,Id(i),IntLiteral(1)));Block([VarDecl(a,BoolType),BinaryOp(=,Id(a),BooleanLiteral(true))]))"
        self.assertTrue(TestChecker.test(input, expect, 440))

    def test_TypeMissMatchInStmt_041(self):
        input = """int a, b;
        void main(){
            a = 0;
            b = 8;
            float f;
            f = 7.8;
            int i;
            for(i = 0; i < 10; i = i + 1){
                boolean a;
                a = true;
            }
        }
        float add(float a, float b){
            return true;
        }
        """
        expect = "Type Mismatch In Statement: Return(BooleanLiteral(true))"
        self.assertTrue(TestChecker.test(input, expect, 441))

    def test_TypeMissMatchInExpr_042(self):
        input = """int a, b;
        void main(){
            float f;
            f = 7.8;
            int i;
            for(i = 0; i < 10; i = i + 1){
                boolean a;
                a = add(2,3);
            }
        }
        float add(float a, float b){
            return a + b;
        }
        """
        expect = "Type Mismatch In Expression: BinaryOp(=,Id(a),CallExpr(Id(add),[IntLiteral(2),IntLiteral(3)]))"
        self.assertTrue(TestChecker.test(input, expect, 442))

    def test_TypeMissMatchInExpr_043(self):
        input = """int a, b;
        void main(){
            float f;
            f = 7.8;
            int i;
            for(i = 0; i < 10; i = i + 1){
                boolean a;
                i = getInt();
                a = getFloat();
            }
        }
        float add(float a, float b){
            return a + b;
        }
        """
        expect = "Type Mismatch In Expression: BinaryOp(=,Id(a),CallExpr(Id(getFloat),[]))"
        self.assertTrue(TestChecker.test(input, expect, 443))

    def test_TypeMissMatchInExpr_044(self):
        input = """int a, b;
        void main(){
            float f;
            f = 7.8;
            boolean check;
            check = f;
        }
        float add(float a, float b){
            return a + b;
        }
        """
        expect = "Type Mismatch In Expression: BinaryOp(=,Id(check),Id(f))"
        self.assertTrue(TestChecker.test(input, expect, 444))

    def test_TypeMissMatchInExpr_045(self):
        input = """int a, b;
        void main(){
            float f;
            f = 7.8;
            boolean check;
            f = add( 3.5, 8.9);
        }
        float[] add(float a, float b){
            return a + b;
        }
        """
        expect = "Type Mismatch In Expression: BinaryOp(=,Id(f),CallExpr(Id(add),[FloatLiteral(3.5),FloatLiteral(8.9)]))"
        self.assertTrue(TestChecker.test(input, expect, 445))

    def test_TypeMissMatchInExpr_046(self):
        input = """int a, b;
        void main(){
            float f[8];
            f[0] = 7.8;
            boolean check;
            f = add( 3.5, 8.9);
        }
        float[] add(float a, float b){
            float c[1];
            return c;
        }
        """
        expect = "Type Mismatch In Expression: BinaryOp(=,Id(f),CallExpr(Id(add),[FloatLiteral(3.5),FloatLiteral(8.9)]))"
        self.assertTrue(TestChecker.test(input, expect, 446))

    def test_TypeMissMatchInExpr_047(self):
        input = """int a, b;
        void main(){
            float f[8];
            f[0] = 7.8;
            boolean check;
            add( 3.5, 8.9)[7];
        }
        float[] add(float a, float b){
            float c[1];
            return c;
        }
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 447))

    def test_TypeMissMatchInExpr_048(self):
        input = """int a, b;
        void main(){
            float f[8];
            f[0] = 7.8;
            boolean check;
            add(f, 8.9)[7];
        }
        float[] add(float a[], float b){
            float c[1];
            return a;
        }
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 448))

    def test_TypeMissMatchInExpr_049(self):
        input = """int a, b;
        void main(int argc[]){
            float f[8];
            f[0] = 7.8;
            boolean check;
            add(f, f)[7];
        }
        float[] add(float a[], float b[]){
            float c[1];
            return a;
        }
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 449))

    def test_FunctionNotReturn_050(self):
        input = """int a, b;
        void main(int argc[]){
            float f[8];
            f[0] = 7.8;
            boolean check;
            add(f, f)[7];
        }
        float[] add(float a[], float b[]){
            float c[1];
            //return a;
        }
        """
        expect = "Function add Not Return "
        self.assertTrue(TestChecker.test(input, expect, 450))

    def test_FunctionNotReturn_051(self):
        input = """int a, b;
        void main(int argc[]){
            float f[8];
            f[0] = 7.8;
            boolean check;
            add(f, f)[7];
        }
        float[] add(float a[], float b[]){
            float c[1];
            boolean check;
            check = false;
            if(check){
                return a;
            }
        }
        """
        expect = "Function add Not Return "
        self.assertTrue(TestChecker.test(input, expect, 451))

    def test_FunctionNotReturn_052(self):
        input = """int a, b;
        void main(int argc[]){
            float f[8];
            f[0] = 7.8;
            boolean check;
            add(f, f)[7];
        }
        float[] add(float a[], float b[]){
            float c[1];
            boolean check;
            check = false;
            if(check){
                
            }
            else{
                return b;
            }
        }
        """
        expect = "Function add Not Return "
        self.assertTrue(TestChecker.test(input, expect, 452))

    def test_FunctionNotReturn_053(self):
        input = """int a, b;
        void main(int argc[]){
            float f[8];
            f[0] = 7.8;
            boolean check;
            add(f, f)[7];
        }
        float[] add(float a[], float b[]){
            float c[1];
            boolean check;
            check = false;
            if(check){
                do{
                    if(!check){
                        return a;
                    }
                }while(!check);
            }
            else{
                return b;
            }
        }
        """
        expect = "Function add Not Return "
        self.assertTrue(TestChecker.test(input, expect, 453))

    def test_FunctionNotReturn_054(self):
        input = """int a, b;
        void main(int argc[]){
            float f[8];
            f[0] = 7.8;
            boolean check;
            add(2, 3);
        }
        int add( int a, int b){
            int i;
            for(i = 0; i < 10; i = i + 1){
                return a + b;
            }
        }
        """
        expect = "Function add Not Return "
        self.assertTrue(TestChecker.test(input, expect, 454))

    def test_FunctionNotReturn_055(self):
        input = """int a, b;
        void main(int argc[]){
            float f[8];
            f[0] = 7.8;
            boolean check;
            add(2, 3);
        }
        int add( int a, int b){
            int i;
            if(true){
                if(false){
                    return 0;
                }
                return 1;
            }
        }
        """
        expect = "Function add Not Return "
        self.assertTrue(TestChecker.test(input, expect, 455))

    def test_FunctionNotReturn_056(self):
        input = """int a, b;
        void main(int argc[]){
            float f[8];
            f[0] = 7.8;
            boolean check;
            add(2, 3);
        }
        int add( int a, int b){
            int i;
            do{
                int i;
            }while(false);
        }
        """
        expect = "Function add Not Return "
        self.assertTrue(TestChecker.test(input, expect, 456))

    def test_FunctionNotReturn_057(self):
        input = """int a, b;
        void main(int argc[]){
            float f[8];
            f[0] = 7.8;
            boolean check;
            add(2, 3);
        }
        int add( int a, int b){
            int i;
            do{
                int i;
                return 0;
            }while(false);
            if(true){
                if(true){
                    return 0;
                }
            }
            else{
                return 1;
            }
        }
        """
        expect = "Function add Not Return "
        self.assertTrue(TestChecker.test(input, expect, 457))

    def test_FunctionNotReturn_058(self):
        input = """int a, b;
        void main(int argc[]){
            float f[8];
            f[0] = 7.8;
            boolean check;
            add(2, 3);
            add;
        }
        int add( int a, int b){
            return 0;
        }
        """
        expect = "Function add Not Return "
        self.assertTrue(TestChecker.test(input, expect, 458))

    
    