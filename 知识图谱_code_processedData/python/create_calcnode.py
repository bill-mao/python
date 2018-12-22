from calc import *

calccsv = read_calc_csv()
# print(json.dumps(calccsv, sort_keys=True, indent=4, separators=(',', ': ')))

def create_calc_node(com='000009', date='20161231'):
    # 遍历abstract 段落
    for key in calccsv:
        calc = calccsv.get(key)

        formulas = calc.get('formulas')
        outs = calc.get('outs')
        inputs = calc.get('inputs')
        abstract = key  #######******

        # 遍历abstract 下面的所有计算公式
        for fo, out, inpu in zip(formulas, outs, inputs):
            if out.split('-')[0].endswith("Abstract"):
                out_path = out
            else:
                out_path = key + '-' + out

            out_node = merge_item(out_path, com, date,
                create = False)

            input_nodes = []
            for each in inpu:
                # judege the real abstract of inputs'
                if not each.split('-')[0].endswith("Abstract"):
                    each = abstract + '-' + each
                input_nodes.append(merge_item(each, com, date ,create=False))


            flag = False
            if out_node is None :
                # print("找不到 out item node ：abstract,   out, formula ", key,  out ,fo, )
                flag = True
            for none,pat in zip(input_nodes, inpu):
                if none is None :
                    # print("can't find input node : abstract, path, formula", key, pat, fo )
                    flag = True
            if  flag :
                continue

            tx = graph.begin()
            ### try:

            calc_node = Node("calculate", formula=fo)
            tx.create(calc_node)
            tx.create(Relationship(out_node, 'calc', calc_node))
            for  i, nn in enumerate(input_nodes):
                tx.create(nn)
                i = i+1
                nai = 's' + str(i)
                # print(nai, type(nai))
                tx.create(Relationship(calc_node, "calc", nn,** {"name": nai }))
            print("successful insert a calculate node ============================")
            tx.commit()


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
for com, date, dw_name in results_dwzd_date[:]:
    create_calc_node(com, date)



