import { defineConfig } from '#q-app/wrappers';

export default defineConfig((ctx) => ({
  boot: ['axios', 'echarts'],

  css: ['app.scss'],

  sassVariables: 'src/css/quasar.variables.scss',

  extras: ['material-icons', 'material-symbols-outlined'],

  build: {
    target: {
      browser: ['es2022', 'firefox115', 'chrome115', 'safari15'],
      node: 'node20'
    },
    vueRouterMode: 'hash',
    typescript: {
      strict: true,
      vueShim: true
    },
    env: {
      APP_PLATFORM: ctx.modeName
    }
  },

  devServer: {
    open: false
  },

  framework: {
    config: {
      dark: 'auto',
      brand: {
        primary: '#0f766e',
        secondary: '#0ea5e9',
        accent: '#22c55e',
        dark: '#0f172a',
        positive: '#16a34a',
        negative: '#dc2626',
        info: '#0284c7',
        warning: '#d97706'
      }
    },
    plugins: ['Notify', 'Loading', 'Dialog', 'LocalStorage']
  },

  animations: [],

  capacitor: {
    hideSplashscreen: true
  }
}));