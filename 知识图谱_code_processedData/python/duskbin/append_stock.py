from sshtunnel import SSHTunnelForwarder
import pymysql
from py2neo import Graph, Node, Relationship, NodeSelector
import re

graph = Graph(
    "http://211.87.234.115:7474",
    username="neo4j",
    # password="neo4jSPLab
    password='123456'
)
selector = NodeSelector(graph)


def write(*string):
    with open("./stock.log", "a+") as file:
        for i in string:
            print(i, file=file, end=" -***- ")
        print("", file=file)


def query(sql):
    connect = pymysql.connect(
        host='211.87.234.115',  # must be
        port=3306,
        user='splabuser',
        passwd='111111',
        db='circ_report',
        charset='utf8'
    )
    cursor = connect.cursor()
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(str(e))


# 将RDB里面一行映射到neo4j里面
def row2neo(neo_node_relation, item_names, row_sql, date, node_member):
    tx = graph.begin()
    nodes_dict = {}
    relations = []
    for row in neo_node_relation:
        label = re.split(':|-', row[0])[1].strip()

        property_keys = [item_names[int(s)] for s in row[1:] if s.strip() != '']
        values = [row_sql[int(s)] for s in row[1:] if s.strip() != '']
        properties = {}
        for i in range(len(property_keys)):
            properties[property_keys[i]] = values[i]

        if row[0].split(':')[0].strip() == 'node':
            # if not exists create node
            n = Node(label, **properties)
            nodes_dict[label] = n
        else:  # create relation
            properties['inst_date'] = date
            properties['member_name'] = node_member['ELE_NAME']
            n = node_member
            m = nodes_dict[row[0].split(':')[1].split('-')[2].strip()]
            relations.append(Relationship(n, label, m, **properties))  # 收集好所有的子图元素，一起create commit，提高效率
    try:
        for n in nodes_dict.values():
            tx.merge(n)
        for r in relations:
            tx.merge(r)
        tx.commit()
    except Exception as e:
        print('neo4j transaction failed')
        print(str(e))
    else:
        print('neo4j transaction success-- one row of RDB success')


sql_dwzd_date ='''
 SELECT   distinct a.DWZD_BH AS '机构编号', a.INST_DATE AS '发生日期'
    FROM psx_dw_instdata a
    where length(a.DWZD_BH) = 6
'''
results_dwzd_date = query(sql_dwzd_date)
###
results_dwzd_date = results_dwzd_date[:2]

# read the er.csv
csv_data = []
'''
keys:
    'table_abstract':table_abstract,
    'tables':tables,
    'item_names':item_names,
    'neo_node_relation':neo_node_relation,
    'sql':sql
'''
import csv

with open('./er.csv', encoding="gbk") as csvfile:
    spamreader = csv.reader(csvfile, quotechar='"')
    paragraph = []  # 每个abstract表的所有要素
    # csvreader里面是二维元组，行-列
    for cols in spamreader:
        # 完整的一段，开始处理一张abstract表
        if cols[0] == 'end':
            # decode 元素
            table_abstract = paragraph[1][0]
            tables = paragraph[1][1].split('-')
            item_names = paragraph[1][2:]
            neo_node_relation = paragraph[4:]  # deep copy
            sql = paragraph[3][1]
            csv_dic = {
                'table_abstract': table_abstract,
                'tables': tables,
                'item_names': item_names,
                'neo_node_relation': neo_node_relation,
                'sql': sql
            }
            csv_data.append(csv_dic)

            paragraph = []
        else:
            c2 = [col for col in cols if col != '']
            paragraph.append(c2)

count = 0  # import json
# for i in csv_data:
#     print(json.dumps(i, sort_keys=True, indent=4, separators=(',', ': ')))

# 复制概念知识图谱的树
# copy from element, and append security and stock to the corresbonding Member
for com, date in results_dwzd_date:
    node_com = selector.select('company', dwzd_bh=com).first()
    if node_com is None:
        node_com = Node('company', dwzd_bh=com)
        graph.merge(node_com)
    node_date = Node('date', inst_date=date)
    graph.create(node_date)
    graph.merge(Relationship(node_com, 'link', node_date))  # 直接新建还是把别人的node_date 给拿过来了？

    tmp = selector.select('element', ELE_NAME='TableOfSolvencyStatusAbstract').first()
    fi = Node('instance', dwzd_bh=com, inst_date=date, ELE_NAME=tmp['ELE_NAME'], LABEL_ZH=tmp['LABEL_ZH'])
    graph.create(fi)
    graph.merge(Relationship(node_date, 'link', fi, name=tmp['ELE_NAME']))

    layer1 = [fi]

    # traverse the element graph , and copy to new instance graph
    for ni in layer1:
        res = graph.data(
            "match(n:element)-[:contains]->(m:element) where n.ELE_NAME = '%s' return m.ELE_NAME as ELE_NAME  " % (ni['ELE_NAME']))
        # 重名的怎么办？？？ -- use id

        layer_str2 = [j['ELE_NAME'] for j in res]
        # create nodes and relationships
        for j in layer_str2:
            node_j = selector.select('element', ELE_NAME=j).first()
            node_next = Node('instance', dwzd_bh=com, inst_date=date, ELE_NAME=node_j['ELE_NAME'],
                             LABEL_ZH=node_j['LABEL_ZH'])
            graph.create(node_next)
            layer1.append(node_next)
            ### first () 就是很有问题的，也因为会可能有很多个啊 ，，，，，
            graph.merge(Relationship(ni, 'link', node_next, name=ni['ELE_NAME']))

            # append the stocks， security ... to member
            for k in csv_data:
                #### 依据 abstract + 直接相连的叫members。 嵌套就不能解决…… 哭死
                if ni['ELE_NAME'] == k['table_abstract'] and j in k['tables']:
                    print(j)

                    ##todo 别的SQL？ 参数数量多？
                    result = query(sql % (com, date, j))
                    if result is None:
                        write("sql - return None  dwbh %s date %s table %s " % (com, date, j))
                        break;

                    for sql_result in result:
                        ####
                        count += 1
                        if count > 12: break

                        # print(type(sql_result))
                        # for tt in sql_result:
                        #     print(str(tt))
                        print(k['item_names'])

                        row2neo(neo_node_relation=k['neo_node_relation'], item_names=k['item_names'],
                                row_sql=sql_result,
                                date=date, node_member=node_next)
                    count = 0
                    break
