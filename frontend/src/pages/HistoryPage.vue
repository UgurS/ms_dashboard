<template>
    <div>
        <h1 class="text-2xl font-semibold text-gray-900 mb-6">History</h1>
        <p class="text-gray-600 mb-6">You are viewing the History section.</p>

        <div
            v-if="diagnosisStore.loadingHistory"
            class="p-4 text-center text-gray-500"
        >
            Loading history...
        </div>
        <div
            v-else-if="diagnosisStore.historyError"
            class="p-4 text-center text-red-500"
        >
            {{ diagnosisStore.historyError }}
        </div>
        <div v-else class="bg-white shadow rounded-lg overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th
                            class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                            Patient
                        </th>
                        <th
                            class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                            Date
                        </th>
                        <th
                            class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                            Diagnosis
                        </th>
                        <th
                            class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                            Confidence
                        </th>
                        <th class="px-4 py-2"></th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-if="diagnosisStore.historyRecords.length === 0">
                        <td colspan="5" class="text-center py-6 text-gray-500">
                            No Results Found
                        </td>
                    </tr>
                    <tr
                        v-else
                        v-for="record in diagnosisStore.historyRecords"
                        :key="record.id"
                    >
                        <td
                            class="px-4 py-2 whitespace-nowrap text-sm text-gray-900"
                        >
                            {{ record.patient }}
                        </td>
                        <td
                            class="px-4 py-2 whitespace-nowrap text-sm text-gray-900"
                        >
                            {{ record.date }}
                        </td>
                        <td
                            class="px-4 py-2 whitespace-nowrap text-sm text-gray-900"
                        >
                            {{ record.diagnosis }}
                        </td>
                        <td
                            class="px-4 py-2 whitespace-nowrap text-sm text-gray-900"
                        >
                            {{ record.confidence }}
                        </td>
                        <td
                            class="px-4 py-2 whitespace-nowrap text-sm text-gray-900 text-right"
                        >
                            <button
                                class="ml-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
                                @click="viewReport(record)"
                            >
                                Report
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useDiagnosisStore } from "../stores/diagnosisStore";
import router from "@/router/index.js";

const diagnosisStore = useDiagnosisStore();

onMounted(() => {
    diagnosisStore.fetchHistoryRecords();
});

function viewReport(record) {
  router.push({ name: "DiagnosisReport", params: { id: record.id } });
}
</script>
