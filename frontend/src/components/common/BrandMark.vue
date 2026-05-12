<template>
  <div class="brand-mark">
    <img class="brand-mark__logo" :src="logoUrl" alt="WhatStats" />

    <div>
      <div class="brand-mark__title">WhatStats</div>
      <div v-if="showSubtitle" class="brand-mark__subtitle">chat analytics</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import logoUrl from 'assets/logo.png';

withDefaults(
  defineProps<{
    showSubtitle?: boolean;
  }>(),
  {
    showSubtitle: true
  }
);
</script>

<style scoped lang="scss">
.brand-mark {
  display: inline-flex;
  align-items: center;
  min-width: 0;
  gap: 10px;
}

.brand-mark__logo {
  width: 44px;
  height: 44px;
  object-fit: contain;
  border-radius: 50%;
  box-shadow: var(--ws-brand-shadow);
}

.brand-mark__title {
  color: var(--ws-text);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: 0.98rem;
  font-weight: 700;
  line-height: 1.05;
}

.brand-mark__subtitle {
  margin-top: 1px;
  color: var(--ws-text-subtle);
  font-size: 0.72rem;
  line-height: 1.1;
}
</style>
