<template>
<v-container>
    <v-row justify="center">
        <v-col xl="8"   cols="12" >
            <bet-card v-if="this.bet!=null"
            :bet="this.bet" 
            :detail="true" 
            :clickable="false" 
            :refresh="true"
            ></bet-card>
           
        </v-col> 
    </v-row>
    <div v-if="isOwner()">
        <v-row v-if="isClosed() && !isRevealed()" justify="center">
            <v-col cols=auto>
                <v-combobox
                clearable
                dense
                filled
                solo
                :items="choices"
                id="cbx"
                >
                </v-combobox>
                
            </v-col>
        </v-row>
        <v-row  v-if="isClosed() && !isRevealed()" justify="center">
            <v-btn @click="revealAnswer">Reveal</v-btn>
        </v-row>
        <v-row v-if="!isClosed()" class="pt-4" justify="center">
            <v-btn @click="closeBet">Close</v-btn>
        </v-row>
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
        this.choices.push(this.bet.choice0);
        this.choices.push(this.bet.choice1);
    },
    props:{
        id:null,
    },
    data(){
        return{
            bet:null,
            choices:[]
        }
    },
    methods:{
        isOwner(){
            if(this.bet!=null){
            return this.$store.state.user.id==this.bet.owner;
            }
        },
        isClosed(){
            return this.bet.isClosed;
        },
        selectedChoice(){
            var elem = document.getElementById('cbx');
            if(elem.value!=''){
                return elem.value;
            }
        },
        sendIndex(){
            if(this.choices.includes(this.selectedChoice())){
                return this.choices.findIndex(choice => choice === this.selectedChoice());
            }
        },
        isRevealed(){
            if(this.bet!=null){
                return this.bet.result!=null;
            }
        },
        async revealAnswer(){
            await Api.patch('bets/'+this.id+'/',{
                result:this.sendIndex()
                });
            this.refreshBet();
            location.reload();
        },
        async refreshBet() {
            //update bet
            this.bet = await Api.get("bets/" + this.id + "/");
        },
        async closeBet(){
            await Api.patch('bets/'+this.id+'/',{
                isClosed:true
                });
            this.refreshBet();
            location.reload();
        }
        
    }
}

</script>

<style>

</style>