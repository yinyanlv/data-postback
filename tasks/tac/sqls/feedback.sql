SELECT F.*,
       V.VIN                                AS "vin",
       V.MODEL_PLATFORM_NAME                AS "carPlatform",
       V.VSN                                AS "vsn",
       V.ENGINE_CODE                        AS "engineNo",
       V.MFG_DATE                           AS "productDate",
       V.BILL_DATE                          AS "billDate",
       V.VEHICLE_CODE                       AS "carCode",
       V.REPAIR_DATE                        AS "repairDate",
       V.TRIP_DISTANCE                      AS "mileage",
       NVL(AQ.ATTACHMENT_QTY, 0)            AS "annexNum",
       NVL(RC.REPLY_CONTENTS, '') AS "historyContent"
FROM (SELECT F.ID                                    AS "tisId",
             UG.NAME                                 AS "dealerName",
             UG.CODE                                 AS "dealerCode",
             F.CONTACT                               AS "repairManager",
             F.CONTACT_MOBILE                        AS "phone",
             FS.NAME                                 AS "feebackStatus",
             F.SUBJECT                               AS "subject",
             TO_NCHAR(SUBSTR(F.CONTENT_10, 0, 2000)) AS "faultDesc",
             TO_NCHAR(SUBSTR(F.CONTENT_20, 0, 2000)) AS "analysisContent",
             TO_NCHAR(SUBSTR(F.CONTENT_30, 0, 2000)) AS "treatmentMeasures",
             F.SUBMIT_DATE                           AS "feedbackTime",
             FL.NAME                                 AS "faultType",
             FM.NAME                                 AS "failureMode",
             FIS.NAME                                AS "infoSource",
             T.NAME                                  AS "infoType",
             L.NAME                                  AS "checkContent",
             RELATE_PART_NO                          AS "partNo",
             RELATE_PART_NAME                        AS "partName"
      FROM T_FEEDBACK F
             JOIN T_FEEDBACK_TYPE T ON F.TYPE_ID = T.ID
             JOIN T_FEEDBACK_STATUS FS ON F.STATUS = FS.ID
             LEFT JOIN T_FEEDBACK_LEVEL L ON F.LEVEL_ID = L.ID
             LEFT JOIN T_FAULT_LOCATION FL ON FL.ID = F.FAULT_LOCATION_ID
             LEFT JOIN T_FEEDBACK_INFO_SOURCE FIS ON FIS.ID = F.INFO_SOURCE_ID
             LEFT JOIN T_FAULT_MODE FM ON FM.ID = F.FAULT_MODE_ID
             LEFT JOIN T_USER_GROUP UG ON F.USER_GROUP_ID = UG.ID
      WHERE (F.STATUS = 'FINISHED' OR F.STATUS = 'REPLIED')
        AND F.IS_CLOSE = 0
        AND F.MODIFIED_DATE >= TO_DATE(:begin, 'yyyy-mm-dd hh24:mi:ss')
        AND F.MODIFIED_DATE <= TO_DATE(:end, 'yyyy-mm-dd hh24:mi:ss')) F
       JOIN T_FEEDBACK_VEHICLE V ON V.FEEDBACK_ID = F."tisId"
       LEFT JOIN (SELECT FEEDBACK_ID, COUNT(1) ATTACHMENT_QTY FROM T_FEEDBACK_ATTACHMENT GROUP BY FEEDBACK_ID) AQ
         ON AQ.FEEDBACK_ID = F."tisId"
       LEFT JOIN (SELECT FEEDBACK_ID, TO_NCHAR(SUBSTR(WMSYS.WM_CONCAT(CASE FROM_SYS WHEN 'TAC' THEN '4S回复人' ELSE '主机厂回复人' END
                                                               || NAME
                                                               || CASE NVL(TELEPHONE, 'NULL')
                                                                    WHEN 'NULL' THEN ''
                                                                    ELSE '('
                                                                           || TELEPHONE
                                                                           || ')' END
                                                               || ':'
                                                               || CONTENT
                                                               || '\n'
                                                 ), 1, 2000)) REPLY_CONTENTS
                  FROM (SELECT FR.FEEDBACK_ID, FR.FROM_SYS, FR.CONTENT, U.NAME, U.TELEPHONE
                        FROM T_FEEDBACK_REPLY FR
                               LEFT JOIN T_USER U ON FR.CREATED_BY = U.ID
                               LEFT JOIN T_FEEDBACK F2 ON FR.FEEDBACK_ID = F2.ID
                        WHERE FR.CONTENT_LENGTH < 500
                          AND F2.MODIFIED_DATE >= TO_DATE(:begin, 'yyyy-mm-dd hh24:mi:ss')
                          AND F2.MODIFIED_DATE <= TO_DATE(:end, 'yyyy-mm-dd hh24:mi:ss')
                        ORDER BY FR.CREATED_DATE DESC)
                  GROUP BY FEEDBACK_ID) RC ON RC.FEEDBACK_ID = F."tisId"