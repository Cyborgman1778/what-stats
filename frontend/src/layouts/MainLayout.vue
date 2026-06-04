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

        <q-item v-if="isNativeRuntime" clickable v-ripple @click="openPrivacyPolicy">
          <q-item-section avatar>
            <q-icon name="lock" />
          </q-item-section>
          <q-item-section>Privacidad</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <SettingsDialog v-model="settingsOpen" />

    <q-dialog v-if="isNativeRuntime" v-model="privacyPolicyOpen">
      <q-card class="privacy-policy-card">
        <q-card-section class="privacy-policy-card__head">
          <div>
            <div class="privacy-policy-card__title">Politicas de privacidad</div>
            <div class="text-muted">proteccion del analisis</div>
          </div>

          <q-btn v-close-popup flat round dense icon="close" aria-label="Cerrar politicas de privacidad" />
        </q-card-section>

        <q-separator />

        <q-card-section>
          <p class="privacy-policy-card__text">
            Privacidad total y automatizada. Tu archivo se procesa 100% en memoria, no guardamos nada en disco. No usamos bases de datos ni registramos tus datos personales, por lo que ningun ser humano vera jamas tus conversaciones. No necesitas crear cuenta y el entorno esta protegido por Cloudflare.
          </p>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<script setup lang="ts">
import { Capacitor } from '@capacitor/core';
import { ref } from 'vue';
import { useQuasar } from 'quasar';
import BrandMark from 'components/common/BrandMark.vue';
import SettingsDialog from 'components/settings/SettingsDialog.vue';
import { usePreferencesStore } from 'stores/preferences-store';

const $q = useQuasar();
const preferencesStore = usePreferencesStore();
const isNativeRuntime = Capacitor.isNativePlatform();

const drawerOpen = ref(false);
const settingsOpen = ref(false);
const privacyPolicyOpen = ref(false);

function openPrivacyPolicy() {
  drawerOpen.value = false;
  privacyPolicyOpen.value = true;
}

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
  height: 64px;
  min-height: 64px;
  gap: 14px;
  overflow: hidden;
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

.privacy-policy-card {
  width: min(460px, calc(100vw - 28px));
  color: var(--ws-text);
  background: var(--ws-surface);
  border: 1px solid var(--ws-border);
  border-radius: var(--ws-radius);
  box-shadow: var(--ws-shadow-floating);
}

.privacy-policy-card__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
}

.privacy-policy-card__title {
  color: var(--ws-text);
  font-size: 1.05rem;
  font-weight: 800;
}

.privacy-policy-card__text {
  margin: 0;
  color: var(--ws-text-muted);
  font-size: 0.94rem;
  line-height: 1.65;
}
</style>
