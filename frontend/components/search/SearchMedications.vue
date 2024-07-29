<script lang="ts">
import {defineComponent} from 'vue'
import SearchItems from './SearchItems.vue'
import AddMedication from '../reports/AddMedication.vue'

export default defineComponent({
  name: "SearchMedications",
  components: {
    SearchItems,
    AddMedication
  },
  props: {
    editable: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      showDialog: false
    }
  },
  mounted() {
    this.showDialog = false
  },
  methods: {
    async getItems(search) {
      return $fetch(
          `${this.$config.public.api.root}/medications/autocomplete/${search}`
      ).then((response) => {
        return response.map((medication) => {
          let name = medication.category;
          if (medication.product) {
            name += `: ${medication.product}`;
          }
          return {
            ...medication,
            title: medication.product || medication.category,
            subtitle: medication.product ? medication.category : undefined,
            value: name,
          }
        })
      })
    }
    }
})
</script>

<template>
  <v-dialog v-model="showDialog" class="w-auto w-xl-25 w-lg-33 w-md-50 w-sm-75">
    <add-medication
        @submitted="(result) => { $emit('update:modelValue', result); showDialog = false }"
        @cancel="showDialog = false"
    ></add-medication>
  </v-dialog>
  <search-items
      v-bind="$attrs"
      :get-items-function="getItems"
      placeholder="Search by name"
  >
    <template #empty-data>
      <v-list-item class="text-wrap text-disabled">
        No medications found matching your search.
        <a href
           v-if="editable"
           @click.prevent="showDialog = true"
           class="font-weight-bold"
        >
          Click here to manually enter details.
        </a>
      </v-list-item>
    </template>
    <template #selection="{ item }">
      <v-list-item>
        <template #title>
          <v-list-item-title>
            {{ item.raw.product ? item.raw.product : item.raw.category }}
          </v-list-item-title>
        </template>
        <template #subtitle>
          <v-list-item-subtitle
              v-if="item.raw.product">
            {{ item.raw.category }}
          </v-list-item-subtitle>
        </template>
      </v-list-item>
    </template>
    <template #item="{ props, item }">
      <v-list-item
        v-bind="props"
      >
        <template #title>
          <v-list-item-title>
            {{ item.raw.product ? item.raw.product : item.raw.category }}
          </v-list-item-title>
        </template>
        <template #subtitle>
          <v-list-item-subtitle
              v-if="item.raw.product">
            {{ item.raw.category }}
          </v-list-item-subtitle>
        </template>
      </v-list-item>
    </template>
  </search-items>
</template>

<style scoped>

</style>