<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "SiteBanner",
});
</script>

<template>
  <head>
    <title>UK pharmacy supply tracker</title>
  </head>
  <v-row class="mb-2">
    <v-col cols="auto">
      <v-card
        rounded="lg"
        class="pa-4 d-flex align-center flex-wrap flex-grow-1 justify-center flex-column"
        color="primary"
        variant="tonal"
      >
        <div class="d-flex align-self-center">
          <div class="mr-4">
            <h1>🇬🇧 ⚕️</h1>
          </div>
          <div class="mr-4">
            <h2 class="font-weight-black">
              UK
              <span class="text-primary">crowd-sourced</span>
              pharmacy medication
              <span class="text-secondary">supply</span>
              tracker
            </h2>
          </div>
        </div>
        <v-spacer />
        <div>
          <v-btn-group variant="tonal">
            <v-btn
              :color="$route.path === '/' ? 'secondary' : 'primary'"
              size="large"
              prepend-icon="mdi-magnify"
              @click="$route.path !== '/' ? $router.push({ path: '/' }) : false"
            >
              Search
            </v-btn>
            <v-btn
              :color="$route.path === '/reports/new' ? 'secondary' : 'primary'"
              size="large"
              prepend-icon="mdi-pen-plus"
              @click="
                $route.path !== '/reports/new'
                  ? $router.push({ path: '/reports/new' })
                  : false
              "
            >
              Add reports
            </v-btn>
          </v-btn-group>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>
