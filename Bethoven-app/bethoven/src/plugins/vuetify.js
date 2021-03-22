import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import colors from 'vuetify/lib/util/colors'


Vue.use(Vuetify);

const vuetify = new Vuetify({
  theme: {
    themes: {
      light: {
        teamA: colors.purple.lighten1,
        teamB: colors.orange.darken1,
      },
      dark: {
      },
    },
  },
})

export default new Vuetify({
});
