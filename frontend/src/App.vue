<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navigation from './components/Navigation.vue'
</script>

<template>
  <div class="min-h-screen bg-secondary-50">
    <Navigation />
    <RouterView />
  </div>
</template>