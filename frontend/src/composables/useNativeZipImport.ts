import { App } from '@capacitor/app';
import { Capacitor } from '@capacitor/core';
import { Notify } from 'quasar';
import { useRouter } from 'vue-router';
import { useNativeImportStore } from 'src/stores/native-import-store';
import { validateChatFile } from 'src/utils/files';

let initPromise: Promise<void> | null = null;
const processedNativeUrls = new Set<string>();

function isZipUrl(nativeUrl: string) {
  const cleanUrl = nativeUrl.split(/[?#]/)[0]?.toLowerCase() ?? '';
  return cleanUrl.endsWith('.zip');
}

function getFileNameFromNativeUrl(nativeUrl: string) {
  try {
    const path = new URL(nativeUrl).pathname;
    const fileName = path.split('/').filter(Boolean).at(-1);

    if (fileName) {
      return decodeURIComponent(fileName);
    }
  } catch {
    const cleanPath = nativeUrl.split(/[?#]/)[0] ?? '';
    const fileName = cleanPath.split('/').filter(Boolean).at(-1);

    if (fileName) {
      return decodeURIComponent(fileName);
    }
  }

  return 'whatsapp-chat.zip';
}

async function createFileFromNativeUrl(nativeUrl: string) {
  const response = await fetch(Capacitor.convertFileSrc(nativeUrl));

  if (!response.ok) {
    throw new Error('No se pudo leer el ZIP recibido.');
  }

  const blob = await response.blob();
  const fileName = getFileNameFromNativeUrl(nativeUrl);

  return new File([blob], fileName, {
    type: blob.type || 'application/zip',
    lastModified: Date.now()
  });
}

export function useNativeZipImport() {
  const router = useRouter();
  const nativeImportStore = useNativeImportStore();

  async function handleNativeUrl(nativeUrl?: string) {
    if (!nativeUrl || processedNativeUrls.has(nativeUrl) || !isZipUrl(nativeUrl)) {
      return;
    }

    processedNativeUrls.add(nativeUrl);

    try {
      const file = await createFileFromNativeUrl(nativeUrl);
      const validation = validateChatFile(file);

      if (!validation.valid) {
        Notify.create({
          type: 'warning',
          message: validation.message ?? 'El ZIP recibido no es válido.'
        });

        return;
      }

      nativeImportStore.setPendingFile(file);

      if (router.currentRoute.value.name !== 'home') {
        await router.push({ name: 'home' });
      }

      Notify.create({
        type: 'positive',
        message: 'ZIP cargado. Pulsa Analizar para enviarlo al backend.'
      });
    } catch {
      Notify.create({
        type: 'negative',
        message: 'No se pudo cargar el ZIP recibido.'
      });
    }
  }

  function initNativeZipImport() {
    if (!Capacitor.isNativePlatform()) {
      return Promise.resolve();
    }

    initPromise ??= (async () => {
      await App.addListener('appUrlOpen', (event) => {
        void handleNativeUrl(event.url);
      });

      const launchUrl = await App.getLaunchUrl();
      await handleNativeUrl(launchUrl?.url);
    })();

    return initPromise;
  }

  return {
    initNativeZipImport
  };
}
