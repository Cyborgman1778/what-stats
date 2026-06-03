import type { AxiosProgressEvent, AxiosRequestConfig } from 'axios';
import { Capacitor } from '@capacitor/core';
import { apiClient } from './client';
import { normalizeApiError } from './api-errors';
import type { HealthcheckResponse, UploadChatResponse } from './types';
import { normalizeUploadFileNameForBackend } from 'src/utils/files';
import { sanitizeApiBaseUrl } from 'src/utils/config';

const UPLOAD_TIMEOUT_MS = 180000;

function getUploadChatUrl() {
  return `${sanitizeApiBaseUrl(apiClient.defaults.baseURL ?? '')}/upload-chat`;
}

function parseResponseHeaders(rawHeaders: string) {
  const headers: Record<string, string> = {};

  rawHeaders
    .trim()
    .split(/[\r\n]+/)
    .forEach((line) => {
      const separatorIndex = line.indexOf(':');

      if (separatorIndex === -1) return;

      const key = line.slice(0, separatorIndex).trim().toLowerCase();
      const value = line.slice(separatorIndex + 1).trim();

      if (key) {
        headers[key] = value;
      }
    });

  return headers;
}

function parseResponseData(responseText: string, headers: Record<string, string>) {
  if (!headers['content-type']?.includes('application/json')) {
    return responseText;
  }

  try {
    return JSON.parse(responseText) as unknown;
  } catch {
    return responseText;
  }
}

function createNativeXhrError(message: string, xhr: XMLHttpRequest, code?: string) {
  const headers = parseResponseHeaders(xhr.getAllResponseHeaders());
  const data = parseResponseData(xhr.responseText, headers);

  return Object.assign(new Error(message), {
    isAxiosError: true,
    code,
    request: xhr,
    response: xhr.status
      ? {
          data,
          status: xhr.status,
          statusText: xhr.statusText,
          headers
        }
      : undefined
  });
}

function emitNativeUploadProgress(
  event: ProgressEvent,
  onUploadProgress?: (event: AxiosProgressEvent) => void
) {
  if (!onUploadProgress) return;

  const total = event.lengthComputable ? event.total : undefined;

  onUploadProgress({
    loaded: event.loaded,
    total,
    progress: total ? event.loaded / total : undefined
  } as AxiosProgressEvent);
}

function uploadChatWithNativeXhr(
  formData: FormData,
  onUploadProgress?: (event: AxiosProgressEvent) => void
): Promise<UploadChatResponse> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    xhr.open('POST', getUploadChatUrl());
    xhr.timeout = UPLOAD_TIMEOUT_MS;
    xhr.responseType = 'text';
    xhr.setRequestHeader('Accept', 'application/json');

    xhr.upload.onprogress = (event) => emitNativeUploadProgress(event, onUploadProgress);

    xhr.onload = () => {
      const headers = parseResponseHeaders(xhr.getAllResponseHeaders());
      const data = parseResponseData(xhr.responseText, headers);

      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(data as UploadChatResponse);
        return;
      }

      reject(createNativeXhrError(`Request failed with status code ${xhr.status}`, xhr));
    };

    xhr.onerror = () => reject(createNativeXhrError('Network Error', xhr, 'ERR_NETWORK'));
    xhr.ontimeout = () => reject(createNativeXhrError(`timeout of ${UPLOAD_TIMEOUT_MS}ms exceeded`, xhr, 'ECONNABORTED'));

    xhr.send(formData);
  });
}

export async function healthcheck(baseUrl?: string): Promise<HealthcheckResponse> {
  try {
    const config: AxiosRequestConfig = { timeout: 10000 };

    if (baseUrl) {
      config.baseURL = sanitizeApiBaseUrl(baseUrl);
    }

    const response = await apiClient.get<HealthcheckResponse>('/', config);

    return response.data;
  } catch (error) {
    throw normalizeApiError(error);
  }
}

export async function uploadChat(
  file: File,
  onUploadProgress?: (event: AxiosProgressEvent) => void
): Promise<UploadChatResponse> {
  try {
    const formData = new FormData();
    const safeFile = normalizeUploadFileNameForBackend(file);

    formData.append('file', safeFile, safeFile.name);

    if (Capacitor.isNativePlatform()) {
      return await uploadChatWithNativeXhr(formData, onUploadProgress);
    }

    const config: AxiosRequestConfig = {};

    if (onUploadProgress) {
      config.onUploadProgress = onUploadProgress;
    }

    const response = await apiClient.post<UploadChatResponse>('/upload-chat', formData, config);

    return response.data;
  } catch (error) {
    throw normalizeApiError(error);
  }
}
