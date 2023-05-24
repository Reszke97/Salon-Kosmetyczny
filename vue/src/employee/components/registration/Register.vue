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
      @closeActivateDialog="closeActivateDialog"
    />
  </v-row>
</template>

<script>
import axios from "axios";

import AboutOwner from "./AboutOwner.vue";
import BusinessActivity from "./BusinessActivity.vue";
import StepperFooter from "./StepperFooter.vue";
import AccountActivation from "./AccountActivation.vue";

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

const userInfo = {
  email: "bromex3125@gmail.com",
  userName: "Recha",
  password1: "Marik1234",
  password2: "Marik1234",
  name: "Marcin",
  lastName: "Reszke",
  selectedSpec: "Tester",
  isNewSpec: true,
}

const businessInfo = {
  name: "Rechas",
  post_code_part1: "84",
  post_code_part2: "200",
  city: "Wejherowo",
  street: "asd",
  apartment_number: "1",
  house_number: "2",
  contact_phone: "",
}

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
        about: "",
      },
      defaultSpecializations: [],
      valid: true,
      validBusiness: true,
      stepperPosition: 1,
      stepperPositionPrev: 1,
      activationDialog: false,
    };
  },
  async created(){
    await this.getAllSpecs();
    this.ownerInfo = {...userInfo}
    this.salonInfo = {...businessInfo}
  },
  methods: {
    async getAllSpecs(){
      await axios.get("http://127.0.0.1:8000/api/v1/employee/all-specs/")
      .then(res => {
        this.defaultSpecializations = res.data;
      })
    },
    closeActivateDialog() {
      this.activationDialog = false;
    },
    toggleSpecInput() {
      this.ownerInfo.isNewSpec = !this.ownerInfo.isNewSpec
    },
    setOwnerInfo({ prop, val }){
      this.ownerInfo[prop] = val;
    },
    setSalonInfo({ prop, val }){
      this.salonInfo[prop] = val;
    },
    async checkValidNames(){
      await axios.get(
        `http://127.0.0.1:8000/api/v1/user/check-for-unique-names/?username=${
          this.ownerInfo.userName
        }&business_name=${this.salonInfo.name}`
      )
      .then( res => {
        const { unique_username, unique_business_name } = res.data;
        if(!unique_username || !unique_business_name) {
          this.valid = false;
          const notUniqueUsernameMessage = "Podana nazwa użytkownika jest już zajęta!\n"
          const notUniqueBusinessNameMessage = "Podana nazwa działalności jest już zajęta!\n"
          let finalMessage = !unique_username ? notUniqueUsernameMessage : "";
          finalMessage += !unique_business_name ? notUniqueBusinessNameMessage : "";
          alert(finalMessage);
        }
      })
    },
    async submit () {
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
        return;
      }
      await this.checkValidNames();
      if(this.valid) await this.sendForm();
    },
    openActivationDialog(){
      this.activationDialog = true;
    },
    async sendForm(){
      await axios.post('http://127.0.0.1:8000/api/v1/user/register/', 
        {
          userForm: {
            is_employee: true,
            email: this.ownerInfo.email,
            user_name: this.ownerInfo.userName,
            password: this.ownerInfo.password1,
            first_name: this.ownerInfo.name,
            last_name: this.ownerInfo.lastName,
            selected_spec: this.ownerInfo.selectedSpec,
            is_new_spec: this.ownerInfo.isNewSpec,
          },
          businessForm: {
            name: this.salonInfo.name,
            city: this.salonInfo.city,
            street: this.salonInfo.street,
            apartment_number: this.salonInfo.apartment_number,
            house_number: this.salonInfo.house_number,
            contact_phone: this.salonInfo.contact_phone,
            post_code: `${this.salonInfo.post_code_part1}-${this.salonInfo.post_code_part2}`,
            about: this.salonInfo.about,
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