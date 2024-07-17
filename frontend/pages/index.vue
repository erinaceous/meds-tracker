<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "index",
  data() {
    return {
      //apiRoot: 'http://localhost:8000',
      apiRoot: '/api',
      searchType: 0,
      medicationGroups: {},
      pharmacies: [],
      medications: [],
      postcodes: [],
      selectedMedications: [],
      selectedPharmacies: [],
      selectedPostcode: null,
      location: null,
      selectedDuration: 86400 * 7,
      selectedDistance: 3,
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
      showReportDialog: false,
      pendingReports: [],
      submittedReports: false,
      loaded: false,
      metadata: {},
    }
  },
  computed: {
    canSearch() {
      return this.selectedMedications?.length > 0 || this.selectedPostcode?.length > 0
    },
    canReport() {
      return this.selectedMedications?.length > 0 && this.selectedPharmacies?.length > 0
    },
  },
  watch: {
    async selectedPostcode(postcode) {
      this.location = await $fetch(
          `https://api.postcodes.io/postcodes/${postcode}`
      ).then((response) => {
        return {
          latitude: response.result.latitude,
          longitude: response.result.longitude,
        }
      })
    }
  },
  beforeMount() {
    useFetch("/metadata.json").then((response) => {
      this.metadata = response.data;
      if (this.metadata?.processed_at) {
        this.metadata.processed_at = new Date(this.metadata.processed_at * 1000.0);
      }
    });
    this.searchMedicationsDebounced = useDebounce(
        this.searchMedications, 750
    );
    this.searchPharmaciesDebounced = useDebounce(
        this.searchPharmacies, 750
    );
    this.searchPostcodesDebounced = useDebounce(
        this.searchPostcodes, 500
    );
  },
  mounted() {
    this.loaded = true
  },
  methods: {
    async searchMedications(search) {
      if (!search || search === '' || search === null) {
        this.medications = [];
        return
      }
      this.loaded = false
      this.medications = await this.getMedications(search);
      this.loaded = true
    },
    async searchPharmacies(search) {
      if (!search || search === '' || search === null) {
        this.pharmacies = [];
        return
      }
      this.loaded = false
      this.pharmacies = await this.getPharmacies(search);
      this.loaded = true
    },
    async searchPostcodes(search) {
      if (!search || search === '' || search === null) {
        this.postcodes = [];
        return
      }
      this.loaded = false
      this.postcodes = await this.getPostcodes(search);
      this.loaded = true
    },
    async getPostcodes(search) {
      search = search.toLowerCase().replace(" ", "");
      return $fetch(
          `https://api.postcodes.io/postcodes/${search}/autocomplete`
      ).then((response) => {
        return response.result;
      })
    },
    async getPharmaciesInArea() {
      if (!this.location) {
        return
      }
      return $fetch(
          `${this.apiRoot}/pharmacies/location`,
          {
            params: {
              ...this.location,
              radius: this.selectedDistance
            }
          }
      )
    },
    async getPharmacies(search) {
      return $fetch(
          `${this.apiRoot}/pharmacies/autocomplete/${search}`
      )
    },
    async getMedications(search) {
      return $fetch(
          `${this.apiRoot}/medications/autocomplete/${search}`
      ).then((response) => {
        return response.map((medication) => {
          let name = medication.category;
          if (medication.product) {
            name += `: ${medication.product}`;
          }
          return name
        })
      })
    },
    newStockReportItems() {
      const today = new Date();
      for (let medication of this.selectedMedications) {
        for (let pharmacy of this.selectedPharmacies) {
          let key = medication + ' at ' + pharmacy.title + ' on ' + today.toDateString()
          if (this.pendingReports.find((report) => report.key === key)) {
            continue;
          }
          this.pendingReports.push({
            medication,
            pharmacy,
            availability: false,
            date: today,
            key,
          })
        }
      }
    },
    showReports() {
      this.newStockReportItems();
      this.showReportDialog = true;
    },
    removeReportItem(item) {
      let idx = this.pendingReports.findIndex((report) => report.key === item.key);
      if (idx < 0) {
        return;
      }
      this.pendingReports = this.pendingReports.toSpliced(idx, 1);
    },
    submitReports() {
      this.submittedReports = true;
    },
    finishReporting() {
      this.pendingReports = [];
      this.showReportDialog = false;
      this.submittedReports = false;
    }
  }
})
</script>

<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <h1 class="font-weight-black">
          🇬🇧 ⚕️ UK
          <span class="text-primary">crowd-sourced</span>
          medication and pharmacy
          <span class="text-secondary">supply</span>
          tracker
        </h1>
      </v-col>
    </v-row>
    <v-row class="mb-2">
      <v-col>
        <v-card rounded elevation="24">
          <v-container fluid>
            <v-row>
              <v-col cols="auto">
                <h3>I'm looking for stock reports about</h3>
              </v-col>
              <v-col cols="12" sm="12" class="flex-grow-1">
                <v-autocomplete
                  v-model="selectedMedications"
                  @update:search="searchMedicationsDebounced"
                  :loading="!loaded"
                  :items="medications"
                  variant="outlined"
                  prepend-inner-icon="mdi-medication"
                  :label="selectedMedications.length > 0 ? 'these medications' : 'any medications'"
                  placeholder="Type in the names of medications, or leave empty"
                  clearable chips multiple closable-chips hide-no-data hide-selected
                ></v-autocomplete>
              </v-col>
              <v-col cols="auto">
                <h3>in</h3>
              </v-col>
              <v-col cols="auto">
                <v-autocomplete
                  v-model="selectedPostcode"
                  @update:search="searchPostcodesDebounced"
                  :loading="!loaded"
                  :items="postcodes"
                  variant="outlined"
                  prepend-inner-icon="mdi-hospital-box-outline"
                  :label="selectedPostcode ? 'pharmacies around this postcode' : 'any pharmacies'"
                  placeholder="Type in a postcode, or leave empty"
                  clearable
                  width="30ch"
                ></v-autocomplete>
              </v-col>
              <v-col cols="auto" :class="!selectedPostcode ? 'text-grey' : ''">
                <h3>within</h3>
              </v-col>
              <v-col cols="auto">
                <v-select
                  v-model="selectedDistance"
                  :disabled="!selectedPostcode"
                  :items="distances"
                  variant="outlined"
                  density="compact"
                ></v-select>
              </v-col>
              <v-col cols="auto">
                <h3>for the past</h3>
              </v-col>
              <v-col cols="auto">
                <v-select
                    v-model="selectedDuration"
                    :items="durations"
                    variant="outlined"
                    density="compact"
                >
                </v-select>
              </v-col>
              <v-spacer></v-spacer>
              <v-col cols="auto">
                <v-btn-group>
                  <v-btn
                    color="success"
                    size="large"
                    append-icon="mdi-magnify"
                    text="Search"
                    :disabled="!canSearch"
                    @click="getPharmaciesInArea"
                  >
                  </v-btn>
                  <v-btn
                    color="primary"
                    size="large"
                    append-icon="mdi-pen-plus"
                    text="Report"
                    :disabled="!canReport"
                    @click="showReports"
                  >
                  </v-btn>
                </v-btn-group>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
    <v-row v-if="showReportDialog" class="ml-2 mr-2 mb-2">
      <v-container fluid>
        <v-row>
          <v-col cols="auto" class="flex-grow-1">
            <v-card rounded elevation="12" class="flex-grow-1">
              <v-card-title class="d-flex">
                Submit reports on medication availability
                <v-spacer></v-spacer>
                <v-btn
                    icon
                    variant="flat"
                    @click="finishReporting"
                >
                  <v-icon>mdi-close</v-icon>
                </v-btn>
              </v-card-title>
              <v-card-text>
                By submitting a report, you're letting other people know where you were and weren't able to buy or fulfil your prescription for the medications listed below.
              </v-card-text>
              <v-table>
                <thead>
                  <tr>
                    <th><v-icon>mdi-medication</v-icon> Medication</th>
                    <th><v-icon>mdi-hospital-box-outline</v-icon> Pharmacy</th>
                    <th><v-icon>mdi-calendar</v-icon> Date</th>
                    <th><v-icon>mdi-store-check</v-icon> Availability</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                      v-for="item of pendingReports"
                      :key="item.key"
                  >
                    <td>

                      {{ item.medication }}
                    </td>
                    <td>

                      {{ item.pharmacy.title }}
                    </td>
                    <td class="cursor-pointer text-primary">
                      {{ item.date.toLocaleDateString() }}
                      <v-menu activator="parent">
                        <v-date-picker show-adjacent-months v-model="item.date">
                        </v-date-picker>
                      </v-menu>
                      <v-icon>mdi-menu-down</v-icon>
                    </td>
                    <td>
                      <v-checkbox
                          v-model="item.availability"
                          :label="item.availability ? 'In stock' : 'Out of stock'"
                          :color="item.availability ? 'success' : 'error'"
                          false-icon="mdi-close-box"
                          density="compact"
                      ></v-checkbox>
                    </td>
                    <td>
                      <v-btn
                          flat icon
                          @click="removeReportItem(item)"
                      >
                        <v-icon>mdi-delete</v-icon>
                      </v-btn>
                    </td>
                  </tr>
                </tbody>
              </v-table>
              <v-card-actions class="mt-2">
                <v-spacer></v-spacer>
                <v-btn
                  color="success"
                  size="large"
                  variant="flat"
                  :disabled="pendingReports.length === 0"
                  @click="submitReports"
                >
                  Submit
                  <v-icon>
                    mdi-pen-plus
                  </v-icon>
                </v-btn>
              </v-card-actions>
              <v-overlay
                v-model="submittedReports"
                contained
                class="overlay-fill"
              >
                <v-progress-circular
                  v-if="submittedReports === null"
                  indeterminate
                  size="large"
                ></v-progress-circular>
                <v-sheet
                    v-if="submittedReports === true"
                    color="success"
                    class="fill-height"
                >
                  <v-container fluid>
                    <v-row>
                      <v-col cols="auto" class="flex-grow-1">
                        <h1 class="d-flex flex-grow-1 ">
                          <v-icon class="mr-4">mdi-check-circle</v-icon>
                          Thank you!
                          <v-spacer></v-spacer>
                          <v-btn
                              icon
                              variant="flat"
                              @click="finishReporting"
                          >
                            <v-icon>mdi-close</v-icon>
                          </v-btn>
                        </h1>
                        <h3>Your reports have been submitted.</h3>
                        <p>For each combination of medication and pharmacy, you can make one report a day.</p>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-sheet>
              </v-overlay>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-row>
    <v-expansion-panels variant="popout" elevation="12">
      <v-expansion-panel>
        <v-expansion-panel-title>Click for background information about this website</v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-row>
            <v-col>
              <h3>What is this?</h3>
              <p>
                This website reports on the availability of medications in UK pharmacies, based on anonymous public reporting.
              </p>
            </v-col>
            <v-col cols="auto">
              <h3>What's it for?</h3>
              <p>
                The UK is has recently been seeing widespread national shortages of some medications due to increased demand
                and supplier issues.  When this happens, it can be difficult for people to know where they can pick up their
                next prescription - standard advice is to keep calling or visiting pharmacies in your local area until you
                find one in which your medication is in stock.  The only major pharmacy with an online stock checker currently
                is Boots.
              </p>
            </v-col>
            <v-col cols="auto">
              <h3>What other resources can I check?</h3>
              <p></p>
            </v-col>
            <v-col cols="auto">
              <h3>How does this website work?</h3>
              <p>
                Anyone can submit a set of reports, once a day. Each report contains this information:
              </p>
              <ul class="ml-4">
                <li>Medication name;</li>
                <li>Pharmacy name and address;</li>
                <li>Date;</li>
                <li>Availability - whether the pharmacy had the meds in stock.</li>
              </ul>
              <p>
                Each pair of "Medication, Pharmacy" is given a score of 1 = available, or 0 = not available.  This score is
                then weighted by how recent it was, with the most recent reports having the most importance.  All of the
                reports for a medication at a pharmacy are combined into a weighted average availability between 0 and 1.
              </p>
              <p>
                An availability below 0.33 is considered "not in stock". Between 0.33 and 0.66 is considered "low stock".
                Between 0.66 and 1 is considered "in stock".
              </p>
            </v-col>
            <v-col cols="auto">
              <h3>What data does it use?</h3>
              <p>
                The medications list comes from the <a href="https://bnf.nice.org.uk" target="_blank">British National Formulary</a>.
                The list of pharmacies comes from the NHS Open Data Portal <a href="https://opendata.nhsbsa.net/dataset/consolidated-pharmaceutical-list" target="_blank">Consolidated Pharmaceutical List</a> (2023-24 Quarter 4).
                Geolocation of postcodes uses the <a href="https://postcodes.io" target="_blank">postcodes.io</a> API.
                <span v-if="metadata && metadata.processed_at">
              The website's copy of this data was last updated at {{ metadata.processed_at.toLocaleString() }}.
            </span>
              </p>
              <p>
                When you submit reports, an anonymous device fingerprint and IP address is recorded in a temporary database
                table. This information is used to check if you've already submitted a report for a medication at a pharmacy
                today. The website allows you to do this once every 24 hours, to reduce the effect of spam. After 24 hours,
                that fingerprint and IP address are removed from the database.
              </p>
            </v-col>
            <v-col cols="auto">
              <h3>Can I see the code?</h3>
              <p>
                All source code for the website, its backend and scripts for data gathering are available at
                <a href="https://github.com/erinaceous/meds-tracker" target="_blank">github.com/erinaceous/meds-tracker</a>.
              </p>
            </v-col>
          </v-row>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-container>
</template>

<style>
.overlay-fill .v-overlay__content {
  width: 100%;
  height: 100%;
}
</style>