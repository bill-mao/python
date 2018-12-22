from sshtunnel import SSHTunnelForwarder  
import pymysql


def query(sql):
    with SSHTunnelForwarder(  
        ('211.87.232.138', 4239),    #B机器的配置  
        ssh_username="uproxy",
        ssh_password="splabSSHproxy",  
        remote_bind_address=('211.87.232.138', 3306))  as server:
        server.start()
        
        connect = pymysql.connect(
            host = '127.0.0.1',# must be
            port=server.local_bind_port, 
            user='pansoft',
            passwd='psx2018',
            db='pansoft_parta1',
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
            print("fetch failure")
            print(str(e))
        

def get_value_ele_dim(ele_name, dim_gid, dwzd_bh, inst_date, PERIOD_NAME = '期末' ):
    sql = '''
        SELECT  CASE WHEN VALUE_TYPE = 0 THEN NUM_VALUE ELSE CHAR_VALUE END AS VALUE_DATA 
            FROM
                psx_dw_instdata a,
                psx_element b,
                (
                    SELECT
                        x.PERIOD_NAME,
                        x.PERIOD_ID,
                        y.OID
                    FROM
                        psx_context_period x
                    LEFT JOIN psx_context y ON(
                        x.PERIOD_ID = y.CON_APPPERIOD
                    )
                )c
            WHERE
                a.ele_id = b.oid
            AND a.CON_ID = c.OID
            AND a.dwzd_bh = '%s'
            AND a.inst_date = '%s'
            AND ele_name = '%s' 
            AND c.PERIOD_NAME = '%s'
          AND  DIM_GID = '%s'
    '''  %(dwzd_bh, inst_date, ele_name ,PERIOD_NAME, dim_gid)
    # ##
    # print(sql)
    result = query(sql)
    return result[0][0]
'''
修正久期 * 利差变动值 = 账面的下跌金额百分比
MC_信用=EX ×RF
RF=RF_0×(1+K)
K=∑_(i=1)^n▒k_i =k_1+k_2+k_3+⋯+k_n，K∈[-0.25, 0.25]，保监会另有规定的除外
对特征系数k_i，由偿付能力监管规则规定和赋值；无明确规定并赋值的，则k_i=0。
MC_信用为信用风险的最低资本；
EX为风险暴露，除特别规定外，信用风险的EX等于该项资产（负债）的认可价值；当该项资产（负债）的认可价值为负值时，EX等于0；
'''
#get the current SpreadRiskOfAssetsDetailsAbstract  CR01-利差风险所涉资产明细表 [abstract]

dwzd_bh = '000018'
inst_date = '20171231'




#TypesOfDomesticInvestmentAssetsMeasuredAtFairValueWithDefiniteTermMember
#以公允价值计量且具有明确期限的境内投资资产类别 [member]
members  = ['PolicyFinanceBondsMember',
'BondsWhichExcludingPolicyFinanceBondsMember',
'AssetSecuritizationProductsUnderSolvencyIIMember',
'FixedIncomeTrustPlansMember',
'OtherFixedIncomeProductsMember']
items = ['SpreadRiskSecurityName', 
'SpreadRiskSecurityCode', 'SpreadRiskCreditRatingsForAssets',  
'SpreadRiskModifiedDuration', 'SpreadRiskAdmittedValue',
'SpreadRiskRiskExposure', 'SpreadRiskBaseRiskFactor', 
'CreditRiskMinimumCapitalForSpreadRisk']
'''
证券名称
证券代码  信用评级
修正久期（年） 认可价值
风险暴露  基础因子RF0
最低资本
'''


previousMinimumCapital = 0.0
currentMinimumCapital = 0.0
spreadRisk = 0.1


i=0

for mem in members:


    sql_name_gid = '''
        select A.VALUE_DATA as '证券名称', A.dim_gid 
        from
        (SELECT
                '证券名称',CASE WHEN VALUE_TYPE = 0 THEN NUM_VALUE ELSE CHAR_VALUE END AS VALUE_DATA,dim_gid
            FROM
                psx_dw_instdata a,
                psx_element b,
                (
                    SELECT
                        x.PERIOD_NAME,
                        x.PERIOD_ID,
                        y.OID
                    FROM
                        psx_context_period x
                    LEFT JOIN psx_context y ON(
                        x.PERIOD_ID = y.CON_APPPERIOD
                    )
                )c
            WHERE
                a.ele_id = b.oid
            AND a.CON_ID = c.OID
            AND a.dwzd_bh = '%s'
            AND a.inst_date = '%s'
            AND ele_name = 'SpreadRiskSecurityName' --  证券名称 - 类别
            AND c.PERIOD_NAME = '期末'
          AND  DIM_GID in (select oid from psx_dimension_group where member_value like (select concat(oid , '%%') from psx_element where ele_name = '%s'))
        ) A
    '''  %(dwzd_bh, inst_date, mem)

    # ##
    # with open("d:/desktop/sql.log", 'a+') as file:
    #     print(sql_name_gid, file =  file)

    result_name_gid = query(sql_name_gid)

    # with open("d:/desktop/dim.log", 'a+') as file:
    #     print(result_name_gid, file =  file)

    print('dim lenth -- ',type(result_name_gid),  len(result_name_gid))

    for name_gid in result_name_gid:
        print(name_gid)
        dim_gid = name_gid[1]
        previousMinimumCapital += float( get_value_ele_dim(items[7], dim_gid, dwzd_bh, inst_date) )
        RF0 =  float( get_value_ele_dim(items[6], dim_gid, dwzd_bh, inst_date) )
        ex =  float( get_value_ele_dim(items[5], dim_gid, dwzd_bh, inst_date) )
        SpreadRiskModifiedDuration =  float ( get_value_ele_dim(items[3], dim_gid, dwzd_bh, inst_date) )

        if previousMinimumCapital == 0 : print("??")
        print( "pre, rf, ex, md", )
        currentMinimumCapital += (1 - SpreadRiskModifiedDuration * spreadRisk) * ex * RF0 
        ##
        print(previousMinimumCapital, "--",  RF0, "--",  ex, "--",  SpreadRiskModifiedDuration)
        print(previousMinimumCapital, '\n', currentMinimumCapital)

        ##
        i+=1 
        if i % 100 == 0 : break

print(previousMinimumCapital, '\n', currentMinimumCapital)
















































