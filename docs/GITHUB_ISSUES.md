# 从 BACKLOG 创建 GitHub Issues

> 仓库：`TinjiYDon/zhixue-multimodal`  
> 目标：为 **P0-2～P0-7** 各建 **1 个 Epic Issue**（共 6 个），Assign 主责，避免重复领活。

---

## 前置条件

1. **成员已是 Collaborator**（Settings → Collaborators → Write）
   - 顺序与角色对应（你按此顺序给的）：
     | 顺序 | GitHub | 角色 | Issue |
     |------|--------|------|-------|
     | 1 | `oceancat91` | 小程序 B | #P0-7 |
     | 2 | `RynnYuan` | 前端 A | #P0-6 ⚠️ Pending Invite |
     | 3 | `whq6830-arch` | 多媒体 C | #P0-3 |
     | 4 | `yucc280` | 后端接口 D | #P0-4 |
2. 负责人本机安装 [GitHub CLI](https://cli.github.com/) 并登录：

```powershell
gh auth login
gh auth status
```

---

## 方式一：一键脚本（推荐）

### 1. 编辑成员 GitHub 用户名

打开 `scripts/create_backlog_issues.ps1`，修改 `$Assignees`（必须是 GitHub **login**，不是昵称）：

```powershell
$Assignees = @{
  P02 = @("TinjiYDon")        # owner upload
  P03 = @("whq6830-arch")     # C multimedia
  P04 = @("yucc280")          # D backend Job API
  P05 = @("TinjiYDon")        # owner RAG
  P06 = @("RynnYuan")         # A web
  P07 = @("oceancat91")       # B miniapp
}
```

### 2. 执行

```powershell
cd d:\project\zhixue-multimodal
powershell -ExecutionPolicy Bypass -File .\scripts\create_backlog_issues.ps1
```

脚本会：创建标签 → 创建 6 个 Issue → Assign → 输出 Issue 链接。

### 3. 发到群里

把脚本输出的 6 个 URL 发到团队群，并说明：

> 每人只领 **Assign 给自己的 Epic**；子任务在 Issue 描述里勾选，不要另开重复 Issue。

---

## 方式二：网页手动创建

1. 打开 https://github.com/TinjiYDon/zhixue-multimodal/issues/new/choose  
2. 选 **「任务」** 模板  
3. 标题格式：`[P0-2] 上传 API + Course PG 协调`  
4. 右侧 **Assignees** 选主责（须已是协作者）  
5. **Labels** 加 `p0-2` `api` 等  
6. 描述里粘贴 BACKLOG 该节的 checkbox  

重复 6 次（P0-2～P0-7）。

---

## 方式三：单条 gh 命令（示例）

```powershell
gh issue create --repo TinjiYDon/zhixue-multimodal `
  --title "[P0-4] Job API + Worker" `
  --label "p0-4,jobs,worker" `
  --assignee whq6830-arch `
  --body-file docs/issue-bodies/P0-4.md
```

（Issue 正文可先放在 `docs/issue-bodies/` 便于复用。）

---

## Epic 与主责对照（已创建）

| Issue | 标题 | 主责 | GitHub |
|-------|------|------|--------|
| [#2](https://github.com/TinjiYDon/zhixue-multimodal/issues/2) | P0-2 upload | 负责人 | `TinjiYDon` · ✅ closed |
| [#4](https://github.com/TinjiYDon/zhixue-multimodal/issues/4) | P0-3 多媒体 | C | `whq6830-arch` · 🔔 request changes |
| [#5](https://github.com/TinjiYDon/zhixue-multimodal/issues/5) | P0-4 Job API | D | `yucc280` · ✅ API/Worker 骨架已合；PG 续作 |
| [#6](https://github.com/TinjiYDon/zhixue-multimodal/issues/6) | P0-5 RAG/ask | 负责人 | `TinjiYDon` · timeline 占位已加 |
| [#7](https://github.com/TinjiYDon/zhixue-multimodal/issues/7) | P0-6 Web | A | `RynnYuan` · PR #9 ✅ merged |
| [#8](https://github.com/TinjiYDon/zhixue-multimodal/issues/8) | P0-7 小程序 | B | `oceancat91` · 🔔 已催 |

负责人 2026-07-22：合 #9 · 催 #4/#5/#7/#8 · `GET .../timeline` 占位  
负责人 2026-07-22b：合入 D `course-job-zyc`（jobs + course CRUD + worker）· upload→job · pytest 含 jobs  
负责人 2026-07-22c：`DEMO_E2E.md`（#P0-5c）· ICU MCP 骨架 · Bugbot 文档

**说明：** P0-2 里 `#P0-2b` Course PG 是 **D** 的子任务，写在 P0-2 或 P0-4 Issue 的 checklist 里，**不要**再开独立 Epic，避免 D 和负责人抢同一个 Issue。

---

## 避免重复领活

| 做法 | 说明 |
|------|------|
| 1 Epic = 1 模块切片 | 不要每人开 10 个小 Issue 抢同一文件 |
| Assign 唯一主责 | 协作者只能领 Assign 给自己的 |
| PR 关联 Issue | 标题写 `fix #12` 或 PR 模板填 `Closes #12` |
| 看板（可选） | Projects → 按 Assignee 分列：Todo / In Progress / Done |

---

## 里程碑 Issue（联调后再建）

`#MILE-1`～`#MILE-4` 建议在 P0-2～P0-5 有进展后再建，或作为 **无 Assign 的跟踪 Issue**，负责人维护。

---

## 常见问题

| 问题 | 处理 |
|------|------|
| Assign 列表里没有某人 | 对方未接受 Collaborator 邀请 |
| `gh: command not found` | 安装 GitHub CLI 或用手动方式二 |
| 已有同名 Issue | 脚本会跳过（见脚本内 `-SkipExisting`） |
| 想改主责 | Issue 右侧 Assignees 修改即可 |
