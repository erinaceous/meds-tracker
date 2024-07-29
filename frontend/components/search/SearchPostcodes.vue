<script lang="ts">
import { defineComponent } from "vue";
import SearchItems from "./SearchItems.vue";
import { VCombobox } from "vuetify/components";

export default defineComponent({
  name: "SearchPostcodes",
  components: {
    SearchItems,
  },
  computed: {
    VCombobox() {
      return VCombobox;
    },
  },
  methods: {
    async getPostcode(postcode: str) {
      return $fetch(`https://api.postcodes.io/postcodes/${postcode}`).then(
        (response) => {
          return {
            latitude: response.result.latitude,
            longitude: response.result.longitude,
          };
        },
      );
    },
    async getItems(search: str) {
      search = search.toLowerCase().replace(" ", "");
      return $fetch(
        `https://api.postcodes.io/postcodes/${search}/autocomplete`,
      ).then((response) => {
        return response.result || undefined;
      });
    },
  },
});
</script>

<template>
  <search-items
    v-bind="$attrs"
    :component="VCombobox"
    :get-items-function="getItems"
    :min-characters="2"
    placeholder="Start typing a postcode"
  />
</template>

<style scoped></style>
