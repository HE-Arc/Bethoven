<template>
  <v-container fill-height fluid>
    <div v-if="hasBets">
      <div v-for="bet in bets" :key="bet.title">
        <h1>{{ bet.title }}</h1>
        <bet-card :title="bet.title" :description="bet.description"></bet-card>
      </div>
    </div>
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
    this.bets = await Api.get("bets/?number=3&");
  },
  data() {
    return {
      bets: [],
    };
  },
  computed: {
    data(){
      return this.bets;
    },
    hasBets() {
      return this.bets != null && this.bets.length > 0;
    },
    lastID(){
      return bets[bets.length - 1].id;
    }
  },
};


</script>

<style>
</style>