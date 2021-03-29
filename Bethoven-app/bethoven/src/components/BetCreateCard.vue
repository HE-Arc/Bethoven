<template>
    <v-form
    ref="form"
    @submit.prevent="submit">
        <v-container fill-height fluid>       
            <v-row align="center" justify="center">
                <v-col align="center">
                    <v-card class="mx-auto" max-width="450">
                        <v-text-field 
                        v-model="form.title"
                        label = "Bet title"
                        class=" pt-10 pl-10 pr-10" >
                        </v-text-field>
                        <v-textarea  
                        v-model="form.description"
                        class=" pt-10 pl-10 pr-10"
                        >
                            <template v-slot:label>
                                <div>
                                    Bet description
                                </div>
                            </template>
                        </v-textarea>
                        <v-row>
                        <v-col>
                            <v-text-field
                            v-model="form.choice0" 
                            label = "First Choice" 
                            class="pt-10 pl-10 pr-10">
                            </v-text-field>
                        </v-col>
                        <v-col>
                            <v-text-field 
                            v-model="form.choice1"
                            label = "Second Choice" 
                            class="pt-10 pl-10 pr-10">
                            </v-text-field>
                        </v-col>
                        </v-row>
                        <v-btn
                        :disabled="!formIsValid"
                        text
                        color="primary"
                        type="submit"
                        class = "pa-10"
                        >
                            Create
                        </v-btn>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </v-form>
</template>

<script>
import Vue from "vue";
import Api from "@/api/ApiRequester";
export default {
    data() {
        const defaultForm = Object.freeze({
            title: "",
            description: "",
            choice0: "",
            choice1: "",
        })
        return{
            form: Object.assign({}, defaultForm),
            defaultForm,
        }
    },
    computed: {
        formIsValid (){
            return(
                this.form.title &&
                this.form.description &&
                this.form.choice0 &&
                this.form.choice1
            )
        }
    },
    methods:{
        async submit(){
            let answer = await Api.post("bets/",{
                title: this.form.title,
                description: this.form.description,
                choice0: this.form.choice0,
                choice1: this.form.choice1,

            });
            let id = answer.bet.id
            this.$router.push({path:"bets/"+id+"/"})
        }
    },
}
</script>

<style>

</style>