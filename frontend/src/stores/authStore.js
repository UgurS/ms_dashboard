import { defineStore } from 'pinia'
import api, { setAccessToken, clearTokens } from '@/axiosInstance'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        userId: null,
        isAuthenticated: !!localStorage.getItem('access_token'),
        loading: false,
        error: null
    }),

    actions: {
        async login(username, password) {
            this.loading = true
            this.error = null
            try {
                const res = await api.post('/auth/login', { username, password })

                localStorage.setItem('refresh_token', res.data.refresh_token)
                setAccessToken(res.data.access_token)

                this.isAuthenticated = true
                // decode token if needed: this.userId = jwt_decode(res.data.access_token).sub
            } catch (err) {
                this.error = err.response?.data?.message || 'Login failed'
                this.isAuthenticated = false
                clearTokens()
            } finally {
                this.loading = false
            }
        },

        async logout() {
            try {
                const token = localStorage.getItem('refresh_token')
                if (token) {
                    await api.post('/auth/logout', { refresh_token: token })
                }
            } catch (_) {}

            clearTokens()
            this.isAuthenticated = false
            this.userId = null
        }
    }
})