from pending   import *
import json 


# i = pd.graph.run("match (n:elment) return n")
# print(type(i))

# with open("d:/desktop/er.json") as file:
#     j = json.loads((str(file.read())))
#     print(j)


del_labels = [
    "security",
    "product",
    "contract",
    "reinsurance",
    "bond",
    "asset",
    "stock",
    "fund",
    "enterprise",
    "company",
    "date",
    "instance",
    "item",
    "own_amount",
    "assets",
    "convertible_bond",
    "forex",
    "equity",
    "real_estate",
    "overseas"
]

del_rels = [
    "link",
    "own",
    "linkitem",
    "tmp",
    "influence"
]

calc_n = ['calculate', 'backup']
calc_r = ['calc', 'backup']

# not -- delete calculation
if     not  True:

    for r in del_rels:
        graph.run("match ()-[r:%s]->() delete r" %r)
    for n in del_labels:
        graph.run("match (n:%s) delete n" %n)
else:
    for r in calc_r:
        graph.run("match ()-[r:%s]->() delete r" %r)
    for n in calc_n:
        graph.run("match (n:%s) delete n" %n)
