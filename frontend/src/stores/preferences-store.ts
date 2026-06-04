import { defineStore } from 'pinia';
import { Dark, LocalStorage } from 'quasar';
import { ref } from 'vue';
import {
  API_BASE_URL_STORAGE_KEY,
  THEME_STORAGE_KEY,
  getDefaultApiBaseUrl,
  sanitizeApiBaseUrl
} from 'src/utils/config';
import { setApiBaseUrl } from 'src/services/api/client';

export type ThemePreference = 'light' | 'dark' | 'auto';

export const usePreferencesStore = defineStore('preferences', () => {
  const theme = ref<ThemePreference>('auto');
  const apiBaseUrl = ref(getDefaultApiBaseUrl());
  const hasHydrated = ref(false);

  function applyTheme() {
    if (theme.value === 'auto') {
      Dark.set('auto');
      return;
    }

    Dark.set(theme.value === 'dark');
  }

  function initPreferences() {
    if (hasHydrated.value) return;

    const storedTheme = LocalStorage.getItem(THEME_STORAGE_KEY);
    const storedApiUrl = LocalStorage.getItem(API_BASE_URL_STORAGE_KEY);

    if (storedTheme === 'light' || storedTheme === 'dark' || storedTheme === 'auto') {
      theme.value = storedTheme;
    }

    if (typeof storedApiUrl === 'string' && storedApiUrl.trim().length > 0) {
      try {
        apiBaseUrl.value = sanitizeApiBaseUrl(storedApiUrl);
      } catch {
        LocalStorage.remove(API_BASE_URL_STORAGE_KEY);
        apiBaseUrl.value = getDefaultApiBaseUrl();
      }
    }

    setApiBaseUrl(apiBaseUrl.value);
    applyTheme();
    hasHydrated.value = true;
  }

  function setTheme(nextTheme: ThemePreference) {
    theme.value = nextTheme;
    LocalStorage.set(THEME_STORAGE_KEY, nextTheme);
    applyTheme();
  }

  function setBackendUrl(nextUrl: string) {
    const sanitized = sanitizeApiBaseUrl(nextUrl);
    apiBaseUrl.value = sanitized;
    LocalStorage.set(API_BASE_URL_STORAGE_KEY, sanitized);
    setApiBaseUrl(sanitized);
  }

  return {
    theme,
    apiBaseUrl,
    hasHydrated,
    initPreferences,
    setTheme,
    setBackendUrl,
    applyTheme
  };
});
