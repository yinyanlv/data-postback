SELECT Q.*,
       NVL(AQ.ATTACHMENT_QTY, 0) AS "attachmentsNum",
       TO_NCHAR(NVL(RB.BULLETINS, ''))     AS "associatedCommunication",
       TO_NCHAR(RC.REPLY_CONTENTS)         AS "historyContent"
FROM (SELECT R.*
      FROM (SELECT Q.ID                                                                 AS "helpCodeId",
                   Q.CONTACT                                                            AS "maintenanceSupervisor",
                   Q.CONTACT_MOBILE                                                     AS "phone",
                   Q.VIN                                                                AS "vin",
                   Q.MODEL_PLATFORM_NAME                                                AS "carPlatform",
                   Q.VSN                                                                AS "vsn",
                   Q.MODEL_CONFIG                                                       AS "carConfigure",
                   Q.ENGINE_CODE                                                        AS "engineNumber",
                   Q.MFG_DATE                                                           AS "productDate",
                   Q.BILL_DATE                                                          AS "invoiceDate",
                   Q.VEHICLE_CODE                                                       AS "carCode",
                   Q.REPAIR_DATE                                                        AS "maintenanceDate",
                   Q.TRIP_DISTANCE                                                      AS "drivingMileage",
                   Q.SUBJECT                                                            AS "subject",
                   TO_NCHAR(SUBSTR(Q.CONTENT,1,2000))                                   AS "content",
                   Q.SUBMIT_DATE                                                        AS "problemDate",
                   QT.NAME                                                              AS "problemType",
                   QL.NAME                                                              AS "problemLevel",
                   UG.CODE                                                              AS "dealerCode",
                   UG.NAME                                                              AS "dealerName",
                   QS.NAME                                                              AS "problemStatus",
                   Q.IS_PUBLIC                                                          AS "isPublic",
                   Q.IS_SITE_SUPPORT                                                    AS "isSupport",
                   Q.IS_BULLETIN                                                        AS "isBulletin",
                   (SELECT CASE
                             WHEN COUNT(1) > 0
                                     THEN 1
                             ELSE 0
                               END FROM T_RB_LNK_QUESTION WHERE LNK_QUESTION_ID = Q.ID) AS "hasBulletin"
            FROM T_QUESTION Q
                   JOIN T_QUESTION_TYPE QT ON Q.TYPE_ID = QT.ID
                   JOIN T_QUESTION_STATUS QS ON Q.STATUS = QS.ID
                   LEFT JOIN T_QUESTION_LEVEL QL ON Q.LEVEL_ID = QL.ID
                   LEFT JOIN T_USER_GROUP UG ON Q.USER_GROUP_ID = UG.ID
            WHERE (Q.STATUS = 'FINISHED' OR Q.STATUS = 'REPLIED')
              AND Q.RESOLVE_DATE >= TO_DATE(:begin, 'yyyy-mm-dd hh24:mi:ss')
              AND Q.RESOLVE_DATE <= TO_DATE(:end, 'yyyy-mm-dd hh24:mi:ss')
              AND Q.IS_CLOSE = 0) R) Q
       LEFT JOIN (SELECT QUESTION_ID, COUNT(1) ATTACHMENT_QTY FROM T_QUESTION_ATTACHMENT GROUP BY QUESTION_ID) AQ
         ON AQ.QUESTION_ID = Q."helpCodeId"
       LEFT JOIN (SELECT LNK_QUESTION_ID, SUBSTR(WMSYS.WM_CONCAT(RB_ID || '(' || TO_CHAR(STATUS_NAME) || ')'),1,2000) BULLETINS
                  FROM (SELECT LNK_Q.LNK_QUESTION_ID, RB.ID RB_ID, RB_S.NAME STATUS_NAME
                        FROM T_RB RB
                               JOIN T_RB_STATUS RB_S ON RB.STATUS = RB_S.ID
                               JOIN T_RB_LNK_QUESTION LNK_Q ON RB.ID = LNK_Q.RB_ID
                        ORDER BY RB_S.LNK_SORT, RB.PUBLISHED_DATE DESC)
                  GROUP BY LNK_QUESTION_ID)RB ON RB.LNK_QUESTION_ID = Q."helpCodeId"
       LEFT JOIN (SELECT QUESTION_ID, SUBSTR(WMSYS.WM_CONCAT(CASE FROM_SYS WHEN 'TAC' THEN '4S回复人' ELSE '主机厂回复人' END
                                                        || NAME
                                                        || CASE NVL(TELEPHONE, 'NULL')
                                                             WHEN 'NULL' THEN ''
                                                             ELSE '(' || TELEPHONE || ')' END || ':'
                                                        || CONTENT || '\n'),1,2000) REPLY_CONTENTS
                  FROM (SELECT QR.QUESTION_ID, QR.FROM_SYS, QR.CONTENT, U.NAME, U.TELEPHONE
                        FROM T_QUESTION_REPLY QR
                               LEFT JOIN T_USER U ON QR.REPLIER_ID = U.ID
                               LEFT JOIN T_QUESTION Q2 ON Q2.ID = QR.QUESTION_ID
                        WHERE QR.CONTENT_LENGTH < 500
                          AND Q2.RESOLVE_DATE >= TO_DATE(:begin, 'yyyy-mm-dd hh24:mi:ss')
                          AND Q2.RESOLVE_DATE <= TO_DATE(:end, 'yyyy-mm-dd hh24:mi:ss')
                        ORDER BY QR.CREATED_DATE DESC)
                  GROUP BY QUESTION_ID)RC ON RC.QUESTION_ID = Q."helpCodeId"