import { defineStore } from "pinia";
import api from "../axiosInstance";

export const useDiagnosisStore = defineStore("diagnosis", {
    state: () => ({
        // …history-related state…
        historyRecords: [],
        page: 1,
        perPage: 10,
        total: 0,
        pages: 0,
        loadingHistory: false,
        historyError: null,

        // New for “run diagnosis”
        currentResult: null, // holds { prediction, confidence, heatmap_base64 }
        loadingDiagnosis: false,
        diagnosisError: null,
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

        // ----------------------
        // runDiagnosis(formData)
        // ----------------------
        async runDiagnosis(formData) {
            this.loadingDiagnosis = true;
            this.diagnosisError = null;
            this.currentResult = null;
            try {
                // POST to /api/diagnoses with exactly one file: field name “image”
                const response = await api.post("/diagnoses", formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                });
                // The Flask route returns:
                // { "prediction": "MS", "confidence": 0.80, "heatmap_base64": "..." }
                this.currentResult = response.data;
            } catch (err) {
                // If Flask returned { "error": "Missing image" }, err.response.data.error holds that
                this.diagnosisError =
                    err.response?.data?.error ||
                    err.response?.data?.message ||
                    err.message ||
                    "Failed to run diagnosis.";
            } finally {
                this.loadingDiagnosis = false;
            }
        },
        async getDiagnosisById(id) {
            try {
                const response = await api.get(`/diagnoses/${id}`);
                return response.data;
            } catch (err) {
                throw new Error(
                    err.response?.data?.error ||
                        err.response?.data?.message ||
                        err.message ||
                        "Failed to fetch diagnosis report."
                );
            }
        },
        async getDiagnosesForPatient(id, page = 1, perPage = 10) {
            try {
                const response = await api.get(
                    `/diagnoses/patient/${id}?page=${page}&per_page=${perPage}`
                );
                return response.data;
            } catch (err) {
                throw new Error(
                    err.response?.data?.error ||
                        err.response?.data?.message ||
                        err.message ||
                        "Failed to fetch diagnoses for patient."
                );
            }
        },
    },
});
