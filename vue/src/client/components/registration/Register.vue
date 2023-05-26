<template>
  <v-row
    align="center"
    justify="center"
  >
    <v-col
      cols="11"
      sm="9"
      md="6"
      lg="3"
    >
      <v-stepper class="indigo" dark>
        <v-stepper-header class="">
          <div style="
              display: flex; 
              justify-content: center; 
              align-items: center; 
              width: 100%;
            "
          >
            <h3>
              Dane użytkownika
            </h3>
          </div>
        </v-stepper-header>
        <v-stepper-items>
          <v-stepper-content 
            :step="1"
          >
            <client-info 
              :inputData="inputData"
              :setInput="setInput"
              ref="clientInfo"
            />
          </v-stepper-content>
        </v-stepper-items>
        <v-row style="padding: 0px 24px 16px">
          <v-col
            cols="6"
            sm="4"
            style="padding-top: 0px!important"
          >
            <v-btn
              color="success"
              @click="submit"
              style="width:100%!important"
            >
              Zapisz
            </v-btn>
          </v-col>
          <v-col
            cols="6"
            sm="4"
            style="padding-top: 0px!important"
          >
          </v-col>
        </v-row>
      </v-stepper>
    </v-col>
    <account-activation
      :activation-dialog="activationDialog"
      @closeActivateDialog="closeActivateDialog"
    />
  </v-row>
</template>

<script>
import axios from 'axios'
import ClientInfo from "./ClientInfo.vue"
import AccountActivation from "./AccountActivation.vue";

export default {
  components: {
    ClientInfo,
    AccountActivation,
  },
  data() {
    return {
      inputData: {
        email: '',
        userName:'',
        password1:'',
        password2:'',
        name: '',
        lastName:'',
        phone: '',
        valid: true,
      },
      activationDialog: false,
    };
  },

  methods: {
    submit () {
      const IS_VALID = this.$refs.clientInfo.validate()
      if(IS_VALID){
        this.sendForm()
      }
    },
    closeActivateDialog() {
      this.activationDialog = false;
      window.location.assign("/client/login");
    },
    openActivationDialog(){
      this.activationDialog = true;
    },
    setInput(value, key){
      this.inputData[key] = value;
    },
    async checkValidNames(){
      await axios.get(
        `http://127.0.0.1:8000/api/v1/user/check-for-unique-names/?username=${
          this.inputData.userName
        }&business_name=${""}`
      )
      .then( res => {
        const { unique_username } = res.data;
        if(!unique_username) {
          this.valid = false;
          const notUniqueUsernameMessage = "Podana nazwa użytkownika jest już zajęta!\n"
          const finalMessage = notUniqueUsernameMessage;
          alert(finalMessage);
        }
      })
    },
    async sendForm(){
      this.inputData.valid = true;
      this.valid = this.$refs.clientInfo.$refs.form.validate();
      if (!this.valid) return;
      await this.checkValidNames();
      if (!this.valid) return;

      await axios.post('http://127.0.0.1:8000/api/v1/user/register/', 
        {
          userForm: {
            is_employee: false,
            email: this.inputData.email,
            user_name: this.inputData.userName,
            password: this.inputData.password1,
            first_name: this.inputData.name,
            last_name: this.inputData.lastName,
          }
        },
      )
      .then(() => {
        this.openActivationDialog();
      })
      .catch(error => {
        alert(error)
      })
    },
  },
};
</script>
<style>
.text-white textarea {
  color: white !important;
}
.label-white label {
  color: white !important;
}
.custom-stepper {
  background: none !important;
  box-shadow: none !important;
}
.custom-header {
  box-shadow: 0 2px 2px -2px rgb(3 13 0) !important;
}
</style>