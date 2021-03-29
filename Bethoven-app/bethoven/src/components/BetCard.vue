<!-- TEMPLATE -->
<template>
  <div>
    <v-card class="ma-2 pt-1">
      <!-- Title and text -->
      <v-row>
        <v-col cols="8">
          <v-row align="start" class="pa-2">
            <v-card-title class="keep-word" :class="isClickableCursor"  @click="goToDetail" 
              >
              {{ currentBet.title }}
              <v-chip v-if="currentBet.isClosed" class="mx-1"> Closed </v-chip>
            </v-card-title>
          </v-row>
        </v-col><v-spacer></v-spacer>
        <v-col cols="auto" class="pa-2 mx-3">
          <!-- "refresh" option -->
          <v-switch v-model="switchMe">
            <template v-slot:label>
              <v-progress-circular
                :indeterminate="switchMe"
                :value="0"
              ></v-progress-circular>
            </template>
          </v-switch>
        </v-col>
      </v-row>

      <v-card-text class="mx-2 px-1 mb-3">{{
        currentBet.description
      }}</v-card-text>

      <!-- 'bet' part with choices and bet buttons -->
      <v-row class="mx-2 px-1">
        <v-card-subtitle class="pa-0"
          >votes : {{ currentBet.bet_ratio.number }}
          <v-icon>mdi-account</v-icon>
        </v-card-subtitle>
        <v-card-subtitle class="pa-0">
          amount : {{ currentBet.bet_ratio.total }}
          <v-icon>mdi-alpha-b-circle-outline</v-icon>
        </v-card-subtitle>
      </v-row>

      <v-row class="mx-2 px-1" align="center" justify="start">
        <!-- display result -->
        <v-card-subtitle class="ml-0 pl-0">
          Result : <span :class="resultColor">{{ betResult }}</span>
        </v-card-subtitle>
        <!-- If the user has already bet : Display the bet -->
        <v-card-subtitle v-if="userBet">
          you bet {{ userBet.amount }}
          <v-icon :class="currentBetColor"
            >mdi-alpha-b-circle-outline</v-icon
          >
        </v-card-subtitle>
        <v-card-subtitle v-if="hasGain">
          you won {{ userBet.gain }}
          <v-icon>mdi-alpha-b-circle-outline</v-icon>
        </v-card-subtitle>
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
                currentBet.choice0
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
                currentBet.choice1
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
      switchMe: this.refresh,
      periodicRefresh: this.refresh,
      isClickable: this.clickable,
    };
  },
  props: {
    bet: {},
    detail: false,
    refresh: false,
    clickable: true,
  },
  watch: {
    //called whenever switchMe changes
    switchMe(switchValue) {
      if (switchValue && !this.periodicRefresh) {
        this.periodicRefresh = setInterval(() => {
          this.refreshBet();
        }, 1000);
      } else {
        clearInterval(this.periodicRefresh);
      }
    },
  },
  computed: {
    hasProgress() {
      return this.currentBet.bet_ratio.number > 0;
    },
    canBet() {
      //can bet if user hasn't already bet and the bet is not closed
      return this.userBet == null && !this.currentBet.isClosed;
    },
    hasAlreadyBet() {
      return this.userBet != null;
    },
    //named lambda functon to be retrieved from other computed functions
    userBet: function () {
      return this.currentBet.currentUserBet;
    },
    hasGain() {
      if (this.userBet == null) return false;
      return this.userBet.gain != null;
    },
    currentBetColor() {
      if (this.userBet == null) return;
      return this.currentBet.currentUserBet.choice == 0
        ? "teamA--text"
        : "teamB--text";
    },
    resultColor() {
      if (this.currentBet.result == null) return;
      return this.currentBet.result == 0 ? "teamA--text" : "teamB--text";
    },
    betResult() {
      if (this.currentBet.result == null) return "Pending";
      return this.currentBet.result == 0
        ? this.currentBet.choice0
        : this.currentBet.choice1;
    },
    isClickableCursor() {
      return this.isClickable ? "clickable" : "";
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

      this.refreshBet();

      //update user
      Api.updateUserInformations();
    },
    async refreshBet() {
      //update bet
      this.currentBet = await Api.get("bets/" + this.bet.id + "/");
      return this.currentBet;
    },
    goToDetail() {
      if (this.isClickable) {
        this.$router.push({ path: "bets/" + this.currentBet.id });
      }
    },
  },
});
</script> 

<style scoped>
.clickable {
  cursor: pointer;
}
</style>