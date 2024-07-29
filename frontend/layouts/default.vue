<script lang="ts">
import { defineComponent } from "vue";
import SiteBanner from "~/components/SiteBanner.vue";
import SiteFooter from "~/components/SiteFooter.vue";

export default defineComponent({
  name: "DefaultLayout",
  components: {
    SiteBanner,
    SiteFooter,
  },
});
</script>

<template>
  <v-app full-height>
    <v-container fluid class="d-flex flex-column fill-height">
      <site-banner />
      <slot>
        <v-row>
          <v-col>
            <v-empty-state
              headline="Whoops, 404"
              title="Page not found"
              text="The page you were looking for does not exist"
            />
          </v-col>
        </v-row>
      </slot>
      <v-spacer />
      <site-footer />
    </v-container>
  </v-app>
</template>

<style></style>
