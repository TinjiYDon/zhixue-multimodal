<script setup lang="ts">
import { onMounted, ref } from "vue";
import { fetchHealth, fetchCourses } from "@/api/client";

const health = ref<unknown>(null);
const courses = ref<Array<{ id: string; title: string }>>([]);
const error = ref<string | null>(null);

onMounted(async () => {
  try {
    health.value = await fetchHealth();
    courses.value = await fetchCourses();
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e);
  }
});
</script>

<template>
  <section>
    <h1>Web 端骨架</h1>
    <p>开发时请先启动后端 <code>uvicorn app.main:app --reload</code>，本页通过代理请求 <code>/api</code>。</p>

    <h2>后端健康检查</h2>
    <pre v-if="health">{{ JSON.stringify(health, null, 2) }}</pre>
    <p v-if="error" class="err">{{ error }}</p>

    <h2>课程列表（内存占位）</h2>
    <ul>
      <li v-for="c in courses" :key="c.id">{{ c.title }}（{{ c.id }}）</li>
    </ul>
  </section>
</template>

<style scoped>
.err {
  color: #b91c1c;
}
pre {
  background: #f3f4f6;
  padding: 0.75rem;
  overflow: auto;
}
code {
  background: #f3f4f6;
  padding: 0 0.25rem;
}
</style>
