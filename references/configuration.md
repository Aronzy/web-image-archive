# 可复用配置

以下字段属于任务配置，不代表对任何站点和库的额外授权。先沿用用户已有要求；遇到影响范围且无法推断的字段再询问。

| 字段 | 用途 |
|---|---|
| source_urls / source_ids | 白板 URL/ID、收藏列表或作品链接 |
| browser_connection | 当前可用的浏览器标签或连接端点，不能固定复用上次端口 |
| runtime_dir / cache_dir / temp_dir | 浏览器运行时、缓存与临时目录 |
| download_root | 本地下载根目录 |
| project_limit | 本次处理的作品链接数量 |
| images_per_project | `all` 表示每个作品内全部图片，或用户明确指定的数量 |
| batch_size / group_count / group_names | 批次数量、组数、命名，不混淆作品数与图片数 |
| grouping | 按作品、作者或批次分组；整套参考图优先保留作品归属 |
| deduplicate | 是否启用去重；参考库归档默认建议启用，尊重用户选择 |
| dedup_manifest_paths | 历史去重清单位置，可有多个 |
| dedup_scope | 当前批次、跨批次、历史下载、目标 Eagle 库 |
| dedup_keys | 稳定资源标识（带站点命名空间）与下载后 SHA256 |
| eagle_import | 用户要求时为 true；不得仅因下载任务就默认导入 |
| eagle_library_path | 必须与当前打开库核对的目标路径 |
| eagle_folder_name / eagle_grouping | Eagle 根分类与作品子分类 |
| verification | 格式、整图解码、尺寸、大小、来源校验和（有可靠依据时）、库内 SHA256 |
| stop_after / on_failure | 审核节点、失败即停或用户许可的有限重试 |

下载根目录、Eagle 库和禁止写入的位置都属于用户配置，不随技能绑定到某台电脑。改变用户指定路径或范围前重新核对。

去重和导入是独立且有顺序的阶段：历史/跨组/库内查重 → 补齐下载 → 本地完整性核验 → Eagle 导入 → 等待异步完成 → 库内副本核验。每阶段保存状态，恢复时只补齐未确认的工作。
