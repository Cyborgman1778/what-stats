import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useNativeImportStore = defineStore('native-import', () => {
  const pendingFile = ref<File | null>(null);

  function setPendingFile(file: File) {
    pendingFile.value = file;
  }

  function consumePendingFile() {
    const file = pendingFile.value;
    pendingFile.value = null;

    return file;
  }

  return {
    pendingFile,
    setPendingFile,
    consumePendingFile
  };
});
