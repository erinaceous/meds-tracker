<script lang="ts">
import { defineComponent } from "vue";
import SearchReports from "~/components/search/SearchReports.vue";
import StockReport from "~/components/reports/StockReport.vue";

export default defineComponent({
  name: "IndexPage",
  components: {
    SearchReports,
    StockReport,
  },
  data() {
    return {
      reports: undefined,
      loading: false,
      error: undefined,
    };
  },
  mounted() {
    this.reports = undefined;
    this.loading = false;
    this.error = undefined;
  },
  methods: {
    onSearchReports(reports) {
      this.error = undefined;
      this.loading = false;
      this.reports = reports;
    },
    onSearchError(error) {
      this.error = error;
    },
  },
});
</script>

<template>
  <v-row class="mb-2 d-flex align-center justify-center w-100">
    <v-slide-y-transition leave-absolute>
      <v-col cols="auto" sm="12" md="8" lg="6" xl="4" class="flex-grow-1">
        <search-reports
          class="flex-grow-1"
          @loading="
            (val) => {
              loading = val;
            }
          "
          @search-reports="onSearchReports"
          @search-error="onSearchError"
        />
      </v-col>
    </v-slide-y-transition>
  </v-row>
  <v-row class="d-flex align-center justify-center w-100">
    <v-fade-transition leave-absolute group>
      <v-col
        v-for="report in reports"
        :key="report._id"
        cols="auto"
        sm="12"
        md="6"
        lg="4"
        xl="3"
        class="flex-grow-1"
      >
        <div>
          <stock-report :report="report" />
        </div>
      </v-col>
      <v-col
        v-if="error || (reports && reports.length === 0)"
        key="no-results"
        cols="auto"
        sm="12"
        md="6"
        lg="4"
        xl="3"
        class="flex-grow-1"
      >
        <v-card
          variant="outlined"
          class="mt-2 d-flex flex-column justify-center"
          :color="error ? 'error' : undefined"
        >
          <v-card-title v-if="error">
            <v-icon>mdi-wrench-cog-outline</v-icon>
            Something went wrong
          </v-card-title>
          <v-card-title v-else>
            <v-icon>mdi-invoice-text-clock</v-icon>
            No results yet
          </v-card-title>
          <v-card-text v-if="error">
            <p>
              We tried to search our database, but something unexpected happened
              on the server.
            </p>
            <p class="mt-4">
              The problem may be temporary - try searching again in a minute.
            </p>
          </v-card-text>
          <v-card-text v-else>
            <p>
              Your search returned no results for your selection of medications
              at these pharmacies for this point in time.
            </p>
            <p class="mt-4">
              We rely on anonymous reporting from the public to build up our
              database of medication availability in pharmacies nation-wide.
            </p>
            <p class="mt-4">
              You can check again in a few hours or tomorrow - some reports are
              pending a human review process, where a new pharmacy, medication
              or dosage has been entered.
            </p>
            <p class="mt-4">
              You can help us grow our database by
              <NuxtLink to="/reports/new" class="font-weight-bold">
                submitting reports of your own </NuxtLink
              >.
            </p>
          </v-card-text>
          <v-card-text v-if="error" class="mt-4 mb-6">
            <p>Details of the error message:</p>
            <pre class="border pa-1 text-pre-wrap fill-height overflow-auto">{{
              error?.detail || error.toString()
            }}</pre>
          </v-card-text>
        </v-card>
      </v-col>
    </v-fade-transition>
  </v-row>
</template>

<style></style>
