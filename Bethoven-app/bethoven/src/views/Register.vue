<template>
  <v-container fill-height fluid>
    <v-row align="center" justify="center">
      <v-col align="center">
        <v-card class="mx-auto" max-width="450">
          <v-card-text>
            <v-text-field
              label="Username"
              v-model="username"
              :disabled="loading"
              :rules="[rules.required]"
              prepend-icon="mdi-account"
              :error-messages="errors['username']"
              class="my-5"
            ></v-text-field>
            <v-text-field
              label="Email"
              v-model="email"
              :disabled="loading"
              :rules="[rules.email]"
              prepend-icon="mdi-email"
              :error-messages="errors['email']"
              class="my-5"
            ></v-text-field>
            <v-spacer></v-spacer>
            <v-text-field
              :append-icon="showPassord ? 'mdi-eye' : 'mdi-eye-off'"
              prepend-icon="mdi-lock"
              :disabled="loading"
              :rules="[rules.required, rules.min]"
              :type="showPassord ? 'text' : 'password'"
              label="Password"
              v-model="password"
              :error-messages="errors['password']"
              class="my-5"
              @click:append="showPassord = !showPassord"
            ></v-text-field>
            <v-text-field
              :append-icon="showPassord ? 'mdi-eye' : 'mdi-eye-off'"
              prepend-icon="mdi-lock"
              :disabled="loading"
              :rules="[rules.required, rules.min]"
              :type="showPassord ? 'text' : 'password'"
              label="Password confirmation"
              v-model="passwordConfirmation"
              class="my-5"
              @keydown.enter="signup"
              @click:append="showPassord = !showPassord"
            ></v-text-field>
          </v-card-text>
          <v-btn
            elevation="4"
            x-large
            class="primary white--text my-3 mt-0 mb-5"
            large
            rounded
            :loading="loading"
            v-on:click="signup"
            >Register</v-btn
          >
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Vue from "vue";
import Api from "@/api/ApiRequester";

export default Vue.extend({
  name: "Register",
  methods: {
    signup: async function () {
      this.loading = true;
      try {
        if (this.password == this.passwordConfirmation) {
          await Api.register({
            username: this.username,
            email: this.email,
            password: this.password,
            password_confirmation: this.passwordConfirmation,
          });
          this.$router.push({ name: "Home" });
        } else {
          this.errors["password"] = "Not the same password";
        }
      } catch (e) {
        console.log(e);
        if ("username" in e) {
          this.errors["username"] = e.username[0];
        }
      } finally {
        this.loading = false;
      }
    },
  },
  data() {
    return {
      username: "",
      email: "",
      password: "",
      passwordConfirmation: "",
      loading: false,
      showPassord: false,
      errors: {
        email: "",
        name: "",
        firstname: "",
        password: "",
      },
      rules: {
        required: (value) => !!value || "Required",
        min: (v) => v.length >= 6 || "Minimum 6 characters",
        email: (value) => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          return pattern.test(value) || "Invalid e-mail.";
        },
      },
    };
  },
});
</script>
