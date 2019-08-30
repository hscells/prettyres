#! /usr/bin/env python3
import argparse
import pandas as pd
from scipy.stats import stats

# this code outputs latex table.
# use the following to convert it to markdown.
# pandoc -s tbl2017.tex -t markdown+grid_tables-simple_tables -o tbl2017.md

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("r", help="list of json evaluation files from entrez_eval", type=str, nargs="+")
    parser.add_argument("m", help="which measures in the evaluation file to tablify", type=str, nargs="+")
    parser.add_argument("x",
                        help="compute statistical significance between [all] rows, only [one row (specify the row)], or [both]",
                        type=str)
    args = parser.parse_args()
    evals = {}
    for e in args.r:
        with open(e, "r") as f:
            evals[e.replace("_", "-")] = pd.read_json(f).T

    d = pd.DataFrame()
    t = pd.concat([x.mean() for x in evals.values()], axis=1)
    t.columns = evals.keys()
    df = t.T
    df2 = t.T
    strs = []
    s = {}
    for x in df:
        for i in df[x].index:
            p = 0.0
            if (len(args.x) > 0 and args.x != "all") or args.x == "both":
                p = stats.ttest_rel(evals[i][x], evals[args.x][x]).pvalue
                if x + i not in s:
                    s[x + i] = []
                s[x + i].append('*')
            if len(args.x) > 0 and (args.x == "all" or args.x == "both"):
                for k, j in enumerate(df[x].index):
                    if i == j:
                        continue
                    if i + j + x in strs:
                        continue
                    p = stats.ttest_rel(evals[i][x], evals[j][x]).pvalue
                    if p < 0.05:
                        if x + i not in s:
                            s[x + i] = []
                        s[x + i].append(str(k + 1))
                    strs.append(i + j + x)
    for x in df:
        for i in df[x].index:
            if x + i in s:
                df2[x][i] = "{:.4f}".format(df[x][i]) + "$^{" + ",".join(s[x + i]) + "}$"
    print(df2[["F1Measure", "AP", "nDCG"]].to_latex(escape=False))
