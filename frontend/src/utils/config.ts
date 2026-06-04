export const API_BASE_URL_STORAGE_KEY = 'whatstats.apiBaseUrl';
export const THEME_STORAGE_KEY = 'whatstats.theme';

export function getDefaultApiBaseUrl() {
  return import.meta.env.VITE_WHATSTATS_API_BASE_URL?.trim() || 'https://api.whatstats.net';
}

export function sanitizeApiBaseUrl(value: string) {
  const trimmed = value.trim();

  if (!trimmed) {
    return getDefaultApiBaseUrl();
  }

  let url: URL;

  try {
    url = new URL(trimmed);
  } catch {
    throw new Error('Introduce una URL valida para el backend.');
  }

  if (url.protocol !== 'http:' && url.protocol !== 'https:') {
    throw new Error('La direccion del backend debe empezar por http:// o https://.');
  }

  if (url.username || url.password) {
    throw new Error('La direccion del backend no debe incluir usuario ni contrasena.');
  }

  if (url.search || url.hash) {
    throw new Error('La direccion del backend no debe incluir parametros ni fragmentos.');
  }

  const path = url.pathname.replace(/\/+$/, '');
  return `${url.origin}${path === '/' ? '' : path}`;
}

export function getInitialApiBaseUrl() {
  return getDefaultApiBaseUrl();
}
