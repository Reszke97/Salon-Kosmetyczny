<template>
  <v-dialog
    :value="signUpForVisitDialog"
    dark
    persistent
    :width="componentDims.width"
  >
    <v-row 
      class="bg-color white-text"
      :style="{ minHeight: `400px` }"
    >
      <v-col
        cols="12"
      >
        <div class="flex-centered">
          <h2>
            <span>
              Zapis na usługę 
            </span>
            <span style="color: orange!important">
              {{ selectedService.service_name }}
            </span>
          </h2>
        </div>
        <div>
          <v-btn 
            @click="closeSignUpForVisitDialog"
            color="success"
          >
            <v-icon left>
              mdi-close-circle
            </v-icon>
            Zamknij
          </v-btn>
        </div>
      </v-col>
    </v-row>
  </v-dialog>
</template>

<script>
  import axios from "axios"
    export default {
        name: "",
        components: {
            
        },
        props: {
          signUpForVisitDialog: { type: Boolean, required: true },
          selectedService: { type: Object, required: true },
          componentDims: { type: Object, required: true },
          closeSignUpForVisitDialog: { type: Function, required: true },
        },
        data: () => ({
          employees: [],
        }),
        computed: {
            
        },
        async created(){
          this.setEmployees();
          await this.getAvailableDateTime();
        },
        methods: {
          setEmployees(){
            for(const employee of this.selectedService.employees){
              this.employees.push({
                emp_id: employee.id,
                user_info: employee.user,
              })
            }
          },
          async getAvailableDateTime(){
            await axios.get(`http://127.0.0.1:8000/api/v1/client/employee-availability/?${
              this.employees.map((employee, idx) => `employee-${idx}=${employee.emp_id}`).join('&')
            }&service_name=${this.selectedService.service_name}`)
          },
        }
    }
</script>

<style>
  @import "../../../../../styles/globalStyles.css";
</style>