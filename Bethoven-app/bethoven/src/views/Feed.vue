<template>
  <v-container fill-height fluid>
    <v-row justify="center" class="overflow-y-auto">
      <v-col v-for="n in columnNumber" :key="n">
        <div v-if="hasBets">
          <div v-for="bet in betsForColumn(n, columnNumber)" :key="bet.id">
            <bet-card :bet="bet" :detail="true"></bet-card>
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
  name: "Feed",
  async beforeMount() {
    this.bets = await Api.get(this.query + "/?number=" + this.betSlice);
  },
  data() {
    return {
      bets: {},
      betSlice: 5,
      query: "bets",
      periodicRefresh: null,
    };
  },
  created() {
    window.addEventListener("scroll", this.handleScroll);
  },
  destroyed() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  props: {},
  methods: {
    betsForColumn(n, columns) {
      let list = [];
      for (let i = n - 1; i < this.bets.length; i += columns) {
        list.push(this.bets[i]);
      }
      return list;
    },
    async queryBets() {
      let newBet = await Api.get(
        this.query + "/?number=" + this.betSlice + "&betFrom=" + this.lastID
      );
      if (newBet.length <= 0) {
        //end of scrolling - no new bet !
        return;
      }
      let IDs = "";
      this.bets.forEach(bet => IDs += (bet.id + ","));
      console.log(IDs);
      console.log("lastid : " + this.lastID );
      IDs = "";
      newBet.forEach(bet => IDs += (bet.id + ","));
      console.log(IDs);
      this.bets = this.bets.concat(newBet);
    },
    handleScroll() {
      window.onscroll = () => {
        let bottomOfWindow =
          Math.max(
            window.pageYOffset,
            document.documentElement.scrollTop,
            document.body.scrollTop
          ) +
            window.innerHeight ===
          document.documentElement.offsetHeight;

        if (bottomOfWindow) {
          this.queryBets();
        }
      };
    },
  },
  computed: {
    data() {
      return this.bets;
    },
    columnNumber() {
      return this.$vuetify.breakpoint.lgAndUp
        ? 3
        : this.$vuetify.breakpoint.mdAndUp
        ? 2
        : 1;
    },
    hasBets() {
      return this.bets != null && this.bets.length > 0;
    },
    lastID() {
      return this.bets[this.bets.length - 1].id;
    },
  },
};
</script>

<style>
</style>