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
    path: "/user/:uid",
    name: "用户",
    component: () => import("../views/UserView.vue"),
  },
  {
    path: "/post",
    name: "帖子列表",
    component: () => import("../views/PostsView.vue"),
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
    path: "/user",
    name: "用户列表",
    component: () => import("../views/UsersView.vue"),
  },
  {
    path: "/jump",
    name: "跳转",
    component: () => import("../views/JumpView.vue"),
    meta: {
      hideHeader: true,
      hideFooter: true,
    },
  },
  {
    // 404 redircet
    path: "/:catchAll(.*)",
    name: "错误",
    component: () => import("../views/404View.vue"),
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
