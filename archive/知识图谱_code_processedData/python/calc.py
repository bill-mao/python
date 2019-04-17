from pending import *
import sys
import json


def write(*string, path="./calc.log"):
    with open(path, "a+") as file:
        for i in string:
            print(i, file=file)
        print("", file=file)
        print("==================", file=file)
        traceback.print_exc(file=file)

        print('========================================================\n\n', file=file)


def read_calc_csv(path='./calc.csv'):
    with open(path, encoding="gbk") as csvfile:
        spamreader = csv.reader(csvfile, quotechar='"')
        paragraph = []  # 每个abstract表的所有要素
        calccsv = {}
        # csvreader里面是二维元组，行-列
        for cols in spamreader:

            try:
                if cols[0] == 'end':
                    abstract = paragraph[0][1]
                    calc = {}
                    calccsv[abstract] = calc
                    calc['formulas'] = []
                    calc['outs'] = []
                    calc['inputs'] = []

                    for p in paragraph[2:]:
                        calc['formulas'].append(p[0])
                        calc['outs'].append(p[1])
                        calc['inputs'].append(p[2:])

                    paragraph = []
                elif cols[0].strip() == "":
                    pass
                else:

                    c2 = [col.strip() for col in cols if col.strip() != '']
                    if c2 != []:
                        paragraph.append(c2)
            except Exception as e:
                traceback.print_exc()
        return calccsv


# 只能update一次！！否则backup
def update_node(item_node,  value):
    # # graph.run("match (n) where id(n) = %d  set n.%s = '%s' and  n.updated = 1" %(remote(node)._id, key, value))
    # cur = graph.run('match (n:instance)-->(m:item) where id(n) = %d return m ' % remote(node)._id)
    # if cur.forward():
    #     node = cur.current().values()[0]
    # else:
    #     print('update failure ,can\'t find item ')
    #     print(node, key, value  )
    #     return 
    #*****必须是item 否则，end， begin


    cql = "match (n:item) \
     where id(n) = %d  \
     and not (n)<-[:backup]-() \
     create \
    (m:backup)-[:backup]->(n) set m = n return count(m) as count " % remote(item_node)._id
    cc = graph.run(cql).data()[0]['count']
    if cc != 1:
        print('update failure')
        print(cql)
        if float(item_node['value']) - float(value) >100 :
            print("不同层次计算结果不一样吗？？？？path太多？？")
            print(item_node['value'], value)
        return 
    item_node['updated'] = '1'
    # node[key] = value
    
    graph.push(item_node)


# 获取abstract下面节点： 包括abstract；
# path 结构和之前一样
def fetch_instance_node(path, com='000009', date='20161231' , debug = False):
    if len(path.split( '-')) > 1:
        S = ["TableOfSolvencyStatusAbstract",
             "TableOfAvailableCapitalAbstract",
             "TableOfAdmittedAssetsAbstract",
             "TableOfAdmittedLiabilitiesAbstract",
             "TableOfMinimumCapitalAbstract", ]



        node_names = path.split('-')
        node_names = [n.strip() for n in node_names]
        abstract = node_names[0]


        mem_cql_piece = ''' -[:link]->(m%d:instance{ ELE_NAME : '%s'})'''
        mem_cql = ''
        for i, name in enumerate(node_names[1:]):
            mem_cql += mem_cql_piece % (i, name)

        target_index = len(node_names) - 2

        # 总表里面是需要模糊查询的； 当时设计结构时候没有和刘方铮说清楚
        # 为了兼容模糊查询和非模糊查询
        # 单个member的总表
        # 
        # 模糊查询
        if abstract in S and  target_index== 0:
            # print("============模糊查询============================================")
            cql =  '''
                match (c:company{dwzd_bh :'%s'})-->(d:date{inst_date: '%s'})-[:link*]->
                    (a:instance{ELE_NAME : '%s'}), 

                 p=  (a)-[:link*0..3]->(ii:instance{ELE_NAME : '%s'})
              
                where  size([ i in nodes(p) where i.ELE_NAME=~'.*Abstract']) <2
                return ii'''% (com, date, abstract, node_names[1])
            # print("总表的cql============================ ", cql)
        
        else:
            cql = '''
                match p= (c:company{dwzd_bh :'%s'})-->(d:date{inst_date: '%s'})-[:link*]->
                (a:instance{ELE_NAME : '%s'})%s
                return m%d
            ''' % (com, date, abstract, mem_cql, target_index)

        
        try:
            if debug:

                print(cql)
            cur = graph.run(cql)
            if cur.forward():
                out_node = cur.current().values()[0]
                return out_node
            else:
                return None
        except Exception as e:
            traceback.print_exc()
            print(cql)
            return None
    elif len(path.split('-')) == 1:
        # print("============================abstract instance")
        name = path
        cql = "match   (c:company{dwzd_bh : '%s'}) -[]->(d:date{inst_date : '%s'}) " \
              "-[:link*]-> (n:instance {ELE_NAME : '%s'}) return n" % (com, date, name)
        try:
            if debug:

                print(cql)
            cur = graph.run(cql)
            if cur.forward():
                out_node = cur.current().values()[0]
                return out_node
            else:
                return None
        except Exception as e:
            traceback.print_exc()
            print(cql)
            return None
    else:
        print("请输入正确的path 格式")


# 获取虚节点 own_amount 节点
def fetch_amount_list(node,  rel_label='own'):
    cql = '''match (n)-[r:%s]->(m) where id(n) = %d  return m  ''' % (rel_label, remote(node)._id)
    try:
        cur = graph.run(cql)
        out_node = []
        while cur.forward():
            out_node.append( cur.current().values()[0] )
        print(cql)
        return out_node
    except Exception as e:
        print(str(e))
        print(cql)


# ========================================================

# path include： abs，item 不能少 ： abstract - members - item
# return path's node,
# create = True 假如没有的话就会创建节点返回； 慎用
# 只能创建明细表的item，因为总表的item总是全的
# 只有item才行
def merge_item(path, com='000009', date='20161231', create = False, debug = False ):
    '''[summary]
    
    [description]
    
    Arguments:
        path {[type]} -- [description]
    
    Keyword Arguments:
        com {str} -- [description] (default: {'000009'})
        date {str} -- [description] (default: {'20161231'})
        create {bool} -- [description] (default: {False})
        debug {bool} -- [description] (default: {False})
    
    Returns:
        [type] -- [description]
    
    Raises:
        Exception -- [description]
        Exception -- [description]
        Exception -- [description]
    '''
    S = ["TableOfSolvencyStatusAbstract",
         "TableOfAvailableCapitalAbstract",
         "TableOfAdmittedAssetsAbstract",
         "TableOfAdmittedLiabilitiesAbstract",
         "TableOfMinimumCapitalAbstract", ]

    spl = path.split('-')
    spl = [s.strip() for s in spl]
    abstract = spl[0]
    members = spl[1:-1]
    item = spl[-1]

    cql_piece = ''
    for i in range(len(members)):
        c = "-[:link]->(m%d:instance{ELE_NAME : '%s'})" % (i, members[i])
        cql_piece = cql_piece + c

    # 总表里面是需要模糊查询的； 当时设计结构时候没有和刘方铮说清楚
    if abstract in S:
        cql =  '''
            match (c:company{dwzd_bh :'%s'})-->(d:date{inst_date: '%s'})-[:link*]->
                (a:instance{ELE_NAME : '%s'}), 

             p= shortestPath(
                (a)-[:link*0..3]->(ii:instance)
            ), 
            (ii)%s-[:linkitem]->(i:item{ELE_NAME:'%s'}) 
            where  size([ i in nodes(p) where i.ELE_NAME=~'.*Abstract']) <2
            return i'''% (com, date, abstract, cql_piece, item)
        # print("总表的cql============================ ", cql)
    else:
        cql = '''
            match p= (c:company{dwzd_bh :'%s'})-->(d:date{inst_date: '%s'})-[:link*]->
            (a:instance{ELE_NAME : '%s'})%s
            -[:linkitem]->(i:item{ELE_NAME:'%s'})
            return i
        ''' % (com, date, abstract, cql_piece, item)

    try:
        if debug:
            print(cql)
        cur = graph.run(cql)
        items_node = []
        while cur.forward():
            ii = list(cur.current().subgraph().nodes())[0]
            items_node.append(ii)
        if len(items_node) > 1:
            print("============================")
            print(path, com, date)
            print(cql)
            raise Exception("========merge_item====================找到不止一个item ")
        # 没找到， 是否创建
        elif len(items_node) < 1  :
            print("****************** 没找到*************")
            print(path, '\n', cql)
            print("========================================================")
            if create:
                if abstract not in S :
                    # create item add default value '0' ； created property - merge 1
                    mi = len(members) - 1
                    if mi < 0:
                        cql = '''
                            match p= (c:company{dwzd_bh :'%s'})-->(d:date{inst_date: '%s'})-[:link*]->
                            (a:instance{ELE_NAME : '%s'})
                            create (a)-[:linkitem]->(ii:item{ELE_NAME: '%s', value : '0', merge: 1})
                            return ii
                        ''' % (com, date, abstract, item)
                    else:
                        cql = '''
                            match (c:company{dwzd_bh :'%s'})-->(d:date{inst_date: '%s'})-[:link*]->
                                (a:instance{ELE_NAME : '%s'}), 
                            p= (a)-[:link*0..3]->(ii:instance)%s
                            where size([ i in nodes(p) where i.ELE_NAME=~'.*Abstract']) <2
                            create (m%d)-[:linkitem]->(ii:item{ELE_NAME: '%s', value : '0', merge: 1})
                            return ii
                        ''' % (com, date, abstract, cql_piece, mi, item)

                    cur = graph.run(cql)
                    if cur.forward():
                        print("--------merge get item ",path)
                        return cur.current().values()[0]
                    else:
                        raise Exception("insert merge item failure")
                else :
                    raise Exception("总表少item！ " + path)
            else:
                return None
        else:
            return items_node[0]
    except Exception as e:

        traceback.print_exc()
        # print("============================Exception cql", cql)
        return None



# 返回挂接外部节点的个数
def count_own_amount(node, rel_label = 'own'):
    if node is None:
        return 0
    cql = "match (n)-[r:%s]->(m) where id(n) = %d \
    return count(m) as count"%(rel_label, remote(node)._id)
    data = graph.data(cql)
    out = data[0]['count']
    # print(out)
    return out

# count_own_amount(graph.node(2726574))

# wrong return '0' ; anyway return str
def sum_rel(node, rel_key, rel_label='own'):
    cql = '''match (n)-[r:%s]->(m) where id(n) = %d  return sum(toFloat(m.%s)) as sum  
       ''' % (rel_label, remote(node)._id, rel_key)
    # print(cql)
    res = graph.data(cql)
    if res is not None or len(res) > 0:
        sum = res[0]['sum']
        return str(sum)
    else:
        print('sum_rel wrong return 0')
        return '0'

# judge whether can be calculated
# 是否存在计算公式
def can_calc(path):
    spl = path.split('-')
    spl = [s.strip() for s in spl]
    abstract = spl[0]
    members = '-'.join(spl[1:-1])  # if null then ''
    item = spl[-1]




    if abstract in calccsv.keys():
        calc = calccsv.get(abstract)

        formulas = calc.get('formulas')
        outs = calc.get('outs')
        inputs = calc.get('inputs')

        if members == '':
            target_out = item
        else:
            target_out = members + '-' + item
        # 是否能够再计算
        if outs is None or outs == [] or target_out not in outs:
            return False
        else:
            # print("can calc============================")
            # print(path, target_out, inputs[outs.index(target_out)])
            # print("end can calc============================")
            return True
    else:
        return False


def has_leaves(path, com,date):
    # 返回点 judge whether has own_amount- 
    leaf_node = fetch_instance_node(path ,com,date, )
    coa = count_own_amount(leaf_node)
    # print("外部节点的个数  sum", coa)

    
    if coa > 0:
        return True
    else:
        return False



# 找不到inputs的那些节点，write信息，返回'0' ； 但是假如能够被下层计算的话，就下层计算
# write( com, date, path ,path = './recurisve.log')
def recursive_calc(path, com='000009', date='20161231', depth=0, depth_limit=99, 
    update = False, debug = False):

    if debug :
        for i in range(depth):
            print('\t', end= '')
        print('recursive depth is ', depth, path, com, date)

    spl = path.split('-')
    spl = [s.strip() for s in spl]
    abstract = spl[0]
    members = '-'.join(spl[1:-1])  # if null then ''
    item = spl[-1]




    # 返回点 judge whether has own_amount- 
    leaf_node = fetch_instance_node('-'.join(spl[:-1]) ,com,date, )
 
    if has_leaves('-'.join(spl[:-1]) ,com,date, ):
        sum = sum_rel(leaf_node, item)
        
        fetch_instance_node('-'.join(spl[:-1]) ,com,date, debug = True)
        if update:
            update_node(merge_item(path),  sum)
            print("update")
        return sum






    # 返回点2 计算返回
    if depth <depth_limit and  can_calc(path):
        calc = calccsv.get(abstract)

        # print(calc)

        formulas = calc.get('formulas')
        outs = calc.get('outs')
        inputs = calc.get('inputs')

        if members == '':
            target_out = item
        else:
            target_out = members + '-' + item

        index = outs.index(target_out)
        formula = formulas[index]
        # print("============================", formula)
        input_path = inputs[index]
        input_values = []
        # add values to inut_values
        for each in input_path:
            # judege the real abstract of inputs'
            real_abstract = abstract
            # print('each============================', each)
            # print('input_path============================', input_path)
            # if input_path[0].endswith("Abstract"):
            if each.split('-')[0] .endswith('Abstract'):
                # each = each
                # real_abstract = input_path[0]
                real_abstract = each.split('-')[0]
            else:
                each = abstract + '-' + each

            # #####**********没有计算外部节点！！！！！
            if has_leaves('-'.join(each.split('-')[:-1]), com, date):
                each_node = fetch_instance_node('-'.join(each.split('-')[:-1]))
                sum = sum_rel(each_node, item)
                coa = count_own_amount(each_node)
                # print("外部节点的个数  sum", coa, sum)
                # fetch_instance_node('-'.join(spl[:-1]) ,com,date, debug = True)
                if update:
                    update_node(merge_item(each) ,  sum)
                    print("update")
                input_values.append(str(sum))



            # 判断items是否要重新计算
            elif can_calc(each):
                input_calc = calccsv.get(real_abstract)
                # if input_calc is not None:

                item_outs = input_calc.get('outs')
                target = each.split('-', 1)[1]
                item_value = recursive_calc(each, com, date, depth=depth + 1, depth_limit=depth_limit, update = update, debug = debug)
                input_values.append(item_value)
            else:
                lio = merge_item(each, com,date )['value'] 
                if lio is None:
                    # deg = merge_item(each, com,date , debug = True)
                    # print("========================================================")
                    # print("ca============================ can't find input item value", deg)
                    # print("========================================================")
                    # ####
                    input_values.append('0')
                else:
                    input_values.append(merge_item(each, com,date )['value'])
        # 竟然出现了缩进问题，仔细仔细啊！！！
        out = '0'
        try:
            # judge whether is formula or programma
            if formula.count('\n') > 1:
                formula = formula % tuple(input_values)
                gl = {'out': '0'}
                exec(formula, gl)
                out = str(gl['out'])
            else:
                for j, invalues in zip(range(len(input_values)), input_values):
                    j = j + 1
                    formula = formula.replace('s%d' % j, str(invalues), 1)
                    # out = str(eval(formula))
                out = str(eval(formula))
            # print(out)
        except Exception as e:
            print("========================================================")
            print('calculate exception *** ', com, date, path)
            print(input_values)
            print(formula, '\n')
            traceback.print_exc()
            print("========================================================")

        if update:
            update_node(merge_item(path), out)
            print("update")
        return out
    # 返回点 不计算
    else:
        #*************
        # out = leaf_node['value']
        out = merge_item(path, com,date)['value']
        # print("???")
        return out


# merge_item('TableOfMinimumCapitalAbstract-SpecificInsuranceContractAdjustedOfLossAbsorptionUpperLimitNotToBeTakenIntoConsideration-end ', debug = True)


# # merge_item(path, debug = True) #5456722912 
# path = 'TableOfMinimumCapitalAbstract-MinimumCapitalUnderSolvencyII-end'
# path = 'TableOfSolvencyStatusAbstract-ComprehensiveSolvencyAdequacyRatio-end'
# print(recursive_calc(path, com='000009', date='20161231',  update = False, depth_limit = 99)) #4964533128.329587 #4809364428
# 原最低资本4809364428.584979 
# 现在最低资本4750590614.3813 删除了mr09 所有股票000开头 风险暴露 248177373.1  ； 最低资本76737575.09

if __name__ == '__main__':
    calccsv = read_calc_csv()
    # print(json.dumps(calccsv, sort_keys=True, indent=4, separators=(',', ': ')))


# 刘方铮统计用
# 写到这个文件 'com-date-实际资本-最低资本.csv'
def recursive_get_real_least():
    calccsv = read_calc_csv()
    # print(json.dumps(calccsv, sort_keys=True, indent=4, separators=(',', ': ')))

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

    liu_csv = []

    zero = [
        (5   ,20170630),
        (26  ,20170630),
        (26  ,20170930),
        (27  ,20170630),
        (35  ,20170630),
        (190 ,20170630),
        (5   ,20170930),
        (14  ,20170930),
        (27  ,20170930),
        (37  ,20170930),
        (128 ,20170930),
        (130 ,20161231),
        (130 ,20170331),
        (140 ,20170930),
        (140 ,20171231),
        (171 ,20170930),
        (190 ,20170630),
        (199 ,20170930),
        (204 ,20170930),
    ]
    
    for com, date, dw_name in results_dwzd_date[:]:
        if (int(com), int(date)) in zero:
            print("zero")
            continue
        # else:
        #     print("no")
        #     continue
        current_csv = []
        # path = 'TableOfMinimumCapitalAbstract-MinimumCapitalUnderSolvencyII-end'
        path = 'EquityPriceRiskStockNoHedgingAndUnqualifiedHedgingAbstract-HeldByCompanyDirectlyMember-EquityPriceRiskStockNoHedgingAndUnqualifiedHedgingMinimumCapital'
        # path = 'TableOfSolvencyStatusAbstract-ComprehensiveSolvencyAdequacyRatio-end'
        current_csv.append(str(com))
        current_csv.append(date)
        # 实际资本
        current_csv.append(merge_item('TableOfSolvencyStatusAbstract-AvailableCapitalUnderSolvencyII-end', com, date)['value'])

        # 最低资本
        rclc = recursive_calc(path, com=com, date=date,  update = False, depth_limit = 99)
        if rclc is None:
            current_csv.append(0)
        else:
            current_csv .append( float(rclc ))#

        liu_csv.append(current_csv)

    # 设置newline，否则两行之间会空一行
    with open('com-date-实际资本-最低资本.csv','w', newline='') as csvFile2 :
        writer = csv.writer(csvFile2)
        for every_row in liu_csv:
            writer.writerow(every_row)

def check_sum(node, rel_key, rel_label='own'):
    sum = sum_rel(node, rel_key, rel_label)
    db_sum = node[rel_key]
    print(sum, '  ', db_sum)




