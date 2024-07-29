// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      api: {
        root: '/api'
      }
    }
  },
  meta: {
    title: 'UK medication supply tracker'
  },
  compatibilityDate: '2024-04-03',
  ssr: true,
  devtools: { enabled: true },
  build: {
    transpile: ['vuetify'],
    sourcemap: true
  },
  plugins: ['~/plugins/vuetify', '~/plugins/localstorage', '~/plugins/api_client', '~/plugins/v_focus.client'],
  modules: [
    (_options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) => {
        // @ts-expect-error
        config.plugins.push(vuetify({ autoImport: true }))
      })
    },
    'nuxt-lodash',
    '@vite-pwa/nuxt',
    '@nuxt/eslint',
    //'@nuxtjs/sentry'
  ],
  vite: {
    server: {
      headers: {
        'Cross-Origin-Opener-Policy': 'same-origin',
        'Cross-Origin-Embedder-Policy': 'require-corp',
      },
    },
    optimizeDeps: {
      exclude: ['@sqlite.org/sqlite-wasm'],
    },
    vue: {
      template: {
        transformAssetUrls,
        compilerOptions: {
          isCustomElement: (tag) => ['altcha-widget'].includes(tag)
        }
      },
    },
  }
})