<template>
  <div class="newspaper-container">
    <header class="masthead">
      <h1 class="title">THE LINKEDIN POST GENERATOR</h1>
      <div class="subtitle">AI-Powered News to Professional Content</div>
    </header>

    <div class="content-wrapper">
      <!-- Input Section -->
      <section class="input-section">
        <label for="topic" class="label">TOPIC</label>
        <input
          id="topic"
          v-model="topic"
          type="text"
          placeholder="Enter a topic (e.g., Artificial Intelligence, Climate Change)"
          class="input-field"
          @keyup.enter="generatePost"
          :disabled="loading"
        />
        <button
          @click="generatePost"
          :disabled="loading || !topic.trim()"
          class="generate-button"
        >
          {{ loading ? 'GENERATING...' : 'GENERATE POST' }}
        </button>
      </section>

      <!-- Loading Spinner -->
      <LoadingSpinner v-if="loading" />

      <!-- Result Display -->
      <ResultDisplay
        v-if="result"
        :result="result"
        @copy="copyToClipboard"
      />

      <!-- Error Banner -->
      <div v-if="error" class="error-banner">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { generateLinkedInPost } from '../services/api';
import LoadingSpinner from './LoadingSpinner.vue';
import ResultDisplay from './ResultDisplay.vue';

const topic = ref('');
const loading = ref(false);
const result = ref(null);
const error = ref('');

const generatePost = async () => {
  if (!topic.value.trim()) return;

  loading.value = true;
  error.value = '';
  result.value = null;

  try {
    const response = await generateLinkedInPost(topic.value);
    result.value = response.data;
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to generate post. Please try again.';
    console.error('Generation error:', err);
  } finally {
    loading.value = false;
  }
};

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    alert('✅ Copied to clipboard!');
  } catch (err) {
    console.error('Failed to copy:', err);
    // Fallback for older browsers
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    try {
      document.execCommand('copy');
      alert('✅ Copied to clipboard!');
    } catch (e) {
      alert('❌ Failed to copy to clipboard');
    }
    document.body.removeChild(textArea);
  }
};
</script>
