import { createRouter, createWebHistory } from "vue-router";
import AdminVmPage from "@/pages/AdminVmPage.vue";
import LoginPage from "@/pages/LoginPage.vue";
import ProfilePage from "@/pages/ProfilePage.vue";
import RegisterPage from "@/pages/RegisterPage.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/login" },
    { path: "/register", component: RegisterPage, meta: { title: "Регистрация" } },
    { path: "/login", component: LoginPage, meta: { title: "Вход" } },
    { path: "/profile", component: ProfilePage, meta: { title: "Профиль" } },
    { path: "/admin/vm", component: AdminVmPage, meta: { title: "ВМ (админ)" } },
  ],
});

router.afterEach((to) => {
  const t = (to.meta.title as string) ?? "Citadel";
  document.title = t;
});

export default router;
