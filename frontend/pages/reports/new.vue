<script lang="ts">
import {defineComponent} from 'vue'
import EditReportItem from '~/components/reports/EditReportItem.vue'
import VerifyButton from '~/components/reports/VerifyButton.vue';

export default defineComponent({
  name: "NewReportsPage",
  components: {
    EditReportItem,
    VerifyButton,
  },
  props: {
    editable: {
      type: Boolean,
      default: false
    },
    source: {
      type: Array[Object],
      default: null,
    }
  },
  data() {
    return {
      reportStage: 'edit',
      signature: null,
      pendingReports: [],
      itemId: 0,
      error: null,
    }
  },
  computed: {
    canSubmit() {
      if (this.reportStage !== 'edit') {
        return false;
      }
      if (this.pendingReports.length === 0) {
        return false;
      }
      for (let report of this.pendingReports) {
        if (!report.medication || !report.pharmacy || !report.reported_for_date) {
          return false;
        }
      }
      return true;
    }
  },
  watch: {
    pendingReports: {
      deep: true,
      handler() {
        if (this.reportStage !== 'submitted') {
          return
        }
        this.reportStage = 'edit';
      }
    },
  },
  mounted() {
    if (this.source) {
      this.pendingReports = [...this.source];
    }
    this.reportStage = 'edit';
  },
  methods: {
    createReport() {
      this.itemId++;
      this.pendingReports.push({_id: this.itemId})
      this.reportStage = 'edit';
    },
    removeReportItem(item) {
      let idx = this.pendingReports.findIndex((report) => report._id === item._id);
      if (idx < 0) {
        return;
      }
      this.pendingReports = this.pendingReports.toSpliced(idx, 1);
    },
    saveReportItem(existingItem, newItem) {
      let idx = this.pendingReports.indexOf(existingItem);
      if (idx === -1) {
        this.pendingReports.push(newItem);
      } else {
        this.pendingReports[idx] = newItem;
      }
    },
    copyReportItem(item) {
      let newItem = useCloneDeep(item);
      this.itemId++;
      newItem._id = this.itemId;
      this.pendingReports.push(newItem)
    },
    dateStr(date: Date) {
      let dateStr = date.getFullYear().toString().padStart(4, "0");
      dateStr += `-${(date.getMonth() + 1).toString().padStart(2, "0")}`;
      dateStr += `-${date.getDate().toString().padStart(2, "0")}`;
      return dateStr;
    },
    async submitReports(altcha) {
      this.reportStage = 'submitting';
      let reports = [];
      for (let report of this.pendingReports) {
        reports.push({
          medication_uid: report.medication.uid,
          pharmacy_uid: report.pharmacy.uid,
          dosage: report.dosage,
          in_stock: report.in_stock,
          reported_for_date: this.dateStr(report.reported_for_date)
        })
      }
      await $fetch(
          `${this.$config.public.api.root}/reports`, {
            method: 'post',
            headers: {
              'Authorization': `Bearer ${altcha.signature}`
            },
            body: reports
          }
      ).then((response) => {
        let newPendingReports = [];
        for (let i in response) {
          let report = response[i]
          newPendingReports.push({
            ...this.pendingReports[i],
            ...report.report,
            changed: report.changed,
            error: report.error
          })
        }
        this.pendingReports = newPendingReports;
        this.signature = altcha.signature;
        this.$nextTick(() => {
          this.reportStage = 'submitted';
        })
      }).catch((error) => {
        this.reportStage = 'error';
        this.error = error
      })
    },
    resetReporting() {
      this.reportStage = 'edit';
    },
    restartReporting() {
      this.reportStage = 'edit';
      this.pendingReports = [];
      this.createReport();
    }
  }
})
</script>

<template>
  <v-row class="w-100 justify-center">
    <v-fade-transition leave-absolute group>
      <v-col
          v-for="(item, i) of pendingReports"
          :key="item._id"
          cols="auto"
          sm="12"
          md="6"
          lg="4"
          xl="3"
      >
        <v-card
            rounded="lg"
            variant="flat"
            :color="item.error ? 'error' : item.pending_review ? 'secondary' : item.changed ? 'success' : undefined"
            elevation="12"
        >
          <v-card-title>
            <div class="d-flex align-self-center">
              <div>
                #{{ i + 1 }}
              </div>
              <div v-if="reportStage === 'submitted'">
                : {{ item.error ? 'Failed to add report' : item.pending_review ? 'Pending review' : item.changed ? 'Report added' : 'Already reported' }}
              </div>
              <v-spacer></v-spacer>
              <v-btn
                  v-if="reportStage === 'edit'"
                  variant="text"
                  append-icon="mdi-delete"
                  @click="removeReportItem(item)"
              >
                Remove
              </v-btn>
              <v-btn
                  v-if="reportStage === 'edit'"
                  variant="text"
                  append-icon="mdi-content-copy"
                  @click="copyReportItem(item)"
              >
                Copy
              </v-btn>
            </div>
          </v-card-title>
          <v-card-subtitle v-if="item.error" class="mb-4 text-error">
            {{ item.error?.details || item.error }}
          </v-card-subtitle>
          <edit-report-item
              auto-save
              :editable="reportStage === 'edit'"
              :source="item"
              @saveReportItem="(newItem) => saveReportItem(item, newItem)"
              @removeReportItem="removeReportItem(item)"
          ></edit-report-item>
        </v-card>
      </v-col>
      <v-col cols="auto" sm="12" md="6" lg="4" xl="3" key="add" v-if="!['error', 'submitted'].includes(reportStage)">
        <v-btn
            v-if="reportStage === 'edit'"
            variant="outlined"
            color="secondary"
            size="large"
            @click="createReport"
            append-icon="mdi-plus"
            class="border-dashed w-100 fill-height pa-4"
            rounded="lg"
        >
          Click to add item
        </v-btn>
      </v-col>
      <v-col cols="auto" sm="12" md="6" lg="4" xl="3" key="submit">
        <v-card
            rounded="lg"
            variant="outlined"
            color="primary"
            v-if="!['error', 'submitted'].includes(reportStage)"
        >
          <v-card-title>
            <v-icon>mdi-note-multiple</v-icon>
            {{ reportStage === 'submitting' ? 'Submitting' : 'Submit' }} reports
          </v-card-title>
          <v-card-text>
            By submitting a report, you're letting other people know where you were and weren't able to buy or fulfil your prescription for these medications.
          </v-card-text>
            <verify-button
                v-if="!['submitted', 'error'].includes(reportStage)"
                :color="reportStage === 'submitted' ? undefined : 'primary'"
                :disabled="!canSubmit"
                :loading="!['edit', 'submitted'].includes(reportStage)"
                @verified="submitReports"
                size="large"
                append-icon="mdi-pen-plus"
                class="ma-4"
            ></verify-button>
        </v-card>
        <v-card
            rounded="lg"
            variant="outlined"
            color="primary"
            v-if="reportStage === 'error'"
        >
          <v-card-title>
            <v-icon>mdi-wrench-cog-outline</v-icon>
            Something went wrong
          </v-card-title>
          <v-card-text>
            <p class="mt-4">
              We tried to submit your reports, but something unexpected happened on the server.
            </p>
            <p class="mt-4">
              The problem might be temporary: you can try submitting again.
              It may also be a problem with the reports; you can
              continue editing and try to submit your reports with some changes.
            </p>
          </v-card-text>
          <div class="mt-4 d-flex flex-wrap flex-space-between">
            <verify-button
                @verified="submitReports"
                color="primary"
                size="large"
                append-icon="mdi-reload"
                class="ma-2"
            >
              Try again
            </verify-button>
            <v-btn
                color="warning"
                @click="resetReporting"
                size="large"
                append-icon="mdi-pencil"
                class="ma-2"
            >
              Continue editing
            </v-btn>
          </div>
          <v-card-text class="mt-4 mb-6" v-if="error">
            <p>
              Details of the error message:
            </p>
            <pre class="border pa-1 text-pre-wrap fill-height overflow-auto">
              {{ error?.detail || error.toString() }}
            </pre>
          </v-card-text>
        </v-card>
        <v-card
            rounded="lg"
            variant="outlined"
            color="primary"
            v-if="reportStage === 'submitted'"
            class="d-flex flex-column"
        >
          <v-card-title>
            <v-icon>mdi-hand-heart</v-icon>
            Thank you
          </v-card-title>
          <v-card-text>
            <p>Your reports have been submitted to the database.</p>
            <p class="mt-4">
              If any of your reports are about new medications, new pharmacies, or dosages which don't yet exist in the database, those reports will be marked for human review.
              Once they have been reviewed, they will be included in the Stock Scores for affected medications and pharmacies.
              They could be pending review for up to several days, depending on reviewer workload and availability.
            </p>
            <p class="mt-4">
              Items coloured <span class="text-error">in red</span> had an error during submission.
              Items coloured <span class="text-grey-darken-2">in grey</span>, we think you have already reported for that
              medication in that pharmacy on that date, with your current signature.
            </p>
          </v-card-text>
          <v-btn
              color="primary"
              @click="restartReporting"
              size="large"
              append-icon="mdi-pen-plus"
              class="ma-4"
          >
            Start again
          </v-btn>
          <v-card-text>
              <p>
                The anonymous signature used to sign your reports for today is:
              </p>
              <pre class="border pa-1 text-secondary text-pre-wrap overflow-auto">{{ signature }}</pre>
          </v-card-text>
        </v-card>
      </v-col>
    </v-fade-transition>
  </v-row>
</template>
