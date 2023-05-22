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
              ref="aboutOwner"
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
              ref="aboutBusiness"
              :salon-info="salonInfo"
              :valid="validBusiness"
              @setSalonInfo="setSalonInfo"
            />
          </v-stepper-content>
        </v-stepper-items>
        <stepper-footer
          :valid="valid"
          @submit="submit"
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

const stepperPositionArray = [
  {
    position: {
      value: 1,
      component: "aboutOwner",
      form: "ownerForm"
    }
  },
  {
    position: {
      value: 2,
      component: "aboutBusiness",
      form: "businessForm"
    }
  },
]

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
        post_code_part1: "",
        post_code_part2: "",
        city: "",
        street: "",
        apartment_number: "",
        house_number: "",
        contact_phone: "",
      },
      defaultSpecializations: employeeSpecs(),
      valid: true,
      validBusiness: true,
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
      this.valid = true;
      const foundItemIdx = stepperPositionArray.findIndex(el => el.position.value === this.stepperPosition);
      const firstItem = { ...stepperPositionArray[foundItemIdx].position };
      const otherItemIdx = foundItemIdx === 0 ? 1 : 0;
      const secondItem = { ...stepperPositionArray[otherItemIdx].position };
      this.validBusiness = true;

      this.valid = this.$refs[firstItem.component].$refs[firstItem.form].validate();
      if(!this.valid) {
        if(firstItem.component === "aboutBusiness") this.validBusiness = false;
        return;
      }
      this.stepperPosition = otherItemIdx + 1;
      this.valid = this.$refs[secondItem.component].$refs[secondItem.form].validate();
      if(!this.valid) {
        if(secondItem.component === "aboutBusiness") this.validBusiness = false;
        return
      }
      alert('all good')

      // ownerForm
      // businessForm
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