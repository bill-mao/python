match (n:item)<--(m:backup) set n = m detach delete m
CREATE INDEX ON :instance (ELE_NAME)
CREATE INDEX ON :instance (LABEL_ZH)
CREATE INDEX ON :item (ELE_NAME)
============================

MATCH (n) 
RETURN
where rand() <= 0.1
DISTINCT labels(n),
avg(size( (n)-[]-() ) ) as Avg_RelationshipCount,

// What is related, and how
CALL db.schema()





bug
   不能多次运行 -- 刘方铮的

   match (k:tmp) where k.value = 23  create(m:tmp)-[:tmp]->(k) set m = k
   match 两个 create set =  上一个  就会创建两遍

   match p= (own:own_amount)<-[r:tmp]-(n:stock) 
       merge (own)-[rr:own]->(n)
       set rr = r 
       delete r
       # return p 
       # 不能return啊！！！所以程序一直不出来
   不要随便怪neo4j 

   // 就和SQL一样，单位是行来进行处理的
       match p = (n:instance)-->(i:item)-[:calc*]->(m:calculate) 
       where n.ELE_NAME = 'MinimumCapitalUnderSolvencyII' 
         with max(length(p)) as ma, p  //length p 每个返回p是一个定值，你取max没有用
         where length(p) = ma
         return p limit 5

        count(distinct nodes(p)) // path有很多条，so 每条path的distinct求sum
        count(m) 是不一样的


    同名路径匹配  abstract members 下面都有item so ，，， [*] 是一件很危险的事情
        merge item 更加危险
        重名问题： S01 越是上层的节点，pattern匹配约容易出现多条路径； 选择最短的路径？-- 然后就不会跑到别的abstract下面了？或者加上限制不带有abstract的中间节点？
        eg： p1= S01 -*-> same name  p2= S05 -*-> same name;  所以p1 包括p2 ；
            解决方法：
            1： 不用* 
            2：使用all， size list之类函数
            3: shortestPath()
        结合size ， all 之类的函数，超级强大

        all(x in nodes(n) WHERE x.storeyName <> “2F”)

        match p= (c:company{dwzd_bh :'000009'})-->(d:date{inst_date: '20161231'})-[:link*]->
        (a:instance{ELE_NAME : 'CounterpartyDefaultRiskFinancialBondsAbstract'})-->
        (m0:instance{ELE_NAME : 'FinancialBondsExcludingCapitalInstrumentsSuchAsSubordinatedBondsAndHybridBondsMember'})
        where   size(  [x in nodes(p) where not  x.ELE_NAME =~ ".*?Abstract"]) <>2
        return p
        
    0 和 '0' 都不报错。 no record~  | MATCH p=()-[r:arc_weight]->() where r.weight = '0'  RETURN p


============================刘方铮

    match p= (c:company{dwzd_bh :'000009'})-->(d:date{inst_date: '20161231'})-[:link*]->
        (a:instance)-[r:own]->(own:own_amount)-[:own]->(n:stock) where n.EquityPriceRiskStockNoHedgingAndUnqualifiedHedgingStockCode starts with '000' 

        with own limit 2 
        create unique (own)<-[rr:tmp]-(x:liufangzheng)
        set x = own
        set own.EquityPriceRiskStockNoHedgingAndUnqualifiedHedgingRiskExposure = 
            toString(toFloat(own.EquityPriceRiskStockNoHedgingAndUnqualifiedHedgingRiskExposure )* 1.3)
        set own.EquityPriceRiskStockNoHedgingAndUnqualifiedHedgingMinimumCapital = 
            toString(toFloat(own.EquityPriceRiskStockNoHedgingAndUnqualifiedHedgingMinimumCapital) * 1.1)
        
        return sum(toFloat(own.EquityPriceRiskStockNoHedgingAndUnqualifiedHedgingRiskExposure)) as totalsum


    match (own:own_amount)<-[rr:tmp]-(x:liufangzheng)
        set own = x
        detach delete (x)
        return own


all( i in .. where ..) any, none size() 
    多 lebel 的方法
    match p= (n)-[:contains*]->(m) where 
        all( i in nodes(p) where not 'template' in  labels(i) and size(labels(i)) < 2 ) 
        return p limit 13

where 里面可以有pattern！！当然可以有的啊， 对neo4j 了解的越多，胆子越小了是吧？。。
    match (m) where not (m)--() return count(distinct m)
    labels(m) = []  label是可以为空的


merge on create on match 
    MERGE (keanu:Person { name: 'Keanu Reeves' })
    ON CREATE SET keanu.created = timestamp()
    ON MATCH SET keanu.lastSeen = timestamp()
    RETURN keanu.name, keanu.created, keanu.lastSeen

唯一约束 CREATE CONSTRAINT ON (movie:Movie) ASSERT movie.title IS UNIQUE
添加索引(在图谱遍历时，快速找到开始节点),大幅提高查询遍历性能 CREATE INDEX ON :Actor(name)
正则表达式 不区分大小写  ； WHERE n.name =~ /(?i)ANDR.*/

cypher 进阶：
    WITH {batch} as data, [k in keys({batch}) | toInt(k)] as ids
    MATCH (n) WHERE id(n) IN ids
    // 单个属性更新
    SET n.count = data[toString(id(n))]

    //foreach case 语句进行所有节点的更新


unwind & param:
    3.3.6.3. Creating a distinct list
    We want to transform a list of duplicates into a set using DISTINCT.
    WITH [1, 1, 2, 2] AS coll
    UNWIND coll AS x 
    WITH DISTINCT x
    RETURN collect(x) AS setOfVals
    Each value of the original list is unwound and passed through DISTINCT to create a unique set.

    
    UNWIND $events AS event
    MERGE (y:Year { year: event.year })
    MERGE (y)<-[:IN]-(e:Event { id: event.id })
    RETURN e.id AS x
    ORDER BY x

    //create one node with param
    {
      "props" : {
        "name" : "Andres",
        "position" : "Developer"
      }
    }
    CREATE ($props)
    //change list into row : can create mutiple nodes
    {
      "props" : [ {
        "awesome" : true,
        "name" : "Andres",
        "position" : "Developer"
      }, {
        "children" : 3,
        "name" : "Michael",
        "position" : "Developer"
      } ]
    }
    UNWIND $props AS properties
    CREATE (n:Person)
    SET n = properties
    RETURN n


path node relation:
    MATCH (charlie:Person { name: 'Charlie Sheen' }),(martin:Person { name: 'Martin Sheen' }), p = shortestPath((charlie)-[*]-(martin))
    WHERE NONE (r IN relationships(p) WHERE type(r)= 'FATHER')
    RETURN p
    allShortestPaths()

list foreach
    RETURN [x IN range(0,10) WHERE x % 2 = 0 | x^3] AS result
    [0.0,8.0,64.0,216.0,512.0,1000.0]
    
    FOREACH (_ IN CASE WHEN predicate THEN [true] ELSE [] END |
        ... update operations ....
        ) 
        FOREACH (n IN nodes(p)| SET n.marked = TRUE )

=============================

探索性cypher语句 2018-3-30
    //查找孤立节点的数量
    match (n:element)-[r:subClassOf]->(m:element),
    set n.tmp = 3
    return count(n)

    match(n:element)
    where n.tmp <> 3 or n.tmp is null
    return count(n)

    //查找
    match(n:element)
    where n.tmp <> 3 or n.tmp is null
    with n
    match (n)<-[r:subClassOf*1..]-(m:element)
    return distinct n.ELE_NAME , m.ELE_NAME
    //返回2008个m节点 20 root节点
        4个孤立节点
        "ExcludedTable"
        "LineNumber"
        "LiquidityRiskProjectOnCashFlowsNetIncreaseInDepositsAndInvestmentsOfPolicyholdersCashInflows"
        "LiquidityRiskProjectOnCashFlowsNetIncreaseInDepositsAndInvestmentsOfPolicyholdersCashOutflows"
============================图数据库创建代码
/var/lib/neo4j/import   
    /*============================2018-1-25
    3.3.1 version of neo4j
    创建图数据库： 偿二代的元素，计算关系，层次关系：包含tag标签
    */

    node - element
        LOAD CSV WITH HEADERS FROM "file:/element.csv" as row
        create (n:element)
        set n = row, n.tag = 0, n.tag_calc =0
    
    relation - arc_weight
        LOAD CSV WITH HEADERS FROM "file:/calu.csv" as calc
        match (ele1:element),(ele2:element)
        where ele1.ELE_NAME = calc.FROM_ELE_NAME and ele2.ELE_NAME = calc.TO_ELE_NAME
        create (ele1)-[r:arc_weight { weight:calc.ARC_WEIGHT }]->(ele2)
        set ele1.tag_calc = ele1.tag_calc + 1
        return r
        //553 relation
        //CREATE INDEX ON :element(oid)

    level 层次关系建立  -  property - 父节点的ele_name
        //添加tag的英文标签
        LOAD CSV WITH HEADERS FROM "file:/level.csv" as level
        match (ele1:element),(ele2:element)
        where ele1.ELE_NAME = level.FromElementName and ele2.ELE_NAME = level.ToElementName
        MERGE (ele1)-[:level]->(ele2) // prevent muti-insert
        set ele2.tag = ele2.tag + 1
        set ele2.tag_en =
        case 
        when ele2.tag_en is null then [level.tag_en] 
        else ele2.tag_en + level.tag_en 
        end 

        ============================ 2018-3-16 ？
    
    改label成subClassOf 符合W3C规范
        match (n)-[r:level]->(m)
        create (n)<-[rr:subClassOf]-(m)
        set rr = r
        with r delete r
    
    property - calculation计算公式
        match (n)-[r:arc_weight]->(m)
        set n.tmp_mark = 
            case when r.weight = "1" then "+"
            when r.weight = "-1" then "-"
            end
        set n.calculation =
            case when n.calculation is null then n.tmp_mark + m.ELE_NAME
            else n.calculation + n.tmp_mark + m.ELE_NAME 
            end
        return n.tmp_mark,  n.calculation
        //Set 1040 properties, started streaming 553 records after 35 ms and completed after 44 ms.

        match (n)-[r:arc_weight]->(m)
        remove n.tmp_mark
        //remove n.calculation

    2018-3-22 知网 
        //create 义原以及之间的关系
        LOAD CSV WITH HEADERS FROM "file:/ele_word.csv" as row
        create (ele:ele_word)
        set ele.id = row.id
        set ele.name = row.name
        return ele
        //1618

        LOAD CSV WITH HEADERS FROM "file:/ele_word.csv" as row
        match (n:ele_word),(m:ele_word)
        where row.id <> row.root and  n.id = row.id and m.id = row.root 
        create (n)-[r:subClassOf]->(m)
        //Created 1609 relationships, completed after 5323 ms.
        //9 roots

        //添加词性： 动词，名次 …… 
        LOAD CSV WITH HEADERS FROM "file:/G_X.csv" as row
        create (n:G_X)
        set n.value = row.G_X

        /*
        LOAD CSV WITH HEADERS FROM "file:/glossary.csv" as row
        match (ele:ele_word),(n:G_X)  //***笛卡尔积
        where ele.name = row.ele_word and n.value = row.G_X
        create (p:phrase)
        set p.id = row.id
        set p.name = row.name
        create (p)-[r:explain]->(ele)
        set r.value = row.relation
        create (p)-[:r_gx]->(n)
        */
        //复杂度 2.5亿次比较; 错误，重复插入了，当时没想清楚，图省力，结果更加费劲

        CREATE CONSTRAINT ON  (n:phrase)
        ASSERT n.id IS UNIQUE

    新增节点： 把整个挂到S01下面： 2018-3-27
        LOAD CSV WITH HEADERS FROM "file:/新增节点.csv" as row
        match(root:element)
        where root.ELE_NAME + 'Abstract' = row.english
        //return root
        create (n:element)
        set n.ELE_NAME = row.english, n.LABEL_ZH = row.chinese, n.new_ele = 1
        merge (n)-[r:subClassOf]->(root)
        set r.new_rela = 1 


        LOAD CSV WITH HEADERS FROM "file:/表层次关系2.csv" as row
        match (ele1:element), (ele2:element)
        where row.root_eng =  ele2.ELE_NAME and row.son_eng = ele1.ELE_NAME
        //return ele1, ele2
        merge (ele1)-[r:subClassOf]->(ele2)
        set r.new_rela = 1  // 352 all new rela = 1

        ============================2018-3-28
        LOAD CSV WITH HEADERS FROM "file:/2018-3-27整理的新增层次关系边.csv" as row
        match (ele1:element), (ele2:element)
        where row.root =  ele2.ELE_NAME and row.son = ele1.ELE_NAME
        //return count(ele2)
        merge (ele1)-[r:subClassOf]->(ele2)
        set r.new_rela = 2
        //Set 62 properties, created 61 relationships, completed after 752 ms.


2018-5-3： 创建template
    LOAD CSV WITH HEADERS FROM "file:/element.csv" as row
    create (n:templ)
    set n = row 

    LOAD CSV WITH HEADERS FROM "file:/level.csv" as level
    match (ele1:templ),(ele2:templ)
    where ele1.ELE_NAME = level.FromElementName and ele2.ELE_NAME = level.ToElementName
    MERGE (ele1)-[:contains]->(ele2) // prevent muti-insert


    LOAD CSV WITH HEADERS FROM "file:/connect_S.csv" as row
    match (ele1:templ), (ele2:templ) // [prevent same name problems]
    where row.root_eng =  ele1.ELE_NAME and row.son_eng = ele2.ELE_NAME
    merge (ele1)-[:contains]->(ele2)
    return ele1.LABEL_ZH, ele2.LABEL_ZH
    // 4 relations created


    LOAD CSV WITH HEADERS FROM "file:/connect.csv" as row
    match (ele1:templ), (n:templ) // [prevent same name problems]
    where row.root_eng =  ele1.ELE_NAME and row.son_eng = n.ELE_NAME
    create (ele2:template)
    set ele2 = n
    create (ele1)-[:contains]->(ele2)
    return ele1.LABEL_ZH, ele2.LABEL_ZH
    //57 relation

    match p = (n:templ)-[:contains*]->()
    where n.ELE_NAME = 'TableOfSolvencyStatusAbstract'
    // !!!!!!!!!!!!!!!! 不能删啊，否则之后就找不到，或者之后 python 加  template | templ
    foreach (k in nodes(p) | set k:template   )

    match p = (n:template)-[:contains*]->(m:template)
    where n.ELE_NAME = 'TableOfSolvencyStatusAbstract'
    and m.ELE_NAME =~ '.*?Abstract'
    return count(distinct m)
    // 61 假如不是distinct的话171 个！！？


    /*
    group by : 是一个拓扑，总表也公用了很多元素
    match p = (n:template)-[:contains*]->(m:template)
    where n.ELE_NAME = 'TableOfSolvencyStatusAbstract'
    and m.ELE_NAME = 'ExchangeRateRiskOfProjectsForeignExchangeForwardAssetsLiabilitiesIneffectivelyHedgedDetailsAbstract'
    return m.LABEL_ZH,m.ELE_NAME,   count(m)
    */

    //运行python create template，创建相关的member

    match p = (n:templ)-[:contains*]->()
    where n.ELE_NAME = 'TableOfSolvencyStatusAbstract'
    // !!!!!!!!!!!!!!!! 不能删啊，否则之后就找不到，或者之后 python 加  template | templ
    foreach (k in nodes(p) | set k:template   remove k:templ )


    // --  last
    match (n:templ) 
    detach delete n

    check:
        match (n:template)-[*]->(n)
        return n

        ercsv 62个csv是否全  -- 英文名竟然弄错了、、


    2018-5-7： 重新create template

        

        //纠正 create_template 里面重复插入的问题

        LOAD CSV WITH HEADERS FROM "file:/element.csv" as row
        create (n:templ)
        set n = row 
        /* 这个不行，csv之所以快，是因为create更新之后neo4j 不是马上更新的！！！！
        LOAD CSV WITH HEADERS FROM "file:/connected_S.csv" as row
        match (tt:template), (t:templ)
        where tt.ELE_NAME = row.father and   t.ELE_NAME = row.son 
        create (n:template)
        set n = t
        create (tt)-[:contains]->(n)
        */


        // 运行程序 创建连接S总表
        // 运行程序 create template , 创建明细表的member

        // 校验检查 574 个template
            match p=(n:template)-[*]->(n)
            return p

            match p= (n:template)-->()<--(m:template)
            where n <> m
            return p

            match (n:template)-[:contains*0..]->(m:template)
            where m.ELE_NAME =~'.*?Abstract' and n.ELE_NAME = 'TableOfSolvencyStatusAbstract'
            return count(m)

             /*这个不行，因为路径太多了，以后好好仔细想想，这种最容易出错
                match (n:template)-[:contains*0..]->(m:template)
                where n.ELE_NAME = 'TableOfSolvencyStatusAbstract'
                return count(distinct m), count(m)
            */ 

            ercsv 62个csv是否全  -- 英文名竟然弄错了、、

        // --  last
        match (n:templ) 
        delete n