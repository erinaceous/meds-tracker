<script lang="ts">
import { defineComponent } from "vue";

if (import.meta.client) {
  import("altcha");
}

export default defineComponent({
  name: "VerifyButton",
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
    appendIcon: {
      type: String,
      default: "mdi-pen-plus",
    },
    appendRetryIcon: {
      type: String,
      default: "mdi-reload",
    },
    color: {
      type: String,
      default: undefined,
    },
    retryColor: {
      type: String,
      default: "warning",
    },
    retryAuth: {
      type: Boolean,
      default: true,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      authenticating: undefined,
    };
  },
  computed: {
    finalColor() {
      if (
        this.retryAuth &&
        this.retryColor &&
        this.authenticating === "error"
      ) {
        return this.retryColor;
      }
      return this.color;
    },
    finalDisabled() {
      if (!this.retryAuth && this.authenticating === "error") {
        return true;
      }
      return this.disabled;
    },
    finalAppendIcon() {
      if (
        this.retryAuth &&
        this.appendRetryIcon &&
        this.authenticating === "error"
      ) {
        return this.appendRetryIcon;
      }
      return this.appendIcon;
    },
    finalLoading() {
      return (
        this.loading || (this.authenticating && this.authenticating !== "error")
      );
    },
  },
  mounted() {
    this.authenticating = undefined;
  },
  methods: {
    altchaStateChange(event) {
      if (event.detail.state === "error") {
        this.authenticating = "error";
      }
    },
    async checkSignature(signature) {
      const result = await fetch(`${this.$config.public.api.root}/altcha`, {
        headers: {
          Authorization: `Bearer ${signature}`,
        },
      })
        .catch((response) => {
          this.$emit("error", { signature, response });
          return false;
        })
        .then((response) => {
          if (response.status !== 204) {
            return false;
          }
          return true;
        });
      return result;
    },
    async beginSubmission() {
      const signature = this.$localStorage.getItem("signature");
      if (signature) {
        this.authenticating = "checking";
        const valid = await this.checkSignature(signature);
        if (valid) {
          this.$emit("verified", { signature });
          this.authenticating = undefined;
          return;
        }
      }
      this.authenticating = "verifying";
    },
    altchaVerification(event) {
      this.$localStorage.setItem(
        "signature",
        event.detail.signature,
        event.detail.expires,
      );
      this.$emit("verified", event.detail);
      this.authenticating = undefined;
    },
  },
});
</script>

<template>
  <v-btn
    v-bind="{ props: $attrs }"
    :loading="finalLoading"
    :append-icon="finalAppendIcon"
    :color="finalColor"
    :disabled="finalDisabled"
    @click="beginSubmission"
  >
    <slot> Submit </slot>
    <template v-if="authenticating === 'error'">
      <slot name="authError"> Retry </slot>
    </template>
    <client-only v-if="authenticating === 'verifying'">
      <altcha-widget
        :challengeurl="`${$config.public.api.root}/altcha/challenge`"
        :verifyurl="`${$config.public.api.root}/altcha/verify`"
        auto="onload"
        class="d-none"
        hidelogo
        hidefooter
        @serververification="altchaVerification"
        @statechange="altchaStateChange"
      />
    </client-only>
  </v-btn>
</template>

<style scoped></style>
