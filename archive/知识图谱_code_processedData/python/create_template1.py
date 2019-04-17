from pending import *

# 载入所有的偿二代元素
load_elecsv_cql = '''
    LOAD CSV WITH HEADERS FROM "file:/element.csv" as row
    create (n:templ)
    set n = row 
    '''
graph.run(load_elecsv_cql)

# 创建S01元素
graph.run('''
     match(t:templ) 
    where t.ELE_NAME = 'TableOfSolvencyStatusAbstract' 
    create (n:template) 
    set n = t
''')

# 根据配置创建所有的abstract元素
with open ('./connected_S.csv') as csvfile:
    spamreader = csv.reader(csvfile, quotechar='"')
    count = 0
    for cols in spamreader:
        # 又犯了同样的问题。。。 match layer1 好几个。。 
        # k 可能是abstract， 可能是普通的
        #  tt一定是a下面的，不属于a下面的aa的下面
        cql = '''
            match pp= shortestPath((a:template)-[:contains*0..5]->(tt:template)) , (t:templ)
            where a.ELE_NAME = '%s' and  tt.ELE_NAME = '%s' and   t.ELE_NAME = '%s'
            create (n:template)
            set n = t
            create (tt)-[:contains]->(n)
            return count(n)
        ''' % (cols[2], cols[0], cols[1], )
        # print(cql)
        cur = graph.run(cql)
        if cur.forward():
            count += cur.current().values()[0]
        print(count)
        # 217  有一个不是cross的






