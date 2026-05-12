<template>
  <q-card flat class="section-card">
    <q-card-section class="section-card__header">
      <div>
        <h2 class="section-card__title">{{ title }}</h2>
        <p v-if="subtitle" class="section-card__subtitle">{{ subtitle }}</p>
      </div>

      <div v-if="$slots.actions" class="section-card__actions">
        <slot name="actions" />
      </div>
    </q-card-section>

    <q-separator />

    <q-card-section class="section-card__body">
      <slot />
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
  subtitle?: string;
}>();
</script>

<style scoped lang="scss">
.section-card {
  overflow: hidden;
  background: var(--ws-section-card-background);
  border: 1px solid var(--ws-border);
  border-radius: var(--ws-radius);
  box-shadow: var(--ws-shadow);
  backdrop-filter: blur(18px);
}

.section-card__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding-top: 14px;
  padding-bottom: 14px;
}

.section-card__title {
  margin: 0;
  color: var(--ws-text);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: 1rem;
  font-weight: 700;
}

.section-card__subtitle {
  margin: 5px 0 0;
  color: var(--ws-text-muted);
  font-size: 0.86rem;
}

.section-card__actions {
  flex: 0 0 auto;
}

.section-card__body {
  min-width: 0;
  overflow: hidden;
}
</style>
