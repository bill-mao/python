




# 查看公司所有stock最低资本和
    from calc import *



    sql_dwzd_date  = ''' SELECT   distinct a.DWZD_BH AS '机构编号', a.INST_DATE AS '发生日期', b.y as name
             FROM psx_dw_instdata a , (
                  select DWZD_BH as x, DWZD_MC  as y from rpt_dwzd where dwzd_bh in (
               SELECT   distinct a.DWZD_BH as bh
                     FROM psx_dw_instdata a
                     where length(a.DWZD_BH) = 6
             )) b
             where length(a.DWZD_BH) = 6 and a.DWZD_BH = b.x
              '''
    results_dwzd_date = query(sql_dwzd_date)

    com_date_stock300=[]

    min_capital_keys = [
        "EquityPriceRiskStockNoHedgingAndUnqualifiedHedgingMinimumCapital",
        "EquityPriceRiskStockQualifiedHedgingMinimumCapitalOfHedgingPortfolio",
        "EquityPriceRiskUnlistedEquitiesMinimumCapital",
        "EquityPriceRiskPreferredSharesMinimumCapital",
        "EquityPriceRiskPreferredSharesMinimumCapital",
        "EquityPriceRiskShortPositionOfStockIndexFuturesOutOfEffectivenessMinimumCapital",
    ]   

    for com, date, dw_name in results_dwzd_date:
        try:
            all_total = 0
            for key in min_capital_keys:

                cql = "match \
                (c:company{dwzd_bh :'%s'})-->(d:date{inst_date: '%s'})-[*]->\n \
                (own:own_amount)-->(s:stock)\
                return sum(toFloat(own.%s)) as sum" %(com, date, key)
                # print(cql)
                # print(graph.data(cql))
                total = graph.data(cql)[0]['sum']
                all_total += total
                # print(total)
            print(com, date, all_total)
        except Exception as e:
            traceback.print_exc()
            raise e




# 查看除了 L01， AC01 之外没有挂载节点的
    from pending import *

    item_id = []
    item_cql = 'match (n:company)-[:link*]->(m:instance)-[:linkitem]->() \
    return id(m) as all '
    item = graph.run(item_cql).data()
    for i in item:
        item_id.append(i['all'])


    all_id = []
    all_cql = ' match (m:instance) \
    where m.ELE_NAME <> "OutstandingBenefitsReserveOfLifeInsuranceContractLiabilitiesAbstract" \
    and m.ELE_NAME <> "TableOfCapitalInstrumentAbstract"  \
     return id(m) as all '
    all = graph.run(all_cql).data()
    for i in all:
        all_id.append(i['all'])  


    else_id = []
    for  i in all_id:
        if i not in item_id:
            else_id.append(i)

    print(else_id)


# 处理哪些instance没有挂上item， print出来

    import csv
    item = {}
    all = {}
    no = {}

    item_id = []
    all_id = []

    with open("d:/desktop/item.csv" , encoding = "utf8") as csvfile:
        spamreader = csv.reader(csvfile, quotechar='"')
        for cols in spamreader:
            item[cols[0]] = cols[1:]
            item_id.append(cols[0])

    with open("d:/desktop/all.csv", encoding = "utf8") as csvfile:
        spamreader = csv.reader(csvfile, quotechar='"')
        for cols in spamreader:
            all[cols[0]] = cols[1:]
            all_id.append(cols[0])

    for i in all_id:
        if i not in item_id:
            no[i] = all[i]

    for i,j in no.items():
        print(j)




#处理把一张表接到另一张表上面： 前缀则为root
import pandas as pd
root_name = pd.read_csv("d:/desktop/root_name.csv");
whole_name = root_name['"n.ELE_NAME"']

out = pd.DataFrame()
for i in whole_name:
    for j in whole_name:
        tmp = i.replace('Abstract"', '')
        if j.startswith(tmp) and i != j:
            //print("find")
            out = pd.concat([out,pd.DataFrame([i,j]).T], ignore_index=True)
 
out.to_csv("d:/desktop/out_name.csv")

#set(df[2])

#2018-1-26
#处理知识图谱里面的tag name； 同一个link_role 里面的对应一个根节点的ele_name --> tag_en
import pandas as pd
levelDf = pd.read_csv("d:/desktop/level.csv")
#label means the root nodes' element_name
label = levelDf[levelDf.FromElementName.isnull()]
label = label.iloc[:,[1,3]]
label.rename(columns={'ToElementName':'tag_en'}, inplace=True)
#join two dataframe; set_index-->change column to row name
#join two dataframe; set_index-->change column to row name
result = levelDf.set_index('LINK_ROLE').join(label.set_index('LINK_ROLE'), how='inner')
#merge suffixes means to distinguish the same name of columns
result = pd.merge(levelDf, label, on='LINK_ROLE', suffixes=['_l', ''])
#result.to_csv("d:/desktop/result.csv")


