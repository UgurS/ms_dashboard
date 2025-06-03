<template>
    <div>
        <h1 class="text-2xl font-semibold text-gray-900 mb-6">
            <span v-if="patientName">{{ patientName }}</span>
            <span v-else>Loading...</span>
        </h1>

        <p class="text-gray-600 mb-6">
            You are viewing the diagnosis report for this patient.
        </p>

        <div v-if="loading" class="p-4 text-center text-gray-500">
            Loading...
        </div>
        <div v-else-if="error" class="p-4 text-center text-red-500">
            {{ error }}
        </div>
        <div v-else class="bg-white shadow rounded-lg overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th
                            class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                            Date
                        </th>
                        <th
                            class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                            Patient
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
                        <th
                            class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                            Model Used
                        </th>
                        <th class="px-4 py-2"></th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-if="diagnoses.length === 0">
                        <td colspan="6" class="text-center py-6 text-gray-500">
                            No Results Found
                        </td>
                    </tr>
                    <tr v-else v-for="record in diagnoses" :key="record.id">
                        <td
                            class="px-4 py-2 whitespace-nowrap text-sm text-gray-900"
                        >
                            {{ record.date }}
                        </td>
                        <td
                            class="px-4 py-2 whitespace-nowrap text-sm text-gray-900"
                        >
                            {{ record.patient }}
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
                            class="px-4 py-2 whitespace-nowrap text-sm text-gray-900"
                        >
                            {{ record.model_used }}
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
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useDiagnosisStore } from "@/stores/diagnosisStore.js";
import { usePatientStore } from "@/stores/patientStore.js";
const diagnosisStore = useDiagnosisStore();
const patientStore = usePatientStore();
const route = useRoute();
const router = useRouter();
const diagnoses = ref([]);
const loading = ref(true);
const error = ref("");
const patientName = ref("Unknown Patient");

function viewReport(record) {
    router.push({ name: "DiagnosisReport", params: { id: record.id } });
}

onMounted(async () => {
    try {
        await patientStore.fetchPatients();
        const p = patientStore.patients.find(
            (x) => String(x.id) === String(route.params.id)
        );
        if (p) patientName.value = `${p.first_name} ${p.last_name}`;
        // Fetch all diagnoses for this patient (route.params.id)
        const data = await diagnosisStore.getDiagnosesForPatient(
            route.params.id
        );
        diagnoses.value = data.diagnoses;
    } catch (err) {
        error.value = err.message;
    } finally {
        loading.value = false;
    }
});
</script>
