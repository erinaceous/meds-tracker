<script lang="ts">
import {defineComponent} from 'vue'
import SearchReports from '~/components/search/SearchReports.vue'
import StockReport from '~/components/reports/StockReport.vue'

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
    }
  },
  computed: {
    rowClasses() {
      return {
        'mb-2': true,
        'ml-n7': this.$vuetify.display.smAndDown,
        'mr-n7': this.$vuetify.display.smAndDown
      }
    }
  },
  mounted() {
    this.reports = undefined;
    this.loading = false;
  },
  methods: {
    onSearchReports(reports) {
      this.loading = false;
      this.reports = reports;
    }
  }
})
</script>

<template>
  <v-row class="mb-2 d-flex justify-center w-100">
    <v-slide-y-transition leave-absolute>
      <v-col cols="auto" sm="12" md="6" lg="4" xl="3">
        <search-reports
            @loading="(val) => { loading = val }"
            @searchReports="onSearchReports"
            class="flex-grow-1"
        ></search-reports>
      </v-col>
    </v-slide-y-transition>
  </v-row>
  <v-row class="d-flex">
    <v-fade-transition leave-absolute group>
      <v-col v-for="report in reports" :key="report._id" cols="auto" sm="12" md="6" lg="4" xl="3" class="flex-grow-1">
        <div>
          <stock-report
            :report="report"
          ></stock-report>
        </div>
      </v-col>
      <v-col v-if="reports && reports.length === 0" key="no-results" cols="auto" sm="12" md="6" lg="4" xl="3" class="flex-grow-1">
        <v-card
          variant="outlined"
          class="mt-2 d-flex flex-column justify-center"
        >
          <v-card-title>
            <v-icon>mdi-invoice-text-clock</v-icon>
            No results yet
          </v-card-title>
          <v-card-text>
            <p>
              Your search returned no results for your selection of medications
              at these pharmacies for this point in time.
            </p>
            <p class="mt-4">
              We rely on anonymous reporting from the public to build up our
              database of medication availability in pharmacies nation-wide.
            </p>
            <p class="mt-4">
              You can check again in a few hours or tomorrow - some reports
              are pending a human review process, where a new pharmacy, medication
              or dosage has been entered.
            </p>
            <p class="mt-4">
              You can help us grow our database by
              <NuxtLink to="/reports/new" class="font-weight-bold">
                submitting reports of your own
              </NuxtLink>.
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-fade-transition>
  </v-row>
</template>

<style>

</style>