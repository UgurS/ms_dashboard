<template>
  <div class="flex items-center justify-between border-t border-gray-200 py-3 px-2">
    <!-- Mobile view -->
    <div class="flex flex-1 justify-between sm:hidden">
      <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Previous
      </button>
      <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Next
      </button>
    </div>

    <!-- Desktop view -->
    <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
      <div>
        <p class="text-sm text-gray-700">
          Showing
          <span class="font-medium">{{ startItem }}</span>
          to
          <span class="font-medium">{{ endItem }}</span>
          of
          <span class="font-medium">{{ totalItems }}</span>
          results
        </p>
      </div>
      <div>
        <nav class="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
          <button
              @click="goToPage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="relative inline-flex items-center rounded-l-md border border-gray-300 bg-white px-2 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span class="sr-only">Previous</span>
            &laquo;
          </button>

          <template v-for="page in displayPages" :key="page">
            <span
                v-if="page === '...'"
                class="relative inline-flex items-center px-4 py-2 text-sm font-medium text-gray-500"
            >
              ...
            </span>
            <button
                v-else
                @click="goToPage(page)"
                :class="[
                'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                page === currentPage
                  ? 'z-10 bg-indigo-600 border-indigo-600 text-white'
                  : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
              ]"
            >
              {{ page }}
            </button>
          </template>

          <button
              @click="goToPage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="relative inline-flex items-center rounded-r-md border border-gray-300 bg-white px-2 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span class="sr-only">Next</span>
            &raquo;
          </button>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps } from "vue";

const {
  currentPage,
  totalPages,
  totalItems,
  perPage
} = defineProps({
  currentPage: Number,
  totalPages: Number,
  totalItems: Number,
  perPage: Number
});

const emit = defineEmits(["page-change"]);

const displayPages = computed(() => {
  const pages = [];
  const maxShown = 5;

  if (totalPages <= maxShown) {
    for (let i = 1; i <= totalPages; i++) pages.push(i);
  } else {
    if (currentPage <= 3) {
      pages.push(1, 2, 3, '...', totalPages);
    } else if (currentPage >= totalPages - 2) {
      pages.push(1, '...', totalPages - 2, totalPages - 1, totalPages);
    } else {
      pages.push(1, '...', currentPage - 1, currentPage, currentPage + 1, '...', totalPages);
    }
  }

  return pages;
});

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages) {
    emit("page-change", page);
  }
};

const startItem = computed(() => (currentPage - 1) * perPage + 1);
const endItem = computed(() =>
  Math.min(currentPage * perPage, totalItems)
);
const pages = computed(() => {
  const range = [];
  for (let i = 1; i <= totalPages; i++) {
    range.push(i);
  }
  return range;
});
</script>