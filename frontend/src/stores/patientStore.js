import { defineStore } from 'pinia'
import api from '@/axiosInstance'

export const usePatientStore = defineStore('patient', {
    state: () => ({
        patients: [],
        page: 1,
        total: 0,
        perPage: 10,
        loading: false,
        error: null
    }),

    actions: {
        async fetchPatients(page = 1) {
            this.loading = true
            this.error = null
            try {
                const res = await api.get(`/patients/?page=${page}&per_page=${this.perPage}`)
                this.patients = res.data.patients
                this.page = res.data.page
                this.total = res.data.total
            } catch (err) {
                this.error = err.response?.data?.message || 'Failed to load patients'
            } finally {
                this.loading = false
            }
        },

        async addPatient(patientData) {
            try {
                const res = await api.post('/patients/', patientData)
                this.patients.unshift(res.data)
            } catch (err) {
                throw new Error(err.response?.data?.message || 'Failed to add patient')
            }
        }
    }
})