# Boardmix 原图适配（已验证，仍需核对当前版本）

## 已验证的差异

画布在小缩放比例时会加载约 120 像素宽的 thumb2。直接下载 Resource Timing 中出现的 URL 会得到缩略图。图片对象有一份主资源记录，`files` 下的 original、preview、thumb1、thumb2 各自可能有不同 hash。

错误方法：用 thumb2 的 hash 当作主资源 hash 查询。服务端可能返回 `files.original`，但它仍是那个小图文件。必须取得画布对象的主 imageHash 或包含完整版本对应关系的资源记录。

## 两条已观察到的只读途径

### 选中图片节点

当前版本为 Vue/Pinia 应用。在允许运行时检查的浏览器环境中，经检查实际对象后可读取 `file-manager` store 的 `getGptActiveShapeInfo()`，返回选中对象的 `imageHash`。再调用其 `getFileDataInfo(fileKey, imageHash)` 获取 files。

这些属于内部接口，不保证稳定。此前 `_SkmAppObj.debugHelper` 的部分方法存在但依赖缺失，不能反复调用报错方法。全选也不保证返回所有子节点；确认返回数量和选区，不以 Ctrl+A 成功作为完整性证据。

### 图片资源响应

已观察到：

```text
POST https://api.boardmix.cn/api/editor/upload/infos
body: {module: "file", module_key: <目标白板ID>, hash_list: [<主资源hash>, ...]}
response.data[hash].files.original
response.data[hash].files.thumb1
response.data[hash].files.thumb2
```

可优先读取编辑器已有缓存或通过其正常请求得到的结果。确需安装临时观察脚本时，仅匹配该端点及目标 module_key；只提取 resource hash、files 下各版本的 hash/url/width/height/size/mime。不要记录请求头、会话材料或无关响应。不得用完整 HAR 替代此限定采集。

某些工具缓存 init-script 内容；修改文件后不代表新内容已安装。观察器未生效时核验注册状态和实际读取到的资源数量，再适当重新注册，不连续盲目刷新。

## 匹配和下载

若从旧缩略图修复：在主资源集合中寻找 `files.thumb1.hash` 或 `files.thumb2.hash` 等于旧文件 hash 的记录，再下载同一记录的 `files.original.url`。

使用元数据的 original 尺寸和大小验证。实际任务中原件为 1920–3200 像素宽，主文件 hash 与文件 MD5 完全吻合；这不是尺寸门槛，也不是所有 hash 通用语义。先核实当前数据中 hash 确为 MD5 后再采用该校验。

资源 URL 带临时签名，失效时重新解析同一主资源，不能自行拼接签名或剥离参数。已加载资源数量不保证等于白板全部图片；完整导出必须证明已遍历全部目标节点，否则仅报告已发现/完成数量。
