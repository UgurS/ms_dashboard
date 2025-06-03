<template>
  <div>
    <transition name="fade">
      <div v-if="showAddModal" class="fixed inset-0 z-50 bg-black/30 flex items-center justify-center">
        <div class="bg-white rounded-lg shadow-xl p-6 w-full max-w-md relative">
          <button
            @click="closeModal"
            class="absolute top-3 right-3 text-gray-400 hover:text-gray-600 focus:outline-none"
            aria-label="Close"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon" class="h-6 w-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12"></path>
            </svg>
          </button>
          <h2 class="text-lg font-semibold mb-4">Add New Patient</h2>
          <AddPatientForm
            @added="() => { patientStore.fetchPatients(); closeModal(); }"
          />
        </div>
      </div>
    </transition>

    <h1 class="text-2xl font-semibold text-gray-900 mb-2">Patients</h1>
    <p class="text-gray-600 mb-6">Manage all patient records, search through the list, and add new patients easily.</p>

    <div class="flex items-center justify-between mb-6">
      <div class="flex-1">
        <input
          v-model="search"
          type="text"
          placeholder="Search patients..."
          class="w-full max-w-xs px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        >
      </div>
      <div>
        <button
          @click="openModal"
          class="ml-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
        >
          Add New Patient
        </button>
      </div>
    </div>

    <div v-if="patientStore.loading" class="text-center text-gray-500">Loading...</div>
    <div v-else-if="patientStore.error" class="text-red-600 text-sm">{{ patientStore.error }}</div>
    <div v-else class="bg-white shadow rounded-lg overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Gender</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">DOB</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="patient in filteredPatients" :key="patient.id">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ patient.first_name }} {{ patient.last_name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ patient.gender }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ patient.date_of_birth }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
              <!-- Changed from a <button> to a <router-link> -->
              <router-link
                :to="{ path: `/patients/${patient.id}/diagnosis` }"
                class="text-indigo-600 hover:text-indigo-900"
              >
                New Diagnosis
              </router-link>
              <router-link
                :to="{ path: `/diagnosis/${patient.id}/report` }"
                class="text-gray-600 hover:text-gray-900"
              >
                History
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { usePatientStore } from '@/stores/patientStore'
import AddPatientForm from '@/components/patients/AddPatientForm.vue'

const patientStore = usePatientStore()
const search = ref('')
const showAddModal = ref(false)

onMounted(() => {
  patientStore.fetchPatients()
})

const filteredPatients = computed(() =>
  patientStore.patients.filter((p) => {
    const name = `${p.first_name} ${p.last_name}`.toLowerCase()
    return name.includes(search.value.toLowerCase())
  })
)

const openModal = () => {
  showAddModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
}
</script>
