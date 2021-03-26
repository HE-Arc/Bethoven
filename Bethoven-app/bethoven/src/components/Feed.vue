<template>
    <v-row justify="center" class="overflow-y-auto">
      <v-col v-for="n in columnNumber" :key="n">
        <div v-if="hasBets">
          <div v-for="bet in betsForColumn(n, columnNumber)" :key="bet.id">
            <bet-card :bet="bet" :detail="true"></bet-card>
          </div>
        </div>
      </v-col>
    </v-row>
</template>

<script>
import BetCard from "./BetCard.vue";
import Api from "@/api/ApiRequester";
import Vue from "vue";
export default {
  components: { BetCard },
  name: "Feed",
  async mounted() {
    this.bets = await Api.get(this.query + "/?number=" + this.betSlice);
  },
  data() {
    return {
      bets: {},
      betSlice: 10,
      periodicRefresh: null,
      query : this.initialQuery,
      currentIDs : [],
    };
  },
  props: {
    initQuery : "",
  },
  created() {
    window.addEventListener("scroll", this.handleScroll);
  },
  destroyed() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  props: {
    initialQuery : "",
  },
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
      newBet.forEach(bet => );

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