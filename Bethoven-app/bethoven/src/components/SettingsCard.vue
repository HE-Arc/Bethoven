<template>
 <v-form
    ref="form"
    @submit.prevent="submit">
        <v-container fill-height fluid>       
            <v-row align="center" justify="center">
                <v-col align="center">
                    <v-card class="mx-auto" max-width="450">
                        <v-text-field 
                        v-model="form.email"
                        label = "Email"
                        :rules="[rules.required, rules.email]"
                        class=" pt-10 pl-10 pr-10" >
                        </v-text-field>
                        <v-text-field 
                        v-model="form.username"
                        label = "Username"
                        :rules="[rules.required]"
                        class=" pt-10 pl-10 pr-10"
                        >
                        </v-text-field>
                        <v-text-field
                        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        v-model="form.password" 
                        label = "Password" 
                        :type="showPassword ? 'text' : 'password'"
                        :rules="[rules.required]"
                        @click:append="showPassword = !showPassword"
                        class="pt-10 pl-10 pr-10">
                        </v-text-field>

                        <v-text-field 
                        :append-icon="showNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        v-model="form.new_password"
                        :type="showNewPassword ? 'text' : 'password'"
                        :rules="[rules.min]"
                        @click:append="showNewPassword = !showNewPassword"
                        class="pt-10 pl-10 pr-10">
                        
                            <template v-slot:label>
                                <div>
                                    New Password <small>(optional)</small>
                                </div>
                            </template>
                        </v-text-field>
                        <v-btn
                        :disabled="!formIsValid"
                        text
                        color="primary"
                        type="submit"
                        class = "pa-10"
                        >
                            Modify
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
            email: this.$store.state.user.email,
            username: this.$store.state.user.username,
            password: "",
            new_password: "",
        })
        return{
            form: Object.assign({}, defaultForm),
            defaultForm,
            showPassword : false,
            showNewPassword : false,
            userId: this.$store.state.user.id,
            rules: {
                required: (value) => !!value || "Required",
                min: (v) => v.length >= 6 || "Minimum 6 characters",
                email: (value) => {
                    const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                    return pattern.test(value) || "Invalid e-mail.";
        },
      },
            
        }
    },
    props:{
        users : {},
    },
    computed: {
        formIsValid (){
            return(
                (this.form.email &&
                this.form.username &&
                this.form.password) ||
                (this.form.email &&
                this.form.username &&
                this.form.password &&
                this.form.new_password)
            )
        }

    },
    methods:{
        async submit(){
            try{
                let answer = await Api.put(`users/${this.userId}`,{
                    email: this.form.email,
                    username: this.form.username,
                    password: this.form.password,
                    new_password: this.form.new_password,

                });
                this.$router.push({path:`users/"+${this.userId}+"/`})
            }
            catch(e){
                //Catch error
                console.log(e);
            }
        }
    },
}
</script>

<style>

</style>