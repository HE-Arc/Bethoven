<template>
  <v-container>
    <v-row justify="center">
      <v-col xl="8" cols="12">
        <bet-card
          v-if="this.bet != null"
          :bet="bet"
          :detail="true"
          :clickable="false"
          :refresh="true"
          ref="betCard"
        ></bet-card>
      </v-col>
    </v-row>
    <div v-if="isOwner()">
      <v-row v-if="isClosed() && !isRevealed()" justify="center">
        <v-col cols="auto">
          <v-combobox clearable dense filled solo :items="choices" id="cbx">
          </v-combobox>
        </v-col>
      </v-row>
      <v-row v-if="isClosed() && !isRevealed()" justify="center">
        <v-btn @click="revealAnswer">Reveal</v-btn>
      </v-row>
      <v-row v-if="!isClosed()" class="pt-4" justify="center">
        <v-btn @click="closeBet">Close</v-btn>
      </v-row>
    </div>
  </v-container>
</template>

<script>
import BetCard from "../components/BetCard.vue";
import Api from "@/api/ApiRequester";
export default {
  components: { BetCard },
  async beforeMount() {
    try {
      this.bet = await Api.get("bets/" + this.id);
      this.choices.push(this.bet.choice0);
      this.choices.push(this.bet.choice1);
    } catch (e) {
      console.log(e);
    }
  },
  props: {
    id: null,
  },
  data() {
    return {
      bet: null,
      choices: [],
    };
  },
  methods: {
    isOwner() {
      if (this.bet != null) {
        return this.$store.state.user.id == this.bet.owner;
      }
    },
    isClosed() {
      return this.bet.isClosed;
    },
    selectedChoice() {
      var elem = document.getElementById("cbx");
      if (elem.value != "") {
        return elem.value;
      }
    },
    sendIndex() {
      if (this.choices.includes(this.selectedChoice())) {
        return this.choices.findIndex(
          (choice) => choice === this.selectedChoice()
        );
      }
    },
    isRevealed() {
      if (this.bet != null) {
        return this.bet.result != null;
      }
    },
    async revealAnswer() {
      try {
        await Api.patch("bets/" + this.id + "/", {
          result: this.sendIndex(),
        });
        this.bet = await this.$refs.betCard.refreshBet();
      } catch (e) {
        console.log(e);
      }
    },
    async closeBet() {
      try {
        await Api.patch("bets/" + this.id + "/", {
          isClosed: true,
        });
        this.bet = await this.$refs.betCard.refreshBet();
      } catch (e) {
        console.log(e);
      }
    },
  },
};
</script>

<style>
</style>