<template>
  <q-page class="page-shell home-page" :class="{ 'home-page--native': isNativeRuntime }">
    <div class="container-xl home-page__container">
      <section class="home-grid">
        <div v-if="!isNativeRuntime" class="home-copy">
          <div class="home-copy__content">
            <h1 class="home-copy__title">WhatStats</h1>

            <div class="home-copy__details">
              <article class="home-info-card">
                <div class="home-info-card__top">
                  <q-icon name="lock" size="20px" />
                  <span>Privacidad</span>
                </div>

                <p>El archivo se procesa en memoria. No hay login ni base de datos visible.</p>

                <div class="home-info-card__chips">
                  <span>memoria</span>
                  <span>sin cuenta</span>
                  <span>limpieza manual</span>
                </div>
              </article>

              <article class="home-info-card home-info-card--export">
                <div class="home-info-card__top">
                  <q-icon name="ios_share" size="20px" />
                  <span>Exportar</span>
                </div>

                <p>Exporta el chat sin multimedia y sube el .txt o un .zip compatible.</p>

                <q-list separator class="home-export-list">
                  <q-expansion-item icon="android" label="Android" group="home-export-help">
                    <q-card-section class="text-muted">
                      Chat > menú > Más > Exportar chat > sin multimedia.
                    </q-card-section>
                  </q-expansion-item>

                  <q-expansion-item icon="phone_iphone" label="iOS" group="home-export-help">
                    <q-card-section class="text-muted">
                      Chat > contacto o grupo > Exportar chat > sin multimedia.
                    </q-card-section>
                  </q-expansion-item>

                  <q-expansion-item icon="rule" label="ZIP" group="home-export-help">
                    <q-card-section class="text-muted">
                      Debe contener un .txt de chat compatible.
                    </q-card-section>
                  </q-expansion-item>
                </q-list>
              </article>
            </div>
          </div>
        </div>

        <div class="home-upload-panel">
          <h1 v-if="isNativeRuntime" class="home-native-title">WhatStats</h1>
          <UploadCard @completed="handleCompleted" />
        </div>
      </section>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { Capacitor } from '@capacitor/core';
import { Notify } from 'quasar';
import { useRouter } from 'vue-router';
import UploadCard from 'components/upload/UploadCard.vue';
import type { ChatStatsPayload } from 'src/services/api/types';

const router = useRouter();
const isNativeRuntime = Capacitor.isNativePlatform();

async function handleCompleted(stats: ChatStatsPayload) {
  Notify.create({
    type: stats.status === 'failed' ? 'info' : 'positive',
    message: stats.status === 'failed' ? 'Sin mensajes válidos.' : stats.message,
    position: 'bottom',
    timeout: 3000
  });

  await router.push('/results');
}
</script>

<style scoped lang="scss">
.home-page__container {
  display: grid;
  min-height: calc(100vh - 154px);
  align-content: center;
  gap: 22px;
}

.home-grid {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(360px, 1fr);
  gap: 22px;
  align-items: stretch;
}

.home-page--native .home-page__container {
  min-height: calc(100vh - 112px);
}

.home-page--native .home-grid {
  grid-template-columns: minmax(0, 720px);
  justify-content: center;
}

.home-page--native .home-upload-panel {
  display: grid;
  gap: clamp(18px, 5vw, 28px);
}

.home-native-title {
  margin: 0;
  color: var(--ws-accent-strong);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: clamp(3rem, 14vw, 5rem);
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.055em;
  text-align: center;
  text-shadow: var(--ws-title-shadow);
}

.home-copy {
  display: flex;
  min-height: 590px;
  position: relative;
  overflow: hidden;
  padding: clamp(28px, 5vw, 48px);
  flex-direction: column;
  justify-content: center;
  background: var(--ws-hero-background);
  border: 1px solid var(--ws-border);
  border-radius: 32px;
  box-shadow: var(--ws-shadow);
  backdrop-filter: blur(22px);
}

.home-copy__content {
  position: relative;
  z-index: 1;
  display: grid;
  align-content: center;
  min-height: 100%;
}

.home-copy::after {
  content: '';
  position: absolute;
  right: -90px;
  bottom: -110px;
  width: 260px;
  height: 260px;
  background: var(--ws-hero-orb);
  pointer-events: none;
}

.home-copy__title {
  max-width: 640px;
  margin: 0;
  color: var(--ws-accent-strong);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: clamp(3.2rem, 6.8vw, 5.35rem);
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.055em;
  white-space: nowrap;
  text-shadow: var(--ws-title-shadow);
}

.home-copy__details {
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
  margin-top: clamp(30px, 5vw, 52px);
}

.home-info-card {
  display: grid;
  grid-template-columns: 1fr;
  align-items: start;
  gap: 12px;
  min-width: 0;
  padding: 16px;
  background: color-mix(in srgb, var(--ws-surface) 66%, transparent);
  border: 1px solid var(--ws-border-muted);
  border-radius: 22px;
}

.home-info-card--export {
  gap: 14px;
}

.home-info-card__top {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--ws-text);
  font-weight: 700;
}

.home-info-card__top .q-icon {
  color: var(--ws-accent-strong);
}

.home-info-card p {
  margin: 0;
  color: var(--ws-text-muted);
  font-size: 0.88rem;
  line-height: 1.55;
}

.home-info-card__chips,
.home-info-card__steps {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  justify-content: flex-start;
  margin-top: 0;
}

.home-info-card__chips span,
.home-info-card__steps span {
  padding: 5px 8px;
  color: var(--ws-accent-chip-text);
  background: var(--ws-accent-chip-background);
  border: 1px solid var(--ws-border-muted);
  border-radius: 999px;
  font-size: 0.76rem;
  line-height: 1.25;
}

.home-export-list {
  overflow: hidden;
  background: color-mix(in srgb, var(--ws-surface-muted) 42%, transparent);
  border: 1px solid var(--ws-border-muted);
  border-radius: 16px;
}

.home-export-list :deep(.q-item) {
  min-height: 42px;
  color: var(--ws-text);
  padding: 8px 12px;
}

.home-export-list :deep(.q-item__section--avatar) {
  min-width: 32px;
  color: var(--ws-accent-strong);
}

.home-export-list :deep(.q-expansion-item__content) {
  background: var(--ws-export-panel-background);
}

@media (max-width: 980px) {
  .home-grid {
    grid-template-columns: 1fr;
  }

  .home-upload-panel {
    order: -1;
  }

  .home-copy {
    min-height: auto;
  }
}

@media (max-width: 680px) {
  .home-copy__title {
    font-size: clamp(2.7rem, 16vw, 4rem);
  }

  .home-info-card__chips,
  .home-info-card__steps {
    margin-top: 2px;
  }
}

@media (max-width: 560px) {
  .home-page__container {
    min-height: auto;
  }
}
</style>
