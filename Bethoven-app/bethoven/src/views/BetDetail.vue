<template>
<v-container>
    <v-row justify="center">
        <v-col xl="4"   cols="12" >
            <bet-card v-if="this.bet!=null"
            :bet="this.bet" 
            :detail="true" 
            :clickable="false" 
            :refresh="true"
            ></bet-card>
           
        </v-col> 
    </v-row>
    <div>
    <v-row v-if="0" justify="center">
        <v-col cols=auto>
            <v-combobox
            clearable
            dense
            filled
            solo
            >
            </v-combobox>
            
        </v-col>
    </v-row>
    <v-row  v-if="0" justify="center">
        <v-btn>Reveal</v-btn>
    </v-row>
    <v-row justify="center">
        <v-btn>Close</v-btn>
    </v-row>
    {{this.$store.state.user.id}}
    {{this.bet.owner}}
    {{isOwner()}}
    </div>
    
</v-container>
</template>

<script>
import BetCard from '../components/BetCard.vue';
import Api from "@/api/ApiRequester";
export default {
  components: { BetCard },
    async beforeMount(){
        this.bet = await Api.get('bets/'+this.id);
        console.log(this.bet.title);
    },
    props:{
        id:null,
    },
    data(){
        return{
            bet:null
        }
    },
    methods:{
        isOwner(){
            return this.$store.state.user.id==this.bet.owner;
        }
    }
}

</script>

<style>

</style>