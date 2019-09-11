#! /usr/bin/env python3
import json
import sys
from pprint import pprint

import trectools

if __name__ == '__main__':
    j = sys.argv[1]
    t = sys.argv[2]

    with open(j, "r") as f:
        jj = json.load(f)

    tt = trectools.TrecRes(t)

    topics = tt.data["query"].unique()

    d = {}
    for topic in topics:
        if topic == "all":
            continue
        d[topic] = {}
        for v in tt.data[tt.data["query"] == topic][["metric", "value"]].values:
            d[topic][v[0]] = v[1]

    x = {}
    for k, v in jj.items():
        x[k] = {**v, **d[k]}

    pprint(x)
