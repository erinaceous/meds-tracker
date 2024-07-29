<script lang="ts">
import {defineComponent} from 'vue'
import EditListItem from './EditListItem.vue'
import SearchMedications from "~/components/search/SearchMedications.vue";
import SearchPharmacies from "~/components/search/SearchPharmacies.vue";

export default defineComponent({
  name: "EditReportItem",
  components: {
    EditListItem,
    SearchMedications,
    SearchPharmacies
  },
  props: {
    editable: {
      type: Boolean,
      default: false
    },
    source: {
      type: Object,
      default: null,
    },
    showTrend: {
      type: Boolean,
      default: true
    },
    showRemoveButton: {
      type: Boolean,
      default: false
    },
    autoSave: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      medications: [],
      pharmacies: [],
      dosages: [],
      types: [],
      changed: false,
      editing: null,
      item: {
        medication: null,
        pharmacy: null,
        type: null,
        dosage: null,
        in_stock: false,
        reported_for_date: null,
        submitted: null,
      }
    }
  },
  computed: {
    canSubmit() {
      if (this.changed) {
        return false;
      }
      if (!this.item.medication || !this.item.pharmacy || !this.item.reported_for_date) {
        return false;
      }
      return true;
    }
  },
  watch: {
    item: {
      deep: true,
      handler() {
        if (this.autoSave) {
          this.saveReportItem()
        } else {
          this.changed = true
        }
      }
    },
    'item.medication': {
      handler(val) {
        if (!val || !val.uid) {
          this.types = []
          this.dosages = []
          return
        }
        this.getTypes(val.uid)
        this.getDosages(val.uid)
      }
    }
  },
  mounted() {
    if (this.source) {
      Object.assign(this.item, this.source);
      this.$nextTick(() => {
        this.changed = false;
        this.$el.scrollTo();
      })
    }
    if (!this.item.reported_for_date) {
      this.item.reported_for_date = new Date();
    }
  },
  methods: {
    async getDosages(medication_uid: string) {
      this.dosages = [];
      this.dosages = await $fetch(
          `${this.$config.public.api.root}/medications/dosages`,
          {
            params: {
              uid: [medication_uid]
            }
          }
      )
    },
    async getTypes(medication_uid: string) {
      this.types = [];
      this.types = await $fetch(
          `${this.$config.public.api.root}/medications/types`,
          {
            params: {
              uid: [medication_uid]
            }
          }
      )
    },
    saveReportItem() {
      this.changed = false;
      this.$emit('saveReportItem', this.item)
    },
    removeReportItem() {
      this.$emit('removeReportItem', this.source)
    }
  }
})
</script>

<template>
  <v-list rounded="lg" elevation="12">
    <!-- MEDICATION -->
    <edit-list-item
        v-model="item.medication"
        :editable="editable"
        label="Medication"
        prepend-icon="mdi-medication"
        placeholder-editable="Click to select"
        placeholder="Not known"
        placeholder-editing="Search for medication by name"
        title-property="category"
        subtitle-property="product"
        required
    >
      <template #list-item-title-text>{{ item.medication?.product || item.medication?.category }}</template>
      <template #list-item-subtitle-text>{{ item.medication?.category }}</template>
      <search-medications
        v-model="item.medication"
        :editable="editable"
        variant="plain"
        density="compact"
        autofocus
      ></search-medications>
    </edit-list-item>

<!--    &lt;!&ndash; TYPE &ndash;&gt;-->
<!--    <edit-list-item-->
<!--      v-model="item.type"-->
<!--      :editable="editable"-->
<!--      :items="types"-->
<!--      :disabled="!item.medication"-->
<!--      label="Method of administration"-->
<!--      prepend-icon="mdi-pill-multiple"-->
<!--      :placeholder-editable="item.medication ? 'Click to edit' : 'Select medication first'"-->
<!--      placeholder-editing="Type in method or choose from list"-->
<!--      placeholder="Not known / not applicable"-->
<!--    ></edit-list-item>-->

    <!-- DOSAGE -->
    <edit-list-item
      v-model="item.dosage"
      autofocus
      :editable="editable"
      :items="dosages"
      :disabled="!item.medication"
      label="Dosage"
      prepend-icon="mdi-pill-multiple"
      :placeholder-editable="item.medication ? 'Click to edit' : 'Select medication first'"
      placeholder-editing="Type in dosage or choose from list"
      placeholder="Not known / not applicable"
    >
    </edit-list-item>

    <!-- PHARMACY -->
    <edit-list-item
        v-model="item.pharmacy"
        :editable="editable"
        label="Pharmacy"
        title-property="name"
        subtitle-property="postcode"
        placeholder="Unknown"
        placeholder-editable="Click to choose"
        placeholder-editing="Search for pharmacy by postcode or address"
        prepend-icon="mdi-hospital-box-outline"
        required
    >
      <search-pharmacies
          v-model="item.pharmacy"
          :editable="editable"
          :readonly="!editable"
          variant="plain"
          density="compact"
          autofocus
      ></search-pharmacies>
    </edit-list-item>

    <!-- DATE -->
    <edit-list-item
      v-model="item.reported_for_date"
      :editable="editable"
      label="Date"
      placeholder="Unknown"
      placeholder-editable="Click to set"
      prepend-icon="mdi-calendar"
      required
    >
      <template #list-item-title-text>{{ item.reported_for_date?.toLocaleDateString() }}</template>
      <v-date-picker
          :readonly="!editable"
          show-adjacent-months
          v-model="item.reported_for_date"
          :max="new Date()"
      ></v-date-picker>
    </edit-list-item>

    <!-- IN STOCK? -->
    <v-list-subheader>In stock? <span class="text-error">&ast;</span></v-list-subheader>
    <v-list-item>
      <v-btn
          :readonly="!editable"
        prepend-icon="mdi-store-check"
        :color="item.in_stock ? 'success' : 'error'"
        class="d-flex flex-grow-1 w-100 justify-space-between"
        size="large"
        @click="() => { if (editable) { item.in_stock = !item.in_stock } }"
      >
        <template #default>
          {{ (item.in_stock ? 'Yes' : 'No') }}
        </template>
        <template #append>
          <v-icon>
            {{ item.in_stock ? 'mdi-checkbox-marked' : 'mdi-checkbox-blank-outline' }}
          </v-icon>
        </template>
      </v-btn>
    </v-list-item>

    <!-- ACTION BUTTONS -->
    <v-divider class="mb-2 mt-2" v-if="!autoSave && showRemoveButton"></v-divider>
    <v-list-item
        v-if="!autoSave && showRemoveButton"
      class="d-flex justify-center"
    >
      <v-btn
          v-if="!autoSave"
          color="primary"
        variant="text"
        prepend-icon="mdi-content-save"
        @click="saveReportItem"
        :disabled="!changed"
      >
        Save
      </v-btn>
      <v-btn
          v-if="showRemoveButton"
          variant="text"
          prepend-icon="mdi-delete"
          @click="removeReportItem"
      >
        Remove
      </v-btn>
    </v-list-item>
  </v-list>
</template>

<style scoped>

</style>