import { defineStore } from "pinia";
import api from "../axiosInstance";

export const useDiagnosisStore = defineStore("diagnosis", {
    state: () => ({
        historyRecords: [],
        page: 1,
        perPage: 10,
        total: 0,
        pages: 0,
        loadingHistory: false,
        historyError: null,
    }),
    actions: {
        async fetchHistoryRecords(page = 1) {
            this.loadingHistory = true;
            this.historyError = null;
            try {
                const response = await api.get(
                    `/diagnoses/?page=${page}&per_page=${this.perPage}`
                );
                this.historyRecords = response.data.diagnoses;
                this.page = response.data.page;
                this.perPage = response.data.per_page;
                this.total = response.data.total;
                this.pages = response.data.pages;
            } catch (err) {
                this.historyError =
                    err.response?.data?.message ||
                    err.message ||
                    "Failed to fetch history records.";
            } finally {
                this.loadingHistory = false;
            }
        },
        setPage(page) {
            this.page = page;
            this.fetchHistoryRecords(page);
        },
    },
});
