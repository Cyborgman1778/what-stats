export function formatNumber(value: number) {
  return new Intl.NumberFormat('es-ES').format(value);
}

export function formatBytes(bytes: number) {
  if (bytes === 0) return '0 B';

  const units = ['B', 'KB', 'MB', 'GB'];
  const index = Math.floor(Math.log(bytes) / Math.log(1024));
  const value = bytes / Math.pow(1024, index);

  return `${value.toFixed(value >= 10 ? 0 : 1)} ${units[index]}`;
}

export function pluralize(value: number, singular: string, plural: string) {
  return value === 1 ? singular : plural;
}

export function truncateText(value: string, maxLength = 160) {
  if (value.length <= maxLength) return value;
  return `${value.slice(0, maxLength).trim()}…`;
}