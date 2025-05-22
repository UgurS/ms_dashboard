<template>
    <div>
        <h1 class="text-2xl font-semibold text-gray-900 mb-6">History</h1>
        <p class="text-gray-600 mb-6">You are viewing the History section.</p>

        <div class="bg-white shadow rounded-lg overflow-hidden">
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
                    <tr v-for="record in historyRecords" :key="record.id">
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
import { ref } from "vue";

// Example data, replace with API call or store as needed
const historyRecords = ref([
    {
        id: 1,
        patient: "John Doe",
        date: "2024-05-01",
        diagnosis: "Condition A",
        confidence: "95%",
    },
    {
        id: 2,
        patient: "Jane Smith",
        date: "2024-05-02",
        diagnosis: "Condition B",
        confidence: "88%",
    },
    // Add more records as needed
]);

function viewReport(record) {
    // Placeholder for report logic
    alert(`Viewing report for ${record.patient}`);
}
</script>
