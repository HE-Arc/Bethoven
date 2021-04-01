<template>
    <v-row justify="center" class="overflow-y-auto">
      <v-col v-for="n in columnNumber" :key="n">
        <div v-if="hasBets">
          <div v-for="bet in betsForColumn(n, columnNumber)" :key="bet.id">
            <bet-card :bet="bet" :detail="true" :clickable="true" ></bet-card>
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
  async beforeMount() {
    this.initQuery();
  },
  data() {
    return {
      bets: {},
      betSlice: 10,
      query : this.initialQuery,
      currentIDs : [],
      parameters : [],
    };
  },
  props: {
    initialQuery : "",
  },
  created() {
    window.addEventListener("scroll", this.handleScroll);
  },
  destroyed() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  methods: {
    betsForColumn(n, columns) {
      let list = [];
      for (let i = n - 1; i < this.bets.length; i += columns) {
        list.push(this.bets[i]);
      }
      return list;
    },
    initQuery : async function(){
      this.currentIDs = [];
      try{
        this.bets = await Api.get(this.query + "/?number=" + this.betSlice + this.getParameters());
        this.bets.forEach(bet => this.currentIDs.push(bet.id));
      } catch(error){
        console.log(error);
        Api.displayError("Could not get feed from server");
      }
    },
    getParameters : function(){
      let stringParameters = "";
      for (const [key, value] of Object.entries(this.parameters)) {
        stringParameters += "&" + key + "=" + value      
      }
      return stringParameters;
    },
    updateParameters(parameters){
      this.parameters = parameters;
      this.initQuery();
    },
    async queryBets() {
      try{
        let newBet = await Api.get(
          this.query + "/?number=" + this.betSlice + "&betFrom=" + this.lastID + this.getParameters()
        );
      } catch(error){
        console.log(error);
        return;
      }
      
      if (newBet.length <= 0) {
        //end of scrolling - no new bet !
        return;
      }

      //filter to be sure we do not have ID duplicity in the vue
      let uniqueNewbets = newBet.filter((bet, index, arr) => { 
          return !this.currentIDs.includes(bet.id);
      });
      uniqueNewbets.forEach(bet => this.currentIDs.push(bet.id));

      this.bets = this.bets.concat(uniqueNewbets);

    },
    handleScroll () {
      window.onscroll = () => {
        //Credits : Renat, at https://renatello.com/check-if-a-user-has-scrolled-to-the-bottom-in-vue-js/
        //Changed "===" to ">=" to avoid 1px difference not triggering the change
        let bottomOfWindow = Math.max(window.pageYOffset, document.documentElement.scrollTop, document.body.scrollTop) + window.innerHeight >= document.documentElement.offsetHeight;
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