<template>
  <v-container fill-height fluid>
    <v-row justify="center" class="overflow-y-auto">
      <v-col v-for="n in columnNumber" :key="n">
        <div v-if="hasBets">
          <div v-for="bet in betForColumn(n, columnNumber)" :key="bet.title">
            <bet-card :bet="bet" :detail="true" :clickable="true"></bet-card>
          </div>
        </div>
      </v-col>
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
  methods: {
    betForColumn(n, columns){
      let list = [];
      for (let i = n-1; i < this.bets.length; i+=columns) {
          list.push(this.bets[i]);
      }
      return list;
    }
  },
  computed: {
    data() {
      return this.bets;
    },
    columnNumber(){
      return this.$vuetify.breakpoint.lgAndUp ? 3 : this.$vuetify.breakpoint.mdAndUp ? 2 : 1;
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