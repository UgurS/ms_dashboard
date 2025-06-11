<template>
  <form @submit.prevent="submitForm" class="space-y-4 w-full max-w-md">
    <div>
      <label class="block text-sm font-medium text-gray-700">Patient Code</label>
      <input
          v-model="form.patient_code"
          type="text"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      />
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700">Gender</label>
      <select
          v-model="form.gender"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      >
        <option disabled value="">Select gender</option>
        <option>Male</option>
        <option>Female</option>
        <option>Other</option>
      </select>
    </div>


    <div class="text-right">
      <button
          type="submit"
          class="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700"
          :disabled="loading"
      >
        {{ loading ? 'Adding...' : 'Add Patient' }}
      </button>
    </div>

    <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
  </form>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { usePatientStore } from '@/stores/patientStore.js'

const emit = defineEmits(['added'])

const form = reactive({
  patient_code: '',
  gender: '',
})

const loading = ref(false)
const error = ref(null)

const patientStore = usePatientStore()

const submitForm = async () => {
  loading.value = true
  error.value = null
  try {
    await patientStore.addPatient(form)
    emit('added') // Notify parent to refresh
    form.patient_code = ''
    form.gender = ''
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>