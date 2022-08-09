import { createRouter, createWebHashHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "主页",
    component: HomeView,
  },
  {
    path: "/login",
    name: "登录",
    component: () => import("../views/LoginView.vue"),
  },
  {
    path: "/register",
    name: "注册",
    component: () => import("../views/RegisterView.vue"),
  },
  {
    path: "/my",
    name: '"我"',
    component: () => import("../views/MyView.vue"),
  },
  {
    path: "/post/:pid",
    name: "帖子",
    component: () => import("../views/ReadPostView.vue"),
  },
  {
    path: "/post/write",
    name: "发布",
    component: () => import("../views/PostView.vue"),
  },
  {
    path: "/mics/reload",
    name: "重新加载",
    component: () => import("../views/ReloadView.vue"),
  },
  {
    path: "/help",
    name: "帮助",
    component: () => import("../views/HelpView.vue"),
  },
  {
    path: "/error/404",
    name: "错误",
    component: () => import("../views/404View.vue"),
  },
  {
    // 404 redircet
    path: "/:catchAll(.*)",
    // name:'错误',
    redirect: "/error/404",
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
