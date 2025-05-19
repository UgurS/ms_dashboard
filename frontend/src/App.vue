<template>
  <div class="flex h-screen">
    <!-- Sidebar -->
    <div
        v-if="!isLoginPage"
        class="flex flex-col w-64 border-r border-gray-200 bg-white"
    >
      <div class="flex items-center h-16 pl-4 pr-8 mt-6">
        <img class="h-8 w-auto" src="./assets/logo.svg" alt="RR Mechatronics">
      </div>
      <nav class="flex-1 overflow-y-auto px-2 py-4">
        <ul class="space-y-1">
          <li>
            <router-link to="/patients" class="group flex items-center px-2 py-3 text-sm font-medium rounded-md" :class="isActive('/patients')">
              <svg class="mr-3 h-5 w-5"
                   :class="isActive('/patients', true)"
                   fill="currentColor" aria-hidden="true"
                   xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M160 32c0-17.7 14.3-32 32-32l32 0c17.7 0 32 14.3 32 32c17.7 0 32 14.3 32 32l0 224c0 17.7-14.3 32-32 32c0 17.7-14.3 32-32 32l-32 0c-17.7 0-32-14.3-32-32c-17.7 0-32-14.3-32-32l0-224c0-17.7 14.3-32 32-32zM32 448l288 0c70.7 0 128-57.3 128-128s-57.3-128-128-128l0-64c106 0 192 86 192 192c0 49.2-18.5 94-48.9 128l16.9 0c17.7 0 32 14.3 32 32s-14.3 32-32 32l-160 0L32 512c-17.7 0-32-14.3-32-32s14.3-32 32-32zm80-64l192 0c8.8 0 16 7.2 16 16s-7.2 16-16 16l-192 0c-8.8 0-16-7.2-16-16s7.2-16 16-16z"/></svg>
              Patients
            </router-link>
          </li>
          <li>
            <router-link to="/history" class="group flex items-center px-2 py-3 text-sm font-medium rounded-md" :class="isActive('/history')">
              <svg class="mr-3 h-5 w-5"
                   :class="isActive('/history', true)"
                   fill="currentColor" aria-hidden="true"
                   xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M75 75L41 41C25.9 25.9 0 36.6 0 57.9L0 168c0 13.3 10.7 24 24 24l110.1 0c21.4 0 32.1-25.9 17-41l-30.8-30.8C155 85.5 203 64 256 64c106 0 192 86 192 192s-86 192-192 192c-40.8 0-78.6-12.7-109.7-34.4c-14.5-10.1-34.4-6.6-44.6 7.9s-6.6 34.4 7.9 44.6C151.2 495 201.7 512 256 512c141.4 0 256-114.6 256-256S397.4 0 256 0C185.3 0 121.3 28.7 75 75zm181 53c-13.3 0-24 10.7-24 24l0 104c0 6.4 2.5 12.5 7 17l72 72c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9l-65-65 0-94.1c0-13.3-10.7-24-24-24z"/></svg>
              History
            </router-link>
          </li>
        </ul>
      </nav>
    </div>

    <!-- Main Content -->
    <div
        :class="[
        isLoginPage ? 'w-full' : 'flex-1',
        'bg-gray-50 p-8 overflow-y-auto'
      ]"
    >
      <router-view />
    </div>
  </div>
</template>

<script>
import { useRoute } from 'vue-router'
import {computed} from "vue";

export default {
  setup() {
    const route = useRoute()

    const isLoginPage = computed(() => route.path === '/login')
    const isActive = (path, icon = false) => {
      if (route.path === path) {
        return icon ? 'text-indigo-600' : 'bg-gray-100 text-indigo-600'
      } else {
        return icon ? 'text-gray-400 group-hover:text-gray-500' : 'text-gray-700 hover:text-gray-900 hover:bg-gray-100'
      }
    }

    return { isLoginPage, isActive }
  }
}
</script>
