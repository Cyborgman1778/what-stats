<template>
  <q-layout view="hHh LpR fFf">
    <q-header class="main-header safe-area-top">
      <q-toolbar class="container-xl main-header__bar">
        <q-btn
          flat
          round
          dense
          icon="menu"
          class="lt-md q-mr-sm main-header__icon"
          aria-label="Abrir navegación"
          @click="drawerOpen = !drawerOpen"
        />

        <BrandMark />

        <q-tabs shrink stretch class="gt-sm main-header__tabs">
          <q-route-tab to="/" exact label="Inicio" />
          <q-route-tab to="/results" label="Resultados" />
        </q-tabs>

        <q-space />

        <q-btn
          flat
          dense
          round
          class="main-header__icon"
          :icon="$q.dark.isActive ? 'light_mode' : 'dark_mode'"
          aria-label="Cambiar tema"
          @click="cycleTheme"
        >
          <q-tooltip>Cambiar tema</q-tooltip>
        </q-btn>

        <q-btn
          flat
          dense
          round
          class="main-header__icon"
          icon="settings"
          aria-label="Abrir ajustes"
          @click="settingsOpen = true"
        >
          <q-tooltip>Ajustes</q-tooltip>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="drawerOpen"
      side="left"
      overlay
      bordered
      :width="280"
      class="drawer-surface"
    >
      <div class="q-pa-md">
        <BrandMark />
      </div>

      <q-separator />

      <q-list padding>
        <q-item clickable v-ripple to="/" exact>
          <q-item-section avatar>
            <q-icon name="upload_file" />
          </q-item-section>
          <q-item-section>Inicio</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/results">
          <q-item-section avatar>
            <q-icon name="insights" />
          </q-item-section>
          <q-item-section>Resultados</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <SettingsDialog v-model="settingsOpen" />
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useQuasar } from 'quasar';
import BrandMark from 'components/common/BrandMark.vue';
import SettingsDialog from 'components/settings/SettingsDialog.vue';
import { usePreferencesStore } from 'stores/preferences-store';

const $q = useQuasar();
const preferencesStore = usePreferencesStore();

const drawerOpen = ref(false);
const settingsOpen = ref(false);

function cycleTheme() {
  if (preferencesStore.theme === 'auto') {
    preferencesStore.setTheme($q.dark.isActive ? 'light' : 'dark');
    return;
  }

  preferencesStore.setTheme(preferencesStore.theme === 'dark' ? 'light' : 'dark');
}
</script>

<style scoped lang="scss">
.main-header {
  color: var(--ws-text);
  background: var(--ws-header-background);
  border-bottom: 1px solid var(--ws-border);
  box-shadow: var(--ws-header-shadow);
  backdrop-filter: blur(18px);
}

.main-header__bar {
  min-height: 64px;
  gap: 14px;
}

.main-header__tabs {
  align-self: stretch;
  color: var(--ws-text-muted);
}

.main-header__tabs :deep(.q-tab) {
  min-height: 64px;
  padding: 0 10px;
  color: var(--ws-text-muted);
  font-size: 0.88rem;
  font-weight: 600;
}

.main-header__tabs :deep(.q-tab--active) {
  color: var(--ws-text);
}

.main-header__tabs :deep(.q-tab__indicator) {
  height: 2px;
  background: var(--ws-accent);
}

.main-header__icon {
  color: var(--ws-text-muted);
}

.main-header__icon:hover {
  color: var(--ws-text);
  background: var(--ws-accent-soft);
}

.drawer-surface {
  color: var(--ws-text);
  background: var(--ws-surface-solid);
}

.drawer-surface :deep(.q-item) {
  min-height: 42px;
  border-radius: var(--ws-radius-sm);
  color: var(--ws-text-muted);
}

.drawer-surface :deep(.q-router-link--active) {
  color: var(--ws-text);
  background: var(--ws-accent-soft);
}
</style>
