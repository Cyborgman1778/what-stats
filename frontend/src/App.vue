<template>
  <router-view />
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useNativeZipImport } from 'src/composables/useNativeZipImport';
import { usePreferencesStore } from './stores/preferences-store';

const preferencesStore = usePreferencesStore();
const { initNativeZipImport } = useNativeZipImport();

preferencesStore.initPreferences();

onMounted(() => {
  void initNativeZipImport();
});
</script>
