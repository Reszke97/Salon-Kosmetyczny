<template>
  <v-row
    align="center"
    justify="center"
  >
    <v-col
      cols="11"
      sm="9"
      md="6"
      lg="5"
    >
      <v-stepper 
        v-model="stepperPosition" 
        class="indigo" 
        dark 
      >
        <v-stepper-header class="">
          <v-stepper-step
            :editable="true"
            :step="1"
            color="secondary"
          >
            Info o właścicielu
          </v-stepper-step>
          <v-divider/>
          <v-stepper-step
            :editable="true"
            :step="2"
            color="secondary"
          >
            Info o salonie
          </v-stepper-step>
        </v-stepper-header>
        <v-stepper-items>
          <v-stepper-content 
            :step="1"
          >
            <about-owner
              :owner-info="ownerInfo"
              :default-specializations="defaultSpecializations"
              @setOwnerInfo="setOwnerInfo"
              @toggleSpecInput="toggleSpecInput"
            />
          </v-stepper-content>
          <v-stepper-content 
            :step="2"
          >
            <business-activity
              :salon-info="salonInfo"
              @setSalonInfo="setSalonInfo"
            />
          </v-stepper-content>
        </v-stepper-items>
        <stepper-footer
          :valid="valid"
        />
      </v-stepper>
    </v-col>
    <account-activation
      :activation-dialog="activationDialog"
    />
  </v-row>
</template>

<script>
import axios from "axios";

import AboutOwner from "./AboutOwner.vue";
import BusinessActivity from "./BusinessActivity.vue";
import StepperFooter from "./StepperFooter.vue";
import AccountActivation from "./AccountActivation.vue";

import { employeeSpecs } from "../../../utils";

export default {
  components: {
    AboutOwner,
    BusinessActivity,
    StepperFooter,
    AccountActivation,
  },
  data() {
    return {
      ownerInfo: {
        email: '',
        userName: '',
        password1: '',
        password2: '',
        name: '',
        lastName: '',
        selectedSpec: "",
        isNewSpec: false,
      },
      salonInfo: {
        name: "",
        post_code: "",
        street: "",
        apartment_number: "",
        house_number: "",
        contact_phone: "",
      },
      defaultSpecializations: employeeSpecs(),
      valid: true,
      stepperPosition: 1,
      stepperPositionPrev: 1,
      activationDialog: false
    };
  },
  methods: {
    toggleSpecInput() {
      this.ownerInfo.isNewSpec = !this.ownerInfo.isNewSpec
    },
    setOwnerInfo({ prop, val }){
      this.ownerInfo[prop] = val;
    },
    setSalonInfo({ prop, val }){
      this.salonInfo[prop] = val;
    },
    submit () {
      // const IS_VALID = this.$refs.form.validate()
      // if(IS_VALID){
      //     this.sendForm()
      // }
    },
    async sendForm(){
      await axios.post('http://127.0.0.1:8000/api/v1/user/register/', {
        'email': this.email,
        'user_name': this.userName,
        'password': this.password1,
        'first_name': this.name,
        'last_name': this.lastName,
      })
      .then(response => {
        this.activation = true
      })
      .catch(error => {
        alert(error)
      })
    },
    setValid(val){
      this.valid = val;
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