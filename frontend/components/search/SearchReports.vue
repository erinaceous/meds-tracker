<script lang="ts">
import {defineComponent} from 'vue'
import SearchMedications from './SearchMedications.vue'
import SearchPharmacies from './SearchPharmacies.vue'

export default defineComponent({
  name: "SearchReports",
  components: {
    SearchMedications,
    SearchPharmacies
  },
  data() {
    return {
      reports: [],
      medications: [],
      dosages: [],
      selectedDosages: [],
      pharmacies: [],
      duration: 86400 * 7,
      distance: 3,
      distances: [
        {
          title: 'this postcode only',
          value: 0
        },
        {
          title: '1 mile',
          value: 1
        },
        {
          title: '3 miles',
          value: 3
        },
        {
          title: '5 miles',
          value: 5,
        },
        {
          title: '10 miles',
          value: 10
        },
        {
          title: '25 miles',
          value: 25
        }
      ],
      durations: [
        {
          title: 'day',
          value: 86400
        },
        {
          title: '3 days',
          value: 86400 * 3
        },
        {
          title: 'week',
          value: 86400 * 7
        },
        {
          title: '2 weeks',
          value: 86400 * 14
        },
        {
          title: 'month',
          value: 86400 * 31
        },
        {
          title: '2 months',
          value: 86400 * 62
        }
      ],
      loading: false,
      error: undefined,
    }
  },
  computed: {
    canSearch() {
      return this.medications?.length > 0 || this.pharmacies?.length > 0
    },
  },
  watch: {
    loading(val) {
      this.$emit('loading', val)
    },
    async medications() {
      await this.getDosages()
    },
  },
  beforeMount() {
    this.searchReportsDebounced = useDebounce(
        this.searchReports, 250
    );
  },
  mounted() {
    this.loading = false
    this.error = undefined
  },
  methods: {
    async getDosages() {
      if (!this.medications || this.medications.length === 0) {
        return undefined;
      }
      this.dosages = await $fetch(
          `${this.$config.public.api.root}/medications/dosages`,
          {
            params: {
              uid: this.medications.map((medication) => medication.uid),
            }
          }
      ).then((response) => {
        if (!response.includes(null)) {
          response.unshift(null);
        }
        return response;
      })
    },
    async searchReports() {
      if (this.medications?.length < 1 && this.pharmacies?.length < 1) {
        return
      }
      this.reports = [];
      this.error = undefined;
      this.loading = true;
      this.reports = await this.getReports(
          this.medications,
          this.pharmacies,
          this.selectedDosages,
          this.duration
      ).then((reports) => {
        return reports.map((report) => {
          return {
            ...report,
            _id: `${report.medication_uid}+${report.pharmacy_uid}+${report.dosage}+${report.scores?.length}`,
          }
        })
      }).catch((error) => {
        this.loading = false;
        this.error = error
      });
      this.loading = false;
      this.$emit('searchReports', this.reports);
    },
    async getReports(medications = [], pharmacies = [], dosages = [], duration = null) {
      return $fetch(
          `${this.$config.public.api.root}/reports/scores`, {
            params: {
              medication_uid: medications.map(medication => medication.uid),
              pharmacy_uid: pharmacies.map(pharmacy => pharmacy.uid),
              dosage: dosages,
              max_age: duration
            }
          }
      )
    },
  }
})
</script>

<template>
  <v-card rounded="lg" elevation="24">
    <v-card-title>
      Search for stock reports
    </v-card-title>
    <v-list density="compact">
      <v-list-subheader>For medications:</v-list-subheader>
      <v-list-item>
        <search-medications
            v-model="medications"
            variant="outlined"
            prepend-inner-icon="mdi-medication"
            clearable chips multiple closable-chips hide-no-data hide-selected
            return-object
        ></search-medications>
      </v-list-item>
      <v-list-subheader>At these dosages <span class="text-grey">(optional)</span>:</v-list-subheader>
      <v-list-item>
        <v-autocomplete
            v-model="selectedDosages"
            :items="dosages"
            :disabled="!medications || medications.length === 0"
            variant="outlined"
            prepend-inner-icon="mdi-pill-multiple"
            clearable chips multiple closable-chips hide-no-data hide-selected
            hide-details
            placeholder="Choose known dosages from list"
            return-object
        ></v-autocomplete>
      </v-list-item>
      <v-list-subheader>In pharmacies:</v-list-subheader>
      <v-list-item>
        <search-pharmacies
            v-model="pharmacies"
            variant="outlined"
            prepend-inner-icon="mdi-hospital-box-outline"
            clearable chips multiple closable-chips hide-no-data hide-selected
            return-object
        ></search-pharmacies>
      </v-list-item>
      <v-list-subheader>
        For the past:
      </v-list-subheader>
      <v-list-item>
        <div class="d-flex justify-space-between">
          <div>
            <v-select
                v-model="duration"
                :items="durations"
                variant="outlined"
                hide-details
            >
            </v-select>
          </div>
          <div class="ml-4">
            <v-btn
                color="success"
                size="x-large"
                append-icon="mdi-magnify"
                text="Search"
                :loading="loading"
                :disabled="!canSearch"
                @click="searchReportsDebounced"
                class="fill-height"
            >
            </v-btn>
          </div>
        </div>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<style>

</style>