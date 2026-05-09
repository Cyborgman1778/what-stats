<template>
  <SectionCard
    title="Mensajes largos"
    subtitle="vista previa"
  >
    <q-table
      v-if="rows.length > 0"
      flat
      bordered
      :rows="rows"
      :columns="columns"
      row-key="id"
      :pagination="{ rowsPerPage: 8 }"
      class="longest-table"
    >
      <template #body-cell-preview="scope">
        <q-td :props="scope">
          <span class="message-preview">{{ scope.row.Message }}</span>
        </q-td>
      </template>

      <template #body-cell-actions="scope">
        <q-td :props="scope">
          <q-btn
            dense
            flat
            round
            color="primary"
            icon="open_in_full"
            aria-label="Ver mensaje completo"
            @click="openMessage(scope.row)"
          />
        </q-td>
      </template>
    </q-table>

    <p v-else class="text-muted">
      Sin mensajes largos.
    </p>

    <q-dialog v-model="dialogOpen">
      <q-card class="message-dialog">
        <q-card-section class="row items-start justify-between q-gutter-md">
          <div>
            <div class="message-dialog__title">Mensaje</div>
            <div v-if="selectedMessage" class="text-muted">
              {{ selectedMessage.Author }} · {{ selectedMessage.Length }} caracteres
            </div>
          </div>

          <q-btn v-close-popup flat round dense icon="close" />
        </q-card-section>

        <q-separator />

        <q-card-section>
          <pre class="full-message">{{ selectedMessage?.Message }}</pre>
        </q-card-section>
      </q-card>
    </q-dialog>
  </SectionCard>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import type { QTableColumn } from 'quasar';
import SectionCard from 'components/common/SectionCard.vue';
import type { LongestMessage } from 'src/services/api/types';
import { truncateText } from 'src/utils/format';

interface Row extends LongestMessage {
  id: number;
  preview: string;
}

const props = defineProps<{
  messages: LongestMessage[];
}>();

const dialogOpen = ref(false);
const selectedMessage = ref<Row | null>(null);

const rows = computed<Row[]>(() =>
  props.messages.map((message, index) => ({
    ...message,
    id: index,
    preview: truncateText(message.Message, 150)
  }))
);

const columns: QTableColumn<Row>[] = [
  {
    name: 'Author',
    label: 'Autor',
    field: 'Author',
    align: 'left',
    sortable: true
  },
  {
    name: 'Length',
    label: 'Longitud',
    field: 'Length',
    align: 'right',
    sortable: true
  },
  {
    name: 'preview',
    label: 'Vista previa',
    field: 'preview',
    align: 'left'
  },
  {
    name: 'actions',
    label: '',
    field: 'id',
    align: 'center'
  }
];

function openMessage(row: Row) {
  selectedMessage.value = row;
  dialogOpen.value = true;
}
</script>

<style scoped lang="scss">
.longest-table {
  border-color: var(--ws-border);
  border-radius: var(--ws-radius);
  overflow: hidden;
  background: var(--ws-surface);
}

.message-dialog {
  width: min(780px, calc(100vw - 28px));
  max-height: 88vh;
  border: 1px solid var(--ws-border);
  border-radius: var(--ws-radius);
  background: var(--ws-surface);
  color: var(--ws-text);
}

.message-dialog__title {
  color: var(--ws-text);
  font-size: 1rem;
  font-weight: 700;
}
</style>
