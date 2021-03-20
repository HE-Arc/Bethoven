<!-- TEMPLATE -->
<template>
  <div>
    <v-card class="ma-1 pt-2">
      <!-- Title and text -->
      <v-card-title>{{ bet.title }}</v-card-title>
      <v-card-text>{{ bet.description }}</v-card-text>

      <!-- 'bet' part with choices and bet buttons -->
      <v-card-subtitle class="pa-0 text-center">
        votes : {{ bet.bet_ratio.number }} <v-icon>mdi-account</v-icon>
      </v-card-subtitle>
      <v-card-subtitle class="pa-0 text-center">
        amount : {{ bet.bet_ratio.total }}
        <v-icon>mdi-alpha-b-circle-outline</v-icon>
      </v-card-subtitle>

      <v-progress-linear
        v-if="hasProgress"
        background-color="teamB"
        color="teamA"
        :value="bet.bet_ratio.ratio[0]"
      ></v-progress-linear>

      <!-- Tab -->
      <v-row no-gutters v-if="detail">
        <v-col>
          <!--Choice 1-->
          <v-card outlined tile>
            <v-col class="text-right">
              <v-card-subtitle class="pa-1">{{ bet.choice1 }}</v-card-subtitle>
              <v-card-subtitle class="pa-1">
                {{ bet.bet_ratio.ratio[0] }} %</v-card-subtitle
              >
              <v-row v-if="canBet" justify="start" align="center">
                <v-col>
                  <v-text-field
                    v-model="amount0"
                    hint="Place your bet"
                    type="number"
                    ref=""
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-btn v-on:click="gamble(0)" color="teamA"
                    >Bet<v-icon>mdi-alpha-b-circle-outline</v-icon></v-btn
                  >
                </v-col>
              </v-row>
            </v-col>
          </v-card>
        </v-col>
        <v-col>
          <!--Choice 2-->
          <v-card outlined tile>
            <v-col class="text-left">
              <v-card-subtitle class="pa-1">{{ bet.choice2 }}</v-card-subtitle>
              <v-card-subtitle class="pa-1"
                >{{ bet.bet_ratio.ratio[1] }} %</v-card-subtitle
              >
              <v-row v-if="canBet" justify="start" align="center">
                <v-col>
                  <v-text-field
                    v-model="amount1"
                    hint="Place your bet"
                    type="number"
                    ref=""
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-btn v-on:click="gamble(1)" color="teamB"
                    >Bet<v-icon>mdi-alpha-b-circle-outline</v-icon></v-btn
                  >
                </v-col>
              </v-row>
            </v-col>
          </v-card>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>


<!-- SCRIPT -->
<script>
import Vue from "vue";
import Api from "@/api/ApiRequester";

export default Vue.extend({
  name: "BetCard",
  data() {
    return { amount0 : 0, amount1 : 0 };
  },
  props: {
    bet: {},
    detail: false,
  },
  computed: {
    hasProgress() {
      return this.bet.bet_ratio.number > 0;
    },
    canBet() {
      return this.bet.currentUserBet == null;
    },
    data() {
      return this.bet;
    },
  },
  methods: {
    getID() {
      return this.bet.id;
    },
    async gamble(choice) {
      //verify that the user is logged in
      if(! this.$store.state.isUserLogged){
        this.$router.push({ name: "Login" });
        return;
      }

      //fetch choice and anount as integer
      let choiceInteger = parseInt(choice);
      let amount = parseInt(choice == 0 ? this.amount0 : this.amount1);

      //gamble
      this.gamble = await Api.post("bets/" + this.bet.id + "/gamble/", {
        choice: choiceInteger,
        amount: amount,
      });
      //update bet
      this.bet = await Api.get("bets/" + this.bet.id + "/");
      //update user
      Api.updateUser();
    },
  },
});
</script> 