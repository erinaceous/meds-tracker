import '@mdi/font/css/materialdesignicons.css'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import colors from 'vuetify/util/colors'

export default defineNuxtPlugin((app) => {
  const vuetify = createVuetify({
    theme: {
      defaultTheme: 'light',
      themes: {
        light: {
          dark: false,
          colors: {
            primary: colors.indigo.base,
            secondary: colors.purple.base,
            background: colors.indigo.lighten4,
            surface: colors.indigo.lighten5,
          }
        },
        dark: {
          dark: true,
          colors: {
            primary: colors.indigo.lighten5,
            secondary: colors.purple.lighten5,
            background: colors.indigo.darken4,
            surface: colors.indigo.darken3,
          }
        }
      }
    }
  })
  app.vueApp.use(vuetify)
})
