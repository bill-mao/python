from calc import *

calccsv = read_calc_csv()
# print(json.dumps(calccsv, sort_keys=True, indent=4, separators=(',', ': ')))


# if has return sum; else: return None
def sum_assets(item_node):

    item_id = remote(item_node)._id
    key = item_node['ELE_NAME']
    '''
    match p=(i)<-[:linkitem]-(m:instance)-[:own]->(o:own_amount)  
    where id(i) = 8193  return count(p) as num, sum(toFloat(o.CounterpartyDefaultRiskOutwardReinsuranceAssetsMinimumCapital)) as sum
    '''
    cql = '''match p = (i)<-[:linkitem]-(m:instance)-[:own]->(o:own_amount)   
        where id(i) = %d  return count(p) as num,  sum(toFloat(o.%s)) as sum  
       ''' %(item_id, key)

    res = graph.data(cql)
    if res is not None :
        if res[0]['num'] > 0:
            sum = res[0]['sum']
            return float(sum)
        else:
            return None
    else:
        raise Exception('sum_assets wrong cql')


# if can, return all rest item_nodes, formular, name(s1)
def can_calculate(item_node):
    # 36471
    cql = "match p =  (i:item)-[:calc]->(ca:calculate)-[rr:calc]->(x:item) where id(i) = %s     return count(p) as num, x as items, ca.formula as formula, rr.name    order by rr.name"\
    %(remote(item_node)._id)

    cur = graph.run(cql)
    res = cur.data()
    if res is not None and res != []:
        # should be num = 1 and an Node
        if res[0]['num'] > 0:
            return res
            # outs = []
            # while cur.forward():
            #     # ????
            #     input_node = list(cur.current().subgraph().nodes())[0] #??###
            #     outs.append(input_node)
            #     formula = cur.current()
            # return outs
        else:
            return None
    elif res is None:
        raise Exception('can_calculate wrong cql')

# calculated_dict = {} # id: (0/1, value) 1:calculated_dict; 0:directly get value
# before return, update calculated_dict{} 
# calculated_dict
def DFS_calc(item_node, depth=0, depth_limit=99, update = False, debug = 1, calc_assets = True):

    item_id = remote(item_node)._id
    # whether calculated already?
    if item_id in calculated_dict.keys():
        return calculated_dict[item_id][1]

    # have assets? and sum_assets 
    sum = sum_assets(item_node)
    if sum is not None and calc_assets:
        calculated_dict[item_id] = (1, sum)
        return sum 

    # can be calculated?  
    data = can_calculate(item_node)
    if data is None:
        # fetch value directly 
        value = item_node['value']
        if value is None:
            value = 0.0
        calculated_dict[item_id] = (0, value)
        return item_node['value']
    else:
        # recursively calculate value
        inputs = []
        formula = data[0]['formula']
        excp_formu = formula
        for  da in data:
            input_node = da['items']
            value = DFS_calc(input_node, depth=depth+1, depth_limit=depth_limit, update = update, debug = debug, calc_assets = calc_assets)
            if value is None:
                print('value is None, id, name', remote(input_node)._id, input_node['ELE_NAME'])
                value = 0.0
            inputs.append(value)

        try:
            # program
            if formula.count('\n') > 1:

                # !
                gl = {'out': '0'}
                formula = formula % tuple([ str(x) for x in inputs])
                exec(formula, gl)
                value = str(gl['out'])
            # formula
            else:
                for i,v in enumerate(inputs[::-1]):
                    # i+1!!
                    i = len(inputs) - i
                    formula = formula.replace('s'+str(i), str(v))
                value = eval(formula)
        except Exception as e:
            print(str(e))
            # traceback.print_exc()
            print()
            print(tuple(inputs))
            print(formula)
            print(excp_formu)
            print('============')
        # ??????
        else:
            calculated_dict[item_id] = (1, value)
            return value
            
        


if __name__ == '__main__':

    path = 'TableOfMinimumCapitalAbstract-MinimumCapitalUnderSolvencyII-end'
    current = merge_item(path, com='000009', date='20161231', create = False, debug = False )
    calculated_dict = {}
    # def DFS_calc(item_node, depth=0, depth_limit=99, update = False, debug = 1, calc_assets = True):
    value = DFS_calc(current, depth=0, depth_limit=3, update = False, debug = 1, calc_assets = True)
    print('--------')
    print(current['value'])
    print(value)
    print(value / float(current['value']))

    print('===========end calculated_dict')
    print(calculated_dict)



    # sql_dwzd_date  = ''' SELECT   distinct a.DWZD_BH AS '机构编号', a.INST_DATE AS '发生日期', b.y as name
    #             FROM psx_dw_instdata a , (
    #                  select DWZD_BH as x, DWZD_MC  as y from rpt_dwzd where dwzd_bh in (
    #               SELECT   distinct a.DWZD_BH as bh
    #                     FROM psx_dw_instdata a
    #                     where length(a.DWZD_BH) = 6
    #             )) b
    #             where length(a.DWZD_BH) = 6 and a.DWZD_BH = b.x
    #              '''

    # results_dwzd_date = query(sql_dwzd_date)
    # for com, date, dw_name in results_dwzd_date[:]:
    #     create_calc_node(com, date)



