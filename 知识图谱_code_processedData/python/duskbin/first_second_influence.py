from calc import *

'''
match (c:company)-->(d:date)-[*]->(i:instance)-->(o:own_amount)-->(s)
    //set i.tmp_dwzd_bh = c.tmp_dwzd_bh 
    set o.tmp_dwzd_bh = c.dwzd_bh 
    set o.tmp_inst_date = d.inst_date

[description]
'''
def first_second_influence(label, key, code):
    cql = "match (o:own_amount)-->(s:%s) where s.%s = '%s' return distinct o.tmp_dwzd_bh as bh" \
        %(label, key, code)

    dwzd_bhs = [i['bh'] for i in graph.data(cql)]

    print("first influence ", dwzd_bhs)

    print("second influence")
    for d in dwzd_bhs:
        cql = "match (c:company)-[:influence]->(c2:company) where c.dwzd_bh = '%s' return distinct c2.dwzd_bh as bh " % d
        dws = [i['bh'] for i in graph.data(cql)]
        print(dws)


def all_influence(label, key, code):
    cql = "match (o:own_amount)-->(s:%s) where s.%s = '%s' return distinct o.tmp_dwzd_bh as bh" \
        %(label, key, code)

    dwzd_bhs = [i['bh'] for i in graph.data(cql)]

    # print("first influence ", dwzd_bhs)

    allbh = set(dwzd_bhs)

    nextbh = set(dwzd_bhs)
    nbh = set([])

    # print("second influence")

    while(nextbh):
        for d in nextbh:
            cql = "match (c:company)-[:influence]->(c2:company) where c.dwzd_bh = '%s' return distinct c2.dwzd_bh as bh " % d
            dws = [i['bh'] for i in graph.data(cql)]
            for dd in dws:
                if dd not in allbh:
                    nbh.add(dd)
            allbh.update(dws)
            # print(dws)
        nextbh = nbh
        nbh = set([])

    print(allbh)


first_second_influence('stock', 'EquityPriceRiskStockNoHedgingAndUnqualifiedHedgingStockCode', '300672')
all_influence('stock', 'EquityPriceRiskStockNoHedgingAndUnqualifiedHedgingStockCode', '300672')


# match (c:company)-[:influence]->(c2:company) where c.dwzd_bh = '%s' return distinct c2.dwzd_bh as bh 


# match (o:own_amount)-->(s:stock) where s.EquityPriceRiskStockNoHedgingAndUnqualifiedHedgingStockCode = '300672' return distinct o.tmp_dwzd_bh 


# match (c:company{dwzd_bh:'000009'})-->(d:date)-[*]->(i:instance)-->(o:own_amount)-->(s)
#     //set i.tmp_dwzd_bh = c.tmp_dwzd_bh 
#     set o.tmp_dwzd_bh = c.dwzd_bh 
#     set o.tmp_inst_date = d.inst_date 