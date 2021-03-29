<template>
  <v-container fill-height fluid>
    <v-row align="center" justify="center">
      <v-col align="center" justify="center" cols="8">
        <img alt="Vue logo" src="../assets/bethoven.png" width="200" />
        <section>
          <p>Welcome to Bethoven !</p>
          <p>Bethoven is a social network-kind of site, akin to reddit. It allows you to share bets with your friend ! <br>
          The social network is centered around feeds of bets. You can navigate between feeds with the navbar at the bottom of this page <br>
          The <a @click="goTo('FeedTrending')">trending feed</a> is available right now. You can see the lastly created and most popular bets of the moments.</p>
          <p>If you wish to discover the full possibilities of Bethoven, we invite to to <a @click="goTo('Register')">create an account</a>. Beeing logged in gives you access to follow the
          best bet-creators of the website (or <a @click="goTo('Search')">your friends</a>). You can access your personnal "home" feed, which gives you a view on your followed friend's bets, and the "mybet"
          feed, which allows you to monitor your bets created and pending.</p>
          <p>This project is made by Ravindranathan Rajinth, Dos Santos Ferrera Julien and Welcken Maxime for the 3rd year course of 
            web development at <a href="https://www.he-arc.ch/">He-Arc Neuchâtel</a>. If you have any issue or want to check the code, the website is entirely open-source
            on <a href="https://github.com/HE-Arc/Bethoven">Github</a> : Don't hesitate to create an issue ! </p>
        </section>
      </v-col></v-row
    ></v-container
  >
</template>

<script>
import Vue from "vue";

export default Vue.extend({
  name: "Home",
  methods : {
    goTo(path) {
      this.$router.push({ name: path });
    },
  }
});
</script>