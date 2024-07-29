<script lang="ts">
import { defineComponent } from "vue";
import VerifyButton from "./VerifyButton.vue";
import SearchPostcodes from "~/components/search/SearchPostcodes.vue";

export default defineComponent({
  name: "AddPharmacy",
  components: {
    VerifyButton,
    SearchPostcodes,
  },
  data() {
    return {
      name: undefined,
      address: undefined,
      postcode: undefined,
      url: undefined,
      loading: false,
      error: undefined,
    };
  },
  mounted() {
    this.clear();
  },
  methods: {
    clear() {
      this.name = undefined;
      this.address = undefined;
      this.postcode = undefined;
      this.url = undefined;
      this.loading = false;
      this.error = undefined;
    },
    async submitPharmacy() {
      this.loading = true;
      const result = await $fetch(
        `${this.$config.public.api.root}/pharmacies`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${this.$localStorage.getItem("signature")}`,
          },
          body: {
            name: this.name,
            address: this.address,
            postcode: this.postcode,
            url: this.url,
          },
        },
      ).then((pharmacy) => {
        return {
          ...pharmacy,
          title: pharmacy.name,
          subtitle: pharmacy.postcode,
          value: pharmacy.postcode,
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
    <v-card-title> Add a new pharmacy </v-card-title>
    <v-card-text>
      Let us know about a pharmacy missing from our database here.
    </v-card-text>
    <v-list density="compact">
      <v-list-subheader>
        Pharmacy company name
        <span class="text-error">&ast;</span>
      </v-list-subheader>
      <v-list-item>
        <v-text-field
          v-model="name"
          single-line
          hide-details
          placeholder="e.g. Boots or Superdrug"
          variant="outlined"
        />
      </v-list-item>
      <v-list-subheader>
        Postcode
        <span class="text-error">&ast;</span>
      </v-list-subheader>
      <v-list-item>
        <search-postcodes v-model="postcode" hide-details variant="outlined" />
      </v-list-item>
      <v-list-subheader> Address </v-list-subheader>
      <v-list-item>
        <v-textarea
          v-model="address"
          multi-line
          hide-details
          placeholder="Enter full address if known (without postcode)"
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
        :disabled="!name || !postcode"
        size="large"
        @verified="submitPharmacy"
      />
    </v-card-actions>
  </v-card>
</template>

<style scoped></style>
