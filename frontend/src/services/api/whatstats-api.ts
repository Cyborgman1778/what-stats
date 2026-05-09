import type { AxiosProgressEvent, AxiosRequestConfig } from 'axios';
import { apiClient } from './client';
import { normalizeApiError } from './api-errors';
import type { HealthcheckResponse, UploadChatResponse } from './types';
import { normalizeUploadFileNameForBackend } from 'src/utils/files';
import { sanitizeApiBaseUrl } from 'src/utils/config';

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
