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
      <v-stepper v-model="stepperPosition" class="indigo" dark>
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
              :disabled="!inputData.valid"
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
    <v-dialog
      v-model="activation"
      width="500"
    >
      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Na podany email został przesłany link do aktywacji konta.
        </v-card-title>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="activation = false"
          >
            Zamknij
          </v-btn>
          <v-btn
            color="primary"
            text
          >
            Przejdź do logowania
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import axios from 'axios'
import ClientInfo from "./ClientInfo.vue"

export default {
  components: {
    ClientInfo,
  },
  data() {
    return {
      stepperPosition: 1,
      stepperPositionPrev: 1,

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
      activation: false,
    };
  },

  methods: {
    submit () {
      const IS_VALID = this.$refs.clientInfo.validate()
      if(IS_VALID){
        this.sendForm()
      }
    },
    reset () {
      this.inputData.checkbox = false
      this.inputData.lastName = ''
      this.inputData.password2 = ''
      this.inputData.password1 = ''
      this.inputData.userName = ''
      this.inputData.email = ''
      this.activation = false
      this.inputData.valid = ''
      this.inputData.name = ''
      this.$refs.clientInfo.resetValidation()
    },
    setInput(value, key){
      this.inputData[key] = value;
    },
    sendForm(){
      axios.post('http://127.0.0.1:8000/api/v1/user/register/', 
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
        this.activation = true
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