# coding=utf-8
"""
DC doesn't post odds on their spin (bonus)
"""
import csv
import pprint
from collections import OrderedDict

i = 0
with open("dc_keno_five_years.csv") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    empirical = {}
    for row in spamreader:
        i += 1
        if i == 1:
            # header
            continue
        value = row[3].split(",")[20]
        if value is None:
            value = "NO"
        if not value:
            value = "NO"
        if value == "S1":
            value = "S01"
        if value == "S2":
            value  = "S02"
        if value == "S5":
            value = "S05"
        if value not in ["S01", "S02","S03","S04", "S05","S10"]:
            value = "NO"
            print(row)
        if value in empirical:
            empirical[value] += 1
        else:
            empirical[value] = 1
    pprint.pprint(empirical)
    for key, value in empirical.items():
        print(key, value/i)
    cumulative_probs = OrderedDict()
    so_far =0.00
    for multipliers in ["01", "02", "03", "04", "05", "10"]:
        what = empirical["S" + multipliers]
        current = what/i
        so_far += current
        cumulative_probs[int(multipliers)] = so_far
    pprint.pprint(cumulative_probs)
