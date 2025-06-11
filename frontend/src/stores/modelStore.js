import { defineStore } from "pinia";
import api from "@/axiosInstance";

export const useModelStore = defineStore("model", {
    state: () => ({
        models: [],
        loading: false,
        error: null,
    }),

    actions: {
        async fetchModels() {
            this.loading = true;
            this.error = null;
            try {
                const res = await api.get("/models/");
                this.models = res.data;
            } catch (err) {
                this.error =
                    err.response?.data?.message || "Failed to load models.";
            } finally {
                this.loading = false;
            }
        },
        getDisplayNameByModelName(modelName) {
            const model = this.models.find((m) => m.model_name === modelName);
            return model ? model.display_name : null;
        },
    },
});