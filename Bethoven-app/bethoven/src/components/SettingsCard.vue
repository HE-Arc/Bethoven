<template>
  <v-container fill-height fluid>
    <v-row align="center" justify="center">
      <v-col align="center">
        <v-card class="mx-auto" max-width="450">
          <v-text-field
            v-model="email"
            :disabled="loading"
            label="Email"
            :rules="[rules.required, rules.email]"
            prepend-icon="mdi-email"
            :error-messages="errors['email']"
            class="pt-10 pl-10 pr-10"
          >
          </v-text-field>
          <v-text-field
            v-model="username"
            :disabled="loading"
            prepend-icon="mdi-account"
            label="Username"
            :rules="[rules.required]"
            :error-messages="errors['username']"
            class="pt-10 pl-10 pr-10"
          >
          </v-text-field>
          <v-text-field
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            prepend-icon="mdi-lock"
            v-model="password"
            :disabled="loading"
            label="Password"
            :type="showPassword ? 'text' : 'password'"
            :rules="[rules.required]"
            :error-messages="errors['password']"
            @click:append="showPassword = !showPassword"
            class="pt-10 pl-10 pr-10"
          >
          </v-text-field>

          <v-text-field
            :append-icon="showNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
            prepend-icon="mdi-lock"
            v-model="new_password"
            :disabled="loading"
            :type="showNewPassword ? 'text' : 'password'"
            :rules="[rules.min]"
            @click:append="showNewPassword = !showNewPassword"
            class="pt-10 pl-10 pr-10"
          >
            <template v-slot:label>
              <div>New Password <small>(optional)</small></div>
            </template>
          </v-text-field>
          <v-btn
            :loading="loading"
            text
            color="primary"
            v-on:click="submit"
            class="pa-10"
          >
            Modify
          </v-btn>
          <v-col justify="start" align="start" class="text-left">
            <v-row align="center" class="px-6">
              Add 15 betcoins :
              <v-btn text v-on:click="addBetcoins" class="pa-8">
                {{ coins }}
                <v-icon>mdi-alpha-b-circle-outline</v-icon>
              </v-btn>
            </v-row>
            <v-switch
              class="px-2"
              :label="`Dark mode : ${switchDarkmode.toString()}`"
              v-model="switchDarkmode"
            ></v-switch>
          </v-col>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Vue from "vue";
import Api from "@/api/ApiRequester";
export default {
  data() {
    return {
      email: this.$store.state.user.email,
      username: this.$store.state.user.username,
      password: "",
      new_password: "",
      showPassword: false,
      showNewPassword: false,
      loading: false,
      userId: this.$store.state.user.id,
      rules: {
        required: (value) => !!value || "Required",
        min: (v) => v.length >= 6 || "Minimum 6 characters",
        email: (value) => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          return pattern.test(value) || "Invalid e-mail.";
        },
      },
      errors: {
        email: "",
        username: "",
        password: "",
        new_password: "",
      },
      switchDarkmode: this.$vuetify.theme.dark,
    };
  },
  watch: {
    switchDarkmode(switched) {
      this.$vuetify.theme.dark = switched;
    },
  },
  computed: {
    coins() {
      return this.$store.state.user.coins;
    },
  },
  methods: {
    async submit() {
      this.loading = true;
      this.errors["username"] = "";
      this.errors["password"] = "";
      try {
        if (this.new_password) {
          await Api.put(`users/${this.userId}/`, {
            email: this.email,
            username: this.username,
            password: this.password,
            new_password: this.new_password,
          });
          Api.updateUserInformations();
          this.$router.push({ path: `/users/${this.userId}/` });
        } else if (this.password) {
          await Api.put(`users/${this.userId}/`, {
            email: this.email,
            username: this.username,
            password: this.password,
          });
          Api.updateUserInformations();
          this.$router.push({ path: `/users/${this.userId}/` });
        }
      } catch (e) {
        if (e.response.data.error) {
          if (e.response.data.error.includes("Username")) {
            this.errors["username"] = e.response.data.error;
          }
          if (e.response.data.error.includes("password")) {
            this.errors["password"] = e.response.data.error;
          }
        }
      } finally {
        this.loading = false;
      }
    },
    async addBetcoins() {
      try {
        await Api.post(`users/${this.userId}/addcoins/`);
        Api.updateUserInformations();
      } catch (e) {
        console.log(e);
      }
    },
  },
};
</script>

<style>
</style>