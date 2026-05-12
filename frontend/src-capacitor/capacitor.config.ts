import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.whatstats.app',
  appName: 'WhatStats',
  webDir: 'www',
  bundledWebRuntime: false,
  plugins: {
    CapacitorHttp: {
      enabled: true
    },
    SplashScreen: {
      launchShowDuration: 0
    }
  },
  server: {
    androidScheme: 'https',
    cleartext: true
  }
};

export default config;
