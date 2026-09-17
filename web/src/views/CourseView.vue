<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import {
  askCourse,
  fetchTimeline,
  loadTimelineFromFixture,
  type TimelineCue,
  type TimelineResponse,
  type TimelineSlide,
} from "@/api/client";

const route = useRoute();
const courseId = computed(() => String(route.params.id || "demo"));

const question = ref("");
const answer = ref("暂无回答");
const sources = ref<string[]>([]);
const asking = ref(false);
const loading = ref(false);
const error = ref("");
const apiStatus = ref("");
const dataSource = ref<string>("");
const banner = ref("");

const cues = ref<TimelineCue[]>([]);
const slides = ref<TimelineSlide[]>([]);
const currentTime = ref(0);

const timelineItems = computed(() =>
  cues.value.map((c) => ({
    time: Math.floor(c.t_start),
    text: c.text,
  })),
);

const currentSubtitle = computed(() => {
  const t = currentTime.value;
  const hit = [...cues.value].reverse().find((c) => c.t_start <= t);
  return hit?.text || "暂无字幕";
});

const currentSlide = ref(1);

const bannerClass = computed(() => {
  if (dataSource.value === "failed") return "banner banner-fail";
  if (dataSource.value === "placeholder") return "banner banner-warn";
  if (dataSource.value === "fixture") return "banner banner-info";
  if (dataSource.value === "asr") return "banner banner-ok";
  return "banner";
});

function applyTimeline(tl: TimelineResponse) {
  apiStatus.value = tl.status;
  dataSource.value = tl.data_source || "";
  cues.value = tl.cues || [];
  slides.value = tl.slides || [];
  if (slides.value.length) {
    currentSlide.value = slides.value[0].page;
  }
  if (tl.data_source === "failed" || tl.status === "failed") {
    banner.value =
      tl.message ||
      "转写失败：当前无可用字幕。请检查录音是否有语音后重新上传。";
  } else if (tl.data_source === "placeholder" || tl.status === "placeholder") {
    banner.value =
      tl.message ||
      "演示占位字幕：尚未有真实转写结果。可点「加载 fixture」或等待任务完成。";
  } else if (tl.data_source === "fixture") {
    banner.value = "当前为 fixture 演示数据，非本场课真实转写。";
  } else if (tl.data_source === "asr") {
    banner.value = "已加载真实 ASR 时间轴。";
  } else {
    banner.value = tl.message || "";
  }
}

function play(time: number) {
  currentTime.value = time;
  const slide = [...slides.value].reverse().find((s) => s.t_start <= time);
  if (slide) currentSlide.value = slide.page;
}

function formatTime(time: number) {
  const m = Math.floor(time / 60);
  const s = time % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
}

async function loadTimeline(useFixtureFallback = true) {
  loading.value = true;
  error.value = "";
  try {
    let tl = await fetchTimeline(courseId.value);
    const failed = tl.status === "failed" || tl.data_source === "failed";
    // V-P0-3b: failed 态不自动灌入 fixture，避免「假成功」误导
    if (
      useFixtureFallback &&
      !failed &&
      (tl.status === "placeholder" || !tl.cues?.length)
    ) {
      tl = await loadTimelineFromFixture(courseId.value);
    }
    applyTimeline(tl);
    if (!cues.value.length && !failed) {
      error.value = tl.message || "timeline 仍为空";
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e);
  } finally {
    loading.value = false;
  }
}

async function ask() {
  if (!question.value.trim()) return;
  asking.value = true;
  error.value = "";
  try {
    const res = await askCourse(courseId.value, question.value.trim());
    answer.value = res.answer;
    sources.value = res.sources || [];
    question.value = "";
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e);
    answer.value = "请求失败";
  } finally {
    asking.value = false;
  }
}

onMounted(() => {
  void loadTimeline(true);
});
</script>

<template>
  <section>
    <h1>课程详情</h1>
    <p class="meta">
      course_id=<code>{{ courseId }}</code>
      · timeline=<code>{{ apiStatus || "…" }}</code>
      · source=<code>{{ dataSource || "…" }}</code>
      <button class="linkish" :disabled="loading" @click="loadTimeline(false)">
        {{ loading ? "加载中…" : "刷新 timeline" }}
      </button>
      <button class="linkish" :disabled="loading" @click="loadTimeline(true)">
        加载 fixture
      </button>
    </p>
    <p v-if="banner" :class="bannerClass">{{ banner }}</p>
    <p v-if="error" class="err">{{ error }}</p>

    <div class="layout">
      <div class="main">
        <div class="video-box">模拟视频播放区域</div>

        <h2>字幕</h2>
        <p>当前时间：{{ formatTime(currentTime) }}</p>
        <div class="subtitle">{{ currentSubtitle }}</div>

        <h2>时间轴</h2>
        <div
          v-for="item in timelineItems"
          :key="item.time + item.text"
          class="timeline-item"
          :class="{ activeTime: item.time === currentTime }"
          @click="play(item.time)"
        >
          {{ formatTime(item.time) }} - {{ item.text }}
        </div>
        <p v-if="!timelineItems.length" class="hint">
          无 cues。失败态不会自动灌入 fixture；可手动「加载 fixture」或等待 job。
        </p>
      </div>

      <div class="side">
        <h2>PPT</h2>
        <div
          v-for="slide in slides"
          :key="slide.page"
          class="slide"
          :class="{ active: currentSlide === slide.page }"
          @click="currentSlide = slide.page; currentTime = Math.floor(slide.t_start)"
        >
          第{{ slide.page }}页：{{ slide.title || "(无标题)" }}
        </div>
        <p v-if="!slides.length" class="hint">暂无 slides</p>

        <h2>问答</h2>
        <input v-model="question" placeholder="请输入问题" @keyup.enter="ask" />
        <button :disabled="asking" @click="ask">
          {{ asking ? "思考中..." : "提问" }}
        </button>
        <div class="answer">{{ answer }}</div>
        <ul v-if="sources.length" class="sources">
          <li v-for="(s, i) in sources" :key="i">{{ s }}</li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
.meta {
  color: #555;
  font-size: 0.9rem;
}
.meta code {
  background: #f3f4f6;
  padding: 0 4px;
}
.linkish {
  margin-left: 8px;
  border: none;
  background: transparent;
  color: #2563eb;
  cursor: pointer;
}
.banner {
  padding: 10px 12px;
  border-radius: 6px;
  font-size: 0.9rem;
}
.banner-fail {
  background: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}
.banner-warn {
  background: #fffbeb;
  color: #92400e;
  border: 1px solid #fde68a;
}
.banner-info {
  background: #eff6ff;
  color: #1e40af;
  border: 1px solid #bfdbfe;
}
.banner-ok {
  background: #f0fdf4;
  color: #166534;
  border: 1px solid #bbf7d0;
}
.err {
  color: #b91c1c;
}
.hint {
  color: #6b7280;
  font-size: 0.9rem;
}
.video-box {
  height: 200px;
  background: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
}
.subtitle {
  margin: 20px 0;
  padding: 20px;
  border: 1px solid #ddd;
}
.timeline-item {
  padding: 10px;
  cursor: pointer;
}
.timeline-item:hover {
  background: #f3f4f6;
}
.activeTime {
  background: #e0e7ff;
}
.layout {
  display: flex;
  gap: 30px;
}
.main {
  flex: 3;
}
.side {
  flex: 1;
  border-left: 1px solid #ddd;
  padding-left: 20px;
}
.slide {
  padding: 8px;
  cursor: pointer;
  border-radius: 4px;
}
.slide.active {
  background: #e0e7ff;
}
.answer {
  margin-top: 12px;
  padding: 12px;
  border: 1px solid #ddd;
  min-height: 4rem;
  white-space: pre-wrap;
}
.sources {
  font-size: 0.85rem;
  color: #4b5563;
}
input {
  width: 100%;
  margin-bottom: 8px;
  padding: 8px;
}
button {
  padding: 6px 12px;
}
</style>
