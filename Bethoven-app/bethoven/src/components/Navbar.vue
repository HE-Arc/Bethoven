<template>
  <v-bottom-navigation :value="value" color="primary" fixed app>
    <v-btn to="/trending">
      <span>Trending</span>
      <v-icon>mdi-trending-up</v-icon>
    </v-btn>

    <v-btn to="/home">
      <span>home</span>
      <v-icon>mdi-home</v-icon>
    </v-btn>

    <v-btn to="/mybet">
      <span>My bet</span>
      <v-icon>mdi-alpha-b-circle</v-icon>
    </v-btn>

    <v-btn to="/create">
      <span>Create bet</span>
      <v-icon>mdi-plus-box</v-icon>
    </v-btn>
  </v-bottom-navigation>
</template>

<script>
export default {
  data: () => ({ value: 0 }),
};
</script>