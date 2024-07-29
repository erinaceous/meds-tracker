<script lang="ts">
import { defineComponent } from "vue";
import StockScore from "./StockScore.vue";

export default defineComponent({
  name: "StockReport",
  components: {
    StockScore,
  },
  props: {
    report: {
      type: Object,
      default: null,
    },
    showTrend: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      medication: undefined,
      pharmacy: undefined,
    };
  },
  async mounted() {
    if (!this.report) {
      return;
    }
    this.medication = await this.getMedication(this.report.medication_uid);
    this.pharmacy = await this.getPharmacy(this.report.pharmacy_uid);
  },
  methods: {
    async getPharmacy(pharmacy_uid: string) {
      return $fetch(
        `${this.$config.public.api.root}/pharmacies/${pharmacy_uid}`,
      );
    },
    async getMedication(medication_uid: string) {
      return $fetch(
        `${this.$config.public.api.root}/medications/${medication_uid}`,
      );
    },
  },
});
</script>

<template>
  <v-card
    variant="flat"
    rounded="lg"
    class="fill-height d-flex flex-column"
    elevation="12"
    color="primary"
  >
    <v-card rounded="lg" elevation="2" color="#000000">
      <v-list>
        <v-list-item>
          <template #prepend>
            <v-icon> mdi-hospital-box-outline </v-icon>
          </template>
          <v-card-title v-if="pharmacy" class="text-wrap">
            {{ pharmacy?.name }}
          </v-card-title>
          <v-card-subtitle v-if="pharmacy" class="text-wrap">
            <p class="text-pre-line">
              {{ pharmacy?.address }}
            </p>
            <p>
              {{ pharmacy?.postcode }}
            </p>
          </v-card-subtitle>
        </v-list-item>
        <v-divider class="mt-2" thickness="2" />
        <v-list-item>
          <template #prepend>
            <v-icon> mdi-medication </v-icon>
          </template>
          <v-card-title class="text-wrap">
            {{
              medication?.product ? medication?.product : medication?.category
            }}
          </v-card-title>
          <v-card-subtitle v-if="medication?.product" class="text-wrap">
            {{ medication?.category }}
          </v-card-subtitle>
        </v-list-item>
        <v-divider class="mt-2 mb-2" thickness="2" />
        <v-list-item>
          <template #prepend>
            <v-icon :disabled="!report?.dosage"> mdi-pill-multiple </v-icon>
          </template>
          <v-card-title class="text-wrap">
            <span v-if="!report?.dosage" class="text-grey">
              Not known / not applicable
            </span>
            <span v-else>
              {{ report?.dosage }}
            </span>
          </v-card-title>
        </v-list-item>
      </v-list>
    </v-card>
    <stock-score :show-trend="showTrend" :report="report" />
  </v-card>
</template>

<style scoped></style>
