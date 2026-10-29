import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from apa_results_formatter.cli import main
from apa_results_formatter.core import (chi_square, correlation, descriptives, f_test, fmt_num, fmt_p, format_result,
                                        regression_coef, t_test)


class FormatTests(unittest.TestCase):
    def test_p_values(self):
        self.assertEqual(fmt_p(0.0004), "*p* < .001")
        self.assertEqual(fmt_p(0.0321, md=False), "p = .032")
        self.assertEqual(fmt_p(0.05, md=False), "p = .050")
        self.assertEqual(fmt_p(0.99999, md=False), "p > .999")
        with self.assertRaises(ValueError):
            fmt_p(1.5)

    def test_numbers(self):
        self.assertEqual(fmt_num(-2.456), "−2.46")
        self.assertEqual(fmt_num(0.456, leading_zero=False), ".46")

    def test_t_and_f(self):
        self.assertEqual(t_test(2.345, 28, 0.026, d=0.85, ci_d=(0.1, 1.6), md=False),
                         "t(28) = 2.35, p = .026, d = 0.85, 95% CI [0.10, 1.60]")
        self.assertEqual(t_test(2.1, 25.37, 0.046, md=False), "t(25.37) = 2.10, p = .046")
        self.assertEqual(f_test(5.23, 2, 57, 0.008, eta2=0.155, md=False),
                         "F(2, 57) = 5.23, p = .008, η²p = .15")

    def test_chi_r_m_b(self):
        self.assertEqual(chi_square(4.5, 1, 0.034, n=120, v=0.19, md=False), "χ²(1, N = 120) = 4.50, p = .034, V = .19")
        self.assertEqual(correlation(-0.32, 98, 0.0012, md=False), "r(98) = −.32, p = .001")
        self.assertEqual(descriptives(5.123, 1.2, n=30, md=False), "n = 30, M = 5.12, SD = 1.20")
        self.assertEqual(regression_coef(0.5, 0.1, 5, 100, 0.00001, beta=0.42, md=False),
                         "b = 0.50, SE = 0.10, β = .42, t(100) = 5.00, p < .001")
        with self.assertRaises(ValueError):
            correlation(1.3, 10, 0.5)

    def test_markdown_italics(self):
        self.assertEqual(t_test(2, 10, 0.07), "*t*(10) = 2.00, *p* = .070")

    def test_dispatch_and_cli(self):
        self.assertEqual(format_result({"test": "anova", "F": 3, "df1": 1, "df2": 20, "p": 0.1}, md=False),
                         "F(1, 20) = 3.00, p = .100")
        with self.assertRaises(ValueError):
            format_result({"test": "bayes"})
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "r.csv")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write("label,test,t,df,p,r\nH1,t,2.5,40,0.016,\nH2,r,,58,0.2,0.17\nH3,t,1,,0.3,\n")
            with redirect_stdout(io.StringIO()) as buf:
                self.assertEqual(main([p, "--plain"]), 1)
            out = buf.getvalue().splitlines()
            self.assertEqual(out[0], "H1: t(40) = 2.50, p = .016")
            self.assertEqual(out[1], "H2: r(58) = .17, p = .200")
            self.assertTrue(out[2].startswith("H3: ERROR"))
            j = os.path.join(d, "r.json")
            with open(j, "w", encoding="utf-8") as fh:
                json.dump([{"test": "m", "mean": 3, "sd": 1}], fh)
            with redirect_stdout(io.StringIO()) as buf:
                main([j])
            self.assertIn("*M* = 3.00", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
