export const API_BASE_URL_STORAGE_KEY = 'whatstats.apiBaseUrl';
export const THEME_STORAGE_KEY = 'whatstats.theme';

export function getDefaultApiBaseUrl() {
  return import.meta.env.VITE_WHATSTATS_API_BASE_URL?.trim() || 'http://127.0.0.1:8000';
}

export function sanitizeApiBaseUrl(value: string) {
  const trimmed = value.trim();

  if (!trimmed) {
    return getDefaultApiBaseUrl();
  }

  return trimmed.replace(/\/+$/, '');
}

export function getInitialApiBaseUrl() {
  return getDefaultApiBaseUrl();
}