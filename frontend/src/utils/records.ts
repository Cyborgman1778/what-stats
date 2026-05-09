import {
  compareOptionalDates,
  parseDDMMYYYY,
  parseHour,
  parseMMYYYY,
  parseYear
} from './dates';

export interface DataPoint {
  label: string;
  value: number;
}

export function recordToDataPoints(record?: Record<string, number>): DataPoint[] {
  if (!record) return [];

  return Object.entries(record)
    .filter(([, value]) => Number.isFinite(value))
    .map(([label, value]) => ({ label, value }));
}

export function sortRecordByValue(record?: Record<string, number>, direction: 'asc' | 'desc' = 'desc') {
  const multiplier = direction === 'asc' ? 1 : -1;

  return recordToDataPoints(record).sort((a, b) => {
    const byValue = (a.value - b.value) * multiplier;
    return byValue === 0 ? a.label.localeCompare(b.label, 'es') : byValue;
  });
}

export function sortRecordByHour(record?: Record<string, number>) {
  return recordToDataPoints(record).sort((a, b) => parseHour(a.label) - parseHour(b.label));
}

export function sortRecordByDay(record?: Record<string, number>) {
  return recordToDataPoints(record).sort((a, b) => {
    const compared = compareOptionalDates(parseDDMMYYYY(a.label), parseDDMMYYYY(b.label));
    return compared === 0 ? a.label.localeCompare(b.label, 'es') : compared;
  });
}

export function sortRecordByMonth(record?: Record<string, number>) {
  return recordToDataPoints(record).sort((a, b) => {
    const compared = compareOptionalDates(parseMMYYYY(a.label), parseMMYYYY(b.label));
    return compared === 0 ? a.label.localeCompare(b.label, 'es') : compared;
  });
}

export function sortRecordByYear(record?: Record<string, number>) {
  return recordToDataPoints(record).sort((a, b) => {
    const compared = compareOptionalDates(parseYear(a.label), parseYear(b.label));
    return compared === 0 ? a.label.localeCompare(b.label, 'es') : compared;
  });
}

export function limitDataPoints(points: DataPoint[], limit: number) {
  return points.slice(0, limit);
}