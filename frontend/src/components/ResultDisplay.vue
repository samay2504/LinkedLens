<template>
  <div class="result-container">
    <div class="result-header">
      <span>Generated LinkedIn Post</span>
      <button @click="handleCopy" class="copy-button">
        📋 Copy to Clipboard
      </button>
    </div>
    
    <div class="result-content">
      <!-- LinkedIn Post -->
      <div class="post-text">{{ result.linkedin_post }}</div>
      
      <!-- Metadata -->
      <div class="metadata">
        <!-- Topic -->
        <div class="metadata-item">
          <div class="metadata-label">Topic</div>
          <div>{{ result.topic }}</div>
        </div>
        
        <!-- News Sources -->
        <div class="metadata-item" v-if="result.news_sources && result.news_sources.length > 0">
          <div class="metadata-label">News Sources</div>
          <ul class="sources-list">
            <li v-for="(source, index) in result.news_sources" :key="index">
              <a v-if="isValidUrl(source)" :href="source" target="_blank" rel="noopener noreferrer">
                {{ formatUrl(source) }}
              </a>
              <span v-else>{{ source }}</span>
            </li>
          </ul>
        </div>
        
        <!-- Image Suggestion -->
        <div class="metadata-item" v-if="result.image_suggestion">
          <div class="metadata-label">Suggested Image</div>
          <div>{{ result.image_suggestion }}</div>
        </div>
        
        <!-- Timestamp -->
        <div class="metadata-item">
          <div class="metadata-label">Generated At</div>
          <div>{{ formatDate(result.generated_at) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  result: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['copy']);

const handleCopy = () => {
  emit('copy', props.result.linkedin_post);
};

const isValidUrl = (string) => {
  try {
    new URL(string);
    return true;
  } catch (_) {
    return false;
  }
};

const formatUrl = (url) => {
  try {
    const urlObj = new URL(url);
    return urlObj.hostname + urlObj.pathname;
  } catch (_) {
    return url;
  }
};

const formatDate = (dateString) => {
  try {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (_) {
    return dateString;
  }
};
</script>
