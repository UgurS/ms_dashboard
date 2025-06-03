<!-- src/pages/DiagnosisPage.vue -->
<template>
  <div class="px-6 py-8 max-w-4xl mx-auto">
    <!-- 1) HEADER & GREETING -->
    <div class="flex items-center mb-4">
      <svg class="mr-3 h-5 w-5" fill="currentColor" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M160 32c0-17.7 14.3-32 32-32l32 0c17.7 0 32 14.3 32 32c17.7 0 32 14.3 32 32l0 224c0 17.7-14.3 32-32 32c0 17.7-14.3 32-32 32l-32 0c-17.7 0-32-14.3-32-32c-17.7 0-32-14.3-32-32l0-224c0-17.7 14.3-32 32-32zM32 448l288 0c70.7 0 128-57.3 128-128s-57.3-128-128-128l0-64c106 0 192 86 192 192c0 49.2-18.5 94-48.9 128l16.9 0c17.7 0 32 14.3 32 32s-14.3 32-32 32l-160 0L32 512c-17.7 0-32-14.3-32-32s14.3-32 32-32zm80-64l192 0c8.8 0 16 7.2 16 16s-7.2 16-16 16l-192 0c-8.8 0-16-7.2-16-16s7.2-16 16-16z"></path></svg>
      <span class="text-gray-800 font-medium text-lg">{{ patientName }}</span>
    </div>
    <p class="text-gray-600 mb-6">
      You may upload one or more microscopic images of the patient’s red blood cell sample(s).
    </p>

    <!-- 2) DROPZONE & MODEL SELECTOR (only shown if no results yet) -->
    <div v-if="!hasResults">
      <!-- 2a) DROPZONE -->
      <div
        class="border-2 border-dashed border-gray-300 rounded-lg p-6 mb-4 relative"
        @click="triggerFileInput"
        @dragover.prevent
        @drop.prevent="handleDrop"
      >
        <div v-if="files.length > 0" class="flex flex-wrap gap-3">
          <div
            v-for="(f, idx) in files"
            :key="idx"
            class="flex items-center bg-gray-100 rounded-lg px-3 py-2 space-x-2"
          >
            <img
              v-if="f.preview"
              :src="f.preview"
              class="w-14 h-14 object-cover rounded bg-gray-200"
            />
            <span class="text-gray-700 text-sm truncate max-w-xs">{{ f.name }}</span>
            <button
              @click.stop="removeFile(idx)"
              class="text-gray-500 hover:text-red-500"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <div v-if="files.length === 0" class="h-32 flex flex-col items-center justify-center text-gray-400">
          <svg class="w-8 h-8 mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 
                 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 
                 5.021C5.137 5.017 5.071 5 5 5a4 4 
                 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 
                 2 2"
            />
          </svg>
          <p class="text-sm">
            <span class="font-semibold">Upload Sample(s)</span>
          </p>
        </div>

        <input
          ref="fileInput"
          type="file"
          class="hidden"
          accept="image/*"
          multiple
          @change="onFileChange"
        />
      </div>

      <!-- 2b) MODEL SELECTOR + RUN BUTTON -->
      <div class="flex items-center mb-6">
        <div>
          <label for="modelSelect" class="block text-sm font-medium text-gray-700 mb-1">
            Model
          </label>
          <select
            id="modelSelect"
            v-model="selectedModel"
            class="border border-transparent border-r-8 outline outline-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-indigo-500 focus:outline-indigo-500"
          >
            <option v-for="model in models" :key="model" :value="model">
              {{ model }}
            </option>
          </select>
        </div>

        <div class="ml-auto">
          <button
            @click="submitDiagnosis"
            :disabled="files.length === 0 || loadingDiagnosis"
            class="inline-flex items-center gap-2 px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-md shadow-sm hover:bg-green-700 disabled:opacity-50"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 4V12C6 12.663 6.26339 13.2989 6.73223 13.7678C7.20107 14.2366 7.83696 14.5 8.5 14.5H15V12C15 11.5956 15.2436 11.2309 15.6173 11.0761C15.991 10.9214 16.4211 11.0069 16.7071 11.2929L20.7071 15.2929C21.0976 15.6834 21.0976 16.3166 20.7071 16.7071L16.7071 20.7071C16.4211 20.9931 15.991 21.0787 15.6173 20.9239C15.2436 20.7691 15 20.4045 15 20V17.5H8.5C7.04131 17.5 5.64236 16.9205 4.61091 15.8891C3.57946 14.8576 3 13.4587 3 12V4C3 3.44772 3.44772 3 4 3H5C5.55228 3 6 3.44772 6 4Z" fill="#fff"/>
            </svg>
            Run Diagnosis
          </button>
        </div>
      </div>

      <!-- 2c) LOADING / ERROR  -->
      <div v-if="loadingDiagnosis" class="text-center text-gray-500 mb-4">
        Diagnosing… please wait.
      </div>
      <div v-else-if="diagnosisError" class="text-red-500 text-sm mb-4">
        {{ diagnosisError }}
      </div>
    </div>

    <!-- 3) RESULTS SECTION (only shown if we have at least one result) -->
    <div v-if="hasResults" class="mb-6">
      <!-- 3a) OVERALL SUMMARY -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-semibold mb-2">Results</h2>
        <p class="text-gray-800">
          The model determined that the given sample(s) are
          <span :class="overallPrediction === 'MSP' ? 'text-red-600' : 'text-green-600'">
            {{ overallPrediction === 'MSP' ? 'likely to be MS' : 'not likely to be MS' }}
          </span>
          with overall confidence <strong>{{ (overallConfidence * 100).toFixed(1) }}%</strong>.
        </p>
      </div>

      <!-- 3b) PER-IMAGE ANALYSIS -->
      <div v-for="(r, idx) in results" :key="idx" class="bg-white rounded-lg shadow p-6 mb-6">
        <h3 class="text-lg font-semibold mb-1">Analysis of {{ r.filename }}</h3>
        <p class="text-gray-800 mb-2">
          <strong>Result:</strong>
          <span :class="r.prediction === 'MSP' ? 'text-red-600' : 'text-green-600'">
            {{ r.prediction }}
          </span>
        </p>
        <p class="text-gray-800 mb-4"><strong>Confidence:</strong> {{ (r.confidence * 100).toFixed(0) }}%</p>
        <div>
          <p class="font-medium mb-1">Heatmap:</p>
          <img
            v-if="r.heatmap_base64"
            :src="`data:image/png;base64,${r.heatmap_base64}`"
            alt="Heatmap"
            class="w-full h-auto rounded-md border"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useDiagnosisStore } from "@/stores/diagnosisStore";
import { usePatientStore } from "@/stores/patientStore";
import { useRoute } from "vue-router";

const diagnosisStore = useDiagnosisStore();
const patientStore = usePatientStore();
const route = useRoute();

const patientId = route.params.id;

// Step A: fetch the patient name so we can display it in the header
const patientName = ref("Unknown Patient");
onMounted(async () => {
  await patientStore.fetchPatients();
  const p = patientStore.patients.find((x) => String(x.id) === String(patientId));
  if (p) patientName.value = `${p.first_name} ${p.last_name}`;
});

// Step B: local state for files + model selector
const files = ref([]);
const selectedModel = ref("MobileNet-V2");
const models = ["MobileNet-V2", "ResNet-50", "Inception-V3"];

// Step C: store results in this component (instead of redirecting)
const results = ref([]);
// “hasResults” is true once we have at least one entry in results[]
const hasResults = computed(() => results.value.length > 0);

// Step D: loading+error while running multiple calls
const loadingDiagnosis = ref(false);
const diagnosisError = ref("");

// Once we’ve gathered individual results, compute “overall” (simple average)
const overallConfidence = computed(() => {
  if (!results.value.length) return 0;
  const sum = results.value.reduce((acc, r) => acc + r.confidence, 0);
  return sum / results.value.length;
});
// If more than half the images say “MS” (or you prefer: if average confidence is closer to MS),
// pick “MS,” otherwise “No MS.” Here’s a simple rule: if majority of predictions are “MS” → overall is MS
const overallPrediction = computed(() => {
  if (!results.value.length) return "";
  const msCount = results.value.filter((r) => r.prediction === "MSP").length;
  return msCount >= results.value.length / 2 ? "MS" : "No MS";
});

// __________________________________________
// DROPZONE HANDLERS
// __________________________________________
const fileInput = ref(null);

function triggerFileInput() {
  fileInput.value.click();
}

function onFileChange(e) {
  const selected = Array.from(e.target.files);
  selected.forEach((f) => addFile(f));
  e.target.value = "";
}

function handleDrop(e) {
  const dropped = Array.from(e.dataTransfer.files);
  dropped.forEach((f) => addFile(f));
}

function addFile(file) {
  const reader = new FileReader();
  reader.onload = (ev) => {
    files.value.push({
      name: file.name,
      preview: ev.target.result,
      raw: file,
    });
  };
  reader.readAsDataURL(file);
}

function removeFile(index) {
  files.value.splice(index, 1);
}

// __________________________________________
// SUBMIT DIAGNOSIS (calls backend once per file)
// __________________________________________
async function submitDiagnosis() {
  if (files.value.length === 0) return;

  // Clear any previous results + errors
  results.value = [];
  diagnosisError.value = "";
  loadingDiagnosis.value = true;

  try {
    // Loop through all selected files one by one
    for (let f of files.value) {
      const formData = new FormData();

      // 1) Append the single file under “image”
      formData.append("image", f.raw);

      // 2) Append model name
      formData.append("model_used", selectedModel.value);

      // 3) Append patient ID
      formData.append("patient_id", patientId);

      // Call the backend
      const resp = await diagnosisStore.runDiagnosis(formData);
      // runDiagnosis sets `diagnosisStore.currentResult` to whatever JSON came back.
      // We’ll grab it immediately and push into our local array:
      if (diagnosisStore.currentResult) {
        results.value.push({
          filename: f.name,
          prediction: diagnosisStore.currentResult.prediction,
          confidence: diagnosisStore.currentResult.confidence,
          heatmap_base64: diagnosisStore.currentResult.heatmap_base64,
        });
      } else {
        throw new Error("No result returned for " + f.name);
      }
    }
  } catch (err) {
    // On any failure, record the error and stop everything
    diagnosisError.value = err.message || "Failed to run diagnosis.";
  } finally {
    loadingDiagnosis.value = false;
  }
}
</script>

<style>
/* No custom CSS—using Tailwind classes throughout */
</style>
