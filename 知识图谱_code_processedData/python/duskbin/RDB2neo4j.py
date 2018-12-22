
import pymysql
from py2neo import Graph, Node, Relationship, NodeSelector
import re



graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    # password="neo4jSPLab
    password = 'maoxingyu'
)
selector = NodeSelector(graph)

def query(sql):
    connect = pymysql.connect(
        host='127.0.0.1',  # must be
        port=3306,
        user='root',
        passwd='123456',
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
def row2neo(neo, names, row_sql, com, date, node_com, table_name):
    # neo--  start to merge node and create relations
    tx = graph.begin()
    nodes_dict = {}
    relations = []
    for row in neo:
        # print(row)
        label = re.split(':|-',row[0])[1].strip()

        property_keys = [names[int(s)] for s in row[1:] if s.strip() != '']
        values = [row_sql[int(s)] for s in row[1:] if s.strip() != '']
        properties = {}
        for i in range(len(property_keys)):
            properties[property_keys[i]] = values[i]

        if row[0].split(':')[0].strip() == 'node':
            # if not exists create node
            n = Node(label, **properties)
            nodes_dict[label] = n
        else:  # create relation
            # n = nodes_dict[row[0].split(':')[1].split('-')[1].strip()]
            # property append date
            properties['inst_date'] = date
            properties['cross_element'] = table_name
            n= node_com
            m = nodes_dict[row[0].split(':')[1].split('-')[2].strip()]
            relations.append(Relationship(n,label, m, **properties ))
    #收集好所有的子图元素，一起create commit，提高效率
    try:
        for n in nodes_dict.values():
            tx.merge(n)
        for r in relations:
            tx.merge(r)
        tx.commit()
    except Exception as e:
        print(str(e))
    else:
        print('neo4j transaction success-- one row of RDB success')


# 任务：
# for table in Tables:
#     for com, date in (dwzd_bh, inst_date):
#         query(sql)
#         根据csv文件给的节点创建 node, relation
#         添加连接到偿二代element的一条边： eg  债权security -instanceOf-> psx_element:(table)


sql_dwzd_date = '''
 SELECT   distinct a.DWZD_BH AS '机构编号', a.INST_DATE AS '发生日期'
    FROM psx_dw_instdata a
    where length(a.DWZD_BH) = 6
'''
results_dwzd_date = query(sql_dwzd_date)

import csv
with open('./er.csv', encoding="gbk") as csvfile:
    spamreader = csv.reader(csvfile, quotechar='"')
    paragraph = [] #每个abstract表的所有要素
    #csvreader里面是二维元组，行-列
    for cols in spamreader:
        #完整的一段，开始处理一张abstract表
        if cols[0] == 'end':
            #decode 元素
            tables = paragraph[1][1].split('-')
            names =  paragraph[1][2:]
            # neo_node_relation  = copy.copy(paragraph[4:])
            neo_node_relation  = paragraph[4:] #deep copy
            sql = paragraph[3][1]

            #开始处理每个abstract表里面的子表
            for tab in tables:
                #遍历每个 单位，报送时间
                for com, date in results_dwzd_date:
                    ##todo  
                    result = query(sql % (com, date, tab))
                    if result is None:
                        print("sql return None %s dwbh %s date" %(dwzd_bh, inst_date))
                        continue
                    node_com = selector.select('company', dwzd_bh=com).first()
                    # print("???", graph.exists(node_com))
                    if node_com is None:
                        node_com= Node('company', dwzd_bh=com)
                        graph.create(node_com)

                    for sql_result in result:
                        row2neo(neo_node_relation , names, sql_result, com ,date, node_com, tab)
            paragraph = []
        else: paragraph.append(cols)







