SELECT RB.*,
       RE.REPLACED_RB_CODES AS "replacedRbCodes",
       LNK.LNK_RB_CODES     AS "lnkRbCodes",
       Q.LNK_QUESTION_IDS   AS "lnkQuestionIds",
       P.LNK_PART_NOS       AS "lnkPartNos"
FROM (SELECT R.*
      FROM (SELECT RB.ID                                 AS "tisMid",
                   RB.CODE                               AS "code",
                   RB.TITLE                              AS "title",
                   TO_NCHAR(SUBSTR(RB.CONTENT, 1, 2000)) AS "content",
                   M.NAME                                AS "modelName",
                   ME.NAME                               AS "codeName"
            FROM T_RB RB
                   JOIN T_MODEL M ON RB.MODEL_ID = M.ID
                   JOIN T_MODULE ME ON RB.MODULE_ID = ME.ID
            WHERE RB.CREATED_DATE >= TO_DATE(:begin, 'yyyy-mm-dd hh24:mi:ss')
              AND RB.CREATED_DATE <= TO_DATE(:end, 'yyyy-mm-dd hh24:mi:ss')) R) RB
       LEFT JOIN (SELECT T_RB_REPLACED.RB_ID, TO_NCHAR(SUBSTR(WMSYS.WM_CONCAT(T_RB.CODE), 1, 2000)) REPLACED_RB_CODES
                  FROM T_RB_REPLACED
                         LEFT JOIN T_RB ON T_RB_REPLACED.REPLACED_RB_ID = T_RB.ID
                  GROUP BY T_RB_REPLACED.RB_ID)RE ON RB."tisMid" = RE.RB_ID
       LEFT JOIN (SELECT T_RB_LNK_BULLETIN.RB_ID, TO_NCHAR(SUBSTR(WMSYS.WM_CONCAT(T_RB.CODE), 1, 2000)) LNK_RB_CODES
                  FROM T_RB_LNK_BULLETIN
                         LEFT JOIN T_RB ON T_RB_LNK_BULLETIN.LNK_RB_ID = T_RB.ID
                  GROUP BY T_RB_LNK_BULLETIN.RB_ID)LNK ON RB."tisMid" = LNK.RB_ID
       LEFT JOIN (SELECT RB_ID, TO_NCHAR(SUBSTR(WMSYS.WM_CONCAT(LNK_QUESTION_ID), 1, 2000)) LNK_QUESTION_IDS
                  FROM T_RB_LNK_QUESTION
                  GROUP BY RB_ID)Q ON RB."tisMid" = Q.RB_ID
       LEFT JOIN (SELECT RB_ID, TO_NCHAR(SUBSTR(WMSYS.WM_CONCAT(LNK_PART_NO), 1, 2000)) LNK_PART_NOS
                  FROM T_RB_LNK_PART
                  GROUP BY RB_ID)P ON RB."tisMid" = P.RB_ID