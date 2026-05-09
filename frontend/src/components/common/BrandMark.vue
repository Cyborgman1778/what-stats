<template>
  <div class="brand-mark">
    <div class="brand-mark__glyph" aria-hidden="true">
      <span />
    </div>

    <div>
      <div class="brand-mark__title">WhatStats</div>
      <div v-if="showSubtitle" class="brand-mark__subtitle">chat analytics</div>
    </div>
  </div>
</template>

<script setup lang="ts">
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

.brand-mark__glyph {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  color: white;
  background: var(--ws-text);
  border-radius: 50%;
}

.brand-mark__glyph span {
  width: 13px;
  height: 13px;
  border: 2px solid var(--ws-canvas);
  border-top-color: transparent;
  border-radius: 50%;
}

.brand-mark__title {
  color: var(--ws-text);
  font-size: 0.98rem;
  font-weight: 700;
  line-height: 1.05;
}

.brand-mark__subtitle {
  margin-top: 1px;
  color: var(--ws-text-muted);
  font-size: 0.72rem;
  line-height: 1.1;
}
</style>
