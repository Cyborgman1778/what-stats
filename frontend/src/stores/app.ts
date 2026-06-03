import { defineStore } from 'pinia';
import { ref } from 'vue';
import { Dark, LocalStorage } from 'quasar';

const DEFAULT_API_BASE_URL = 'https://api.whatstats.net';

const getStoredTheme = () => {
  const storedTheme = LocalStorage.getItem('theme-dark');
  return typeof storedTheme === 'boolean' ? storedTheme : Dark.isActive;
};

const getStoredApiBaseUrl = () => {
  const storedApiBaseUrl = LocalStorage.getItem('api-base-url');

  if (typeof storedApiBaseUrl === 'string' && storedApiBaseUrl.trim() !== '') {
    return storedApiBaseUrl.trim();
  }

  return DEFAULT_API_BASE_URL;
};

export const useAppStore = defineStore('app', () => {
  const isDark = ref(getStoredTheme());
  const apiBaseUrl = ref(getStoredApiBaseUrl());

  Dark.set(isDark.value);

  const setDarkMode = (val: boolean) => {
    isDark.value = val;
    Dark.set(val);
    LocalStorage.set('theme-dark', val);
  };

  const setApiBaseUrl = (url: string) => {
    const normalizedUrl = url.trim() || DEFAULT_API_BASE_URL;

    apiBaseUrl.value = normalizedUrl;
    LocalStorage.set('api-base-url', normalizedUrl);
  };

  return { isDark, apiBaseUrl, setDarkMode, setApiBaseUrl };
});
