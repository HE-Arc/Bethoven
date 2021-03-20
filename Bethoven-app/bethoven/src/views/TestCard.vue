<template>
  <v-container fill-height fluid>
    <v-row justify="center" class="overflow-y-auto">
      <div v-if="hasBets">
        <div v-for="bet in bets" :key="bet.title">
          <bet-card :bet="bet"></bet-card>
        </div>
      </div>
    </v-row>
  </v-container>
</template>

<script>
import BetCard from "../components/BetCard.vue";
import Api from "@/api/ApiRequester";
import Vue from "vue";
export default {
  components: { BetCard },
  name: "TestCard",
  async beforeMount() {
    this.bets = await Api.get("bets/?number=" + this.startingbets);
  },
  data() {
    return {
      bets: [],
      startingbets: "10",
    };
  },
  computed: {
    data() {
      return this.bets;
    },
    hasBets() {
      return this.bets != null && this.bets.length > 0;
    },
    lastID() {
      return bets[bets.length - 1].id;
    },
  },
};
</script>

<style>
</style>