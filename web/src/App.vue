<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <header class="bar">
    <strong>智学多模态 Agent</strong>
    <nav>
      <RouterLink to="/">首页</RouterLink>
    </nav>
  </header>
  <main class="main">
    <RouterView />
  </main>
</template>

<style scoped>
.bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.25rem;
  border-bottom: 1px solid #e5e7eb;
}
nav a {
  margin-left: 1rem;
  color: #2563eb;
  text-decoration: none;
}
.main {
  padding: 1.25rem;
  max-width: 960px;
  margin: 0 auto;
}
</style>
