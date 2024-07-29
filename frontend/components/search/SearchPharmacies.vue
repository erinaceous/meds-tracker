<script lang="ts">
import { defineComponent } from "vue";
import SearchItems from "./SearchItems.vue";
import AddPharmacy from "~/components/reports/AddPharmacy.vue";

export default defineComponent({
  name: "SearchPharmacies",
  components: {
    AddPharmacy,
    SearchItems,
  },
  props: {
    editable: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      showDialog: false,
    };
  },
  methods: {
    async getItems(search) {
      return $fetch(
        `${this.$config.public.api.root}/pharmacies/autocomplete/${search}`,
      ).then((response) => {
        return response.map((pharmacy) => {
          return {
            ...pharmacy,
            title: pharmacy.name,
            subtitle: pharmacy.postcode,
            value: pharmacy.postcode,
          };
        });
      });
    },
  },
});
</script>

<template>
  <v-dialog v-model="showDialog" class="w-auto w-xl-25 w-lg-33 w-md-50 w-sm-75">
    <add-pharmacy
      @submitted="
        (result) => {
          $emit('update:modelValue', result);
          showDialog = false;
        }
      "
      @cancel="showDialog = false"
    />
  </v-dialog>
  <search-items
    v-bind="$attrs"
    :get-items-function="getItems"
    :min-characters="3"
    placeholder="Search by postcode"
  >
    <template #empty-data>
      <v-list-item class="text-wrap text-disabled">
        No pharmacies found matching your search.
        <a
          v-if="editable"
          href
          class="font-weight-bold"
          @click.prevent="showDialog = true"
        >
          Click here to manually enter details.
        </a>
      </v-list-item>
    </template>
    <template #item-subtitle="{ item }">
      <div class="d-flex">
        <v-list-item-subtitle class="flex-grow-1">
          {{ item.raw.address.replace("\n", ", ") }}
        </v-list-item-subtitle>
        <v-list-item-subtitle class="flex-shrink-0 ml-3">
          <strong>{{ item.raw.postcode }}</strong>
        </v-list-item-subtitle>
      </div>
    </template>
  </search-items>
</template>

<style scoped></style>
