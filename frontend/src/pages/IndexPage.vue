<template>
  <q-page class="page-shell home-page">
    <div class="container-xl home-page__container">
      <section class="home-grid">
        <div class="home-copy">
          <div class="repo-label">
            <q-icon name="lock" size="16px" />
            privado por defecto
          </div>

          <h1 class="home-copy__title">Sube un chat. Mira patrones.</h1>
          <p class="home-copy__subtitle">TXT o ZIP de WhatsApp. WhatStats procesa el archivo y convierte el chat en un dashboard claro.</p>

          <div class="home-copy__meta">
            <span>sin login</span>
            <span>memoria</span>
            <span>web móvil</span>
          </div>
        </div>

        <UploadCard @completed="handleCompleted" />
      </section>

      <div class="home-secondary">
        <PrivacyBanner />
        <ExportHelp />
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { Notify } from 'quasar';
import { useRouter } from 'vue-router';
import ExportHelp from 'components/upload/ExportHelp.vue';
import PrivacyBanner from 'components/upload/PrivacyBanner.vue';
import UploadCard from 'components/upload/UploadCard.vue';
import type { ChatStatsPayload } from 'src/services/api/types';

const router = useRouter();

async function handleCompleted(stats: ChatStatsPayload) {
  Notify.create({
    type: stats.status === 'failed' ? 'info' : 'positive',
    message: stats.status === 'failed' ? 'Sin mensajes válidos.' : 'Análisis listo.'
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

.home-copy {
  display: flex;
  min-height: 520px;
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

.repo-label {
  display: inline-flex;
  align-items: center;
  align-self: flex-start;
  gap: 7px;
  padding: 5px 9px;
  color: var(--ws-accent-strong);
  background: var(--ws-pill-background);
  border: 1px solid var(--ws-border);
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 600;
}

.home-copy__title {
  max-width: 640px;
  margin: 22px 0 0;
  color: var(--ws-accent-strong);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: clamp(2.4rem, 6vw, 5rem);
  font-weight: 700;
  line-height: 0.95;
  letter-spacing: -0.055em;
  text-shadow: var(--ws-title-shadow);
}

.home-copy__subtitle {
  max-width: 470px;
  margin: 18px 0 0;
  color: var(--ws-text-muted);
  font-size: 1rem;
  line-height: 1.6;
}

.home-copy__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 24px;
  color: var(--ws-text-subtle);
  font-size: 0.78rem;
}

.home-copy__meta span {
  padding: 6px 10px;
  background: var(--ws-meta-background);
  border: 1px solid var(--ws-border-muted);
  border-radius: 999px;
}

.home-copy__meta span::before {
  content: '';
}

.home-secondary {
  display: grid;
  grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
  gap: 22px;
}

@media (max-width: 980px) {
  .home-grid,
  .home-secondary {
    grid-template-columns: 1fr;
  }

  .home-copy {
    min-height: 340px;
  }
}

@media (max-width: 560px) {
  .home-page__container {
    min-height: auto;
  }
}
</style>
