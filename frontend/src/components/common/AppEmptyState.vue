<template>
  <q-card flat class="premium-card empty-state">
    <q-card-section class="text-center">
      <q-icon :name="icon" size="44px" class="empty-state__icon" />

      <h2 class="empty-state__title">{{ title }}</h2>
      <p class="empty-state__message">{{ message }}</p>

      <div v-if="$slots.default" class="q-mt-lg">
        <slot />
      </div>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    icon?: string;
    title: string;
    message: string;
  }>(),
  {
    icon: 'inbox'
  }
);
</script>

<style scoped lang="scss">
.empty-state {
  max-width: 680px;
  margin: 0 auto;
  padding: 28px 16px;
}

.empty-state__icon {
  color: var(--ws-text-subtle);
}

.empty-state__title {
  margin: 18px 0 8px;
  font-size: clamp(1.4rem, 2.5vw, 2rem);
  font-weight: 700;
}

.empty-state__message {
  max-width: 520px;
  margin: 0 auto;
  color: var(--ws-text-muted);
  line-height: 1.55;
}
</style>
