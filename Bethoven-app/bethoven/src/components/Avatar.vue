<!-- TEMPLATE -->
<template>
  <v-avatar :color="getColor()" size="40">
    <span class="white--text headline text-center">{{ getInitials() }}</span>
  </v-avatar>
</template>

<!-- SCRIPT -->
<script>
import Vue from "vue";

export default Vue.extend({
  props: {
    uname: "",
  },
  data() {
    return {
      r: 0,
      g: 0,
      b: 0,
    };
  },
  methods: {
    getColor() {
      var s = this.uname;
      var hash = s.split("").reduce(function (a, b) {
        a = (a << 5) - a + b.charCodeAt(0);
        return a & a;
      }, 0);
      var r = (hash & 0xff0000) >> 16;
      var g = (hash & 0x00ff00) >> 8;
      var b = hash & 0x0000ff;
      return "rgb(" + r + "," + g + "," + b + ")";
    },
    getInitials: function () {
      if (this.uname) {
        return this.uname
          .match(/\b(\w)/g)
          ?.join("")
          .toUpperCase();
      } else {
        return "??";
      }
    },
  },
});
</script>
