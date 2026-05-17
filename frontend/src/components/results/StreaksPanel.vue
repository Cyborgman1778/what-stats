<template>
  <SectionCard title="Rachas">
    <div v-if="streaks.length > 0" class="row q-col-gutter-md">
      <div v-for="(streak, index) in streaks" :key="`${streak.start}-${streak.end}-${index}`" class="col-12 col-md-4">
        <q-card
          v-ripple
          flat
          class="streak-card"
          role="button"
          tabindex="0"
          @click="openStreak(streak)"
          @keydown.enter="openStreak(streak)"
          @keydown.space.prevent="openStreak(streak)"
        >
          <q-card-section>
            <div class="row items-center justify-between">
              <q-avatar color="primary" text-color="white" size="30px">
                {{ index + 1 }}
              </q-avatar>

              <q-chip
                class="ws-chip streak-duration-chip"
                :class="getStreakLevel(streak.duration).className"
                icon="local_fire_department"
              >
                <span class="streak-duration-chip__text">{{ streak.duration }} días</span>
              </q-chip>
            </div>

            <div class="streak-card__dates q-mt-md">
              <div>
                <div class="text-muted">Inicio</div>
                <div class="text-weight-bold">{{ formatIsoDate(streak.start) }}</div>
              </div>

              <q-icon name="east" class="text-muted" />

              <div>
                <div class="text-muted">Fin</div>
                <div class="text-weight-bold">{{ formatIsoDate(streak.end) }}</div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <p v-else class="text-muted">
      Sin rachas.
    </p>

    <q-dialog v-model="dialogOpen" @hide="resetDialog">
      <q-card v-if="selectedStreak" class="streak-dialog">
        <q-card-section class="streak-dialog__header">
          <div class="streak-dialog__dates">
            <div class="streak-dialog__date-block">
              <div class="streak-dialog__label">Inicio</div>
              <div class="streak-dialog__value">{{ formatIsoDate(selectedStreak.start) }}</div>
            </div>

            <q-icon name="east" class="streak-dialog__arrow" />

            <div class="streak-dialog__date-block">
              <div class="streak-dialog__label">Fin</div>
              <div class="streak-dialog__value">{{ formatIsoDate(selectedStreak.end) }}</div>
            </div>
          </div>

          <div class="streak-dialog__actions">
            <div class="streak-tier-badge" :class="selectedStreakLevel.className">
              <span class="streak-tier-badge__label">Nivel</span>
              <span class="streak-tier-badge__value">{{ selectedStreakLevel.label }}</span>
            </div>

            <q-chip
              class="ws-chip streak-duration-chip streak-dialog__duration"
              :class="selectedStreakLevel.className"
              icon="local_fire_department"
            >
              <span class="streak-duration-chip__text">{{ selectedStreak.duration }} días</span>
            </q-chip>

            <q-btn
              flat
              round
              dense
              icon="close"
              class="streak-dialog__close"
              aria-label="Cerrar detalle de racha"
              @click="dialogOpen = false"
            />
          </div>
        </q-card-section>

        <q-separator />

        <q-card-section v-if="selectedRange" class="streak-dialog__body">
          <div class="streak-calendar__toolbar">
            <q-btn
              v-if="hasMultipleMonths"
              flat
              round
              dense
              icon="chevron_left"
              aria-label="Mes anterior"
              :disable="visibleMonthIndex === 0"
              @click="changeMonth(-1)"
            />
            <div v-else class="streak-calendar__nav-placeholder" />

            <div class="streak-calendar__title-block">
              <div class="streak-calendar__title">{{ currentMonthLabel }}</div>
            </div>

            <q-btn
              v-if="hasMultipleMonths"
              flat
              round
              dense
              icon="chevron_right"
              aria-label="Mes siguiente"
              :disable="visibleMonthIndex === streakMonths.length - 1"
              @click="changeMonth(1)"
            />
            <div v-else class="streak-calendar__nav-placeholder" />
          </div>

          <div class="streak-calendar__grid" role="grid" aria-label="Calendario de la racha">
            <div v-for="weekday in weekdays" :key="weekday" class="streak-calendar__weekday">
              {{ weekday }}
            </div>

            <div v-for="day in calendarDays" :key="day.key" class="streak-calendar__cell">
              <div v-if="day.date && day.iso" class="streak-calendar__day-shell">
                <button
                  type="button"
                  class="streak-calendar__day"
                  :class="{
                    'streak-calendar__day--active': day.isInStreak,
                    'streak-calendar__day--selected': messageBubbleOpen && selectedDayIso === day.iso
                  }"
                  :disabled="!day.isInStreak"
                  :aria-label="getDayAriaLabel(day)"
                  @click.stop="selectDay(day)"
                >
                  <span class="streak-calendar__day-number">{{ day.day }}</span>
                  <span v-if="day.isInStreak" class="streak-calendar__day-marker" />
                </button>

                <q-menu
                  v-if="!useInlineDayDetail && day.isInStreak && selectedDayIso === day.iso"
                  v-model="messageBubbleOpen"
                  class="streak-day-menu"
                  anchor="top middle"
                  self="bottom middle"
                  :offset="[0, 10]"
                >
                  <div class="streak-day-detail">
                    <div class="streak-day-detail__date">{{ formatDayDetailTitle(day.date) }}</div>
                    <div class="streak-day-detail__messages">
                      {{ formatNumber(day.messages) }}
                      {{ pluralize(day.messages, 'mensaje', 'mensajes') }}
                    </div>
                  </div>
                </q-menu>
              </div>

              <div v-else class="streak-calendar__empty" />
            </div>
          </div>

          <div
            v-if="useInlineDayDetail && selectedDayDetail && selectedDayDetail.date"
            class="streak-day-detail streak-day-detail--inline"
          >
            <div class="streak-day-detail__date">
              {{ formatDayDetailTitle(selectedDayDetail.date) }}
            </div>
            <div class="streak-day-detail__messages">
              {{ formatNumber(selectedDayDetail.messages) }}
              {{ pluralize(selectedDayDetail.messages, 'mensaje', 'mensajes') }}
            </div>
          </div>
        </q-card-section>

        <q-card-section v-else>
          <p class="text-muted q-mb-none">
            No se pudo construir el calendario de esta racha.
          </p>
        </q-card-section>
      </q-card>
    </q-dialog>
  </SectionCard>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useQuasar } from 'quasar';
import SectionCard from 'components/common/SectionCard.vue';
import type { TopStreak } from 'src/services/api/types';
import { formatNumber, pluralize } from 'src/utils/format';
import { formatIsoDate, parseDDMMYYYY } from 'src/utils/dates';

interface CalendarDay {
  key: string;
  date: Date | null;
  day: number | null;
  iso: string | null;
  isInStreak: boolean;
  messages: number;
}

const props = defineProps<{
  streaks: TopStreak[];
  messagesPerDay: Record<string, number>;
}>();

const quasar = useQuasar();
const weekdays = ['L', 'M', 'X', 'J', 'V', 'S', 'D'];

const dialogOpen = ref(false);
const selectedStreak = ref<TopStreak | null>(null);
const visibleMonthIndex = ref(0);
const selectedDayIso = ref<string | null>(null);
const messageBubbleOpen = ref(false);

const messagesByDate = computed(() => {
  const dateMap = new Map<string, number>();

  Object.entries(props.messagesPerDay).forEach(([day, messages]) => {
    if (!Number.isFinite(messages)) return;

    const parsedDate = parseCalendarDate(day);
    if (!parsedDate) return;

    const dateKey = toDateKey(parsedDate);
    dateMap.set(dateKey, (dateMap.get(dateKey) ?? 0) + messages);
  });

  return dateMap;
});

const selectedRange = computed(() => {
  if (!selectedStreak.value) return null;

  const start = parseCalendarDate(selectedStreak.value.start);
  const end = parseCalendarDate(selectedStreak.value.end);

  if (!start || !end) return null;

  if (start.getTime() <= end.getTime()) {
    return { start, end };
  }

  return { start: end, end: start };
});

const streakMonths = computed(() => {
  if (!selectedRange.value) return [];

  const months: Date[] = [];
  const cursor = new Date(
    selectedRange.value.start.getFullYear(),
    selectedRange.value.start.getMonth(),
    1
  );
  const lastMonth = new Date(
    selectedRange.value.end.getFullYear(),
    selectedRange.value.end.getMonth(),
    1
  );

  while (cursor.getTime() <= lastMonth.getTime()) {
    months.push(new Date(cursor));
    cursor.setMonth(cursor.getMonth() + 1);
  }

  return months;
});

const hasMultipleMonths = computed(() => streakMonths.value.length > 1);

const visibleMonth = computed(() => streakMonths.value[visibleMonthIndex.value] ?? null);

const selectedStreakLevel = computed(() => getStreakLevel(selectedStreak.value?.duration ?? 0));

const useInlineDayDetail = computed(() => quasar.screen.width <= 620);

const selectedDayDetail = computed(() => {
  if (!messageBubbleOpen.value || !selectedDayIso.value) return null;

  return calendarDays.value.find((day) => day.iso === selectedDayIso.value && day.date) ?? null;
});

const currentMonthLabel = computed(() => {
  if (!visibleMonth.value) return '';
  const month = new Intl.DateTimeFormat('es-ES', { month: 'long' }).format(visibleMonth.value);

  return `${month} ${visibleMonth.value.getFullYear()}`;
});

const calendarDays = computed<CalendarDay[]>(() => {
  if (!visibleMonth.value || !selectedRange.value) return [];

  const year = visibleMonth.value.getFullYear();
  const month = visibleMonth.value.getMonth();
  const firstDay = new Date(year, month, 1);
  const leadingEmptyDays = getMondayBasedWeekday(firstDay);
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const days: CalendarDay[] = [];

  for (let index = 0; index < leadingEmptyDays; index += 1) {
    days.push({
      key: `empty-${year}-${month}-${index}`,
      date: null,
      day: null,
      iso: null,
      isInStreak: false,
      messages: 0
    });
  }

  for (let day = 1; day <= daysInMonth; day += 1) {
    const date = new Date(year, month, day);
    const iso = toDateKey(date);
    const isInStreak = isDateInRange(date, selectedRange.value.start, selectedRange.value.end);

    days.push({
      key: iso,
      date,
      day,
      iso,
      isInStreak,
      messages: messagesByDate.value.get(iso) ?? 0
    });
  }

  return days;
});

function openStreak(streak: TopStreak) {
  selectedStreak.value = streak;
  visibleMonthIndex.value = 0;
  selectedDayIso.value = null;
  messageBubbleOpen.value = false;
  dialogOpen.value = true;
}

function resetDialog() {
  selectedStreak.value = null;
  visibleMonthIndex.value = 0;
  selectedDayIso.value = null;
  messageBubbleOpen.value = false;
}

function changeMonth(direction: -1 | 1) {
  const lastIndex = Math.max(streakMonths.value.length - 1, 0);
  visibleMonthIndex.value = Math.min(Math.max(visibleMonthIndex.value + direction, 0), lastIndex);
  selectedDayIso.value = null;
  messageBubbleOpen.value = false;
}

function selectDay(day: CalendarDay) {
  if (!day.isInStreak || !day.iso) return;

  selectedDayIso.value = day.iso;
  messageBubbleOpen.value = true;
}

function parseCalendarDate(value: string) {
  const parsedDay = parseDDMMYYYY(value);
  if (parsedDay) return parsedDay;

  const isoMatch = /^(\d{4})-(\d{2})-(\d{2})/.exec(value);

  if (isoMatch) {
    const [, year, month, day] = isoMatch;
    return new Date(Number(year), Number(month) - 1, Number(day));
  }

  const parsedDate = new Date(value);

  if (Number.isNaN(parsedDate.getTime())) return null;

  return new Date(parsedDate.getFullYear(), parsedDate.getMonth(), parsedDate.getDate());
}

function toDateKey(date: Date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
}

function getMondayBasedWeekday(date: Date) {
  return (date.getDay() + 6) % 7;
}

function isDateInRange(date: Date, start: Date, end: Date) {
  const time = date.getTime();

  return time >= start.getTime() && time <= end.getTime();
}

function getStreakLevel(duration: number) {
  if (duration >= 365) return { label: 'Diamante', className: 'streak-level--diamond' };
  if (duration >= 150) return { label: 'Oro', className: 'streak-level--gold' };
  if (duration >= 50) return { label: 'Plata', className: 'streak-level--silver' };
  if (duration >= 10) return { label: 'Bronce', className: 'streak-level--bronze' };

  return { label: 'Gris', className: 'streak-level--gray' };
}

function formatLongDate(date: Date) {
  return new Intl.DateTimeFormat('es-ES', {
    weekday: 'long',
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  }).format(date);
}

function formatDayDetailTitle(date: Date) {
  const weekday = new Intl.DateTimeFormat('es-ES', { weekday: 'long' }).format(date);
  const formattedDate = new Intl.DateTimeFormat('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).format(date);

  return `${weekday}, ${formattedDate}`;
}

function getDayAriaLabel(day: CalendarDay) {
  if (!day.date || !day.isInStreak) return 'Día fuera de la racha';

  return `${formatLongDate(day.date)}: ${formatNumber(day.messages)} ${pluralize(
    day.messages,
    'mensaje',
    'mensajes'
  )}`;
}
</script>

<style scoped lang="scss">
.streak-card {
  height: 100%;
  position: relative;
  overflow: hidden;
  border-radius: var(--ws-radius);
  background: var(--ws-table-inset-background);
  border: 1px solid var(--ws-border);
  cursor: pointer;
  outline: none;
  transition:
    transform 180ms ease,
    border-color 180ms ease,
    background 180ms ease,
    box-shadow 180ms ease;
}

.streak-card:hover,
.streak-card:focus-visible {
  transform: translateY(-2px);
  border-color: color-mix(in srgb, var(--ws-accent) 42%, var(--ws-border));
  background: color-mix(in srgb, var(--ws-surface-muted) 60%, transparent);
  box-shadow: 0 16px 38px rgba(0, 0, 0, 0.18);
}

.streak-card__dates {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.streak-duration-chip {
  gap: 4px;
  margin: 0;
}

.streak-duration-chip :deep(.q-chip__icon) {
  color: #ff7a18;
  filter: drop-shadow(0 0 7px rgba(255, 122, 24, 0.32));
}

.streak-duration-chip__text {
  font-weight: 700;
  white-space: nowrap;
}

.streak-duration-chip.streak-level--gray .streak-duration-chip__text {
  color: var(--ws-text-muted);
}

.streak-duration-chip.streak-level--bronze .streak-duration-chip__text {
  color: #c98242;
}

.streak-duration-chip.streak-level--silver .streak-duration-chip__text {
  color: #cbd8e6;
}

.streak-duration-chip.streak-level--gold .streak-duration-chip__text {
  color: #f4b84a;
}

.streak-duration-chip.streak-level--diamond .streak-duration-chip__text {
  color: #8fe8ff;
}

.streak-dialog {
  width: min(720px, calc(100vw - 28px));
  max-height: 88vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid var(--ws-border);
  border-radius: var(--ws-radius);
  background: var(--ws-surface-solid);
  color: var(--ws-text);
}

.streak-dialog__header {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  background: radial-gradient(circle at 0% 0%, rgba(21, 151, 255, 0.12), transparent 36%);
}

.streak-dialog__dates,
.streak-dialog__actions {
  display: flex;
  align-items: center;
  gap: 14px;
}

.streak-dialog__dates {
  min-width: 0;
}

.streak-dialog__date-block {
  min-width: 0;
}

.streak-dialog__label {
  color: var(--ws-text-muted);
  font-size: 0.78rem;
  font-weight: 600;
}

.streak-dialog__value {
  margin-top: 3px;
  color: var(--ws-text);
  font-weight: 700;
}

.streak-dialog__arrow {
  flex: 0 0 auto;
  color: var(--ws-text-muted);
}

.streak-dialog__actions {
  flex: 0 0 auto;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.streak-dialog__duration {
  color: var(--ws-accent-chip-text);
}

.streak-dialog__close {
  flex: 0 0 auto;
}

.streak-tier-badge {
  display: grid;
  gap: 2px;
  min-width: 92px;
  padding: 7px 12px;
  border: 1px solid var(--ws-border);
  border-radius: 999px;
  background: color-mix(in srgb, var(--ws-surface-muted) 74%, transparent);
}

.streak-tier-badge__label {
  color: var(--ws-text-muted);
  font-size: 0.66rem;
  font-weight: 700;
  line-height: 1;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.streak-tier-badge__value {
  font-size: 0.82rem;
  font-weight: 800;
  line-height: 1.1;
}

.streak-tier-badge.streak-level--gray .streak-tier-badge__value {
  color: var(--ws-text-muted);
}

.streak-tier-badge.streak-level--bronze .streak-tier-badge__value {
  color: #c98242;
}

.streak-tier-badge.streak-level--silver .streak-tier-badge__value {
  color: #cbd8e6;
}

.streak-tier-badge.streak-level--gold .streak-tier-badge__value {
  color: #f4b84a;
}

.streak-tier-badge.streak-level--diamond .streak-tier-badge__value {
  color: #8fe8ff;
}

.streak-dialog__body {
  display: grid;
  gap: 18px;
  min-height: 0;
  overflow: auto;
}

.streak-calendar__toolbar {
  display: grid;
  grid-template-columns: 36px minmax(0, 1fr) 36px;
  align-items: center;
  gap: 10px;
}

.streak-calendar__nav-placeholder {
  width: 36px;
  height: 36px;
}

.streak-calendar__title-block {
  min-width: 0;
  text-align: center;
}

.streak-calendar__title {
  color: var(--ws-text);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: 1.08rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  text-transform: capitalize;
}

.streak-calendar__grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 8px;
  padding: 12px;
  border: 1px solid var(--ws-border);
  border-radius: var(--ws-radius);
  background: var(--ws-table-inset-background);
}

.streak-calendar__weekday {
  color: var(--ws-text-muted);
  font-size: 0.76rem;
  font-weight: 700;
  text-align: center;
}

.streak-calendar__cell,
.streak-calendar__empty,
.streak-calendar__day-shell {
  min-width: 0;
  aspect-ratio: 1;
}

.streak-calendar__day-shell {
  position: relative;
}

.streak-calendar__day {
  width: 100%;
  height: 100%;
  position: relative;
  display: grid;
  place-items: center;
  padding: 0;
  color: var(--ws-text-subtle);
  background: transparent;
  border: 1px solid transparent;
  border-radius: 16px;
  font: inherit;
  font-weight: 700;
}

.streak-calendar__day--active {
  color: #ffffff;
  background: linear-gradient(145deg, var(--ws-accent), #2f6dff);
  border-color: color-mix(in srgb, var(--ws-accent) 72%, white);
  box-shadow: 0 10px 26px rgba(21, 151, 255, 0.22);
  cursor: pointer;
}

.streak-calendar__day--active:hover,
.streak-calendar__day--selected {
  transform: translateY(-1px);
  box-shadow: 0 14px 32px rgba(21, 151, 255, 0.3);
}

.streak-calendar__day:disabled {
  cursor: default;
}

.streak-calendar__day-number {
  position: relative;
  z-index: 1;
}

.streak-calendar__day-marker {
  width: 4px;
  height: 4px;
  position: absolute;
  bottom: 7px;
  left: 50%;
  border-radius: 999px;
  background: #ffffff;
  transform: translateX(-50%);
  opacity: 0.9;
}

:global(.streak-day-menu) {
  max-height: none !important;
  overflow: visible !important;
}

.streak-day-detail {
  min-width: 210px;
  position: relative;
  padding: 12px 14px;
  overflow: visible;
  color: var(--ws-text);
  background: var(--ws-surface-solid);
  border: 1px solid var(--ws-border);
  border-radius: var(--ws-radius-sm);
  box-shadow: var(--ws-shadow-floating);
  white-space: nowrap;
}

.streak-day-detail--inline {
  width: min(100%, 280px);
  justify-self: center;
  text-align: center;
}

.streak-day-detail__date {
  color: var(--ws-text-muted);
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: capitalize;
}

.streak-day-detail__messages {
  margin-top: 4px;
  color: var(--ws-accent-strong);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  letter-spacing: -0.03em;
}

@media (max-width: 620px) {
  .streak-dialog__header {
    align-items: flex-start;
    flex-direction: column;
    padding-right: 52px;
  }

  .streak-dialog__dates {
    width: 100%;
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
    gap: 10px;
  }

  .streak-dialog__date-block:last-child {
    text-align: right;
  }

  .streak-dialog__actions {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
    justify-content: initial;
  }

  .streak-dialog__close {
    position: absolute;
    top: 10px;
    right: 10px;
  }

  .streak-tier-badge,
  .streak-dialog__duration {
    width: 100%;
    min-width: 0;
  }

  .streak-tier-badge {
    justify-items: center;
    padding-inline: 10px;
  }

  .streak-dialog__duration {
    justify-content: center;
  }

  .streak-calendar__grid {
    gap: 5px;
    padding: 8px;
  }

  .streak-calendar__day {
    border-radius: 13px;
    font-size: 0.86rem;
  }
}
</style>
