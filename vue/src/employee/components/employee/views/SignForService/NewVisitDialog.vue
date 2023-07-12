<template>
    <v-dialog
      :value="newVisitDialog"
      dark
      persistent
      :width="componentDims.width"
    >
      <v-row 
        class="bg-color white-text"
      >
        <v-col
          cols="12"
        >
            <div class="d-flex flex-column justify-center align-center">
                <h3>Tworzenie nowej wizyty dnia <span style="color:orange;">{{ newVisitData.date }}</span></h3>
                <v-form
                    ref="form"
                    v-model="formValid"
                >
                    <div style="width: 300px!important;">
                        <v-select
                            :items="services"
                            :value="newVisitData.service_id"
                            label="Wybór usługi"
                            item-text="service_name"
                            item-value="service_id"
                            :rules="required"
                            @change="val => $emit('updateNewVisitData', { key: 'service_id', val: val })"
                        />
                    </div>
                    <div class="d-flex flex-column">
                        <div 
                            style="width: 300px!important;"
                            v-if="newVisitData.user_does_not_exists"
                        >
                            <v-text-field
                                label="Podaj nazwę użytkownika"
                                :value="newVisitData.non_existent_user"
                                :rules="newVisitData.user_does_not_exists ? required : []"
                                @change="val => $emit('updateNewVisitData', { key: 'non_existent_user', val: val })"
                            />
                        </div>
                        <div
                            style="width: 300px!important;"
                            class="d-flex flex-column"
                            v-else
                        >
                            <v-autocomplete
                                :value="newVisitData.client_id"
                                label="Wybór użytkownika"
                                item-text="user_name"
                                item-value="user_id"
                                :items="clients"
                                :rules="!newVisitData.user_does_not_exists ? required : []"
                                @change="val => $emit('updateNewVisitData', { key: 'client_id', val: val })"
                            />
                        </div>
                        <div style="width: 300px!important;">
                            <v-checkbox
                                label="Brak użytkownika w liście"
                                :input-value="newVisitData.user_does_not_exists"
                                @change="val => $emit('updateNewVisitData', { key: 'user_does_not_exists', val: val })"
                            />
                        </div>
                    </div>
                </v-form>
                <div class="d-flex">

                    <v-btn
                        class="indigo"
                        dark
                        text
                        @click="checkValidityAndChooseHour"
                    >
                        Wybór godziny
                    </v-btn>
                    <v-btn
                        class="indigo ml-2"
                        dark
                        text
                        @click="$emit('closeNewVisitDialog')"
                    >
                        Zamknij
                    </v-btn>
                </div>
            </div>
            <choose-visit-time
                v-if="hourDialog"
                :visit-time-dialog="hourDialog"
                :selected-date="preparedDate"
                :component-dims="componentDims"
                :selected-service="preparedService"
                :userInfo="{
                    'user_does_not_exists': newVisitData.user_does_not_exists,
                    'non_existent_user': newVisitData.non_existent_user,
                    'client_id': newVisitData.client_id,
                }"
                type="new"
                @closeDialog="closeHourDialog"
                @successSave="closeTimeDialogAndRefresh"
            />
        </v-col>
      </v-row>
    </v-dialog>
</template>

<script>
    import { AUTH_API } from "../../../../authorization/AuthAPI"
    import { appendMimeType } from "../../../../../client/utils";
    import ChooseVisitTime from "./ChooseVisitTime.vue";
    export default {
        name: "",
        components: {
            ChooseVisitTime
        },
        props: {
            componentDims: { type: Object, required: true },
            newVisitDialog: { type: Boolean, required: true },
            newVisitData: { type: Object, required: true },
        },
        emits: [ "closeNewVisitDialog", "updateNewVisitData", "closeNewVisitDialogAndGetNewData" ],
        data: () => ({
            chooseTimeDialog: false,
            formValid: true,
            clients: [],
            services: [],
            required: [ v => !!v || 'Pole wymagane', ],
            preparedDate: {},
            preparedService: {},
            hourDialog: false,
        }),
        computed: {
            
        },
        async created(){
            await this.getEmployeeServicesAndClients();
        },
        methods: {
            closeTimeDialogAndRefresh(){
                this.closeHourDialog();
                this.$emit('closeNewVisitDialogAndGetNewData');
            },
            openHourDialog(){
                this.hourDialog = true;
            },
            closeHourDialog(){
                this.hourDialog = false;
            },
            async getEmployeeServicesAndClients(){
                const API = await AUTH_API();
                API.get(`/api/v1/employee/services-clients/?employee_id=${this.newVisitData.employee_id}`)
                .then(res => {
                    this.clients = res.data.clients;
                    this.services = res.data.services;
                })
                .catch(err => {
                    alert(err);
                })
            },
            async getWorkHoursForGivenDate(){
                const API = await AUTH_API();
                await API.get(`/api/v1/employee/new-visit/?employee_id=${this.newVisitData.employee_id}&service_id=${this.newVisitData.service_id}&date=${this.newVisitData.date}`)
                .then( async (res) => {
                    this.preparedDate = {
                        date: this.newVisitData.date,
                        day_name: res.data[0].day_name,
                        employee: res.data[0].employee,
                        items: res.data[0].items,
                        service: res.data[0].service,
                        employee: res.data[0].employee
                    }
                    await API.post(`/api/v1/employee/change-visit/?operation=get&employee=${this.newVisitData.employee_id}`, { name: res.data[0].service.service_name  })
                    .then(res2 => {
                        this.preparedService = {
                            ...res2.data,
                            price: res.data[0].service.price,
                            service_name: res.data[0].service.service_name
                        }
                        this.preparedService.employees.forEach((el, idx) =>{
                            let img = this.preparedService.employees[idx].avatar;
                            if(Object.hasOwn(this.preparedService.employees[idx].avatar, "image")){
                                img = appendMimeType(el.avatar)
                            }
                            this.preparedService.employees[idx].avatar = {...img};
                        })
                    })
                    
                })
                .catch(err => {
                    alert(err);
                })
            },
            async checkValidityAndChooseHour(){
                const valid = this.$refs.form.validate();
                if(valid){
                    await this.getWorkHoursForGivenDate();
                    this.openHourDialog();
                }
            },
        }
    }
</script>