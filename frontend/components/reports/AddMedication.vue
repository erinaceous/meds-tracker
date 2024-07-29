<script lang="ts">
import { defineComponent } from "vue";
import VerifyButton from "./VerifyButton.vue";

export default defineComponent({
  name: "AddMedication",
  components: {
    VerifyButton,
  },
  data() {
    return {
      categories: [],
      category: undefined,
      product: undefined,
      url: undefined,
      loading: false,
      error: undefined,
    };
  },
  async mounted() {
    this.clear();
    this.categories = await this.getCategories();
  },
  methods: {
    clear() {
      this.category = undefined;
      this.product = undefined;
      this.url = undefined;
      this.loading = false;
      this.error = undefined;
    },
    async getCategories() {
      return $fetch(`${this.$config.public.api.root}/medications/categories`);
    },
    async submitMedication(altcha) {
      this.loading = true;
      const result = await $fetch(
        `${this.$config.public.api.root}/medications`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${altcha.signature}`,
          },
          body: {
            category: this.category,
            product: this.product,
            url: this.url,
          },
        },
      ).then((medication) => {
        let name = medication.category;
        if (medication.product) {
          name += `: ${medication.product}`;
        }
        return {
          ...medication,
          title: medication.product || medication.category,
          subtitle: medication.product ? medication.category : undefined,
          value: name,
        };
      });
      this.loading = false;
      this.$emit("submitted", result);
      this.clear();
    },
  },
});
</script>

<template>
  <v-card rounded="lg">
    <v-card-title> Add a new medication </v-card-title>
    <v-card-text>
      Let us know about a medication missing from our database here.
    </v-card-text>
    <v-list density="compact">
      <v-list-subheader>
        Medication category
        <span class="text-error">&ast;</span>
      </v-list-subheader>
      <v-list-item>
        <v-combobox
          v-model="category"
          :items="categories"
          single-line
          hide-details
          variant="outlined"
          placeholder="Choose existing category or enter a new one"
        />
      </v-list-item>
      <v-list-subheader> Product name </v-list-subheader>
      <v-list-item>
        <v-text-field
          v-model="product"
          placeholder="Leave blank if generic"
          single-line
          hide-details
          variant="outlined"
        />
      </v-list-item>
      <v-list-subheader> Website link </v-list-subheader>
      <v-list-item>
        <v-text-field
          v-model="url"
          placeholder="https://"
          single-line
          hide-details
          variant="outlined"
        />
      </v-list-item>
    </v-list>
    <v-card-actions class="justify-end">
      <v-btn variant="text" @click="$emit('cancel')"> Cancel </v-btn>
      <verify-button
        color="primary"
        :disabled="!category"
        size="large"
        @verified="submitMedication"
      />
    </v-card-actions>
  </v-card>
</template>

<style scoped></style>
