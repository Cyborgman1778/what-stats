import { boot } from 'quasar/wrappers';
import { apiClient, setApiBaseUrl } from 'src/services/api/client';
import { getInitialApiBaseUrl } from 'src/utils/config';

export default boot(({ app }) => {
  setApiBaseUrl(getInitialApiBaseUrl());
  app.config.globalProperties.$api = apiClient;
});

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $api: typeof apiClient;
  }
}