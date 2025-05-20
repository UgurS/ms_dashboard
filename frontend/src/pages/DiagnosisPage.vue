<template>
  <div>
    <h1 class="text-2xl font-semibold text-gray-900 mb-6">Analysis</h1>

    <!-- Full Dropzone Container -->
    <div
        class="flex flex-wrap gap-4 p-4 border-2 border-dashed border-gray-400 rounded-lg bg-white cursor-pointer"
        @click="triggerFileInput"
        @dragover.prevent
        @drop.prevent="onDrop"
    >
      <!-- File Previews -->
      <div
          v-for="(file, index) in files"
          :key="index"
          class="flex items-center bg-gray-100 rounded-lg p-2 pr-4 space-x-4"
      >
        <img
            v-if="file.preview"
            :src="file.preview"
            class="w-16 h-16 object-cover rounded bg-gray-200"
        />
        <div class="text-gray-700">{{ file.name }}</div>
        <button @click.stop="removeFile(index)" class="text-gray-500 hover:text-red-500 text-xl">×</button>
      </div>

      <!-- If No Files -->
      <div v-if="files.length === 0" class="flex flex-col items-center justify-center w-full h-36 text-center text-gray-500">
        <svg class="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
        </svg>
        <p class="mb-2 text-sm text-gray-500 dark:text-gray-400"><span class="font-semibold">Click to upload sample(s)</span> or drag and drop</p>
      </div>

      <!-- Hidden File Input -->
      <input
          ref="fileInput"
          id="dropzone-file"
          type="file"
          class="hidden"
          accept="image/*"
          @change="onFileChange"
          multiple
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'DiagnosisPage',
  data() {
    return {
      files: []
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    onFileChange(event) {
      const selected = Array.from(event.target.files);
      selected.forEach(file => this.addFile(file));
      event.target.value = ''; // clear input so same file can be reselected
    },
    onDrop(event) {
      const dropped = Array.from(event.dataTransfer.files);
      dropped.forEach(file => this.addFile(file));
    },
    addFile(file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.files.push({
          name: file.name,
          preview: e.target.result,
          raw: file
        });
      };
      reader.readAsDataURL(file);
    },
    removeFile(index) {
      this.files.splice(index, 1);
    }
  }
};
</script>
