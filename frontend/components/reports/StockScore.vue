<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "StockScore",
  props: {
    report: {
      type: Object,
      default: null,
    },
    showTrend: {
      type: Boolean,
      default: true
    },
  },
  computed: {
    scores() {
      if (!this.report?.scores) {
        return undefined
      }
      return this.report.scores.map(item => item.score);
    },
    scoresDated() {
      if (!this.report?.scores) {
        return undefined
      }
      return this.report.scores.map(item => {
        return {
          score: item.score,
          reported_for_date: new Date(item.reported_for_date)
        }
      }).toSorted((a, b) => a.reported_for_date - b.reported_for_date)
    },
    scoresInterpolated() {
      if (!this.scoresDated) {
        return undefined
      }
      if (this.scoresDated.length === 0) {
        return []
      }
      if (this.scoresDated.length === 1) {
        return this.scoresDated;
      }
      let lastScore = this.scoresDated[this.scoresDated.length - 1];
      let newScores = [];
      let currentScore = this.scoresDated[0];
      let date = new Date(currentScore.reported_for_date);
      while (true) {
        let nextScore = this.scoresDated.find(
            (score) => score.reported_for_date.toLocaleDateString() === date.toLocaleDateString()
        )
        if (nextScore) {
          newScores.push(nextScore);
          currentScore = nextScore;
        } else {
          newScores.push({
            ...currentScore,
            reported_for_date: new Date(date),
          })
        }
        date.setTime(date.getTime() + 86400000)
        if (date > lastScore.reported_for_date) {
          break
        }
      }
      return newScores;
    },
    trend() {
      if (!this.scoresInterpolated) {
        return []
      }
      return this.scoresInterpolated.map(item => item.score)
    },
    labels() {
      if (!this.scoresInterpolated) {
        return []
      }
      return this.scoresInterpolated.map(item => item.reported_for_date)
    },
    currentScore() {
      if (this.scores?.length === 0) {
        return undefined
      }
      return (useSum(this.scores) / this.scores.length);
    },
    scoreIcon() {
      if (this.currentScore === undefined) {
        return 'mdi-progress-question'
      }
      if (this.currentScore <= 0.33) {
        return 'mdi-close-circle'
      }
      if (this.currentScore > 0.66) {
        return 'mdi-check-circle'
      }
      return 'mdi-help-circle'
    },
    scoreColour() {
      if (this.currentScore === undefined) {
        return undefined
      }
      if (this.currentScore <= 0.33) {
        return this.$vuetify.theme.current.colors.error
      }
      if (this.currentScore > 0.66) {
        return this.$vuetify.theme.current.colors.success
      }
      return this.$vuetify.theme.current.colors.warning
    }
  },
})
</script>

<template>
  <v-sheet
      theme="dark"
      rounded="lg"
      class="ma-2 d-flex flex-column justify-center flex-grow-1"
  >
    <div class="d-flex justify-center align-center">
      <div class="d-block">
        <v-card-title class="text-wrap">
          <div v-if="currentScore === undefined">
            No reports yet
          </div>
          <div v-else-if="currentScore <= 0.33">
            Low stock reported
          </div>
          <div v-else-if="currentScore > 0.66">
            Reported in stock
          </div>
          <div v-else>
            Might be in stock
          </div>
          <div v-if="currentScore !== undefined">
            Score: <strong>{{ currentScore.toFixed(2) }}</strong>
          </div>
        </v-card-title>
        <v-card-subtitle v-if="report?.scores?.length === 1" class="text-wrap mb-2">
          Based on <strong>1</strong> report on <strong>{{ report?.scores[0].reported_for_date }}</strong>
        </v-card-subtitle>
        <v-card-subtitle v-else-if="report?.scores?.length > 1" class="text-wrap mb-2">
          Based on <strong>{{ report?.scores.length }}</strong> reports from <strong>{{ report?.scores[0].reported_for_date }}</strong> until <strong>{{ report?.scores[report?.scores.length - 1].reported_for_date }}</strong>
          <ul class="ml-4">
            <li></li>
          </ul>
        </v-card-subtitle>
      </div>
      <v-spacer></v-spacer>
      <v-icon
          class="ma-4"
          size="48"
          :color="scoreColour"
      >
        {{ scoreIcon }}
      </v-icon>
    </div>
    <v-sparkline
        v-if="showTrend && trend && trend.length > 1"
        :model-value="trend"
        :color="$vuetify.theme.current.colors.surface"
        stroke-linecap="round"
        smooth
        min="0"
        max="1"
        fill
        type="trend"
        :gradient="[$vuetify.theme.current.colors.success, $vuetify.theme.current.colors.warning, $vuetify.theme.current.colors.error]"
    ></v-sparkline>
  </v-sheet>
</template>

<style scoped>

</style>