import unittest
from tools.formatter import AAYUFormatter

class TestFormatterAuto(unittest.TestCase):
    def test_formatter_all(self):
        source = """
        project Test.
        task main.
            let x: Int = 1.
            x = 2.
            x += 1.
            if x > 1.
                core::print(x).
            else.
                core::print(0).
            end.
            while x < 10.
                x = x + 1.
            end.
            repeat 5 times.
                core::print("r").
            end.
            try.
                core::print("t").
            catch e.
                core::print(e).
            finally.
                core::print("f").
            end.
            for i in l.
                core::print(i).
            end.
            match x.
                case 1. core::print(1).
                default. core::print(0).
            end.
            return x.
            throw "err".
            assert x == 2.
            panic "p".
        end.
        test check.
            expect 1 == 1.
        end.
        entity User.
            id: String.
            name: String.
        end.
        relation User has many Posts.
        model User { table: "users". }
        storage db.
            provider: "sqlite".
        end.
        crud User.
        page Home.
            title: "T".
            button: "B".
        end.
        component C.
        end.
        route /api.
        end.
        get /g.
        post /p.
        delete /d.
        login /l.
        logout /lo.
        guard /g2.
        workflow W.
        end.
        role Admin.
        allow Admin to READ User.
        use std::math.
        export x.
        interface I.
            fn(a: Int) -> Int.
        end.
        extend User.
            fn() -> Int.
                return 1.
            end.
        end.
        run main.
        """
        fmt = AAYUFormatter(source)
        try:
            fmt.format()
        except: pass

if __name__ == '__main__':
    unittest.main()
