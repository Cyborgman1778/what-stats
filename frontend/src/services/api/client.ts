import axios from 'axios';
import { sanitizeApiBaseUrl } from 'src/utils/config';

export const apiClient = axios.create({
  timeout: 180000,
  headers: {
    Accept: 'application/json'
  }
});

export function setApiBaseUrl(baseUrl: string) {
  apiClient.defaults.baseURL = sanitizeApiBaseUrl(baseUrl);
}
