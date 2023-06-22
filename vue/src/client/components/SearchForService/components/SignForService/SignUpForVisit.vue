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
        <div class="d-flex flex-column">
          <div
            v-for="schedule of employeeSchedule"
            class="d-flex flex-column pt-1"
          >
            <div class="d-flex flex-row pb-1">
              <div class="flex-centered flex-column" style="min-width: 140px;">
                <span style="width: 140px; text-align: center; word-wrap: break-word;">
                  {{ `${schedule.employee.user_info.first_name} ${schedule.employee.user_info.last_name}` }}
                </span>
                <v-avatar 
                  size="100"
                >
                  <v-icon
                    v-if="!schedule.employee.avatar.image"
                    :id="`employee-${schedule.employee.emp_id}`"
                    style="font-size:100px"
                    dark
                  >
                    mdi-account-circle
                  </v-icon>
                  <img
                    v-else
                    class="avatar"
                    :src="schedule.employee.avatar.image"
                    style="width:100%;height: 100%;"
                  />
                </v-avatar>
              </div>
              <div
                class="d-flex flex-column pr-2 flex-centered"
                v-for="idx of Math.floor(schedule.dates.length/4) + ((schedule.dates.length % 4) > 0 ? 1 : 0)"
              >
                <template
                  v-for="jdx of 4"
                >
                  <div
                    v-if="schedule.dates[(idx * 4) - (5 - jdx)]"
                  >
                    <v-chip
                      class="ma-1"
                      color="success"
                      label
                      text-color="white"
                      @click="test"
                    >
                      {{ schedule.dates[(idx * 4) - (5 - jdx)].date }}
                      <v-icon right>
                        mdi-plus
                      </v-icon>
                    </v-chip>
                  </div>
                </template>
              </div>
            </div>
            <v-divider></v-divider>
          </div>
        </div>
        <div class="pt-2">
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
          employeeSchedule: [],
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
                avatar: employee.avatar,
              })
            }
          },
          async getAvailableDateTime(){
            await axios.get(`http://127.0.0.1:8000/api/v1/client/employee-availability/?${
              this.employees.map((employee, idx) => `employee-${idx}=${employee.emp_id}`).join('&')
            }&service_name=${this.selectedService.service_name}`)
            .then(res => {
              res.data.forEach(item => {
                this.employeeSchedule.push({
                  employee: this.employees.find(emp => emp.emp_id === item.employee),
                  dates: item.dates
                })
              })
            })
          },
          test(){
            alert("test")
          }
        }
    }
</script>

<style>
  @import "../../../../../styles/globalStyles.css";
</style>