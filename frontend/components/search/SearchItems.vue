<script lang="ts">
import { defineComponent } from "vue";
import { VAutocomplete } from "vuetify/components";

export default defineComponent({
  name: "SearchItems",
  props: {
    modelValue: true,
    component: {
      type: Object,
      default: VAutocomplete,
    },
    getItemsFunction: {
      type: Function,
      default: undefined,
    },
    autocompleteUrl: {
      type: String,
      default: undefined,
    },
    minCharacters: {
      type: Number,
      default: 2,
    },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      items: undefined,
      loading: false,
      search: undefined,
    };
  },
  computed: {
    model: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
  },
  beforeMount() {
    this.fetchItemsDebounced = useDebounce(this.fetchItems, 500);
  },
  mounted() {
    this.loading = false;
    this.searchItems(this.search);
  },
  methods: {
    async getItems(search) {
      if (!this.autocompleteUrl) {
        return undefined;
      }
      return $fetch(this.autocompleteUrl.replace("${search}", search));
    },
    async fetchItems(search) {
      this.loading = true;
      if (this.getItemsFunction) {
        this.items = await this.getItemsFunction(search);
      } else {
        this.items = await this.getItems(search);
      }
      this.loading = false;
    },
    async searchItems(search) {
      if (
        !search ||
        search === "" ||
        search === null ||
        search.length < this.minCharacters
      ) {
        this.fetchItemsDebounced.cancel();
        this.items = undefined;
        this.loading = false;
        return;
      }
      await this.fetchItemsDebounced(search);
    },
  },
});
</script>

<template>
  <div class="w-100">
    <slot name="prepend" />
    <component
      :is="component"
      ref="search"
      v-model="model"
      v-bind="$attrs"
      :loading="loading"
      :items="items"
      clearable
      hide-details
      return-object
      no-filter
      :hide-no-data="
        items === undefined || !search || search?.length < minCharacters
      "
      @update:search="searchItems"
    >
      <template v-if="items !== undefined && items.length === 0" #append-item>
        <slot name="empty-data">
          <v-list-item disabled> No results found for your search </v-list-item>
        </slot>
      </template>
      <template #selection="{ item }">
        <slot name="selection" v-bind="{ item }">
          <v-list-item class="d-flex">
            <template #title>
              <v-list-item-title>
                {{ item.raw.title || item.raw }}
              </v-list-item-title>
            </template>
            <template #subtitle>
              <v-list-item-subtitle v-if="item.raw.subtitle">
                {{ item.raw.subtitle }}
              </v-list-item-subtitle>
            </template>
            <template #append>
              <div
                v-if="model instanceof Array && model?.length > 1"
                class="text-grey ml-8"
              >
                <h4>&plus;</h4>
              </div>
            </template>
          </v-list-item>
        </slot>
      </template>
      <template #item="{ props, item }">
        <slot name="item" v-bind="{ props, item }">
          <v-list-item v-bind="props">
            <template #title>
              <slot name="item-title" v-bind="{ item }">
                <v-list-item-title>
                  {{ item.raw.title || item.raw }}
                </v-list-item-title>
              </slot>
            </template>
            <template #subtitle>
              <slot name="item-subtitle" v-bind="{ item }">
                <v-list-item-subtitle v-if="item.raw.subtitle">
                  {{ item.raw.subtitle }}
                </v-list-item-subtitle>
              </slot>
            </template>
            <slot name="item-text" v-bind="{ item }" />
          </v-list-item>
        </slot>
      </template>
    </component>
    <slot name="append" />
  </div>
</template>

<style scoped></style>
