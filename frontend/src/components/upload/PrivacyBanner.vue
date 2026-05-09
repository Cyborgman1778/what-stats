<template>
  <q-card flat class="soft-card privacy-card">
    <q-card-section>
      <div class="privacy-card__top">
        <q-icon name="shield_lock" size="20px" />
        <span>Privacidad</span>
      </div>

      <p>El archivo se procesa en memoria. No hay login ni base de datos visible.</p>

      <div class="privacy-card__checks">
        <span>memoria</span>
        <span>sin cuenta</span>
        <span>limpieza manual</span>
      </div>
    </q-card-section>
  </q-card>
</template>

<style scoped lang="scss">
.privacy-card {
  height: 100%;
}

.privacy-card__top {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--ws-text);
  font-weight: 700;
}

.privacy-card p {
  margin: 12px 0 0;
  color: var(--ws-text-muted);
  line-height: 1.55;
}

.privacy-card__checks {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
}

.privacy-card__checks span {
  padding: 4px 8px;
  color: var(--ws-text-muted);
  background: var(--ws-surface-muted);
  border: 1px solid var(--ws-border);
  border-radius: 999px;
  font-size: 0.78rem;
}
</style>
