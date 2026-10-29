# apa-results-formatter

**Turn statistical output into correctly formatted APA 7 result strings: `t(28) = 2.35, p = .026,
d = 0.85, 95% CI [0.10, 1.60]`, for t, F, chi-square, correlations, descriptives and regression.**

Part of the *Research Automation Toolkit*: 100 open tools for daily research work.

## Why

Hand-typing results into a manuscript is a major source of reporting errors: one in eight
psychology papers contains a p-value inconsistent with its test statistic (Nuijten et al., 2016).
APA style has many small rules (italic symbols, no leading zero for p and r, `p < .001`, true minus
signs). Generating the strings from the analysis output removes both kinds of errors.

## Features

- `fmt_p`: exact p to three decimals, `p < .001`, `p > .999`, no leading zero
- t-tests (integer or Welch fractional df, Cohen's d with CI), F/ANOVA with (partial) eta squared,
  chi-square with N and Cramer's V, Pearson r and Spearman rs, M/SD/n, regression coefficients
- Markdown italics or plain text; Unicode minus, chi and eta symbols
- Batch mode from CSV/JSON (one row per result, `test` column), errors reported per row

## Usage

```bash
pip install .
apa-results-formatter results.csv --plain
apa-results-formatter results.json
```

```python
from apa_results_formatter import t_test, fmt_p
print(t_test(2.345, 28, 0.026, d=0.85))   # *t*(28) = 2.35, *p* = .026, *d* = 0.85
```

## Testing

```bash
python -m unittest discover -s tests -t .
```

## License

MIT (c) JANIN A APURBA
