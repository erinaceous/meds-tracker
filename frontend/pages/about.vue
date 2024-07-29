<script lang="ts">
import {defineComponent} from 'vue'


export default defineComponent({
  name: "About",
  data() {
    return {
      metadata: {},
    }
  },
  mounted() {
    useFetch(`${this.$config.public.api.root}/static/metadata.json`).then((response) => {
      this.metadata = response.data;
      if (this.metadata?.processed_at) {
        this.metadata.processed_at = new Date(this.metadata.processed_at * 1000.0);
      }
    });
  }
})
</script>

<template>
  <v-row>
    <v-col>
      <v-btn
          color="primary"
          variant="text"
          @click="$router.back()"
          prepend-icon="mdi-arrow-left-circle"
      >
        Go back
      </v-btn>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="auto" sm="12" md="12" lg="6" xl="4">
      <v-card rounded="lg" variant="flat">
        <v-card-title>What is this?</v-card-title>
        <v-card-text>
          This website reports on the availability of medications in UK pharmacies, based on anonymous public reporting.
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="auto" sm="12" md="12" lg="6" xl="4">
      <v-card rounded="lg" variant="flat">
        <v-card-title>What's it for?</v-card-title>
        <v-card-text>
          The UK is has recently been seeing widespread national shortages of some medications due to increased demand
          and supplier issues.  When this happens, it can be difficult for people to know where they can pick up their
          next prescription - standard advice is to keep calling or visiting pharmacies in your local area until you
          find one in which your medication is in stock.  The only major pharmacy with an online stock checker currently
          is <a href="https://www.boots.com/online/psc/" target="_blank">Boots</a>.
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="auto" sm="12" md="12" lg="6" xl="4">
      <v-card rounded="lg" variant="flat">
        <v-card-title>What other resources can I check?</v-card-title>
        <v-card-text></v-card-text>
      </v-card>
    </v-col>
    <v-col cols="auto" sm="12" md="12" lg="6" xl="4">
      <v-card rounded="lg" variant="flat">
        <v-card-title>How does this website work?</v-card-title>
        <v-card-text>
          <p class="mb-4">Anyone can submit a set of reports, once a day. Each report contains this information:</p>
          <ul class="ml-4 mb-4">
            <li>Medication type and name;</li>
            <li>Prescribed dosage (if known) - for example, "18 milligram tablets";</li>
            <li>Pharmacy name and address;</li>
            <li>Date;</li>
            <li>Availability - whether the pharmacy had the meds in stock.</li>
          </ul>
          <p class="mb-4">
            Each pair of "Medication, Pharmacy" is given a score of 1 = available, or 0 = not available.  This score is
            then weighted by how recent it was, with the most recent reports having the most importance.  All of the
            reports for a medication at a pharmacy are combined into a weighted average availability between 0 and 1.
          </p>
          <p>
            An availability below 0.33 is considered "not in stock". Between 0.33 and 0.66 is considered "low stock".
            Between 0.66 and 1 is considered "in stock".
          </p>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="auto" sm="12" md="12" lg="6" xl="4">
      <v-card rounded="lg" variant="flat">
        <v-card-title>What data does it use?</v-card-title>
        <v-card-text>
          <p class="mb-4">
            The medications list comes from the <a href="https://bnf.nice.org.uk" target="_blank">British National Formulary</a>.
            The list of pharmacies comes from the NHS Open Data Portal <a href="https://opendata.nhsbsa.net/dataset/consolidated-pharmaceutical-list" target="_blank">Consolidated Pharmaceutical List</a> (2023-24 Quarter 4).
            Geolocation of postcodes uses the <a href="https://postcodes.io" target="_blank">postcodes.io</a> API, which itself is using public data.
            <span v-if="metadata && metadata.processed_at">
              The website's copy of this data was last updated at {{ metadata.processed_at.toLocaleString() }}.
            </span>
          </p>
          <p>
            When you submit your first report of the day, your browser spends about five to ten seconds calculating a
            unique cryptographic "signature". This signature is used to sign your reports for that day. That allows the website to
            accept reports anonymously whilst still reducing the impact of spammers. This is using a "proof of work"
            algorithm, powered by the open-source <a href="https://altcha.org/" target="_blank">Altcha</a> project.
          </p>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="auto" sm="12" md="12" lg="6" xl="4">
      <v-card rounded="lg" variant="flat">
        <v-card-title>Can I see (and contribute to!) the code?</v-card-title>
        <v-card-text>
          Yes! All source code for the website, its backend and scripts for data gathering are available at
          <a href="https://github.com/erinaceous/meds-tracker" target="_blank"><v-icon>mdi-github</v-icon>github.com/erinaceous/meds-tracker</a>.
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped>

</style>