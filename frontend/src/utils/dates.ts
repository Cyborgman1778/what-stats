export function parseDDMMYYYY(value: string): Date | null {
  const match = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(value);
  if (!match) return null;

  const [, day, month, year] = match;
  return new Date(Number(year), Number(month) - 1, Number(day));
}

export function parseMMYYYY(value: string): Date | null {
  const match = /^(\d{2})\/(\d{4})$/.exec(value);
  if (!match) return null;

  const [, month, year] = match;
  return new Date(Number(year), Number(month) - 1, 1);
}

export function parseYear(value: string): Date | null {
  const match = /^(\d{4})$/.exec(value);
  if (!match) return null;

  return new Date(Number(value), 0, 1);
}

export function parseHour(value: string): number {
  const match = /^(\d{1,2}):/.exec(value);
  if (!match) return Number.MAX_SAFE_INTEGER;
  return Number(match[1]);
}

export function compareOptionalDates(a: Date | null, b: Date | null) {
  if (a && b) return a.getTime() - b.getTime();
  if (a) return -1;
  if (b) return 1;
  return 0;
}

export function formatIsoDate(value: string) {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat('es-ES', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  }).format(date);
}

export function formatDateTime(value: string) {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat('es-ES', {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(date);
}