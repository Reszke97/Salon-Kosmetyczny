<template>
  <v-dialog
    :value="visitTimeDialog"
    dark
    persistent
  >
    <v-row 
      class="bg-color white-text"
      :style="{ minHeight: `400px` }"
    >
      <v-col
        cols="12"
      >
        <div class="flex-centered flex-column" style="font-size:medium;">
          <span>
            <span class="font-bold">
              {{ `Data: ${selectedDate.date}` }}
            </span>
          </span>
          <span>
            <span class="font-bold">
              {{ `Cena: ${selectedDate.service.price} zł, Czas: ${selectedDate.service.duration}min` }}
            </span>
          </span>
          <span 
            v-if="selectedTime"
            class="font-bold" 
            style="color: orange;"
          >
            {{ `Godzina: ${selectedTime.start_time} - ${selectedTime.end_time}` }}
          </span>
        </div>
        <div class="flex-centered flex-column pb-1">
          <div class="d-flex flex-row">
            <div
              :class=" idx === 1 ? 'd-flex flex-column pr-2' : 'd-flex flex-column pr-2'"
              v-for="idx of Math.floor(mappedDateItems.items.length/7) + ((mappedDateItems.items.length % 7) > 0 ? 1 : 0)"
            >
              <template
                v-for="jdx of 7"
              >
                <div
                  v-if="mappedDateItems.items[(idx * 7) - (8 - jdx)]"
                >
                  <v-chip
                    class="ma-1"
                    color="success"
                    label
                    text-color="white"
                    style="width: 100%;"
                    @click="setSelectedTime(mappedDateItems.items[(idx * 7) - (8 - jdx)])"
                  >
                    {{ 
                      `${
                        mappedDateItems.items[(idx * 7) - (8 - jdx)].start_time
                      } - ${mappedDateItems.items[(idx * 7) - (8 - jdx)].end_time}` 
                    }}
                    <v-icon right>
                      mdi-plus
                    </v-icon>
                  </v-chip>
                </div>
              </template>
            </div>
          </div>
          <div 
            class="mt-5 d-flex flex-row w-100 ml-2"
          >
            <div class="mr-2">
              <v-btn
                @click="$emit('closeDialog')"
                color="background"
              >
                <v-icon left>
                  mdi-close-circle
                </v-icon>
                Zamknij
              </v-btn>
            </div>
            <div class="mr-2">
              <v-btn
                @click="setConfirmationDialog(true)"
                color="background"
                :disabled="!selectedTime"
              >
                <v-icon left>
                  mdi-content-save-outline 
                </v-icon>
                Zapisz
              </v-btn>
            </div>
          </div>
        </div>
      </v-col>
      <confirm-dialog
        v-if="confirmationDialog"
        :dialog="confirmationDialog"
        :onConfirmAction="saveVisitAndOpenSummaryDialog"
        :setDialog="setConfirmationDialog"
      />
      <visit-summary
        v-if="summaryDialog"
        :dialog="summaryDialog"
        :summary="summary"
        @closeSummary="closeSummaryDialog"
      />
    </v-row>
  </v-dialog>
</template>

<script>
  import ConfirmDialog from "../../../../utils/Components/Dialog.vue"
  import VisitSummary from "./VisitSummary.vue"
  import { AUTH_API } from "../../../../authorization/AuthAPI"

  export default {
    name: "",
    components: {
      ConfirmDialog,
      VisitSummary,
    },
    props: {
      visitTimeDialog: { type: Boolean, required: true },
      selectedDate: { type: Object, required: true },
      componentDims: { type: Object, required: true },
      selectedService: { type: Object, required: true },
    },
    emits: [ "closeDialog", "successSave" ],
    data: () => ({
      selectedTime: null,
      confirmationDialog: false,
      summaryDialog: false,
      summary: null,
    }),
    computed: {
      mappedDateItems(){
        const mappedHours = this.selectedDate.items.map(item => {
          const mappedStartTime =  item.start_time.length === 7 ? "0" + item.start_time : item.start_time
          const mappedEndTime =  item.end_time.length === 7 ? "0" + item.end_time : item.end_time
          return {
            start_time: mappedStartTime,
            end_time: mappedEndTime,
          }
        })
        return {
          ...this.selectedDate,
          items: [...mappedHours]
        }
      }
    },
    methods: {
      setSelectedTime(time){
        this.selectedTime = { ...time }
      },
      setConfirmationDialog(val){
        this.confirmationDialog = val;
      },
      async saveVisit(resolve, reject){
        this.summary = {
          service_id: this.selectedDate.service.service_id,
          employee_id: this.selectedDate.employee.employee_id,
          employee_first_name: this.selectedDate.employee.employee_first_name,
          employee_last_name: this.selectedDate.employee.employee_last_name,
          user: "client",
          service_name: this.selectedService.service_name,
          business: this.selectedService.business,
          dateTime: {
            date: this.selectedDate.date,
            ...this.selectedTime,
          }
        }
        const API = await AUTH_API();
        await API.post("/api/v1/client/visit/", { ...this.summary })
        .then(res => {
          resolve(res)
        })
        .catch(err => {
          reject(err)
        })
      },
      async saveVisitAndOpenSummaryDialog(){
        new Promise( async (resolve, reject) => {
          await this.saveVisit(resolve, reject);
        })
        .then(() => {
          this.setConfirmationDialog(false);
          this.openSummaryDialog();
        })
        .catch(err => {
          console.log(err)
        })
      },
      openSummaryDialog(){
        this.summaryDialog = true;
      },
      closeSummaryDialog(){
        this.summaryDialog = false;
        this.$emit("successSave");
      },
    }
  }
</script>