<!-- TEMPLATE -->
<template>
  <div>
    <v-card>
        <v-card-title>{{title}}</v-card-title>
        <h3>{{description}}</h3>
    </v-card>
  </div>
</template>


<!-- SCRIPT -->
<script>
import Vue from "vue";
import Api from "@/api/ApiRequester";

export default Vue.extend({
  name: "BetCard",
  props : {
    title : "",
    description : "",
  },
  computed: {
  },
  methods: {
  },
});
</script>