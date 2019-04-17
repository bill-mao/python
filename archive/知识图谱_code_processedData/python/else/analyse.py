from pending import *
import pandas as pd


def second_influence(com, date, ):
    sql = '''
        select DWZD_BH,DWZD_MC from rpt_dwzd where DWZD_MC in (SELECT 
        DISTINCT 
        MAX(CASE T.ELE_NAME WHEN 'CounterpartyDefaultRiskOutwardReinsuranceAssetsInwardReinsurerName' THEN T.VALUE_DATA ELSE 0 END ) '再保分入人名称' FROM 
        (
        SELECT
                ELE_NAME,CASE WHEN VALUE_TYPE = 0 THEN NUM_VALUE ELSE CHAR_VALUE END AS VALUE_DATA,DIM_GID
            FROM
                PSX_DW_INSTDATA A,
                PSX_ELEMENT B,
                (
                    SELECT
                        X.PERIOD_NAME,
                        X.PERIOD_ID,
                        Y.OID              
                    FROM
                        PSX_CONTEXT_PERIOD X
                    LEFT JOIN PSX_CONTEXT Y ON(        
                        X.PERIOD_ID = Y.CON_APPPERIOD
                    )
                ) C
            WHERE
                A.ELE_ID = B.OID
            AND A.CON_ID = c.OID
            AND A.DWZD_BH = '%s' -- 单位
            AND A.INST_DATE = '%s' -- 日期
            AND ELE_NAME in ('CounterpartyDefaultRiskOutwardReinsuranceAssetsInwardReinsurerName') --   元素名称
            AND C.PERIOD_NAME = '期末' 
            AND  DIM_GID IN (SELECT OID FROM psx_dimension_group WHERE MEMBER_VALUE like (SELECT concat('%%',OID,'%%') FROM psx_element WHERE ELE_NAME = 'DomesticInwardReinsurerMember'))
        ) T

        GROUP BY T.DIM_GID
        ) 
    ''' % (com, date)
    result = query (sql)
    return result


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
for com, date, dw_name in results_dwzd_date:
    res = second_influence(com, date)
    tx = graph.begin()
    for i, j in res:
        print("start one ", i, j )
        cql = "match (c1:company),(c2:company) where \
            c1.dwzd_bh = '%s' and c2.dwzd_bh = '%s' \
            merge p= (c1)-[:influence]->(c2) \
            return count(p) as count" %(com, i  )
        print(cql)
        count = tx.run(cql).data()[0]['count']
        if count >0 :
            print(count)

    tx.commit()





