import pymysql
from py2neo import Graph, Node, Relationship, NodeSelector, remote
import traceback
import csv
import sys  


graph = Graph(
    "http://211.87.234.115:7474",
    username="neo4j",
    # password="neo4jSPLab
    password='123456'
)
selector = NodeSelector(graph)


# load csv convert to dict
'''
ercsv[abstract] = {
    'tables' :  paragraph[1][1].split('-'),
    'tables_zh' : paragraph[2][1].split('-'),

    'items' : paragraph[1][2:],
    'items_zh' :  paragraph[2][2:],
    'layers' : layers,
    'layers_zh' : layers_zh,
    'dim' : dim,
    'sql' : sql,
    'nodes' : nodes ,
    'relations' :  relations
}
'''


def write(*string):
    with open("./stock.log", "a+") as file:
        for i in string:
            print(i, file=file)
        print("", file=file)
        print("==================", file = file)
        traceback.print_exc(file = file)

        print('========================================================\n\n', file= file)

# return ( (row,,,), (row2, ,,) )
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
            if results is None:
                write("query() - sql None   ", sql)
            # connect.commit()
    except Exception as e:
        write("query() Exception ")

    finally:
        connect.close()
    return results


##todo
def add_assets(node_member, items, sql, parameters, date, nodes, relations):

    if sql.count("%s") != len(parameters):
        write("  ")    
    sql_results = query(sql % parameters)
    if sql_results is None or sql_results is ():
        write("============================sql None - member_node:",node_member['ELE_NAME'], " - dwbh date table .. is  ", parameters)
        return
    for row in sql_results:
        ### 0 is the total value?
        if row[0] == '0':
            insert_values(node_member, items, row)  ###
        else:
            tx = graph.begin()
            nodes_dict = {}
            relationships = []
            for no in nodes:
                label = no[0].split(':')[1]
                property_keys = [items[int(i)] for i in no[1:]]
                values = [row[int(i)] for i in no[1:]]
                properties = {}
                for i in range(len(property_keys)):
                    properties[property_keys[i]] = values[i]

                n = Node(label, **properties)
                nodes_dict[label] = n
                # print(label, properties)
            for rel in relations:
                # label = rel[0].split(':')[1].split('-')[0]
                label = 'own'
                property_keys = [items[int(i)] for i in rel[1:]]
                values = [row[int(i)] for i in rel[1:]]
                properties = {}
                for i in range(len(property_keys)):
                    properties[property_keys[i]] = values[i]

                m = nodes_dict[rel[0].split(":")[1].split("-")[2]]
                relationships.append(Relationship(node_member, label, m, **properties))
                # print(label, properties)

            try:
                for n in nodes_dict.values():
                    tx.merge(n)
                # for r in relations:
                for r in relationships:
                    tx.merge(r)
                tx.commit()
            except Exception as e:
                print('neo4j transaction failed')
                print(str(e))
                print(traceback.print_exc())
            else:
                # print('neo4j transaction success-- one row of RDB success')
                pass


# create linkitems relation -> items node
def insert_values(node_member, items, values, label= 'item', rel_label= 'linkitem'):
    # print(items, values)
    if values is None or len(values) == 0:
        return
    # #bug !!!*** item  ;;;直接变成属性名称了。。
    # nodes = [Node(label, item=value) for item, value in zip(items, values)]
    nodes = []
    #####****
    # for i, v in items, values:
    # print( items, values )
    for i,v in zip(items, values):
        pro = {
            'ELE_NAME' : i,
            'value' : v
        }
        # print(pro)
        nodes.append(Node(label, **pro))
    relations = [Relationship(node_member, rel_label, node) for node in nodes]
    # for r in relations:
    #     print(r)
    tx = graph.begin()
    try:
        # for n in nodes:
        #     tx.create(n)
        for r in relations:
            # print("*******", r)
            tx.create(r)
        tx.commit()
    except KeyError as k:
        pass
    except Exception as e:
        pass
        print('insert values failed  ', str(e))
        for r in relations:
            print("*******", r)
        print(traceback.print_exc())
    



# return nodes
def create_son_nodes(node, label, rel_label):
    # id id id
    id = node['id']
    records = graph.run("match(n:element)-[:contains]->(m:element) where id(n) = %d return m  " % (id))
    node_eles = []
    for r in records:
        node_eles.extend(r.subgraph().nodes())

    nodes = []
    tx = graph.begin()
    for n in node_eles:
        new = Node(label, ELE_NAME=n['ELE_NAME'], LABEL_ZH=n['LABEL_ZH'], id=remote(n)._id)
        tx.create(new)
        nodes.append(new)
    tx.commit()

    tx = graph.begin()
    for w in nodes:
        # create relation
        tx.create(Relationship(node, rel_label, w , ELE_NAME = node['ELE_NAME']))
    tx.commit()
    return nodes


def read_csv(path='./er.csv'):
    with open(path, encoding="gbk") as csvfile:
        spamreader = csv.reader(csvfile, quotechar='"')
        paragraph = []  # 每个abstract表的所有要素
        ercsv = {}
        # csvreader里面是二维元组，行-列
        count = 0
        for cols in spamreader:

            # print(cols)
            ###
            if cols == [] or cols[0].strip() == '':
                continue
            # count +=1
            # if count >7: break
            # print (cols)
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
                            layers.append(row[1].split('-'))
                            # has dim
                            # if len(row) >2 :
                            #     dim.append(row [3])
                        # elif row[0] == 'layers_zh':
                        elif row[0] == 'layer_zh':			
                            layers_zh.append(row[1].split('-'))
                        elif row[0] == 'sql':
                            sql = row[1]
                            if len(row) > 2:
                                dim = row[2]
                            else:
                                dim = ''
                        elif row[0].split(":")[0] == 'node':
                            nodes.append(row)
                        elif row[0].split(":")[0] == 'relation':
                            relations.append(row)

                    ercsv[abstract] = {
                        'abstract_zh' : abstract_zh,
                        'tables': paragraph[1][1].split('-'),
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


if __name__ == '__main__':
    single_dim_gid = '''
    and DIM_GID in (SELECT OID FROM psx_dimension_group WHERE MEMBER_VALUE = 
    (SELECT OID FROM psx_element 
    WHERE ELE_NAME = '%s') 
    )
    '''

    # frame_info ='' , sys._getframe().f_code.co_name , sys._getframe().f_lineno # 当前函数名 
    # write(frame_info) 

    ercsv = read_csv()

    # import json

    # print(json.dumps(ercsv, sort_keys=True, indent=4, separators=(',', ': ')))

    sql_dwzd_date = '''
     SELECT   distinct a.DWZD_BH AS '机构编号', a.INST_DATE AS '发生日期'
        FROM psx_dw_instdata a
        where length(a.DWZD_BH) = 6
    '''

    results_dwzd_date = query(sql_dwzd_date)
    ###
    results_dwzd_date = results_dwzd_date[:2]
    for com, date in results_dwzd_date:
        node_com = Node('company', dwzd_bh=com)
        graph.merge(node_com)
        node_date = Node('date', inst_date=date)
        graph.create(node_date)
        graph.merge(Relationship(node_com, 'link', node_date))

        tmp = selector.select('element', ELE_NAME='TableOfSolvencyStatusAbstract').first()
        fi = Node('instance', ELE_NAME=tmp['ELE_NAME'], LABEL_ZH=tmp['LABEL_ZH'], id=remote(tmp)._id)
        graph.create(fi)
        graph.merge(Relationship(node_date, 'link', fi, name=tmp['ELE_NAME']))
        # traversal by Abstract  每次遇到子的abstract node 就放入queue_abstract 里面，并且不添加其子节点
        queue_abstract = [fi]  # consist of Abstract Node id()

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
            if name_abstract in ercsv.keys():
                dicta = ercsv[name_abstract]

            try:
                # stock directly hangs in the Abstract node
                if name_abstract in dicta['tables']:
                    if dicta['layers'] == []:
                        if dicta['nodes'] != []:
                            # hang the stocks
                            para = (com, date)
                            if len(para) != dicta['sql'].count('%s'):
                                frame_info ='' , sys._getframe().f_code.co_name , sys._getframe().f_lineno, '\n' # 当前函数名 
                                write(frame_info, 'lenth para != sql % qa', dicta['sql'], para) 
                            else:
                                add_assets(qa, dicta['items'], dicta['sql'], para, date, dicta['nodes'], dicta['relations'])
                        else:
                            # insert values; no need due to 不是member但是 行的名字
                            pass
                            # for member in
                            # values = query(sql %member)
                            # insert_values(qa, dicta['items'], values)

                    else:
                        print('abstract not only one ? impossible')
            except KeyError as k:
                pass
            except Exception as e:
                print(traceback.print_exc())

            # BFS qa tree
            # find all son_node of qa, if not endswith Abstract then append to queue_node
            # query mysql, insert data into instance_graph in neo4j
            for qn in queue_node:
                wait = create_son_nodes(qn, 'instance', 'link')
                for w in wait:
                    if w['ELE_NAME'].endswith("Abstract"):
                        queue_abstract.append(w)
                    else:
                        queue_node.append(w)
                # search qn in ercsv's tables, if matched then query mysql
                # ### no need deal with dim, dirctly sql
                # if dicta['dim'] == '':
                #     pass
                # else:
                #     sql

                try:
                    if dicta['layers'] == []:

                        if qn['ELE_NAME'] in dicta['tables']:
                            # insert value
                            if dicta['nodes'] == []:
                                values = query(dicta['sql'] % (com, date, qn['ELE_NAME']))
                                if values is None or values == (): 
                                    write("sql None -- ", com, date, qn['ELE_NAME'])
                                    continue
                                #### 返回的是2维元祖！！ 
                                if len(values) == 1:
                                    values = values[0]
                                    insert_values(qn, dicta['items'], values, )
                                # else:
                                #     write("sql error: values len is 0 or >1， values is \n", values," sql is \n  ", dicta['sql'] )                        
                            # hang the stock and insert values
                            else:
                                para = (com, date,  qn['ELE_NAME']  )
                                # para = (com, date, dicta['dim'] % qn['ELE_NAME']  )  # dim_gid = ' ' 没有用啊。。
                                if len(para) != dicta['sql'].count('%s'):
                                    frame_info ='' , sys._getframe().f_code.co_name , sys._getframe().f_lineno, '\n' # 当前函数名 
                                    write(frame_info, 'lenth para != sql % qa', dicta['sql'], para) 
                                else:
                                    add_assets(qn, dicta['items'], dicta['sql'], para, date , dicta['nodes'], dicta['relations'])
                                # 多层嵌套！！！   自己新建node layer2
                    else:
                        # if qn['ELE_NAME'] in  dicta['tables']:
                        layer1 = dicta['layers'][0]
                        layer2 = dicta['layers'][1]
                        # print('-----', dicta['layers'], dicta['layers_zh'])
                        if qn['ELE_NAME'] in layer1:
                            # insert value of muti-layers' values
                            # 笛卡尔积-- 最对2维 -- 这儿就是2维
                            l1 = qn['ELE_NAME']
                            values = query(dicta['sql'] % (com, date, single_dim_gid % l1))
                            if values is None or values == (): 
                                write("sql None -- ", com, date, qn['ELE_NAME'])
                                continue
                            #### 返回的是2维元祖！！ 
                            if len(values) == 1:
                                values = values[0]
                                insert_values(qn, dicta['items'], values)
                            # else:
                            #     write("sql error: values len is 0 or >1， values is \n", values," sql is \n  ", dicta['sql'] )    

                            # for l2, l2_zh in zip(layer2, dicta['layers_zh']):
                            for l2, l2_zh in zip(layer2, dicta['layers_zh'][1]):
                                # print("layer2_zh name is ---", l2_zh)
                                new_node = Node('instance', ELE_NAME=l2, LABEL_ZH=l2_zh )
                                graph.create(new_node)
                                graph.create(Relationship(qn, 'link', new_node))

                                # insert values
                                if dicta['nodes'] == []:
                                    l1 = qn['ELE_NAME']
                                    values = query(dicta['sql'] % (com, date, dicta['dim'] % (l1, l2)))
                                    if values is None or values == (): 
                                        write("sql None -- ", com, date, qn['ELE_NAME'])
                                    #### 返回的是2维元祖！！ 
                                    if len(values) == 1:
                                        values = values[0]
                                        insert_values(new_node, dicta['items'], values, )
                                    # else:
                                    #     write("sql error: values len is 0 or >1， values is \n", values," sql is \n  ", dicta['sql'] )    
                                    # insert_values(qn, dicta['items'], values, )
                                # add_asset
                                else:
                                    para = (com, date, dicta['dim'] % (l1, l2))
                                    # print("--------- layer2 add_assets", para)
                                    # add_assets(qn, dicta['items'], dicta['sql'], para, date)
                                    if len(para) != dicta['sql'].count('%s'):
                                        frame_info ='' , sys._getframe().f_code.co_name , sys._getframe().f_lineno, '\n' # 当前函数名 
                                        write(frame_info, 'lenth para != sql % qa', dicta['sql'], para) 
                                    else:
                                        add_assets(new_node, dicta['items'], dicta['sql'], para, date,dicta['nodes'], dicta['relations'] )
                except KeyError as k:
                    pass
                except Exception as e:
                    print(dicta['sql'])
                    print(str(e))
                    print(traceback.print_exc())

    # print('sd')


