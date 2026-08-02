import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import CourseView from "@/views/CourseView.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
  {
    path: "/",
    name: "home",
    component: HomeView
  },
  {
    path: "/course/:id",
    name: "course",
    component: CourseView
  }
],
});
