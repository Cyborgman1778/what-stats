export const MAX_UPLOAD_SIZE_BYTES = 50 * 1024 * 1024;
export const ACCEPTED_EXTENSIONS = ['txt', 'zip'] as const;

export interface FileValidationResult {
  valid: boolean;
  message?: string;
}

export function getFileExtension(fileName: string) {
  const parts = fileName.split('.');
  return parts.length > 1 ? parts.at(-1)?.toLowerCase() ?? '' : '';
}

export function validateChatFile(file: File | null): FileValidationResult {
  if (!file) {
    return {
      valid: false,
      message: 'Selecciona un archivo exportado de WhatsApp.'
    };
  }

  const extension = getFileExtension(file.name);

  if (!ACCEPTED_EXTENSIONS.includes(extension as 'txt' | 'zip')) {
    return {
      valid: false,
      message: 'Solo se admiten archivos .txt o .zip exportados desde WhatsApp.'
    };
  }

  if (file.size > MAX_UPLOAD_SIZE_BYTES) {
    return {
      valid: false,
      message: 'El archivo supera el tamaño máximo permitido de 50 MB.'
    };
  }

  return { valid: true };
}

export function normalizeUploadFileNameForBackend(file: File) {
  const extension = getFileExtension(file.name);
  const hasUppercaseExtension = /\.(TXT|ZIP)$/.test(file.name);

  if (!hasUppercaseExtension) {
    return file;
  }

  const withoutExtension = file.name.replace(/\.(TXT|ZIP)$/, '');
  const normalizedName = `${withoutExtension}.${extension}`;

  return new File([file], normalizedName, {
    type: file.type,
    lastModified: file.lastModified
  });
}