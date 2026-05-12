import axios from 'axios';

export type ApiErrorKind =
  | 'bad-request'
  | 'too-large'
  | 'rate-limit'
  | 'validation'
  | 'server'
  | 'network'
  | 'unknown';

export interface NormalizedApiError extends Error {
  name: 'WhatStatsApiError';
  kind: ApiErrorKind;
  status?: number;
  detail?: string;
  userMessage: string;
  technicalMessage?: string;
  retryAfterSeconds?: number;
  troubleshooting?: string[];
}

interface NormalizedApiErrorInput {
  kind: ApiErrorKind;
  status?: number | undefined;
  detail?: string | undefined;
  userMessage: string;
  technicalMessage?: string | undefined;
  retryAfterSeconds?: number | undefined;
  troubleshooting?: string[] | undefined;
}

function createNormalizedApiError(input: NormalizedApiErrorInput): NormalizedApiError {
  const error = new Error(input.technicalMessage ?? input.userMessage) as NormalizedApiError;

  Object.assign(error, input);
  error.name = 'WhatStatsApiError';

  return error;
}

function extractDetail(data: unknown): string | undefined {
  if (!data || typeof data !== 'object') return undefined;

  const record = data as Record<string, unknown>;
  const detail = record.detail;

  if (typeof detail === 'string') return detail;

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (item && typeof item === 'object' && 'msg' in item) {
          return String((item as { msg: unknown }).msg);
        }

        return JSON.stringify(item);
      })
      .join('\n');
  }

  if (typeof record.message === 'string') return record.message;

  return undefined;
}

function parseRetryAfter(value: unknown): number | undefined {
  if (typeof value !== 'string') return undefined;

  const numeric = Number(value);
  if (Number.isFinite(numeric)) return numeric;

  const parsedDate = Date.parse(value);
  if (Number.isNaN(parsedDate)) return undefined;

  return Math.max(0, Math.ceil((parsedDate - Date.now()) / 1000));
}

export function normalizeApiError(error: unknown): NormalizedApiError {
  if (!axios.isAxiosError(error)) {
    return createNormalizedApiError({
      kind: 'unknown',
      userMessage: 'Ha ocurrido un error inesperado al procesar la solicitud.',
      technicalMessage: error instanceof Error ? error.message : String(error)
    });
  }

  if (!error.response) {
    return createNormalizedApiError({
      kind: 'network',
      userMessage:
        'No se pudo conectar con el servicio. Comprueba tu conexión e inténtalo de nuevo.',
      technicalMessage: error.message
    });
  }

  const status = error.response.status;
  const detail = extractDetail(error.response.data);
  const retryAfterSeconds = parseRetryAfter(error.response.headers?.['retry-after']);

  if (status === 400) {
    return createNormalizedApiError({
      kind: 'bad-request',
      status,
      detail,
      userMessage: detail ?? 'El archivo no es válido o no se ha podido procesar.'
    });
  }

  if (status === 413) {
    return createNormalizedApiError({
      kind: 'too-large',
      status,
      detail,
      userMessage: detail ?? 'El archivo supera el tamaño máximo permitido (50 MB).'
    });
  }

  if (status === 429) {
    return createNormalizedApiError({
      kind: 'rate-limit',
      status,
      detail,
      retryAfterSeconds,
      userMessage:
        'Has superado el límite temporal de peticiones. Espera unos segundos antes de volver a intentarlo.'
    });
  }

  if (status === 422) {
    return createNormalizedApiError({
      kind: 'validation',
      status,
      detail,
      userMessage:
        detail ?? 'El formulario enviado no es válido. Revisa que se haya adjuntado el archivo correctamente.'
    });
  }

  if (status >= 500) {
    return createNormalizedApiError({
      kind: 'server',
      status,
      detail,
      userMessage:
        detail ??
        'El servicio no ha podido completar el análisis. Prueba con otro archivo o inténtalo más tarde.'
    });
  }

  return createNormalizedApiError({
    kind: 'unknown',
    status,
    detail,
    userMessage: detail ?? 'El servicio ha devuelto una respuesta no esperada.',
    technicalMessage: error.message
  });
}
