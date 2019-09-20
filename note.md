## pac sql
缺isDeleted，status字段
字段CauseId -> CauseContent

## lac sql
字段CloseDate -> ClosDate

## 真实接口状态码约定
```
200
    {"status":200,"response":[{"autoId":41689,"status":"success"}]}  // 成功
    {"status":201,"response":[{"msg":"SQL执行失败","autoId":41689,"status":"fail"},{"autoId":41690,"status":"success"}]}  // 写入数据部分成功
    {"status":202,"response":[{"msg":"SQL执行失败","autoId":41689,"status":"fail"},{"msg":"SQL执行失败","autoId":41690,"status":"fail"}]}  // 写入数据全部失败
    {"status":400,"body":{"errorMsg":"请求路径不正确"}}
    {"status":903,"body":{"errorMsg":"请求格式不对"}}
500
    {"status":500,"body":{"errorMsg":"服务器未知错误"}}
    {"status":501,"body":{"errorMsg":"请求超时"}}
    {"status":900,"body":{"errorMsg":"AppId错误！ | 业务逻辑错误 | ..."}}
    {"status":901,"body":{"errorMsg":"Token验证失败"}}
    {"status":902,"body":{"errorMsg":"Token失效"}}
```