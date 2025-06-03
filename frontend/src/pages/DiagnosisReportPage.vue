<template>
  <div class="max-w-4xl mx-auto px-6 py-10">
    <h1 class="text-2xl font-bold text-gray-800 mb-4">Diagnosis Report</h1>

    <div v-if="loading" class="text-gray-500">Loading report...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else class="bg-white rounded-lg shadow p-6">
      <p class="mb-2"><strong>Patient:</strong> {{ report.patient_name }}</p>
      <p class="mb-2"><strong>Prediction:</strong>
        <span :class="report.prediction === 'MSP' ? 'text-red-600' : 'text-green-600'"> {{ report.prediction }}</span>
      </p>
      <p class="mb-2"><strong>Confidence:</strong> {{ (report.confidence * 100).toFixed(1) }}%</p>
      <p class="mb-4"><strong>Model Used:</strong> {{ report.model_used }}</p>

      <div v-if="report.heatmap_base64">
        <p class="font-medium mb-1">Heatmap:</p>
        <img
            :src="`data:image/png;base64,${report.heatmap_base64}`"
            alt="Heatmap"
            class="w-full h-auto rounded-md border"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import {useDiagnosisStore} from "@/stores/diagnosisStore.js";
const diagnosisStore = useDiagnosisStore();

const route = useRoute();
const report = ref(null);
const loading = ref(true);
const error = ref("");

onMounted(async () => {
  try {
    const data = await diagnosisStore.getDiagnosisById(route.params.id);
    report.value = data;
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});
</script>