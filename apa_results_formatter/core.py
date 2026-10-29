"""APA rules: italic statistic symbols, no leading zero for values bounded by 1, exact p to 3 decimals."""


def _it(sym, md):
    return ("*%s*" % sym) if md else sym


def fmt_num(x, decimals=2, leading_zero=True):
    s = "%.*f" % (decimals, x)
    if s.startswith("-"):
        s = "−" + s[1:]
    if not leading_zero:
        s = s.replace("0.", ".", 1) if s.lstrip("−").startswith("0.") else s
    return s


def fmt_p(p, md=True):
    """APA p-value: p < .001, otherwise exact to three decimals without leading zero."""
    if not 0 <= p <= 1:
        raise ValueError("p must be between 0 and 1")
    if p < 0.001:
        return "%s < .001" % _it("p", md)
    s = "%.3f" % p
    if s == "1.000":
        return "%s > .999" % _it("p", md)
    return "%s = %s" % (_it("p", md), s[1:])


def _df(df):
    return ("%d" % df) if float(df).is_integer() else ("%.2f" % df)


def ci(lo, hi, decimals=2, level=95):
    return "%d%% CI [%s, %s]" % (level, fmt_num(lo, decimals), fmt_num(hi, decimals))


def t_test(t, df, p, d=None, ci_d=None, md=True):
    s = "%s(%s) = %s, %s" % (_it("t", md), _df(df), fmt_num(t), fmt_p(p, md))
    if d is not None:
        s += ", %s = %s" % (_it("d", md), fmt_num(d))
        if ci_d:
            s += ", " + ci(*ci_d)
    return s


def f_test(f, df1, df2, p, eta2=None, partial=True, md=True):
    s = "%s(%s, %s) = %s, %s" % (_it("F", md), _df(df1), _df(df2), fmt_num(f), fmt_p(p, md))
    if eta2 is not None:
        sym = "η²" + ("p" if partial else "")
        s += ", %s = %s" % (_it(sym, md), fmt_num(eta2, 2, leading_zero=False))
    return s


def chi_square(chi2, df, p, n=None, v=None, md=True):
    s = "%s(%s%s) = %s, %s" % (_it("χ²", md), _df(df), ", %s = %d" % (_it("N", md), n) if n else "",
                              fmt_num(chi2), fmt_p(p, md))
    if v is not None:
        s += ", %s = %s" % (_it("V", md), fmt_num(v, 2, leading_zero=False))
    return s


def correlation(r, df, p, md=True, symbol="r"):
    if not -1 <= r <= 1:
        raise ValueError("correlation must be between -1 and 1")
    return "%s(%s) = %s, %s" % (_it(symbol, md), _df(df), fmt_num(r, 2, leading_zero=False), fmt_p(p, md))


def descriptives(mean, sd, n=None, md=True, decimals=2):
    s = "%s = %s, %s = %s" % (_it("M", md), fmt_num(mean, decimals), _it("SD", md), fmt_num(sd, decimals))
    if n is not None:
        s = "%s, " % ("%s = %d" % (_it("n", md), n)) + s
    return s


def regression_coef(b, se, t, df, p, beta=None, md=True):
    s = "%s = %s, %s = %s" % (_it("b", md), fmt_num(b), _it("SE", md), fmt_num(se))
    if beta is not None:
        s += ", β = %s" % fmt_num(beta, 2, leading_zero=False)
    return s + ", %s(%s) = %s, %s" % (_it("t", md), _df(df), fmt_num(t), fmt_p(p, md))


def format_result(rec, md=True):
    """Format a dict such as {"test": "t", "t": 2.1, "df": 28, "p": 0.04, "d": 0.77}."""
    kind = rec.get("test", "").lower()
    if kind in ("t", "ttest", "t-test"):
        ci_d = (rec["d_lo"], rec["d_hi"]) if "d_lo" in rec else None
        return t_test(rec["t"], rec["df"], rec["p"], rec.get("d"), ci_d, md)
    if kind in ("f", "anova"):
        return f_test(rec["F"], rec["df1"], rec["df2"], rec["p"], rec.get("eta2"), rec.get("partial", True), md)
    if kind in ("chi2", "chisq", "chi-square"):
        return chi_square(rec["chi2"], rec["df"], rec["p"], rec.get("n"), rec.get("v"), md)
    if kind in ("r", "correlation", "pearson"):
        return correlation(rec["r"], rec["df"], rec["p"], md)
    if kind in ("rho", "spearman"):
        return correlation(rec["rho"], rec["df"], rec["p"], md, symbol="rₛ")
    if kind in ("m", "descriptives", "mean"):
        return descriptives(rec["mean"], rec["sd"], rec.get("n"), md)
    if kind in ("b", "regression"):
        return regression_coef(rec["b"], rec["se"], rec["t"], rec["df"], rec["p"], rec.get("beta"), md)
    raise ValueError("unknown test type %r" % rec.get("test"))
