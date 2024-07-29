<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "SiteFooter"
})
</script>

<template>
  <v-footer class="flex-grow-0 mt-4" rounded="lg">
    <slot name="page-footer">
      <NuxtLink
          v-if="$route.path !== '/about'"
          to="/about"
      >
        <v-btn
            color="primary"
            prepend-icon="mdi-information-slab-circle"
            variant="text"
        >
          What is this website?
        </v-btn>
      </NuxtLink>
      <v-btn
          v-else
          color="primary"
          variant="text"
          @click="$router.back()"
          prepend-icon="mdi-arrow-left-circle"
      >
        Go back
      </v-btn>
    </slot>
  </v-footer>
</template>