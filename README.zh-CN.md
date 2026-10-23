# Atlas Context

**让你的 Agent 带着你的人生背景，理解并帮助你。**

[English](README.md) · [五分钟审阅](docs/reviewer-guide.md) · [产品方向](docs/product-direction.md) · [手机接入](docs/phone-handoff.md) · [隐私说明](PRIVACY.md) · [路线图](ROADMAP.md) · [MIT 许可](LICENSE)

Atlas Context 希望从你选定的日常照片和你自己的讲述中，逐渐整理出经历、兴趣与偏好，让 Agent 在提供帮助时拥有连续的背景。你应当能查看它如何理解你、纠正错误，并决定哪些内容可以交给哪个 Agent 使用。

当前开源实现包括手机照片反思流程、Python 审核核心和只读 MCP：最多选择五张照片，用 Apple Vision 在本地提供有限的场景提问，由你解释或纠正含义、确认具体文字，再单独决定哪些内容可以交给 Agent。它使用场景分类和固定问题，没有生成式视觉理解、自动多轮对话或长期人格模型。

**当前状态：实验性 Alpha。** 当前路径是：选照片 → 本地场景提问 → 本人解释或纠正 → 确认措辞 → 单独审核披露 → 传送 JSON → MCP 接入 → Agent 根据已分享的背景帮助你。也可完全不用照片，直接体验虚构场景。USB 自动扫描、生产版 Atlas Memoir 集成、实时同步和长期偏好学习仍待实现。

> **隐私优先：** 默认不选记录、不开云端权限；不导出原图、视频、GPS、相册标识或完整备份。文字仍可能包含隐私，需要逐句审核。使用云端模型会把批准文字发送给模型服务商；撤销仅能阻止后续读取，不能追回已发送的副本。详见 [隐私说明](PRIVACY.md)。

## 一条命令体验偏好与纠错

审核者可以先运行不需要照片、账号、SDK 或 API Key 的完整生命周期演示：

```sh
python3 -m atlas_context.review_demo --output ../atlas-review-demo
```

预期九项检查通过，模型与网络调用均为零。打开生成的 `private-review-walkthrough.md`，查看本人陈述、错误推测未被导出、修改草稿后失效、撤销旧访问、重新审核新偏好的过程。新偏好是本次休息日想参加有固定时间的室内艺术工作坊。演示不自动刷新手机资料，也不代表长期记忆。详见 [审阅指南](docs/reviewer-guide.md)。

以下命令保留最初的偏好场景：

```sh
python3 -m atlas_context.phone demo --scenario personal-assistance --output ../atlas-assistance-demo
```

虚构人物喜欢安静散步、摄影和有自由时间的休息日；咖啡馆照片来自工作，不能据此推断喜欢探店。命令只导出两条带引用的本人陈述，不创建或导出探店偏好，并生成独立 MCP 目录。预览不是模型回答，命令本身不联网。配置 `session/private-server.json` 后，把 `session/private-agent-task.md` 交给 Agent，再询问“帮我安排轻松的一天，并说明我的偏好如何影响方案”。默认 `local_only` 只应配合本地模型使用。

手机体验：运行 `python3 scripts/create_phone_project.py --output ../atlas-phone-app`，在 Xcode 打开生成的项目。选择 **Try fictional walk-through**，或通过系统选择器明确选择少量照片。真实照片的解释初始为空；修改文字会取消确认。确认不等于分享，导出页仍默认不选记录、不开云端权限。**Clear this session** 清空 App 内存中的照片与解释，已导出的文件须另行撤销或删除。详见 [接入指南](docs/phone-handoff.md)。

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

照片提供线索，你的解释赋予它个人意义。拍了很多咖啡，可能是喜欢探店，也可能是在做菜单设计。Agent 应先求证，再决定是否把它作为偏好。

第一版体验是：选定照片线索 → 固定场景问题 → 本人解释或纠正 → 审核后形成生活背景 → Agent 带着背景提供帮助。比如，你说明周末散步是为了放慢节奏、喜欢留出自由时间；已连接的 Agent 可以依据这段获准的解释提出方案、引用理由，并确认偏好是否仍然适用。项目没有内置本地语言模型。

站在你的角度思考，需要理解你认可的目标和取舍，也要能提醒盲点、提供其他选择。观察、本人陈述和模型猜测应分开记录，不能把几张照片变成固定的人格标签。已有同一虚构任务在 [无背景、原偏好和新偏好下的实际客户端样例](docs/context-comparison.md)，尚未建立真实用户的效果优势。详见 [产品方向与虚构场景](docs/product-direction.md)。

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
- 尚未实现 Atlas 全量备份解码、迁移、生产 App 集成和实时来源刷新。已有独立的原生照片反思与最小文字导出；验证使用虚构记录和程序生成的图片。
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

测试覆盖批准规则、私人字段排除、过期、撤销、偏好纠正、MCP 传输与发布历史；未安装可选 SDK 时，MCP 测试会跳过。CI 还编译 iOS 组件并验证 Swift/Python 契约和本地图片检查。实际结果与验证边界见 [验证说明](docs/evidence.md)。发布脚本检查白名单、素材精确哈希和历史文件，不能代替人工核查。

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

仓库包含代码、文档、合成生成器，以及经人工核查并在 `PUBLIC_MEDIA` 绑定哈希的合成 App 展示素材。其他照片、视频、真实资料、草稿、批准清单和日志应放在仓库外。`.gitignore` 提供便利，不能作为隐私边界。

复现问题请使用合成记录，见[贡献指南](CONTRIBUTING.md)。代码使用 [MIT 许可](LICENSE)，个人运行记录不属于源码发布内容。
