<template>
  <q-page class="page-shell results-page">
    <div class="container-xl">
      <div class="results-toolbar">
        <div>
          <div class="results-toolbar__kicker">dashboard</div>
          <h1 class="results-toolbar__title">Resultados</h1>
        </div>

        <div class="results-toolbar__actions">
          <q-btn outline color="primary" icon="upload_file" label="Analizar otro" @click="analyzeAnother" />
          <q-btn
            flat
            color="negative"
            icon="delete_sweep"
            label="Limpiar"
            :disable="!analysisStore.hasStats"
            @click="confirmClear"
          />
        </div>
      </div>

      <AppEmptyState
        v-if="!stats"
        icon="query_stats"
        title="Sin análisis"
        message="Sube un chat para ver estadísticas."
      >
        <q-btn color="primary" unelevated icon="upload_file" label="Ir al inicio" to="/" />
      </AppEmptyState>

      <ResultFailureState
        v-else-if="stats.status === 'failed'"
        :message="stats.message"
        @analyze-another="analyzeAnother"
      />

      <template v-else>
        <SummaryKpis
          :stats="stats"
          :file-name="analysisStore.currentFile?.name"
          :file-size="analysisStore.currentFile?.size"
          :analyzed-at="analysisStore.currentFile?.analyzedAt"
        />

        <q-card flat class="premium-card results-card q-mt-lg">
          <q-tabs
            v-model="tab"
            dense
            align="left"
            active-color="primary"
            indicator-color="primary"
            class="results-tabs"
          >
            <q-tab name="overview" label="Resumen" />
            <q-tab name="activity" label="Actividad" />
            <q-tab name="content" label="Contenido" />
            <q-tab name="messages" label="Mensajes" />
          </q-tabs>

          <q-separator />

          <q-tab-panels v-model="tab" animated class="results-panels">
            <q-tab-panel name="overview">
              <div class="q-gutter-lg">
                <ParticipantsPanel :participants="stats.participants" />
                <MessagesByUser :data="normalized.messagesByUser.value" />
              </div>
            </q-tab-panel>

            <q-tab-panel name="activity">
              <TemporalActivity
                :hot-hours="normalized.hotHours.value"
                :messages-per-day="normalized.messagesPerDay.value"
                :messages-per-month="normalized.messagesPerMonth.value"
                :messages-per-year="normalized.messagesPerYear.value"
                :top-messages-per-day="normalized.topMessagesPerDay.value"
              />
            </q-tab-panel>

            <q-tab-panel name="content">
              <ContentStats
                :top-words="normalized.topWords.value"
                :top-emojis="normalized.topEmojis.value"
              />
            </q-tab-panel>

            <q-tab-panel name="messages">
              <div class="q-gutter-lg">
                <LongestMessages :messages="normalized.longestMessages.value" />
                <StreaksPanel :streaks="normalized.topStreaks.value" />
              </div>
            </q-tab-panel>
          </q-tab-panels>
        </q-card>
      </template>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { Dialog } from 'quasar';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import AppEmptyState from 'components/common/AppEmptyState.vue';
import ContentStats from 'components/results/ContentStats.vue';
import LongestMessages from 'components/results/LongestMessages.vue';
import MessagesByUser from 'components/results/MessagesByUser.vue';
import ParticipantsPanel from 'components/results/ParticipantsPanel.vue';
import ResultFailureState from 'components/results/ResultFailureState.vue';
import StreaksPanel from 'components/results/StreaksPanel.vue';
import SummaryKpis from 'components/results/SummaryKpis.vue';
import TemporalActivity from 'components/results/TemporalActivity.vue';
import { useAnalysisStore } from 'stores/analysis-store';
import { useNormalizedStats } from 'src/composables/useNormalizedStats';

const router = useRouter();
const analysisStore = useAnalysisStore();
const { stats } = storeToRefs(analysisStore);
const normalized = useNormalizedStats(computed(() => stats.value));

const tab = ref('overview');

function analyzeAnother() {
  analysisStore.clearAnalysis();
  void router.push('/');
}

function confirmClear() {
  Dialog.create({
    title: 'Limpiar análisis',
    message: 'Se eliminará el resultado en memoria.',
    cancel: true,
    persistent: true,
    ok: {
      color: 'negative',
      label: 'Limpiar'
    }
  }).onOk(() => {
    analysisStore.clearAnalysis();
  });
}
</script>

<style scoped lang="scss">
.results-toolbar {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 22px;
}

.results-toolbar__kicker {
  color: var(--ws-accent-strong);
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.results-toolbar__title {
  margin: 2px 0 0;
  color: var(--ws-accent-strong);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: clamp(1.8rem, 4vw, 3rem);
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.045em;
}

.results-toolbar__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 8px;
}

.results-card {
  overflow: hidden;
  background: var(--ws-results-card-background);
  border-radius: 28px;
}

.results-tabs {
  color: var(--ws-text-muted);
  background: var(--ws-results-tabs-background);
}

.results-tabs :deep(.q-tab) {
  min-height: 46px;
  padding: 0 16px;
  font-size: 0.86rem;
  font-weight: 600;
}

.results-panels {
  background: transparent;
}

.results-panels :deep(.q-tab-panel) {
  padding: clamp(16px, 3vw, 26px);
}

@media (max-width: 720px) {
  .results-toolbar {
    align-items: flex-start;
    flex-direction: column;
  }

  .results-toolbar__actions {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
