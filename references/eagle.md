# 可选 Eagle 导入

仅在用户要求时启用。使用任务配置的 eagle_library_path，每次都要核对当前实际库路径。不要直接写入 images 目录或修改 metadata 索引。

## 官方 API

已验证默认地址为 `http://127.0.0.1:41595/api`。连接失败时检查应用与连接限制，不直接判定未安装。

- `GET /library/info`：读取 `data.library.path`，与目标路径比对。
- `POST /folder/create`：`{"folderName":"本批名称"}`，保留返回 `data.id`。
- 按作品分组时可用 `{"folderName":"作品标题 [作品ID]","parent":"根文件夹ID"}` 创建子分类。图片条目名用稳定 ID 和序号，作品标题放备注，避免标题中的文件系统特殊字符影响路径。
- `POST /item/addFromPaths`：`{"items":[{"path":"本地完整路径","name":"名称","website":"来源页","tags":[],"annotation":"原始尺寸与来源标识"}],"folderId":"..."}`。
- `GET /item/list?folders=<id>&limit=<数量>`：查询入库情况；大批次必须处理 offset 分页。

接口变化时核对官方文档：
- https://api.eagle.cool/item/add-from-paths
- https://api.eagle.cool/item/list
- https://api.eagle.cool/folder/create
- https://api.eagle.cool/library/info

避免打印 `/application/info` 完整响应，里面可能含偏好与 API token；任务通常只需要库路径和图片信息。

## 幂等与异步

创建文件夹、导入前分别检查已有目录/回执/条目，不因目录已存在就重复创建。批次回执至少保留库路径、文件夹 ID、源清单、请求提交时间和响应状态。

导入前对目标库已有图片建立 SHA256 索引。已有相同内容时记录对应条目 ID 并跳过新增，保留作品归属映射。跨作品的同图不应重复入库；若尚未将旧条目归入新的作品分类，应明确报告“已有条目引用”，不要把空分类说成包含完整副本。未经验证的 folder 更新字段不应猜用。

调用写入前持久化 request_pending 状态，收到响应后记录 accepted，再只读核验并标记 verified。创建分类但导入失败时保留回执，不自动删除或重新提交。

导入返回 success 只是受理。对目标文件夹短时间只读轮询，直到预期数量和元数据就绪；可每 2 秒一次，限定总等待。超时或 API 连接中断时先查询目标库和本地回执，标记待确认，不重发同一批。

## 入库核验

确认每个导入条目尺寸、字节数与本地原件一致，必要时只读实际文件以核对 SHA256。已观察到库内原件路径为 `images/<item.id>.info/<item.name>.<item.ext>`；以当前实际文件结构为准，不猜测后写入。按源哈希映射而不是依赖 API 返回顺序。

只有库内条目数、唯一内容数、文件与源件均符合预期才报告入库完成。旧缩略图不自动删除或替换；保留原图批次明确命名，是否清理旧测试项由用户决定。
