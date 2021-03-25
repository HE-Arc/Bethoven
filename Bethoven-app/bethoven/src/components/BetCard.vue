<!-- TEMPLATE -->
<template>
  <div>
    <v-card class="ma-2 pt-1">
      <!-- Title and text -->
      <v-card-title
        >{{ currentBet.title }}
        <v-chip v-if="currentBet.isClosed" class="ma-2">
          Closed
        </v-chip></v-card-title
      >

      <v-card-text>{{ currentBet.description }}</v-card-text>

      <!-- 'bet' part with choices and bet buttons -->
      <v-row class="align-left mx-1">
        <v-card-subtitle >
          votes : {{ currentBet.bet_ratio.number }} <v-icon>mdi-account</v-icon>
        </v-card-subtitle>
        <v-card-subtitle >
          amount : {{ currentBet.bet_ratio.total }}
          <v-icon>mdi-alpha-b-circle-outline</v-icon>
        </v-card-subtitle>
      </v-row>

      <!-- If the user has already bet : Display the bet -->
      <v-row v-if="hasAlreadyBet">
        <v-col align="center">
          <v-card-subtitle class="pa-0 float-right">
            Bet : {{ userBet.amount }}
            <v-icon :class="currentBetColor">mdi-alpha-b-circle-outline</v-icon>
          </v-card-subtitle>
        </v-col>
      </v-row>

      <v-progress-linear
        v-if="hasProgress"
        background-color="teamB"
        color="teamA"
        class="mt-1"
        :value="currentBet.bet_ratio.ratio[0]"
      ></v-progress-linear>

      <!-- Tab -->
      <v-row no-gutters v-if="detail">
        <v-col>
          <!--Choice 0-->
          <v-card outlined tile>
            <v-col class="text-right">
              <v-card-subtitle class="pa-1">{{
                currentBet.choice1
              }}</v-card-subtitle>
              <v-card-subtitle class="pa-1">
                {{ currentBet.bet_ratio.ratio[0] }} %</v-card-subtitle
              >

              <!-- Choice 0 button -->
              <v-row v-if="canBet" justify="start" align="center">
                <v-col>
                  <v-text-field
                    v-model="amount0"
                    hint="Place your bet"
                    type="number"
                    min="0"
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
          <!--Choice 1-->
          <v-card outlined tile>
            <v-col class="text-left">
              <v-card-subtitle class="pa-1">{{
                currentBet.choice2
              }}</v-card-subtitle>
              <v-card-subtitle class="pa-1"
                >{{ currentBet.bet_ratio.ratio[1] }} %</v-card-subtitle
              >
              <!-- Choice 1 button -->
              <v-row v-if="canBet" justify="start" align="center">
                <v-col>
                  <v-text-field
                    v-model="amount1"
                    hint="Place your bet"
                    type="number"
                    min="0"
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
    return {
      amount0: 0,
      amount1: 0,
      currentBet: this.bet,
    };
  },
  props: {
    bet: {},
    detail: false,
  },
  computed: {
    hasProgress() {
      return this.currentBet.bet_ratio.number > 0;
    },
    canBet() {
      //can bet if user hasn't already bet and the bet is not closed
      return this.userBet == null && !this.currentBet.isClosed;
    },
    hasAlreadyBet(){
      return this.userBet != null;
    },
    //named lambda functon to be retrieved from other computed functions
    userBet : function() {
      return this.currentBet.currentUserBet;
    },
    currentBetColor() {
      if (this.userBet == null) return;
      return this.currentBet.currentUserBet.choice == 0
        ? "teamA--text"
        : "teamB--text";
    },
  },
  methods: {
    getID() {
      return this.bet.id;
    },
    async gamble(choice) {
      //verify that the user is logged in
      if (!this.$store.state.isUserLogged) {
        this.$router.push({ name: "Login" });
        return;
      }

      //fetch choice and amount as integer
      let choiceInteger = parseInt(choice);
      let amount = parseInt(choice == 0 ? this.amount0 : this.amount1);

      //gamble
      this.gamble = await Api.post("bets/" + this.bet.id + "/gamble/", {
        choice: choiceInteger,
        amount: amount,
      });

      //update bet
      this.currentBet = await Api.get("bets/" + this.bet.id + "/");
      //update user
      Api.updateUserInformations();
    },
  },
});
</script> 