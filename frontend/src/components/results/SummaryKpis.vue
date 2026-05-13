<template>
  <div class="summary-stack">
    <div class="summary-grid">
      <q-card flat class="summary-chat-card">
        <q-card-section>
          <div class="summary-chat-card__head">
            <span>Chat</span>
            <q-icon name="chat" size="18px" />
          </div>

          <div class="summary-chat-card__value">{{ chatTitle }}</div>
          <div class="summary-chat-card__label">conversación</div>
        </q-card-section>
      </q-card>

      <div>
        <MetricCard icon="forum" eyebrow="Mensajes" :value="formatNumber(stats.total_messages)" label="total" />
      </div>

      <div>
        <MetricCard icon="group" eyebrow="Usuarios" :value="formatNumber(stats.total_users)" label="detectados" />
      </div>

      <div>
        <MetricCard icon="database" eyebrow="Tamaño" :value="chatSize" label="del chat" />
      </div>

      <div>
        <MetricCard icon="event" eyebrow="Fecha" :value="analysisDate" label="análisis" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import MetricCard from 'components/common/MetricCard.vue';
import type { ChatStatsPayload } from 'src/services/api/types';
import { formatBytes, formatNumber } from 'src/utils/format';
import { formatDateTime } from 'src/utils/dates';

const props = defineProps<{
  stats: ChatStatsPayload;
  fileName?: string | undefined;
  fileSize?: number | undefined;
  analyzedAt?: string | undefined;
}>();

const chatTitle = computed(() => formatChatTitle(props.fileName));
const chatSize = computed(() => (typeof props.fileSize === 'number' ? formatBytes(props.fileSize) : '—'));
const analysisDate = computed(() => (props.analyzedAt ? formatDateTime(props.analyzedAt) : '—'));

function formatChatTitle(fileName?: string) {
  if (!fileName) return 'Chat';

  const baseName = fileName.replace(/\.(txt|zip)$/i, '').trim();
  const match = baseName.match(/\bcon\s+(.+)$/i);
  const chatName = (match?.[1] ?? baseName).trim();

  return chatName ? `Chat con ${chatName}` : 'Chat';
}
</script>

<style scoped lang="scss">
.summary-stack {
  display: grid;
  gap: 16px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 16px;
}

.summary-chat-card {
  height: 100%;
  overflow: hidden;
  color: var(--ws-text);
  background: var(--ws-metric-card-background);
  border: 1px solid var(--ws-border);
  border-radius: var(--ws-radius);
  box-shadow: var(--ws-shadow);
}

.summary-chat-card__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: var(--ws-text-muted);
  font-size: 0.8rem;
  font-weight: 600;
}

.summary-chat-card__head .q-icon {
  color: var(--ws-accent-strong);
}

.summary-chat-card__value {
  margin-top: 18px;
  overflow-wrap: anywhere;
  color: var(--ws-accent-strong);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: clamp(1.25rem, 2.5vw, 1.75rem);
  font-weight: 700;
  line-height: 1.08;
  letter-spacing: -0.04em;
}

.summary-chat-card__label {
  margin-top: 7px;
  color: var(--ws-text-muted);
  font-size: 0.84rem;
}
</style>
