<template>
  <v-container>
    <v-card class="ma-2 pt-1">
        <v-card-title>Follows</v-card-title>
      <v-slide-group multiple show-arrows>
        <v-slide-item v-for="follow in follows" :key="follow.id">
                
          <v-card elevation="0" class="ma-1 pt-1 usercard" @click="goToProfil(follow.id)">
            <v-row >
              <v-col align="center">
                <avatar :uname="follow.username"></avatar>
              </v-col>
            </v-row>
            <v-row >
              <v-col align="center" >
                <v-card-subtitle class="ma-0 pa-0 text-truncate">{{ follow.username }}</v-card-subtitle>
              </v-col>
            </v-row>
          </v-card>
          <!-- </v-btn> -->
        </v-slide-item>
      </v-slide-group>
      <span>{{userNameHover}}</span>
    </v-card>
  </v-container>
</template>

<script>
import Avatar from "./Avatar.vue";
export default {
  components: { Avatar },
  props: {
    follows: null,
  },
  data(){
      return{
          userNameHover:"",
      }
  },
  methods:{
      goToProfil(id){
          console.log("coucou");
          this.$router.push({path:`/profil/${id}/`});
          this.$location.reload();
        //   this.$router.go();
      }
  }
};
</script>

<style>
.usercard{
    width: 100px;
}
</style>