import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.whatstats.app',
  appName: 'WhatStats',
  webDir: 'www',
  bundledWebRuntime: false,
  plugins: {
    SplashScreen: {
      launchShowDuration: 0
    }
  },
  server: {
    androidScheme: 'https'
  }
};

export default config;