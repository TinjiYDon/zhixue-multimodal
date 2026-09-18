# -*- coding: utf-8 -*-
"""Generate architecture / pipeline figures and formula sheets for zhixue reports."""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(r"d:\project\zhixue-multimodal\docs\report-figures")
OUT.mkdir(parents=True, exist_ok=True)

# Prefer Chinese-capable fonts on Windows
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def _box(ax, xy, w, h, text, fc="#E8F4F8", ec="#1F4E79", fontsize=9):
    x, y = xy
    patch = FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.05",
        linewidth=1.4, edgecolor=ec, facecolor=fc,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize, color="#0D2137", wrap=True)


def _arrow(ax, start, end):
    ax.annotate(
        "", xy=end, xytext=start,
        arrowprops=dict(arrowstyle="->", color="#334155", lw=1.5),
    )


def fig_architecture():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=160)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.set_title("智学多模态 Agent · 系统架构", fontsize=14, pad=12, color="#0F172A")

    # Clients
    _box(ax, (0.4, 4.6), 2.2, 1.2, "Web\n(Vue3 + Vite)", fc="#DBEAFE")
    _box(ax, (0.4, 2.8), 2.2, 1.2, "微信小程序\n(UniApp)", fc="#DBEAFE")

    # API
    _box(ax, (3.5, 3.2), 2.6, 2.2, "FastAPI\nupload / courses\njobs / timeline / ask", fc="#FEF3C7", fontsize=9)

    # Infra
    _box(ax, (7.0, 4.8), 3.4, 1.0, "PostgreSQL · Course / Job", fc="#D1FAE5")
    _box(ax, (7.0, 3.5), 3.4, 1.0, "MinIO · 媒体对象", fc="#D1FAE5")
    _box(ax, (7.0, 2.2), 3.4, 1.0, "Redis（可选队列）", fc="#D1FAE5")

    # Worker / models
    _box(ax, (3.5, 0.6), 2.6, 1.6, "Worker\nFFmpeg → ASR / OCR", fc="#FCE7F3", fontsize=9)
    _box(ax, (7.0, 0.6), 3.4, 1.6, "对齐 · Timeline\n占位/正式 RAG", fc="#EDE9FE", fontsize=9)

    _arrow(ax, (2.6, 5.2), (3.5, 4.5))
    _arrow(ax, (2.6, 3.4), (3.5, 4.0))
    _arrow(ax, (6.1, 4.6), (7.0, 5.3))
    _arrow(ax, (6.1, 4.2), (7.0, 4.0))
    _arrow(ax, (6.1, 3.6), (7.0, 2.7))
    _arrow(ax, (4.8, 3.2), (4.8, 2.2))
    _arrow(ax, (6.1, 1.4), (7.0, 1.4))

    ax.text(0.4, 0.15, "边界：与 ICU 预警/调度零运行时耦合；fixture 可降级重模型。", fontsize=8, color="#64748B")
    fig.tight_layout()
    path = OUT / "01-architecture.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def fig_pipeline():
    fig, ax = plt.subplots(figsize=(12, 3.8), dpi=160)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.set_title("数据处理链路（上传 → 感知 → 时间轴 → 问答）", fontsize=13, pad=10)

    stages = [
        (0.3, "① 上传\npresign/PUT\ncomplete"),
        (2.3, "② Job\n创建任务\n调度 Worker"),
        (4.3, "③ 抽音\nFFmpeg\n16kHz WAV"),
        (6.3, "④ 感知\nASR + OCR\n契约 JSON"),
        (8.3, "⑤ 对齐\nTimeline\nT_c / S_c"),
        (10.3, "⑥ 问答\nRetrieve\n+ Generate"),
    ]
    colors = ["#DBEAFE", "#FEF3C7", "#FCE7F3", "#E0E7FF", "#D1FAE5", "#EDE9FE"]
    for (x, text), fc in zip(stages, colors):
        _box(ax, (x, 1.2), 1.7, 1.8, text, fc=fc, fontsize=8)
    for i in range(len(stages) - 1):
        x0 = stages[i][0] + 1.7
        x1 = stages[i + 1][0]
        _arrow(ax, (x0, 2.1), (x1, 2.1))

    ax.text(0.3, 0.4, "默认样例媒体：MP4；输出契约：TranscriptResult / OcrResult / Timeline / AskResponse。", fontsize=8, color="#64748B")
    fig.tight_layout()
    path = OUT / "02-data-pipeline.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def fig_rag():
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=160)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.axis("off")
    ax.set_title("课程级 RAG 问答流程（算法示意）", fontsize=13, pad=10)

    _box(ax, (0.3, 2.4), 1.8, 1.2, "问题 q", fc="#DBEAFE")
    _box(ax, (2.6, 2.4), 2.2, 1.2, "检索\nTop-K 证据 E", fc="#FEF3C7")
    _box(ax, (5.4, 2.4), 2.2, 1.2, "提示词拼装\nPrompt(q,E)", fc="#FCE7F3")
    _box(ax, (8.0, 2.4), 1.7, 1.2, "生成\n答案 a", fc="#D1FAE5")
    _box(ax, (2.6, 0.5), 4.0, 1.2, "课程语料库：Timeline T_c ∪ 幻灯片 S_c\n隔离键 course_id", fc="#E0E7FF", fontsize=9)

    _arrow(ax, (2.1, 3.0), (2.6, 3.0))
    _arrow(ax, (4.8, 3.0), (5.4, 3.0))
    _arrow(ax, (7.6, 3.0), (8.0, 3.0))
    _arrow(ax, (4.6, 2.4), (4.6, 1.7))

    ax.text(0.3, 0.1, "现状：占位检索可命中 fixture；规划：pgvector 向量检索 + 正式 LLM。", fontsize=8, color="#64748B")
    fig.tight_layout()
    path = OUT / "03-rag-flow.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def fig_formulas():
    """Render key formulas as a clean sheet image (mathtext-safe)."""
    fig = plt.figure(figsize=(9.5, 10.5), dpi=160)
    fig.patch.set_facecolor("white")
    fig.text(0.05, 0.96, "智学多模态 · 关键算法公式（结项用）", fontsize=14, weight="bold", va="top")

    lines = [
        r"$(1)\ \mathrm{Timeline:}\ T_c=\{(t_i^{s},\,t_i^{e},\,\mathrm{text}_i)\}_{i=1}^{N}$",
        r"$\qquad S_c=\{(p_j,\,t_j^{s},\,\mathrm{title}_j)\}_{j=1}^{M}$",
        r"$(2)\ \hat{y}=\mathrm{ASR}(x_{16\mathrm{kHz}}),\ \hat{y}_i=(\mathrm{text}_i,t_i^{s},t_i^{e})$",
        r"$(3)\ O_p=\{(\mathrm{text}_k,\,\mathrm{box}_k)\},\ \mathrm{box}_k\in\mathbb{R}^{4\times 2}$",
        r"$(4)\ \mathrm{overlap}(u,v)=\frac{|I(u)\cap I(v)|}{|I(u)\cup I(v)|},\ I(\cdot)=[t^{s},t^{e}]$",
        r"$(5)\ \mathrm{sim}(u,v)=\alpha\cdot\mathrm{overlap}(u,v)+(1-\alpha)\cdot\mathrm{sem}(u,v)$",
        r"$(6)\ j^*(i)=\arg\max_j\ \mathrm{sim}(\mathrm{seg}_i,\mathrm{page}_j)$",
        r"$(7)\ \mathrm{score}(q,e)=\cos(\phi(q),\phi(e))\ \mathrm{or}\ \mathrm{BM25}(q,e)$",
        r"$(8)\ E=\mathrm{TopK}_{e\in T_c\cup S_c}\ \mathrm{score}(q,e)$",
        r"$(9)\ a=\mathrm{LLM}(\mathrm{Prompt}(q,E)),\ \mathrm{sources}\subseteq E$",
        r"$(10)\ \mathrm{nsim}(a,b)=1-\frac{\mathrm{Lev}(a,b)}{\max(|a|,|b|)}$",
    ]
    y = 0.90
    for line in lines:
        fig.text(0.06, y, line, fontsize=12, va="top")
        y -= 0.075

    fig.text(
        0.06, 0.08,
        "注：φ 为文本向量编码器（规划 pgvector）；现网占位 RAG 可用关键词/片段匹配近似 score。",
        fontsize=9, color="#475569",
    )
    path = OUT / "04-formulas.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def fig_alignment_timeline():
    fig, ax = plt.subplots(figsize=(10, 3.6), dpi=160)
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.set_title("时间轴对齐示意（字幕片段 与 PPT 页）", fontsize=12, pad=8)

    # time axis
    ax.plot([2, 38], [1.2, 1.2], color="#94A3B8", lw=2)
    for t, lab in [(2, "0s"), (12, "8s"), (24, "20s"), (36, "35s")]:
        ax.plot([t, t], [1.05, 1.35], color="#64748B", lw=1.2)
        ax.text(t, 0.6, lab, ha="center", fontsize=8, color="#64748B")

    # ASR segments
    ax.add_patch(mpatches.Rectangle((2, 2.4), 9, 0.7, color="#93C5FD"))
    ax.text(6.5, 2.75, "seg1 欢迎…核心概念", ha="center", va="center", fontsize=8)
    ax.add_patch(mpatches.Rectangle((12, 2.4), 11, 0.7, color="#93C5FD"))
    ax.text(17.5, 2.75, "seg2 问题定义与边界", ha="center", va="center", fontsize=8)
    ax.add_patch(mpatches.Rectangle((24, 2.4), 12, 0.7, color="#93C5FD"))
    ax.text(30, 2.75, "seg3 数据验证假设", ha="center", va="center", fontsize=8)

    # slides
    ax.add_patch(mpatches.Rectangle((2, 3.6), 9, 0.7, color="#C4B5FD"))
    ax.text(6.5, 3.95, "第1页 封面", ha="center", va="center", fontsize=8)
    ax.add_patch(mpatches.Rectangle((12, 3.6), 11, 0.7, color="#C4B5FD"))
    ax.text(17.5, 3.95, "第2页 要点一", ha="center", va="center", fontsize=8)
    ax.add_patch(mpatches.Rectangle((24, 3.6), 12, 0.7, color="#C4B5FD"))
    ax.text(30, 3.95, "第3页 要点二", ha="center", va="center", fontsize=8)

    ax.text(2, 4.7, "紫色：S_c（页）　蓝色：T_c（字幕）　对齐按时间重叠 + 语义相似", fontsize=8, color="#475569")
    fig.tight_layout()
    path = OUT / "05-alignment-timeline.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


if __name__ == "__main__":
    paths = [
        fig_architecture(),
        fig_pipeline(),
        fig_rag(),
        fig_formulas(),
        fig_alignment_timeline(),
    ]
    for p in paths:
        print(p)
