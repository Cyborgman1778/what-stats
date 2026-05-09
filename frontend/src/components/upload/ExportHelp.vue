<template>
  <q-card flat class="soft-card export-help">
    <q-card-section class="export-help__head">
      <div>
        <div class="export-help__title">Exportar</div>
        <div class="text-muted">sin multimedia, .txt o .zip</div>
      </div>
    </q-card-section>

    <q-list separator>
      <q-expansion-item icon="android" label="Android" group="export-help">
        <q-card-section class="text-muted">
          Chat > menú > Más > Exportar chat > sin multimedia.
        </q-card-section>
      </q-expansion-item>

      <q-expansion-item icon="phone_iphone" label="iOS" group="export-help">
        <q-card-section class="text-muted">
          Chat > contacto o grupo > Exportar chat > sin multimedia.
        </q-card-section>
      </q-expansion-item>

      <q-expansion-item icon="rule" label="ZIP" group="export-help">
        <q-card-section class="text-muted">
          Debe contener un .txt de chat compatible.
        </q-card-section>
      </q-expansion-item>
    </q-list>
  </q-card>
</template>

<style scoped lang="scss">
.export-help {
  overflow: hidden;
}

.export-help__head {
  padding-bottom: 12px;
}

.export-help__title {
  color: var(--ws-text);
  font-size: 1rem;
  font-weight: 700;
}

.export-help :deep(.q-item) {
  color: var(--ws-text);
}
</style>
