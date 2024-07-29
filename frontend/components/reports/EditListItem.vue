<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "EditListItem",
  props: {
    modelValue: true,
    items: {
      type: Array,
      default: undefined,
    },
    label: {
      type: String,
      default: undefined,
    },
    required: {
      type: Boolean,
      default: false,
    },
    editable: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    prependIcon: {
      type: String,
      default: undefined,
    },
    closeIcon: {
      type: String,
      default: 'mdi-check'
    },
    placeholderEditable: {
      type: String,
      default: 'Click to edit'
    },
    placeholderEditing: {
      type: String,
      default: undefined,
    },
    placeholder: {
      type: String,
      default: 'Not set'
    },
    titleProperty: {
      type: String,
      default: undefined,
    },
    subtitleProperty: {
      type: String,
      default: undefined,
    },
  },
  emits: [
      'update:modelValue'
  ],
  watch: {
    show() {
      if (!this.editable) {
        this.show = false;
      }
    }
  },
  data() {
    return {
      show: false
    }
  },
  computed: {
    model: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      }
    }
  },
  methods: {
    close() {
      this.show = false
      this.$emit('close')
    }
  }
})
</script>

<template>
  <slot name="label">
    <v-list-subheader v-if="label">
      {{ label }}
      <span v-if="required" class="text-error">&ast;</span>
    </v-list-subheader>
  </slot>
  <v-menu
      :close-on-content-click="false"
      v-model="show"
      origin="overlap"
      offset="4"
  >
    <template #activator="{ props }">
      <slot name="list-item">
        <v-list-item
            v-bind="props"
            :disabled="disabled"
            :class="{
              'cursor-default': !editable
            }"
        >
          <template #prepend>
            <slot name="prepend-icon">
              <v-icon v-if="prependIcon">
                {{ prependIcon }}
              </v-icon>
            </slot>
          </template>
          <slot name="list-item-title">
            <v-list-item-title>
              <span v-if="(titleProperty && (!model || !model[titleProperty])) || !model" class="text-grey">{{ editable ? placeholderEditable : placeholder }}</span>
              <span v-else>
                <slot name="list-item-title-text">
                  {{ titleProperty ? model[titleProperty] : model }}
                </slot>
              </span>
            </v-list-item-title>
          </slot>
          <slot name="list-item-subtitle">
            <v-list-item-subtitle v-if="subtitleProperty && model && model[subtitleProperty]">
              <slot name="list-item-subtitle-text">
                {{ model[subtitleProperty] }}
              </slot>
            </v-list-item-subtitle>
          </slot>
          <template #append>
            <slot name="list-item-append">
              <v-icon v-if="editable">
                mdi-pencil
              </v-icon>
            </slot>
          </template>
        </v-list-item>
      </slot>
    </template>
    <v-sheet v-if="show">
      <div
          :class="{'d-flex': true, 'pa-2': true}"
      >
        <slot name="prepend-edit-icon">
          <v-icon v-if="prependIcon" class="ml-2 mr-4 align-self-center">
            {{ prependIcon }}
          </v-icon>
        </slot>
        <slot v-bind="{ show }">
          <v-combobox
              autofocus
              clearable
              :readonly="!editable"
              :placeholder="placeholderEditing"
              v-model="model"
              :items="items"
              hide-details
              hide-no-data
              variant="plain"
              density="compact"
              class="ml-4"
          >
          </v-combobox>
        </slot>
        <slot name="close-button">
          <v-btn
              v-if="closeIcon"
              :icon="closeIcon"
              variant="flat"
              tile
              @click="close"
              class="align-self-center ml-2"
              size="small"
          >
          </v-btn>
        </slot>
      </div>
    </v-sheet>
  </v-menu>
</template>

<style scoped>

</style>