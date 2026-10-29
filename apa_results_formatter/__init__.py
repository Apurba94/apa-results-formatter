"""Format statistical results in APA 7 style."""
from .core import fmt_p, fmt_num, t_test, f_test, chi_square, correlation, descriptives, ci, format_result

__version__ = "0.1.0"
__all__ = ["fmt_p", "fmt_num", "t_test", "f_test", "chi_square", "correlation", "descriptives", "ci", "format_result"]
