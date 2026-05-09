<template>
  <q-page class="page-shell flex flex-center">
    <AppEmptyState
      icon="travel_explore"
      title="404"
      message="Ruta no encontrada."
    >
      <q-btn color="primary" unelevated icon="home" label="Volver al inicio" to="/" />
    </AppEmptyState>
  </q-page>
</template>

<script setup lang="ts">
import AppEmptyState from 'components/common/AppEmptyState.vue';
</script>
