<template>
  <v-container >
    <v-card class="ma-2 pt-1">
      <v-row align="center"> 
        <v-col align="center" cols="3"> 
        <avatar v-if="this.user!=null" :uname="this.user.user.username"></avatar>
        </v-col >
        <v-col cols="5"> 
            <v-card-title v-if="this.user!=null" >{{this.user.user.username}} </v-card-title>
            <v-card-subtitle v-if="this.user!=null">
                {{this.user.user.coins}}
                <v-icon>mdi-alpha-b-circle</v-icon>
            </v-card-subtitle>
        </v-col>
        <v-col align="center" cols="4" v-if="this.$store.state.user.id != this.user.user.id"> 
            <v-btn v-on:click="this.follow"><v-icon>mdi-account-plus</v-icon></v-btn>
        </v-col>
        
        </v-row>
    </v-card>
    </v-container>
</template>

<script>
import Avatar from './Avatar.vue'
export default {
    components:{Avatar,},
    props:{
        user:{},
    },
    methods:{
        follow(){
            console.log("Follow");
            //TODO FOLLOW
        }
    }
}
</script>

<style>

</style>