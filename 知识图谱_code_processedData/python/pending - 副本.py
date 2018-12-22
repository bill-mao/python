import pymysql
from py2neo import Graph, Node, Relationship, NodeSelector, remote
import traceback
import csv
# import sys  


# py2neo 里面的查询工具； 全局变量
graph = Graph(
    # "http://localhost:7474", 
    # username="neo4j", 
    # password="neo4jSPLab"

    "http://211.87.234.115:7474",
    # host = 'localhost',
    username='neo4j',
    password = '123456'

)

selector = NodeSelector(graph)


'''写入log文件 调试

Arguments:
    *string {str} -- 写入字符串内容

Keyword Arguments:
    path {str} -- 写入log文件位置 (default: {"./default.log"})
'''
def write(*string, path ="./default.log" ):
    with open(path , "a+") as file:
        for i in string:
            print(i, file=file)
        print("", file=file)
        print("==================", file = file)
        traceback.print_exc(file = file)
        print('========================================================\n\n',file = file)


'''封装 pymysql 里面的函数

当SQL出错时写入日志文件：./sql_wrong.log 返回 None      
        
Arguments:  
    sql {str} -- 查询SQL

Returns:
    tuple -- ( (row,,,), (row2, ,,) )
'''
def query(sql):
    connect = pymysql.connect(
        host='211.87.234.115',  # must be
        port=3306,
        user='splabuser',
        passwd='111111',
        db='circ_report',
        charset='utf8'
    )
    try:
        with connect.cursor() as cursor:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            # connect.commit()
            return results
    except Exception as e:
        write("wrong sql ", sql, path = './sql_wrong.log')
        return None

    finally:
        connect.close()


'''读取配置文件
 
Keyword Arguments:
    path {str} --  (default: {'./er.csv'})

Returns:
    dict -- key是abstract 表的ele_name
'''
def read_csv(path='./er.csv'):
    with open(path, encoding="gbk") as csvfile:
        spamreader = csv.reader(csvfile, quotechar='"')
        paragraph = []  # 每个abstract表的所有要素
        ercsv = {}
        # csvreader里面是二维元组，行-列
        count = 0
        for cols in spamreader:

            #跳过空行
            if cols == [] or cols[0].strip() == '':
                continue
            # 完整的一段，开始处理一张abstract表
            try:
                if cols[0] == 'end':
                    abstract = paragraph[1][0]
                    abstract_zh = paragraph[2][0]
                    layers = []
                    layers_zh = []
                    dim = ''
                    sql = ''
                    nodes = []
                    relations = []

                    for row in paragraph:
                        if row[0] == 'layer':
                            # 人工写错，一定要清洗一下数据
                            layers.append([rs.strip() for rs in row[1].split('-') ])
                        elif row[0] == 'layer_zh':          
                            layers_zh.append([rs.strip() for rs in row[1].split('-') ])

                        elif row[0] == 'sql':
                            sql = '#' +abstract_zh +'\n\n' +row[1]
                            if len(row) > 2:
                                dim = row[2]
                            else:
                                dim = ''
                        elif row[0].split(":")[0].strip() == 'node':
                            nodes.append(row)
                        elif row[0].split(":")[0].strip() == 'relation':
                            relations.append(row)

                    ercsv[abstract] = {
                        'abstract_zh' : abstract_zh,
                        'tables': [ i.strip() for i in paragraph[1][1].split('-')],
                        'tables_zh': paragraph[2][1].split('-'),
                        'items': paragraph[1][2:],
                        'items_zh': paragraph[2][2:],
                        'layers': layers,
                        'layers_zh': layers_zh,
                        'dim': dim,
                        'sql': sql,
                        'nodes': nodes,
                        'relations': relations
                    }
                    paragraph = []
                else:
                    c2 = [col.strip() for col in cols if col.strip() != '']
                    if c2 != []:
                        paragraph.append(c2)
            except Exception as e:
                print(traceback.print_exc())

    return ercsv


'''添加有行次的member节点下面的外部节点
    错误写入的日志文件：
         "./sql_parameters.log")   
         "./assets_sql_wrong.log")
        "./assets_sql_null.log")
         "./assets_sql_000.log"
Arguments:
    node_member {py2neo.Node} -- 外部节点的父节点
    items {list} -- 
    sql {str} -- 查询行次的sql
    parameters {list} -- 格式化SQL的变量
    date {str} -- 报送时间
    nodes {list} -- 存放er.csv node行的数据
    relations {list} -- er.csv 里面relation行的数据

Returns:
    bool -- 是否插入成功； if seccessiful return True else return None
'''
def add_assets(node_member, items, sql, parameters, date, nodes, relations):
    try:
        # 有问题就插入 '0' 保证 item 不空
        if sql.count("%s") != len(parameters):
            insert_values(node_member, items, [])
            print("add_assets,  wrong sql, parameters", parameters, sql)
            return 

        sql_results = query(sql % parameters)
        
        # 说明SQL有问题，一般不会发生，所以print
        if sql_results is None :
            print("sql None - member_node:",node_member['ELE_NAME'], " - dwbh date table .. is  ", 
                parameters, sql % parameters,  )
        elif sql_results is ():
            # write("sql return () ",node_member['ELE_NAME'], " - dwbh date table .. is  ", 
            #     parameters,sql % parameters, path = 'asset_sql_().log'  )
            pass

        count_0 = 0
        to_insert_values = []
        for row in sql_results:
            # 0 is the total value
            # 比较特殊的Mr 03 债券节点里面的名称都是'0'
            # if row.count('0') > 3:
            if row[0] == '0' and  row.count('0') > 2 :
                to_insert_values.append(row)
                count_0+=1

            else:
                tx = graph.begin()
                no = nodes[0]
                rel = relations[0]

                # asset node
                label = no[0].split(':')[1]
                property_keys = [items[int(i)] for i in no[1:]]
                values = [row[int(i)] for i in no[1:]]
                properties = {}
                for i in range(len(property_keys)):
                    properties[property_keys[i]] = values[i]
                asset_node = Node(label, **properties)

                # relation node
                label = 'own_amount'
                property_keys = [items[int(i)] for i in rel[1:]]
                values = [row[int(i)] for i in rel[1:]]
                properties = {}
                for i in range(len(property_keys)):
                    properties[property_keys[i]] = values[i]
                amount_node = Node(label, **properties)

                # link these two together

                try:
                    tx.merge(asset_node)
                    tx.create(amount_node)
                    tx.create(Relationship(node_member, "own", amount_node))
                    tx.create(Relationship(amount_node, "own", asset_node))
                    tx.commit()
                except Exception as e:
                    print('neo4j transaction failed')
                    print(traceback.print_exc())
                # else:
                    # print('neo4j transaction success-- one row of RDB success')
            
        # end of add_assets
        
        if count_0 > 1:
            
            # print("0 太多。。。to_insert_values",to_insert_values , items, parameters,'\n\n' , sql % parameters)
            # print("but insert still")
            insert_values(node_member, items, to_insert_values[0])

            for cols_0 in to_insert_values[1:]:

                tx = graph.begin()
                no = nodes[0]
                rel = relations[0]

                # asset node
                label = no[0].split(':')[1]
                property_keys = [items[int(i)] for i in no[1:]]
                values = [cols_0[int(i)] for i in no[1:]]
                properties = {}
                for i in range(len(property_keys)):
                    properties[property_keys[i]] = values[i]
                asset_node = Node(label, **properties)

                # relation node
                label = 'own_amount'
                property_keys = [items[int(i)] for i in rel[1:]]
                values = [cols_0[int(i)] for i in rel[1:]]
                properties = {}
                for i in range(len(property_keys)):
                    properties[property_keys[i]] = values[i]
                amount_node = Node(label, **properties)

                # link these two together

                try:
                    tx.merge(asset_node)
                    tx.create(amount_node)
                    tx.create(Relationship(node_member, "own", amount_node))
                    tx.create(Relationship(amount_node, "own", asset_node))
                    tx.commit()
                except Exception as e:
                    print('neo4j transaction failed')
                    print(traceback.print_exc())
                # else:
                    # print('neo4j transaction success-- one row of RDB success')

        elif count_0 ==1:
            insert_values(node_member, items, to_insert_values[0])  
        # 保证，最终有item， 不会漏
        elif count_0 == 0:
            insert_values(node_member, items, [])
        return True
    except Exception as e:
        print("========================================================")
        print("appending assets (node_member, items, sql, parameters, date, nodes, relations):")
        print(node_member, items, sql, parameters, date, nodes, relations)
        traceback.print_exc()
        print("========================================================")



'''查询一行的值然后插入 neo4j 的member下面的item 

'insert_values_null.log'

Arguments:
    node_member {py2neo.Node} -- item节点的父节点
    items {list} -- item的英文名
    values {lsit} -- 数据库里面返回的一行

Keyword Arguments:
    label {str} -- 插入节点的label (default: {'item'})
    rel_label {str} -- 插入边的label (default: {'linkitem'})
    debug {number} -- 调试等级 (default: {1})

Returns:
    bool -- if seccessiful return True else return None
'''
def insert_values(node_member, items, values, label= 'item', rel_label= 'linkitem' , debug = 1):

    # print(items, values)
    # 假如为空就插入'0'  ； 这样能够省很多事！！！！****
    if values is None or len(values) == 0 or len(values) != len(items):
        # write("values are None or () " , node_member['ELE_NAME'], path= 'insert_values_null.log')
        values = ['0' for i in range(len(items))]

    nodes = []
    for i,v in zip(items, values):
        pro = {
            'ELE_NAME' : i,
            'value' : v
        }
        # print(pro)
        nodes.append(Node(label, **pro))

    relations = [Relationship(node_member, rel_label, node) for node in nodes]
    for node in nodes:
        if not isinstance(node, Node):
            print(node , "is not Node !!! insert_values")
    tx = graph.begin()
    try:
        # for n in nodes:
        #     tx.create(n)
        for r in relations:
            tx.create(r)
        tx.commit()
    except Exception as e:
        print("============================ com,date ")
        global com, date
        print(com,date)
        print('insert values failed  node_member, items, values, ')
        print(node_member['ELE_NAME'], items, values)
        print("============================")
        for n in nodes:
            print("*******nodes name ",n['ELE_NAME'])
        traceback.print_exc()
    return True


'''BFS遍历template树中的一个节点

创建instance 对应的下一层的子节点，然后返回

Arguments:
    node {py2neo.Node} -- instance树的父节点： 里面存在一个id属性，记录对应template树中的相应节点的 _id
    label {str} -- 新创建的节点的label
    rel_label {str} -- 

Returns:
    py2neo.Node -- 返回新创节点
'''
def create_son_nodes(node, label, rel_label):
    # id id id
    id = node['id']
    records = graph.run("match(n:template)-[:contains]->(m:template) where id(n) = %d return m  " % (id))
    node_sons = []
    for r in records:
        node_sons.extend(r.subgraph().nodes())

    # create nodes
    nodes = []
    tx = graph.begin()
    for n in node_sons:
        new = Node(label, ELE_NAME=n['ELE_NAME'], LABEL_ZH=n['LABEL_ZH'], id=remote(n)._id)
        tx.create(new)
        nodes.append(new)
    tx.commit()

    # create relationships
    tx = graph.begin()
    for w in nodes:
        # create relation
        tx.create(Relationship(node, rel_label, w , ELE_NAME = node['ELE_NAME']))
    tx.commit()
    return nodes


'''查看SQL返回tuple是否有问题

Arguments:
    values {tuple} -- sql返回

Keyword Arguments:
    debug {number} -- 调试等级，默认输出全部调试信息 (default: {1})

Returns:
    bool -- 是否有问题
'''
def values_sql_log(values, debug  =1):
    if values is None : 
        if debug > 0:
            write("sql values None --   ", com, date, qn['ELE_NAME'], path = './layer1_sql.log')
        return False
    elif values == ():
        if debug > 0:
            write("sql values is () --   ", com, date, qn['ELE_NAME'], path = './layer1_sql.log')
        return False
    elif len(values) != 1:
        if debug > 0:
            write("sql values len  >1 --   ", com, date, qn['ELE_NAME'], path = './layer1_sql.log')
        return False

    else :
        return True


'''返回父节点
Arguments:
    son_node {py2neo.Node} -- 

Keyword Arguments:
    father_label {str} --  (default: {'instance'})
    son_label {str} --  (default: {'instance'})
    rela_label {str} --  (default: {'link'})

Returns:
    list -- 所有的父节点
'''
def find_father_node(son_node, father_label = 'instance', son_label ='instance', rela_label= 'link'):

    try:
        cur = graph.run(''' 
            match (m:%s)-[:%s]->(n:%s)
            where id(n) = %d
            return m                
         ''' %(father_label, rela_label, son_label, remote(son_node)._id))
        fathers =[]
        while cur.forward():
            father_node = list(cur.current().subgraph().nodes())[0] #??###
            fathers.append(father_node)
        return fathers
    except Exception as e:
        write("can't find father", path = './no_father.log')
        return None


if __name__ == '__main__':
    single_dim_gid = '''
     and DIM_GID in (SELECT OID FROM psx_dimension_group WHERE MEMBER_VALUE = 
    (SELECT OID FROM psx_element 
    WHERE ELE_NAME = '%s') 
    )
    '''
    ercsv = read_csv()
    # import json
    # print(json.dumps(ercsv, sort_keys=True, indent=4, separators=(',', ': ')))

    sql_dwzd_date = '''
        SELECT   distinct a.DWZD_BH AS '机构编号', a.INST_DATE AS '发生日期'
        FROM psx_dw_instdata a
        where length(a.DWZD_BH) = 6
    '''

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
    ###
    # results_dwzd_date = results_dwzd_date[3:9]

    for com, date, dw_name in results_dwzd_date:
        node_com = Node('company', dwzd_bh=com, name = dw_name)
        graph.merge(node_com)
        node_date = Node('date', inst_date=date)
        graph.create(node_date)
        graph.merge(Relationship(node_com, 'link', node_date))

        tmp = selector.select('template', ELE_NAME='TableOfSolvencyStatusAbstract').first()
        fi = Node('instance', ELE_NAME=tmp['ELE_NAME'], LABEL_ZH=tmp['LABEL_ZH'], id=remote(tmp)._id)
        graph.create(fi)
        graph.merge(Relationship(node_date, 'link', fi, name=tmp['ELE_NAME']))
        # traversal by Abstract  每次遇到子的abstract node 就放入queue_abstract 里面，并且不添加其子节点
        # 按照一颗一颗abstract树来遍历
        queue_abstract = [fi] 

        # 遍历abstract表
        for qa in queue_abstract:
            wait = create_son_nodes(qa, 'instance', 'link')
            queue_node = []  # consist of pending nodes of a abstract tree
            for w in wait:
                if w['ELE_NAME'].endswith("Abstract"):
                    queue_abstract.append(w)
                else:
                    queue_node.append(w)

            name_abstract = qa['ELE_NAME']
            # dicta -- dict_abstract 调试时候，abstract 不全
            dicta = {}
            # 开始SQL建立实例过程
            if name_abstract in ercsv.keys():
                dicta = ercsv[name_abstract]
                # 添加abstract直属的assets
                # stock directly hangs in the Abstract node
                if name_abstract in dicta['tables']:
                    if dicta['layers'] == []:
                        if dicta['nodes'] != []:
                            # hang the stocks
                            para = (com, date)
                            add_assets(qa, dicta['items'], dicta['sql'], para, date, dicta['nodes'], dicta['relations'])
                # 插入空值，，
                # insert_values(qa, dicta['items'] , [])
                else:
                    insert_values(qa, dicta['items'] , [])
  
            # BFS 当前abstract表下面的所有元素
            # find all son_node of qa, if not endswith Abstract then append to queue_node
            # query mysql, insert data into instance_graph in neo4j
            for qn in queue_node:
                wait = create_son_nodes(qn, 'instance', 'link')
                for w in wait:
                    if w['ELE_NAME'].endswith("Abstract"):
                        queue_abstract.append(w)
                    else:
                        queue_node.append(w)

                # member节点的实例化
                try:
                    # 一层
                    # if dicta['layers'] == [] and qn['ELE_NAME'] in dicta['tables']:
                    # 改了条件，就应该全部改掉啊！！
                    if dicta['layers'] == [] :
                        if qn['ELE_NAME'] in dicta['tables']:
                            # insert value
                            if dicta['nodes'] == []:
                                values = query(dicta['sql'] % (com, date, qn['ELE_NAME']))
                                if values is None or values == (): 
                                    # write("sql None -- 第一层 insert values ", com, date, qn['ELE_NAME'])
                                    pass
                                    # continue
                                #### 返回的是2维元祖！！ 
                                # if len(values) == 1:
                                # 否则的话，values就会因为是None报错
                                elif len(values) ==1 :
                                    values = values[0]
                                #### 
                                elif len(values) > 1:
                                    print("========================================================")
                                    print("query value return more than one !!")
                                    print(qa['LABEL_ZH'], qn['LABEL_ZH'], com, date)
                                    values = ()
                                insert_values(qn, dicta['items'], values )

                            # hang the stock and insert values
                            else:
                                para = (com, date,  qn['ELE_NAME']  )
                                # para = (com, date, dicta['dim'] % qn['ELE_NAME']  )  # dim_gid = ' ' 没有用啊。。
                                add_assets(qn, dicta['items'], dicta['sql'], para, date , dicta['nodes'], dicta['relations'])
                        else:
                            # should be in tables ? why 
                            print("==============qn['ELE_NAME'] not  in dicta['tables']:============== ")
                            print(qn['ELE_NAME'], qn['LABEL_ZH'], dicta['tables'])
                            print('========================================================')

                    # 两层
                    else:
                        layer1 = dicta['layers'][0]
                        layer2 = dicta['layers'][1]
                        # 在layer1 的时候处理下层的所有member，毕竟只有两层， 而且已经create son node 了
                        if qn['ELE_NAME'] in layer1:
                            # insert value of muti-layers' values
                            # 笛卡尔积-- 最对2维 -- 这儿就是2维
                            l1 = qn['ELE_NAME']
                            values = query(dicta['sql'] % (com, date, single_dim_gid % l1))
                            if not values_sql_log(values, debug = -1):
                                #### 返回的是2维元祖！！ 
                                values = []
                            else:    
                                values = values[0]

                            insert_values(qn, dicta['items'], values, debug = -1)
                                                        
                        #######
                        elif qn['ELE_NAME'] in layer2:    
                            # find father node 
                            fas = find_father_node(qn)
                            if fas is None :
                                write('can\'t find father')
                                continue
                            elif len(fas) != 1:
                                write('fathers != 1 ')
                                continue
                            else :
                                father_node = fas[0]
                            l1 = father_node['ELE_NAME']
                            l2 = qn['ELE_NAME']
                            # insert values
                            if dicta['nodes'] == []:
                                values = query(dicta['sql'] % (com, date, dicta['dim'] % (l1, l2)))
                                if values_sql_log(values):
                                    #### 返回的是2维元祖！！ 
                                    values = values[0]
                                else:
                                    values = []
                                insert_values(qn, dicta['items'], values)

                            # add_asset
                            else:
                                para = (com, date, dicta['dim'] % (l1, l2))
                                if len(para) != dicta['sql'].count('%s'):
                                    pass
                                    # frame_info ='' , sys._getframe().f_code.co_name , sys._getframe().f_lineno, '\n' # 当前函数名 
                                    # write(frame_info, 'lenth para != sql % qa', dicta['sql'], para) 
                                add_assets(qn, dicta['items'], dicta['sql'], para, date,dicta['nodes'], dicta['relations'] )
                except TypeError as te:
                    print("========================================================")
                    print((com, date, single_dim_gid % l1), dicta['sql'] , )
                    traceback.print_exc()
                    print("========================================================")

                except Exception as e:
                    print(dicta)
                    print(traceback.print_exc())



