import axios from 'axios'

// Store access token in memory
let accessToken = localStorage.getItem('access_token') || null
const refreshToken = localStorage.getItem('refresh_token') || null

export const setAccessToken = (token) => {
    accessToken = token
    localStorage.setItem('access_token', token)
}

export const clearTokens = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    accessToken = null
}

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/api',
    headers: {
        'Content-Type': 'application/json'
    },
})

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => Promise.reject(error)
)

// Auto-refresh access token on 401
let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
    failedQueue.forEach((prom) => {
        if (error) prom.reject(error)
        else prom.resolve(token)
    })
    failedQueue = []
}

api.interceptors.response.use(
    (res) => res,
    async (error) => {
        const originalRequest = error.config

        if (
            error.response?.status === 401 &&
            !originalRequest._retry &&
            localStorage.getItem('refresh_token')
        ) {
            if (isRefreshing) {
                return new Promise(function (resolve, reject) {
                    failedQueue.push({ resolve, reject })
                })
                    .then((token) => {
                        originalRequest.headers.Authorization = 'Bearer ' + token
                        return api(originalRequest)
                    })
                    .catch((err) => Promise.reject(err))
            }

            originalRequest._retry = true
            isRefreshing = true

            try {
                const response = await axios.post(
                    `${import.meta.env.VITE_API_URL}/auth/refresh`,
                    {
                        refresh_token: localStorage.getItem('refresh_token'),
                    }
                )

                const newAccessToken = response.data.access_token
                const newRefreshToken = response.data.refresh_token

                setAccessToken(newAccessToken)
                localStorage.setItem('refresh_token', newRefreshToken)

                api.defaults.headers.Authorization = 'Bearer ' + newAccessToken
                originalRequest.headers.Authorization = 'Bearer ' + newAccessToken

                processQueue(null, newAccessToken)
                return api(originalRequest)
            } catch (err) {
                processQueue(err, null)
                clearTokens()
                window.location.href = '/login'
                return Promise.reject(err)
            } finally {
                isRefreshing = false
            }
        }

        return Promise.reject(error)
    }
)

export default api