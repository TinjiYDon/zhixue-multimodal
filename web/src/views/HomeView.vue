<script setup lang="ts">
import { onMounted, ref } from "vue";
import { fetchHealth, fetchCourses } from "@/api/client";

const health = ref<unknown>(null);
const courses = ref<Array<{ id: string; title: string }>>([]);
const error = ref<string | null>(null);
const loading = ref(false);

onMounted(async () => {
  try {
    health.value = await fetchHealth();
  } catch (e) {
    console.warn("health error:", e);
  }

  try {
  loading.value = true;
  courses.value = await fetchCourses();
} catch (e) {
  console.warn("courses api error:", e);

  courses.value = [
    {
      id: "001",
      title: "人工智能导论"
    },
    {
      id: "002",
      title: "机器学习基础"
    }
  ];
} finally {
  loading.value = false;
}
});
</script>

<template>
  <section>
    <h1>课程列表</h1>

    <h2>后端健康检查</h2>
    <pre v-if="health">{{ JSON.stringify(health, null, 2) }}</pre>
    <p v-if="error" class="err">{{ error }}</p>

    <h2>课程列表</h2>

<p v-if="loading">
  加载中...
</p>

<p v-else-if="courses.length === 0">
  暂无课程
</p>

<div v-else class="course-list">
  <div
    v-for="c in courses"
    :key="c.id"
    class="course-card"
  >
    <h3>{{ c.title }}</h3>

    <p>
      课程ID：{{ c.id }}
    </p>

    <router-link :to="`/course/${c.id}`">
  <button>
    进入课程
  </button>
</router-link>
  </div>
</div>
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
.course-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.course-card {
  width: 240px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background: white;
}

.course-card h3 {
  margin-top: 0;
}

button {
  padding: 8px 16px;
  cursor: pointer;
}
</style>
