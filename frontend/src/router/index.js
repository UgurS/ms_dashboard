// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import PatientsPage from "@/pages/PatientsPage.vue";
import HistoryPage from "@/pages/HistoryPage.vue";
import LoginPage from "@/pages/LoginPage.vue";
import DiagnosisPage from "@/pages/DiagnosisPage.vue";
import PatientHistory from "../pages/PatientHistory.vue";
import { createPinia, setActivePinia } from "pinia";
import { useAuthStore } from "@/stores/authStore";

setActivePinia(createPinia());

const routes = [
    { path: "/", redirect: "/patients" },
    { path: "/login", component: LoginPage },
    {
        path: "/patients",
        component: PatientsPage,
        meta: { requiresAuth: true },
    },
    {
        path: "/patients/:id/diagnosis",
        component: DiagnosisPage,
        props: true,
        meta: { requiresAuth: true },
    },
    {
        path: "/history",
        component: HistoryPage,
        meta: { requiresAuth: true },
    },
    {
        path: "/diagnosis/:id/report",
        name: "DiagnosisReport",
        component: () => import("@/pages/DiagnosisReportPage.vue"),
        meta: { requiresAuth: true },
    },
    {
        path: "/patient/:id/history",
        name: "PatientHistory",
        component: PatientHistory,
        meta: { requiresAuth: true },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to) => {
    const auth = useAuthStore();
    if (to.meta.requiresAuth && !auth.isAuthenticated) {
        return { path: "/login" };
    }
});

export default router;
