# Atlas Context

**把你选定并审核的经历，连同来源和不确定性，交给你选择的 Agent。**

[English](README.md) · [手机接入](docs/phone-handoff.md) · [隐私说明](PRIVACY.md) · [路线图](ROADMAP.md) · [MIT 许可](LICENSE)

Atlas Context 将选定的人生记录整理成有范围、可追溯的背景，用于个人介绍、年度回顾等写作任务。你选择资料、检查实际将披露的文字，并设置本地批准的有效期。输出保留“资料记录”“本人陈述”和“系统推测”的区别。

**当前状态：实验性 Alpha。** 已实现 SwiftUI 手机审核导出组件、独立虚构资料 App、严格的文件接入命令和只读 MCP。当前路径是：手机选记录 → 审核每句文字 → 传送 JSON → 本地核对接入 → Agent 生成带引用的总结。尚未实现 USB 自动扫描、生产版 Atlas Memoir 集成或手机实时同步。自动化合成测试不调用模型；实际模型试验另行说明。

> **隐私优先：** 默认不选记录、不开云端权限；不导出原图、视频、GPS、相册标识或完整备份。文字仍可能包含隐私，需要逐句审核。使用云端模型会把批准文字发送给模型服务商；撤销仅能阻止后续读取，不能追回已发送的副本。详见 [隐私说明](PRIVACY.md)。

## 一条命令体验手机资料接入

```sh
python3 -m atlas_context.phone demo --output ../atlas-phone-demo
```

生成四条虚构手机记录、默认三条带引用的依据预览，以及独立 MCP 运行目录。预览只是逐句引用，不是模型总结；命令本身不联网、不调用模型。将 `session/private-server.json` 配置给 MCP 宿主后，交给 Agent 执行 `session/private-agent-task.md`。默认 `local_only` 只应配合本地模型使用。手机组件、实际文件核对和撤销步骤见 [接入指南](docs/phone-handoff.md)。

## 新增的公开演示

- [三年虚构故事](docs/demo.md)：16 条草稿、14 条明确选择的记录、默认输出 13 条，涵盖 8 个检索场景。
- [MCP 接入](docs/mcp.md)：Python 3.11+，固定的本地配置，仅开放 `query` 和 `include_inferred` 两个参数。
- [App 展示与素材来源](docs/app-showcase.md)：独立构建和全新模拟器中的真实界面，全部使用新的虚构数据。原生分享审核与 Agent 批准分别处理。
- [验证范围](docs/evidence.md)：区分自动化协议测试、有限模型试验与尚未完成的功能。

```sh
python3 -m atlas_context.synthetic --output ../atlas-story-demo
```

可选 MCP 验证需 Python 3.11+，在源码目录外创建环境：

```sh
python3 -m venv ../atlas-env
../atlas-env/bin/python -m pip install '.[mcp]'
../atlas-env/bin/python -m atlas_context.mcp_demo --output ../atlas-mcp-demo
```

这会验证 16 项传输与披露边界，并在结束时撤销样例批准。不要把这份已撤销的运行目录当作正常连接样例。下面保留原来的最小四条记录示例。

## 为什么做这个项目

照片时间能说明某个瞬间发生在什么时候，却很少能解释它对你意味着什么。写作助手需要你的解释、可供核查的来源，以及你同意分享的范围。

首个任务很小：为一次个人介绍或回顾准备几条审核过的经历。无需先整理完整人生。允许披露某句话，也不代表这句话已经被证实。

## 用虚构资料运行

需要 **Python 3.10+**，仅使用标准库，无需安装依赖或填写 API Key。在仓库根目录运行：

```sh
python3 demo.py --output ../atlas-synthetic-runtime
python3 -m atlas_context.cli preview \
  --draft ../atlas-synthetic-runtime/private-draft.json \
  --grant ../atlas-synthetic-runtime/private-grant.json \
  --purpose write_short_bio \
  --audience synthetic_agent \
  --query photography
```

输出目录必须为空，已有文件不会被覆盖。演示批准有效期为一小时；需要重跑时，换一个新的空目录。

演示生成四条私人草稿，明确批准其中三条。默认查询返回两条，排除尚未确认的旅行推测，并检查以下场景：

| 查询 | 预期结果 |
|---|---|
| 摄影经历（`photography`） | 两条审核过的记录 |
| 未批准的 OCR 内容 | 无已授权依据 |
| 默认查询推测的旅行 | 无已授权依据 |
| 显式包含旅行推测 | 一条记录，仍标记为 `inferred` |

同时检查撤销后拒绝读取、引用在本地可核查、只读导入不改变生成的媒体目录。运行文件保存在源码目录外。草稿、批准清单和背景预览即使没有照片，也属于私人运行数据。

返回的单条记录如下；不同运行之间的引用编号会变化：

```json
{
  "citation": "E-4969f55dd5150e8c",
  "attribution": "user_statement",
  "wording": "user_reviewed",
  "source": "atlas_memoir",
  "text": "In 2025, I started learning photography.",
  "evidence_label": "User-written stage summary (synthetic)",
  "period": "2025"
}
```

完整响应还会提醒：没有记录不能被解释为某件事从未发生。这是可供核对的背景预览，当前没有运行 Agent 来生成个人介绍。

## 三个部分如何结合

```text
Atlas 摘要投影 ──────┐
                    ├─> 私人草稿 ─> 本地审核具体措辞
选定的媒体目录条目 ─┘                      │
                                         v
                                用途 + 接收方 + 有效期
                                         │
                                         v
                                  只检索已批准表达
                                         │
                                         v
                                  背景预览 + 来源引用
```

- **Local Media Library**：整理照片、视频和备注。当前适配器只读用户明确选择的目录行。
- **Atlas Memoir**：计划作为时间线、本人解释和纠错入口。已有摘要适配器，另提供可复用的 SwiftUI 选择性导出组件和虚构资料 App；生产 App 集成仍待完成。完整备份包会被拒绝。
- **Atlas Context**：本仓库内可独立使用的审核和查询核心。
- **Agent 接入**：已提供只读 `search_life_context` MCP stdio 工具，配置中的文件、用途和接收方由可信本地宿主固定。

## 当前已经实现的规则

| 规则 | 当前行为 |
|---|---|
| 明确选择 | 导入只生成草稿，不自动获得披露许可 |
| 精确措辞 | 保存用户明确选择披露的文字，不自动替用户脱敏任意文本 |
| 有范围的读取 | 每次查询检查本地用途、接收方、有效期和启用状态 |
| 只搜批准内容 | 仅匹配批准文本、年份或月份、城市；不搜索私人标题、原始 OCR 和原件位置 |
| 保留来源属性 | 区分 `recorded`、`user_statement`、`inferred`，默认排除推测 |
| 草稿变化后重新审核 | 当前草稿版本与批准版本不一致时，该记录不再返回 |
| 可核查来源 | 对外只给不透明引用；原件定位由独立的可信本地函数解析 |

可选披露字段包括年份或月份、城市和审核过的依据标签。查询函数不返回原始文件位置或原始媒体。**文字本身也要审核**：即使字段很少，一句话仍可能包含姓名、精确地点或其他私人信息。

## 当前边界

- 用途和接收方是**本地配置标签**，没有实现客户端身份认证。批准文件不是签名凭据；能修改这些文件的进程可以改变配置。
- 版本检查比较传入的草稿和批准版本。原型不监听原生 App 或原媒体库的变化；后续连接需要在来源更新时刷新草稿。
- 尚未实现 Atlas 全量备份解码、校验、迁移和原生导出。媒体适配器使用生成的目录验证，无需读取个人资料。
- 引用帮助人核查，不能自动证明摘要语义受原资料支持。将检索文本标为“不可信证据”，也不等于已经验证未来模型的提示词注入防护。
- 连接云端模型会将实际发送的文字传出设备。撤销只能阻止这一层的后续读取，不能收回对方已经收到的副本。
- 静态加密、多用户隔离、大资料库性能和实际 Agent 回答质量尚未验证。

MCP 接入说明见 [MCP 边界方案](MCP_PLAN.md)，后续步骤见[路线图](ROADMAP.md)。

## 开发与验证

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_release.py
python3 -m atlas_context.cli --help
```

现有 33 项测试覆盖批准规则、私人字段排除、过期、撤销、MCP 传输与发布历史；未安装可选 SDK 时，MCP 测试会跳过。GitHub Actions 配置了 Python 3.10/3.12 核心检查和 3.11/3.12 MCP 检查，实际状态以远程运行结果为准。发布脚本检查白名单、经人工核查素材的精确哈希和历史文件，不能代替对私人内容的人工核查。

```text
atlas_context/
  core.py             # 记录、本地批准、检索、仅限本地的依据定位
  importers.py        # 摘要投影和选定媒体目录适配器
  cli.py              # 本地导入、批准和预览命令
demo.py               # 生成虚构记录并验证四个查询场景
tests/test_context.py # 合成行为测试
scripts/check_release.py
PUBLIC_FILES          # 明确列出的源码发布白名单
```

## 公开代码，保留私人记录

仓库包含代码、文档、合成生成器，以及四份经人工核查并在 `PUBLIC_MEDIA` 绑定哈希的合成 App 展示素材。其他照片、视频、真实资料、草稿、批准清单和日志应放在仓库外。`.gitignore` 提供便利，不能作为隐私边界。

复现问题请使用合成记录，见[贡献指南](CONTRIBUTING.md)。代码使用 [MIT 许可](LICENSE)，个人运行记录不属于源码发布内容。
