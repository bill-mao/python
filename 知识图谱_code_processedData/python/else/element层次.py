from py2neo import Graph,Node,Relationship, NodeSelector

graph = Graph(
    # "http://localhost:7474", 
    # username="neo4j", 
    # password="neo4jSPLab"


    "http://211.87.234.115:7474",
    username='neo4j',
    password = '123456'


)

selector = NodeSelector(graph)

# 递归程序 bug
 # node_label = node_label)
 # 别忘记了
def get_node(dic,direction = 1 , depth= 0, limit = 99, relations = 'subClassOf', whole = set([]), 
    node_label = 'element'):
    if depth == limit: return {}
    for k in dic.keys():
        # 查找这一层的孩子节点的id 
        if direction > 0:
            cql = '''
                match(n:&&)<-[r:%s]-(m:&&) 
                where id(n) =%d
                return id(m) as id
                ''' %(relations, int(k))
        else : 
            cql = '''
              match(n:&&)-[r:%s]->(m:&&) 
              where id(n) =%d
              return id(m) as id
              ''' %(relations, int(k))

        cql = cql.replace('&&', node_label)
        links = graph.data(cql)
        # 去除多重边 json里面int 是key，不允许在同一层重复
        links = set([ i['id'] for i in links])
        v = dic[k] #v 也会一个dict， 空的 {}
        for i in links:
            v[i] = {} # 规格化每个节点都是dict ， key 作为值，然后value-存放子节点
        
        for i in range(depth):
            print('\t', end= '')
        if k not in whole:
            # select args 是 & not | 
            ni = selector.select(node_label).where("id(_) = %d " %k) .first() 
            print(ni['LABEL_ZH'],'  ', ni['ELE_NAME'])
            # not dulplicate
            # whole.add(k) 
            if len(dic[k]) != 0:
                get_node(dic = dic[k], direction = direction , depth =  depth+1, limit = limit, relations = relations, whole = whole , node_label = node_label)
        else: print('duplicate - ', k)
    return dic

# MR27-汇率风险所涉项目明细表，未套保及套保无效的外汇资产（负债） [abstract] -- nothing 
# all  = ['ExchangeRateRiskOfProjectsForeignCurrencyDenominatedAssetsLiabilitiesUnhedgedOrIneffectivelyHedgedDetailsAbstract']

# CR01-利差风险所涉资产明细表 [abstract] -- 结果扁平化，完全没有用，只有风险暴露 = 认可价值这么一个arc_weight
# all = [ 'SpreadRiskOfAssetsDetailsAbstract', 'SpreadRiskOfAssetsDetailsTable', 'TypesOfDomesticInvestmentAssetsMeasuredAtFairValueWithDefiniteTermAxis', 'TypesOfDomesticInvestmentAssetsMeasuredAtFairValueWithDefiniteTermMember', 'PolicyFinanceBondsMember', 'BondsWhichExcludingPolicyFinanceBondsMember', 'AssetSecuritizationProductsUnderSolvencyIIMember', 'FixedIncomeTrustPlansMember', 'OtherFixedIncomeProductsMember', 'SpreadRiskOfAssetsDetailsLineItems', 'SpreadRiskSecurityName', 'SpreadRiskSecurityCode', 'SpreadRiskCreditRatingsForAssets', 'SpreadRiskModifiedDuration', 'SpreadRiskAdmittedValue', 'SpreadRiskRiskExposure', 'SpreadRiskBaseRiskFactor', 'CreditRiskMinimumCapitalForSpreadRisk', ]
# CR01-利差风险所涉资产明细表，政策性金融债 [abstract] -- 和上面那个总表结果一样。。。 
# all = [ 'SpreadRiskOfAssetsPolicyFinancialBondsDetailsAbstract',  'SpreadRiskOfAssetsDetailsTable',  'TypesOfDomesticInvestmentAssetsMeasuredAtFairValueWithDefiniteTermAxis',  'TypesOfDomesticInvestmentAssetsMeasuredAtFairValueWithDefiniteTermMember',  'PolicyFinanceBondsMember',  'SpreadRiskOfAssetsPolicyFinancialBondsDetailsLineNumberAxis',  'SpreadRiskOfAssetsDetailsLineItems',  'SpreadRiskSecurityName',  'SpreadRiskSecurityCode',  'SpreadRiskCreditRatingsForAssets',  'SpreadRiskModifiedDuration',  'SpreadRiskAdmittedValue',  'SpreadRiskRiskExposure',  'SpreadRiskBaseRiskFactor',  'CreditRiskMinimumCapitalForSpreadRisk',  ] 
# all = ['MinimumCapitalForQuantifiableRisk' ] # 量化最低资本 s05

'''
all = [ 'TableOfSolvencyStatusAbstract'] #so1 subclass of 
all = [graph.data("match (n:element) where n.ELE_NAME = '%s' return id(n) as id "% i)[0]['id'] for i in all ]

for first in all :
    dic = {first:{}}
    # rela = '|'.join(('subClassOf',))
    # get_node(dic, 1, relations= rela)


    # rela = 'arc_weight'
    rela = '|'.join (['contains', 'lineitems'])
    # rela = 'contains'
    out = get_node( dic, -1,relations = rela, limit = 99)

    # import json
    # out = json.dumps( out, sort_keys=True, indent=4, separators=(',', ': '))
    # print (out)

# 解决重名问题， id 存在json里面
'''


all = [ 'TableOfSolvencyStatusAbstract']
al = [graph.data("match (n:template) where n.ELE_NAME = '%s' return id(n) as id "% i)  for i in all]
all =[]
for i in al:
    for j in i:
        all.append(j['id'])

print(all)

for first in all :
    dic = {first:{}}
    rela = '|'.join (['contains' ])
    out = get_node( dic, -1,relations = rela, limit = 9, node_label = 'template')
    

