# -*- coding: utf-8 -*-
"""Generate zhixue closing-report Word documents (with formulas & figures)."""
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, Inches

OUT = Path(r"d:\project\zhixue-multimodal\docs")
FIG = OUT / "report-figures"


def set_run_font(run, name="宋体", size=12, bold=False, east_asia=None):
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia or name)


def add_heading_cn(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    for run in p.runs:
        set_run_font(run, "黑体", 16 if level == 1 else 14 if level == 2 else 12, bold=True)
    return p


def add_para(doc, text, first_line_indent=True, size=12, bold=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_after = Pt(6)
    if first_line_indent:
        pf.first_line_indent = Cm(0.74)
    run = p.add_run(text)
    set_run_font(run, "宋体", size, bold=bold)
    return p


def add_bullet(doc, text, size=12):
    p = doc.add_paragraph(style="List Bullet")
    p.clear()
    run = p.add_run(text)
    set_run_font(run, "宋体", size)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    return p


def add_formula(doc, label: str, expr: str, explain: str = ""):
    """Human-readable formula block (label + monospace-ish expression + explain)."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Cm(0.5)
    r1 = p.add_run(f"{label}  ")
    set_run_font(r1, "黑体", 11, bold=True)
    r2 = p.add_run(expr)
    set_run_font(r2, "Times New Roman", 11)
    r2.font.name = "Times New Roman"
    r2._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    if explain:
        add_para(doc, explain, first_line_indent=False, size=10)


def add_figure(doc, filename: str, caption: str, width_in: float = 5.8):
    path = FIG / filename
    if not path.exists():
        add_para(doc, f"[缺图: {filename}]", first_line_indent=False, size=10)
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    run = p.add_run()
    run.add_picture(str(path), width=Inches(width_in))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(10)
    cr = cap.add_run(caption)
    set_run_font(cr, "楷体", 10)


def setup_doc(title: str) -> Document:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)

    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run(title)
    set_run_font(r, "黑体", 18, bold=True)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sr = sub.add_run("智学多模态 Agent（zhixue-multimodal）")
    set_run_font(sr, "楷体", 12)

    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    mr = meta.add_run("仓库：TinjiYDon/zhixue-multimodal　·　文稿日期：2026-08-14")
    set_run_font(mr, "宋体", 10)
    return doc


def build_part1():
    doc = setup_doc("结项报告 · 第 1 部分\n模型架构与算法（可用正文稿）")
    note = doc.add_paragraph()
    nr = note.add_run(
        "说明：本稿按结项报告书语气撰写，可直接删改后作为「第 1 部分」正文。"
        "含算法公式与架构/链路图；正式 RAG/真 WhisperX 为演进项，勿改写成已全面生产上线。"
    )
    set_run_font(nr, "楷体", 10)
    note.paragraph_format.space_after = Pt(12)

    add_heading_cn(doc, "1.1 问题定义与目标", 1)
    add_para(
        doc,
        "课堂场景中，音视频、板书/PPT 与师生问答往往割裂存储：学生复习时难以按时间点回看讲解，"
        "教师也难以基于整节课内容做即时答疑。智学多模态 Agent 面向「课程级」多模态理解，目标是："
        "在一次课程媒体上传后，自动完成语音转写与版面文字提取，形成带时间戳的课程时间轴（timeline），"
        "并在此基础上提供基于检索增强（RAG）的课程问答能力，支撑 Web 端与微信小程序端的学习交互。",
    )
    add_para(
        doc,
        "本项目强调工程可复现与契约先行：转写与 OCR 输出统一到 TranscriptResult / OcrResult 等模式；"
        "无 GPU 或未安装重型模型时，可通过 fixture 后端完成联调与验收，避免将「演示可跑」等同于"
        "「生产级语音模型已默认上线」。本系统与 ICU 临床预警/床位调度项目零代码耦合，仅在工程方法上可并列对照。",
    )

    add_heading_cn(doc, "1.2 总体算法与数据流", 1)
    add_para(
        doc,
        "端到端主链路可概括为：媒体对象入库 → 异步任务调度 → 音视频预处理与多模态感知 → "
        "页级/时间对齐 → 时间轴物化 → 问答检索与生成。对课程 c，记媒体对象为 M_c，系统输出如下。",
    )
    add_formula(
        doc,
        "式(1)",
        "T_c = {(t_i^s, t_i^e, text_i)} (i=1..N)",
        "时间轴字幕片段集合：起止时刻与文本。",
    )
    add_formula(
        doc,
        "式(2)",
        "S_c = {(p_j, t_j^s, title_j)} (j=1..M)",
        "幻灯片/板书页序列：页号、页起始时刻与标题。",
    )
    add_formula(
        doc,
        "式(3)",
        "Ask: (q, c) → (a, E),  E ⊆ T_c ∪ S_c",
        "问答：在课程 c 上对问题 q 返回答案 a 与可追溯证据集 E。",
    )
    add_figure(doc, "02-data-pipeline.png", "图1-1 数据处理链路（上传→感知→时间轴→问答）")
    add_para(doc, "关键阶段如下。", first_line_indent=False)
    add_bullet(doc, "上传与对象存储：客户端经预签名 URL 将媒体写入 MinIO；complete 校验对象存在后创建 Job。")
    add_bullet(doc, "Worker 调度：BackgroundTasks（后续可换队列）调用多媒体流水线，更新 Job 进度与状态。")
    add_bullet(doc, "感知：FFmpeg 抽取 16 kHz 单声道 WAV；ASR 生成带时间戳字幕；OCR 提取板书/PPT 文本与框。")
    add_bullet(doc, "对齐：将字幕片段与 OCR 页在时间或语义上对齐，形成统一 timeline。")
    add_bullet(doc, "问答：课程隔离检索（现为占位 RAG；规划 pgvector + LLM）返回答案与来源。")

    add_heading_cn(doc, "1.3 多媒体感知模块", 1)
    add_heading_cn(doc, "1.3.1 音频预处理", 2)
    add_para(
        doc,
        "为降低 ASR 对采样率与声道的敏感性，系统使用 FFmpeg 将输入媒体解封装并重采样为 16 kHz 单声道 PCM WAV。"
        "联调默认推荐 MP4（video/mp4）；上传 API 层当前未强制 MIME 白名单，实际能否抽音取决于本机 FFmpeg。",
    )
    add_formula(
        doc,
        "式(4)",
        "x_wav = Resample_16kHz_mono( Demux(M_c) )",
        "预处理算子：解封装后重采样，得到 ASR 输入波形。",
    )

    add_heading_cn(doc, "1.3.2 语音识别与时间对齐（ASR）", 2)
    add_para(
        doc,
        "语音识别路径以 Whisper 族模型为核心，工程上支持 WhisperX / faster-whisper 等实现，并可选字词级强制对齐，"
        "输出映射到 TranscriptResult / TranscriptSegment。无 GPU 时可切换 fixture 后端，保证契约测试与联调。",
    )
    add_formula(
        doc,
        "式(5)",
        "ŷ = ASR(x_wav),  ŷ_i = (text_i, t_i^s, t_i^e)",
        "ASR 将波形映射为带时间戳的文本片段序列。",
    )

    add_heading_cn(doc, "1.3.3 版面文字识别（OCR）", 2)
    add_para(
        doc,
        "对课件页或板书截图，采用 RapidOCR（ONNXRuntime）等轻量方案提取文本块及四点坐标框，"
        "组装为 OcrResult / OcrPageResult，与 ASR 共同构成多模态证据。",
    )
    add_formula(
        doc,
        "式(6)",
        "O_p = {(text_k, box_k)},  box_k ∈ R^{4×2}",
        "单页 OCR：文本块与四点框；多页聚合后进入对齐。",
    )

    add_heading_cn(doc, "1.4 对齐与时间轴构建", 1)
    add_para(
        doc,
        "对齐模块将 ASR 片段与 OCR/PPT 页关联到统一时间轴。可采用时间重叠与语义相似的加权分数，"
        "并为每个字幕片段选择最佳页。对外以 GET /api/v1/courses/{id}/timeline 暴露。",
    )
    add_formula(
        doc,
        "式(7)",
        "overlap(u,v) = |I(u)∩I(v)| / |I(u)∪I(v)|,  I(·)=[t^s, t^e]",
        "时间区间 Jaccard 重叠度。",
    )
    add_formula(
        doc,
        "式(8)",
        "sim(u,v) = α·overlap(u,v) + (1-α)·sem(u,v)",
        "综合对齐分数；sem 可为嵌入余弦或归一化编辑相似度。",
    )
    add_formula(
        doc,
        "式(9)",
        "j*(i) = arg max_j sim(seg_i, page_j)",
        "将第 i 个字幕片段指派到得分最高的页。",
    )
    add_formula(
        doc,
        "式(10)",
        "nsim(a,b) = 1 - Levenshtein(a,b) / max(|a|,|b|)",
        "基于编辑距离的辅助文本相似度（可用于标题—字幕对齐）。",
    )
    add_figure(doc, "05-alignment-timeline.png", "图1-2 时间轴对齐示意（字幕片段 ↔ PPT 页）")

    add_heading_cn(doc, "1.5 检索增强问答（RAG）", 1)
    add_para(
        doc,
        "问答接口为 POST /api/v1/courses/{id}/ask。流程：检索 Top-K 证据 → 拼装提示词 → 生成答案并回传来源。"
        "现阶段为占位 RAG；规划 pgvector 向量索引与正式 LLM，API 契约保持不变。",
    )
    add_formula(
        doc,
        "式(11)",
        "score(q,e) = cos(φ(q), φ(e))  或  BM25(q,e)",
        "检索打分：向量余弦（规划）或词法 BM25/关键词匹配（占位可近似）。",
    )
    add_formula(
        doc,
        "式(12)",
        "E = TopK_{e∈T_c∪S_c} score(q,e)",
        "在课程语料上取 Top-K 证据，保证 course_id 隔离。",
    )
    add_formula(
        doc,
        "式(13)",
        "a = LLM( Prompt(q, E) ),  sources ⊆ E",
        "条件生成；sources 用于前端展示与可审计引用。",
    )
    add_figure(doc, "03-rag-flow.png", "图1-3 课程级 RAG 问答流程")
    add_figure(doc, "04-formulas.png", "图1-4 关键公式一览（排版图）", width_in=5.4)

    add_heading_cn(doc, "1.6 与系统边界相关的算法约束", 1)
    add_bullet(doc, "课程隔离：所有检索与时间轴必须以 course_id 为键，禁止跨课串数据。")
    add_bullet(doc, "异步与可观测：感知计算放入 Job/Worker，API 层保持快速返回；状态可查询。")
    add_bullet(doc, "降级优先：重模型不可用时 fixture 保契约，避免阻塞前后端与验收。")
    add_bullet(doc, "诚实表述：不将占位 RAG、模拟视频区或 fixture ASR 写成生产级已交付能力。")

    add_heading_cn(doc, "1.7 小结", 1)
    add_para(
        doc,
        "智学多模态 Agent 的算法主线是多媒体感知（ASR/OCR）+ 时间对齐 + 课程级 RAG。"
        "上文式(1)–(13)给出形式化记号，便于与实现模块对照；正式向量检索与生产级语音识别为规划增强项，"
        "结项材料中应按「已实现 / 演进中」分层陈述。",
    )

    path = OUT / "结项报告-第1部分-模型架构与算法.docx"
    doc.save(path)
    return path


def build_intro_234():
    doc = setup_doc("智学多模态 Agent\n项目详细介绍与结项材料（第 2–4 部分）")
    note = doc.add_paragraph()
    nr = note.add_run(
        "结构：前半为项目详细介绍（含架构/链路图）；后半为第 2、3、4 部分关键词与信息补充。"
    )
    set_run_font(nr, "楷体", 10)
    note.paragraph_format.space_after = Pt(12)

    add_heading_cn(doc, "一、项目详细介绍", 1)

    add_heading_cn(doc, "1.1 一句话定位", 2)
    add_para(
        doc,
        "智学多模态 Agent 是面向课堂教学的多模态实时理解系统：完成课程音视频上传后，"
        "自动转写与版面识别，生成可交互时间轴，并支持基于课程内容的智能问答；"
        "提供 Vue3 Web 与 UniApp 微信小程序两端入口。",
    )

    add_heading_cn(doc, "1.2 背景与意义", 2)
    add_para(
        doc,
        "传统网课回放多为「整段视频 + 静态课件」，缺少细粒度时间索引与可追溯答疑。"
        "本项目将 ASR、OCR、时间轴与 RAG 串成一条可工程化交付的链路，使「听到的」与「看到的」"
        "在同一时间坐标系下可检索、可跳转、可引用，从而提升复习效率与答疑质量。",
    )

    add_heading_cn(doc, "1.3 功能范围", 2)
    add_bullet(doc, "课程管理：Course 创建与查询（已落 PostgreSQL）。")
    add_bullet(doc, "媒体上传：MinIO 预签名上传、complete 校验、自动创建转写 Job。")
    add_bullet(doc, "多媒体处理：FFmpeg 抽音、ASR、OCR（真模型可选；fixture 默认可测）。")
    add_bullet(doc, "时间轴：GET timeline；支持 from-fixture 注入演示数据。")
    add_bullet(doc, "问答：POST /api/v1/courses/{id}/ask（课程隔离）。")
    add_bullet(doc, "前端：Web 课程列表/详情；小程序列表与问答骨架。")

    add_heading_cn(doc, "1.4 技术架构", 2)
    add_para(
        doc,
        "后端 FastAPI，前端 Vue3 + Vite，小程序 UniApp。Docker Compose 提供 PostgreSQL（主机端口 5435）、"
        "Redis 与 MinIO。异步任务当前以 BackgroundTasks 触发 Worker，后续可演进为独立队列。",
    )
    add_figure(doc, "01-architecture.png", "图A-1 系统架构总览")
    add_figure(doc, "02-data-pipeline.png", "图A-2 数据处理链路")

    add_heading_cn(doc, "1.5 协作与里程碑（摘要）", 2)
    add_bullet(doc, "P0 多媒体 schema + fixture：已完成（PR #12）。")
    add_bullet(doc, "MILE-1 Course/Job PostgreSQL：已完成。")
    add_bullet(doc, "MILE-2 Web 接真 timeline/ask：骨架已完成（Issue #7 仍 open）。")
    add_bullet(doc, "MILE-3 小程序骨架：已完成（PR #11）。")
    add_bullet(doc, "正式 pgvector RAG、MILE-4 答辩彩排：进行中/未做。")
    add_bullet(doc, "人工验收（2026-08-14）：有条件通过；见 ACCEPTANCE_ZHIXUE.md。")

    add_heading_cn(doc, "1.6 使用与演示要点", 2)
    add_para(
        doc,
        "本地：docker compose up -d 后启动 uvicorn（8000）与 npm run dev（5173）。"
        "上传联调默认 mp4。演示：健康检查 → 课程列表 → 进入课程 → timeline → 提问。"
        "无账号登录。Release：zhixue-mile2。",
    )

    add_heading_cn(doc, "1.7 边界与非目标", 2)
    add_bullet(doc, "不与 ICU 预警/床位系统做运行时数据耦合。")
    add_bullet(doc, "不宣称生产级 WhisperX / 正式向量 RAG 已默认上线。")
    add_bullet(doc, "视频区可为模拟播放器占位。")

    add_heading_cn(doc, "二、第 2 部分 · 系统实现与工程交付（关键词与信息补充）", 1)
    add_heading_cn(doc, "2.1 建议标题", 2)
    add_para(doc, "系统架构、工程实现与可复现交付", first_line_indent=False)
    add_heading_cn(doc, "2.2 核心关键词", 2)
    for k in [
        "仓独立 / 契约优先 / OpenAPI",
        "FastAPI · Vue3 · UniApp",
        "Docker Compose：PostgreSQL · Redis · MinIO",
        "upload：presign → PUT → complete → 自动 Job",
        "Worker · FFmpeg 16kHz · ASR/OCR · fixture 降级",
        "timeline / ask 课程隔离 · pytest · Release zhixue-mile2",
    ]:
        add_bullet(doc, k)
    add_heading_cn(doc, "2.3 信息补充", 2)
    add_bullet(doc, "架构与链路图见上文图A-1、图A-2；公式见《第1部分》式(1)–(13)或公式排版图。")
    add_bullet(doc, "转写契约：backend/app/schemas/transcript.py。")
    add_bullet(doc, "ask 路径：POST /api/v1/courses/{id}/ask。")
    add_bullet(doc, "已知限制：无登录；占位 RAG；Issue #6/#7；PR #13。")
    add_heading_cn(doc, "2.4 建议章节提纲", 2)
    for i, t in enumerate(
        [
            "总体架构图与模块职责",
            "上传、Job 与多媒体流水线",
            "timeline 与前端交互",
            "ask 与课程隔离",
            "部署、配置与复现",
        ],
        1,
    ):
        add_bullet(doc, f"{i}. {t}")

    add_heading_cn(doc, "三、第 3 部分 · 实验评测与验收（关键词与信息补充）", 1)
    add_heading_cn(doc, "3.1 建议标题", 2)
    add_para(doc, "实验设计、指标与验收结论", first_line_indent=False)
    add_heading_cn(doc, "3.2 核心关键词", 2)
    for k in [
        "契约测试 / schema",
        "pytest 14 passed（2026-08-14）",
        "冒烟：health → courses → timeline → ask",
        "有条件通过 · fixture ≠ 真 Whisper 上线",
        "Open Issue #6 #7 · Open PR #13",
    ]:
        add_bullet(doc, k)
    add_heading_cn(doc, "3.3 信息补充", 2)
    add_bullet(doc, "验收报告：docs/ACCEPTANCE_ZHIXUE.md；截图：docs/acceptance-screens/。")
    add_bullet(doc, "轻微失败：首页「课程列表」标题重复；预期：模拟视频区、占位 RAG。")
    add_heading_cn(doc, "3.4 建议章节提纲", 2)
    for i, t in enumerate(
        ["测试分层", "fixture 策略", "验收结果表", "缺陷与边界", "正式 RAG/ASR 评测计划"],
        1,
    ):
        add_bullet(doc, f"{i}. {t}")

    add_heading_cn(doc, "四、第 4 部分 · 总结与展望（关键词与信息补充）", 1)
    add_heading_cn(doc, "4.1 建议标题", 2)
    add_para(doc, "工作总结、创新点、不足与下一步", first_line_indent=False)
    add_heading_cn(doc, "4.2 核心关键词", 2)
    for k in [
        "课堂多模态实时 Agent · 时间轴驱动",
        "契约先行 · fixture 可演示 · Web+小程序",
        "pgvector 正式 RAG · MILE-4 彩排（展望）",
    ]:
        add_bullet(doc, k)
    add_heading_cn(doc, "4.3 信息补充", 2)
    add_bullet(doc, "已完成：基建、多媒体契约、Course/Job PG、Web 骨架、小程序 P0、有条件验收。")
    add_bullet(doc, "不足：正式 RAG/生产 ASR 未默认交付；#6/#7 未关；无账号体系。")
    add_bullet(doc, "下一步：对齐 docs/ROADMAP.md。")
    add_heading_cn(doc, "4.4 禁止表述", 2)
    add_bullet(doc, "「已具备完整账号登录」。")
    add_bullet(doc, "「生产级 WhisperX 已默认上线」。")
    add_bullet(doc, "「与 ICU 风险/床位已打通」。")

    add_heading_cn(doc, "附录 · 文档索引", 1)
    add_bullet(doc, "GitHub：https://github.com/TinjiYDon/zhixue-multimodal")
    add_bullet(doc, "PROGRESS / ROADMAP / CHANGELOG / ACCEPTANCE_ZHIXUE / report-figures/")

    path = OUT / "项目详细介绍与结项第2-4部分补充.docx"
    doc.save(path)
    return path


def build_formula_viz_pack():
    """Standalone pack: formulas + all figures for slides/appendix."""
    doc = setup_doc("算法公式与架构可视化补充材料")
    note = doc.add_paragraph()
    nr = note.add_run("可单独作为答辩附录或插入总报告；与第1部分公式编号一致。")
    set_run_font(nr, "楷体", 10)

    add_heading_cn(doc, "1. 架构与数据链路图", 1)
    add_figure(doc, "01-architecture.png", "图S-1 系统架构")
    add_figure(doc, "02-data-pipeline.png", "图S-2 数据处理链路")
    add_figure(doc, "05-alignment-timeline.png", "图S-3 时间轴对齐示意")
    add_figure(doc, "03-rag-flow.png", "图S-4 RAG 流程")

    add_heading_cn(doc, "2. 公式表（文字版）", 1)
    formulas = [
        ("式(1)", "T_c = {(t_i^s, t_i^e, text_i)}", "课程时间轴字幕集合"),
        ("式(2)", "S_c = {(p_j, t_j^s, title_j)}", "幻灯片页序列"),
        ("式(3)", "(q,c)→(a,E), E⊆T_c∪S_c", "问答输入输出"),
        ("式(4)", "x_wav = Resample_16kHz_mono(Demux(M_c))", "抽音预处理"),
        ("式(5)", "ŷ = ASR(x_wav), ŷ_i=(text_i,t_i^s,t_i^e)", "语音识别"),
        ("式(6)", "O_p={(text_k,box_k)}, box_k∈R^{4×2}", "OCR 单页"),
        ("式(7)", "overlap(u,v)=|I(u)∩I(v)|/|I(u)∪I(v)|", "时间重叠"),
        ("式(8)", "sim=α·overlap+(1-α)·sem", "对齐综合分"),
        ("式(9)", "j*(i)=arg max_j sim(seg_i,page_j)", "片段指派页"),
        ("式(10)", "nsim=1-Lev/max(|a|,|b|)", "编辑相似度"),
        ("式(11)", "score=cos(φ(q),φ(e)) 或 BM25", "检索打分"),
        ("式(12)", "E=TopK score(q,e)", "证据集"),
        ("式(13)", "a=LLM(Prompt(q,E))", "生成"),
    ]
    for lab, expr, exp in formulas:
        add_formula(doc, lab, expr, exp)

    add_heading_cn(doc, "3. 公式排版图", 1)
    add_figure(doc, "04-formulas.png", "图S-5 公式一览（便于直接贴 PPT）", width_in=5.5)

    path = OUT / "算法公式与架构可视化补充.docx"
    doc.save(path)
    return path


if __name__ == "__main__":
    import subprocess
    import sys

    # Ensure figures exist
    subprocess.check_call([sys.executable, str(OUT / "_gen_report_figures.py")])
    paths = [build_part1(), build_intro_234(), build_formula_viz_pack()]
    for p in paths:
        print(p)

