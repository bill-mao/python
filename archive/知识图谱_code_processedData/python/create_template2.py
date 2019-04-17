from pending import *
import traceback
import csv
import sys  




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


ercsv = read_csv()

# import json
# print(json.dumps(ercsv, sort_keys=True, indent=4, separators=(',', ': ')))

# 只创建明细表的
target_abstract = [
    # "TableOfCapitalInstrumentAbstract",
    "InsuranceRiskOfNonLifeInsuranceBusinessOfPropertyAndCasualtyInsuranceCompanyAndLifeInsuranceCompanyPremiumAndReserveRiskAbstract",
    "InsuranceRiskOfNonLifeInsuranceBusinessOfPropertyAndCasualtyInsuranceCompanyAndLifeInsuranceCompanyCatastropheRiskAbstract",
    "InsuranceRiskOfNonLifeReinsuranceBusinessOfReinsuranceCompanyPremiumAndReserveRiskAbstract",
    "InsuranceRiskOfNonLifeReinsuranceBusinessOfReinsuranceCompanyCatastropheRiskAbstract",
    "InsuranceRiskOfLifeInsuranceBusinessAbstract",
    "InterestRateRiskOfLifeInsuranceCompanyAbstract",
    "InterestRateRiskOfReinsuranceCompanyAbstract",
    "InterestRateRiskBondAssetsNoHedgingAndUnqualifiedHedgingAbstract",
    "InterestRateRiskAssetSecuritizationProductsAbstract",
    "InterestRateRiskInterestRateDerivativesInterestRateSwapsAbstract",
    "InterestRateRiskInterestRateDerivativesGovernmentBondFuturesQualifiedHedgingAbstract",
    "InterestRateRiskInterestRateDerivativesGovernmentBondFuturesUnqualifiedHedgingAbstract",
    "InterestRateRiskOtherFixedIncomeProductsAbstract",
    "EquityPriceRiskStockNoHedgingAndUnqualifiedHedgingAbstract",
    "EquityPriceRiskStockQualifiedHedgingAbstract",
    "EquityPriceRiskUnlistedEquitiesAbstract",
    "EquityPriceRiskSecuritiesInvestmentFundHeldByCompanyDirectlyAbstract",
    "EquityPriceRiskSecuritiesInvestmentFundHeldByLookThroughMethodAbstract",
    "EquityPriceRiskConvertibleBondAbstract",
    "EquityPriceRiskInfrastructureEquityInvestmentPlansAbstract",
    "EquityPriceRiskAssetManagementProductsAbstract",
    "EquityPriceRiskUnlistedEquityInvestmentPlansAbstract",
    "EquityPriceRiskEquityTrustPlansAbstract",
    "EquityPriceRiskShortPositionOfStockIndexFuturesOutOfEffectivenessAbstract",
    "EquityPriceRiskPreferredSharesHeldByCompanyDirectlyAbstract",
    "EquityPriceRiskPreferredSharesHeldByLookThroughMethodAbstract",
    "EquityPriceRiskLongTermEquityInvestmentsInSubsidiariesJointVenturesAndAssociatedCompaniesAbstract",
    "PropertyPriceRiskInvestmentPropertyHeldByCompanyDirectlyAbstract",
    "PropertyPriceRiskInvestmentPropertyHeldByLookThroughMethodAbstract",
    "PriceRiskOfOverseasFixedIncomeInvestmentAssetsDetailsAbstract",
    "PriceRiskOfOverseasEquityInvestmentAssetsDetailsAbstract",
    "ExchangeRateRiskOfProjectsForeignCurrencyDenominatedAssetsLiabilitiesUnhedgedOrIneffectivelyHedgedDetailsAbstract",
    "ExchangeRateRiskOfProjectsForeignCurrencyDenominatedAssetsLiabilitiesEffectivelyHedgedDetailsAbstract",
    "ExchangeRateRiskOfProjectsForeignExchangeForwardAssetsLiabilitiesIneffectivelyHedgedDetailsAbstract",
    "SpreadRiskOfAssetsDetailsAbstract",
    "CounterpartyDefaultRiskCashAndLiquidityManagementInstrumentsAbstract",
    "CounterpartyDefaultRiskBankDepositsAbstract",
    "CounterpartyDefaultRiskFinancialBondsAbstract",
    "CounterpartyDefaultRiskEnterpriseBondsCorporateBondsAbstract",
    "CounterpartyDefaultRiskAssetSecuritizationProductsAbstract",
    "CounterpartyDefaultRiskWealthManagementProductsOfCommercialBankAbstract",
    "CounterpartyDefaultRiskTrustPlansAbstract",
    "CounterpartyDefaultRiskTrustPlansThatCanBeLookedThroughDetailsAbstract",
    "CounterpartyDefaultRiskAssetManagementProductsAbstract",
    "CounterpartyDefaultRiskInfrastructureDebtInvestmentPlansAbstract",
    "CounterpartyDefaultRiskPropertyDebtInvestmentPlansAbstract",
    "CounterpartyDefaultRiskProjectAssetBackedPlansAbstract",
    "CounterpartyDefaultRiskForwardForeignExchangeContractsAndInterestRateSwapsForPurposeOfHedgingAbstract",
    "CounterpartyDefaultRiskOfPropertyAndCasualtyInsuranceCompanyAndLifeInsuranceCompanyOutwardReinsuranceAssetsAbstract",
    "CounterpartyDefaultRiskOfReinsuranceCompanyOutwardReinsuranceAssetsAbstract",
    "CounterpartyDefaultRiskInwardReinsuranceAssetsAbstract",
    "CounterpartyDefaultRiskPremiumReceivableAbstract",
    "CounterpartyDefaultRiskOtherReceivablesAndPrepaymentsAbstract",
    "CounterpartyDefaultRiskDebtGuaranteeAbstract",
    "CounterpartyDefaultRiskPolicyLoansAbstract",
    # "OutstandingBenefitsReserveOfLifeInsuranceContractLiabilitiesAbstract"
    # ac01 l01 不考虑
]

# 创建明细表下面的元素
for ta in target_abstract:

    abstract_node = selector.select("template", ELE_NAME = ta)
    if abstract_node is None:
        raise Exception("cypher is wrong")
    dicta = ercsv.get(ta)
    if dicta is None:
        # print(ta)
        raise Exception(ta, "  ercsv should be covering whole abstract tables !! why not?")
    # have only one layer member
    print("abstract  ", dicta['abstract_zh'], "  ", ta)
    if dicta['layers'] == []:
        # create only one layer
        for tt in dicta['tables']:
            if tt.endswith("Abstract"):
                continue

            print ("    create node name : ", tt)
            graph.run('''
                match (n:template), (m:templ) 
                where n.ELE_NAME = '%s' 
                    and m.ELE_NAME = '%s'
                    //and ('templ' in labels(m)  or 'template' in labels(m))
                create (k:template)
                set k = m
                create (n)-[:contains]->(k)
                ''' %(ta, tt))

    else:
        # create two layers
        for l1 in dicta['layers'][0]:
            # print("abstract  ", ta)
            print ("    create node name : ", l1)
            graph.run('''
                match (n:template), (m:templ) 
                where n.ELE_NAME = '%s' 
                    and m.ELE_NAME = '%s'
                    //and ('templ' in labels(m)  or 'template' in labels(m))
                create (k:template)
                set k = m
                create (n)-[:contains]->(k)
                ''' %(ta, l1))
            for l2 in dicta['layers'][1]:
                print ("        create node name : ", l2)
                k1 = selector.select("templ",ELE_NAME = l2 )
                if k1 is None or len(list(k1)) >1:
                    raise Exception("??")
                #***** l1可能会匹配多个，造成重复！！
                cur = graph.run('''
                    match (a:template)-->(n:template), (m :templ) 
                    where n.ELE_NAME = '%s' 
                        and m.ELE_NAME = '%s'
                        and a.ELE_NAME = '%s'
                        //and ('templ' in labels(m)  or 'template' in labels(m))
                    create (k:template)
                    set k = m
                    create (n)-[:contains]->(k)
                    return count(k)
                ''' %(l1, l2, ta)
                )

                if cur.forward():
                    res = cur.current().values()[0]
                    if res != 1:
                        raise Exception("重复插入")


                # if graph.run('''
                #     match p = (n:template)--> (m:template) 
                #     where n.ELE_NAME = '%s' 
                #         and m.ELE_NAME = '%s'
                #     return p
                # ''' %(l1, l2)):
                #     print("exist")


# create 362 member












