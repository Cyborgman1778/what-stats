<template>
  <SectionCard title="Mensajes largos">
    <q-table
      v-if="rows.length > 0"
      flat
      bordered
      :rows="rows"
      :columns="columns"
      row-key="id"
      :pagination="{ rowsPerPage: 5 }"
      :rows-per-page-options="[5, 10, 20]"
      rows-per-page-label="Filas por página"
      :pagination-label="getPaginationLabel"
      class="longest-table"
    >
      <template #body-cell-preview="scope">
        <q-td :props="scope">
          <span class="message-preview">{{ scope.row.preview }}</span>
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

const authorColumnStyle = 'width: 1%; max-width: 180px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding-right: 8px;';
const lengthColumnStyle = 'width: 1%; max-width: 90px; white-space: nowrap; padding-left: 8px; padding-right: 10px;';
const actionColumnStyle = 'width: 1%; white-space: nowrap; padding-left: 8px; padding-right: 10px;';

const columns: QTableColumn<Row>[] = [
  {
    name: 'Author',
    label: 'Autor',
    field: 'Author',
    align: 'left',
    sortable: true,
    style: authorColumnStyle,
    headerStyle: authorColumnStyle
  },
  {
    name: 'Length',
    label: 'Longitud',
    field: 'Length',
    align: 'left',
    sortable: true,
    style: lengthColumnStyle,
    headerStyle: lengthColumnStyle
  },
  {
    name: 'actions',
    label: 'Ver',
    field: 'id',
    align: 'center',
    style: actionColumnStyle,
    headerStyle: actionColumnStyle
  },
  {
    name: 'preview',
    label: 'Vista previa',
    field: 'preview',
    align: 'left',
    style: 'width: 100%;'
  }
];

function openMessage(row: Row) {
  selectedMessage.value = row;
  dialogOpen.value = true;
}

function getPaginationLabel(firstRowIndex: number, endRowIndex: number, totalRowsNumber: number) {
  return `${firstRowIndex}-${endRowIndex} de ${totalRowsNumber}`;
}
</script>

<style scoped lang="scss">
.longest-table {
  border-color: var(--ws-border);
  border-radius: var(--ws-radius);
  overflow: hidden;
  background: var(--ws-table-inset-background);
}

.message-dialog {
  width: min(780px, calc(100vw - 28px));
  max-height: 88vh;
  border: 1px solid var(--ws-border);
  border-radius: var(--ws-radius);
  background: var(--ws-surface-solid);
  color: var(--ws-text);
}

.message-dialog__title {
  color: var(--ws-text);
  font-size: 1rem;
  font-weight: 700;
}
</style>
