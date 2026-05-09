<template>
  <router-view />
</template>

<script setup lang="ts">
import { usePreferencesStore } from './stores/preferences-store';

const preferencesStore = usePreferencesStore();
preferencesStore.initPreferences();
</script>