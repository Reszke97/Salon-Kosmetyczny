<template>
  <v-row
        :style="{
            height: screenSize.screenHeight + 'px',
            paddingTop: '8px',
            paddingBottom: '8px',
        }"
        justify="center"
    >
        <v-col 
            id="visits"
            cols="11"
            sm="9"
            md="6"
            lg="5" 
            :style="{
                backgroundColor:'#3f51b5',
                height: '100%',
                overflowY: 'auto',
            }"
        >
            <div class="flex-centered">
                <h3 style="color: white;">Moje wizyty</h3>
            </div>
            <div class="flex-centered pt-2">
                <v-btn
                    :color="getSelectedBtnColor('planned')"
                    @click="changeVisitType('planned')"
                >
                    Zaplanowane wizyty
                </v-btn>
                <v-btn
                    :color="getSelectedBtnColor('historical')"
                    @click="changeVisitType('historical')"
                >
                    Historia wizyt
                </v-btn>
            </div>
            <v-card
                style="color: white;"
                color="secondary"
                class="mt-2"
                dark
                v-for="visit in visits"
            >
                <div class="d-flex flex-no-wrap justify-space-between">
                    <div>
                        <v-card-title
                            class="text-h5"
                            v-text="visit.service_name"
                        ></v-card-title>

                        <v-card-subtitle>
                            <span class="font-bold">{{ visit.appointment_date }}</span>
                            <span class="px-2 font-bold">{{`${visit.appointment_start_time} - ${visit.appointment_end_time}`}}</span>
                            <div class="d-flex flex-column">
                                <span class="font-bold">Cena: <span>{{ `${visit.price} zł` }}</span></span>
                                <span class="font-bold">Usługodawca: </span>
                                <div class="d-flex flex-column pl-4">
                                    <span>{{`${visit.employee_name} ${visit.employee_last_name}`}}</span>
                                    <span>{{`${visit.employee_mail}`}}</span>
                                    <span>{{`tel. ${visit.employee_phone ? visit.employee_phone : '-'}`}}</span>
                                </div>
                            </div>
                        </v-card-subtitle>

                        <v-card-actions
                            v-if="selectedVisitType==='planned'"
                        >
                            <div>
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                    <v-btn
                                        class="ml-2 mt-3"
                                        fab
                                        icon
                                        height="40px"
                                        width="40px"
                                        @click="openConfirmationDialog(visit)"
                                    >
                                            <v-icon
                                                v-on="on"
                                                color="red"
                                            >
                                                mdi-trash-can
                                            </v-icon>
                                        </v-btn>
                                    </template>
                                    <span>Odwołaj wizytę</span>
                                </v-tooltip>
                            </div>
                            <div>
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                    <v-btn
                                        class="ml-2 mt-3"
                                        fab
                                        icon
                                        height="40px"
                                        right
                                        width="40px"
                                        @click="setMessageDialog(true, visit)"
                                    >
                                        <v-icon v-on="on" color="indigo lighten-4">mdi-message-text</v-icon>
                                        </v-btn>
                                    </template>
                                    <span>Napisz wiadomość do usługodawcy</span>
                                </v-tooltip>
                            </div>
                        </v-card-actions>
                    </div>
                    <div class="d-flex flex-column ma-3">
                        <span class="font-bold">Firma: <span>{{ visit.business_name }}</span></span>
                        <v-avatar
                            size="150"
                            tile
                        >
                            <v-img :src="visit.business_img.image"></v-img>
                        </v-avatar>
                        <div class="d-flex flex-column">
                            <span>{{`${visit.business_city} ${visit.business_post_code}`}}</span>
                            <span>{{`ul. ${visit.business_street} ${visit.business_house_number}${visit.business_apartment_number ? "/" + visit.business_apartment_number: ""}`}}</span>
                        </div>
                    </div>
                </div>
            </v-card>
            <confirm-dialog
                v-if="confirmationDialog"
                :dialog="confirmationDialog"
                :onConfirmAction="deleteVisit"
                :setDialog="setConfirmationDialog"
            />
            <message-to-employee
                v-if="showMessageDialog"
                :selectedVisit="selectedVisit"
                :showDialog="showMessageDialog"
                :componentDims="componentDims"
                @closeDialog="setMessageDialog(false)"
                @sendMessage="sendMessage"
            />
        </v-col>
  </v-row>
</template>

<script>
    import { AUTH_API } from "../../authorization/AuthAPI";
    import { appendMimeType } from "../../utils";
    import ConfirmDialog from "../../utils/Components/Dialog.vue"
    import MessageToEmployee from "./MessageToEmployee.vue";

    const visitTypes = [
        "planned",
        "historical"
    ]
    export default {
        name: "",
        components: {
            ConfirmDialog,
            MessageToEmployee,
        },
        props: {
            
        },
        data: () => ({
            selectedVisitType: "planned",
            visits: [],
            confirmationDialog: false,
            selectedVisit: null,
            showMessageDialog: false,
            componentDims: null,
        }),
        inject: ["screenSize"],
        computed: {
            
        },
        async created(){
            await this.getVisits();
        },
        methods: {
            async sendMessage(message){
                await AUTH_API.post("/api/v1/client/message/", { 
                    employee_mail: this.selectedVisit.employee_mail,
                    employee_full_name: `${this.selectedVisit.employee_name} ${this.selectedVisit.employee_last_name}`,
                    date: this.selectedVisit.appointment_date,
                    duration: `${this.selectedVisit.appointment_start_time} - ${this.selectedVisit.appointment_end_time}`,
                    message: message,
                })
                .then(() => {
                    alert("Wysłano wiadomość");
                    this.setMessageDialog(false);
                })
                .catch(() => {
                    alert("Coś poszło nie tak");
                    this.setMessageDialog(false);
                })
            },
            setComponentDims(){
                this.componentDims = {
                    height: `${document.getElementById('visits').offsetHeight - 200}px`,
                    width: `${document.getElementById('visits').offsetWidth}px`,
                }
            },
            setMessageDialog(dialog, selectedVisit){
                if(dialog) {
                    this.setComponentDims();
                    this.selectedVisit = selectedVisit;
                }
                this.showMessageDialog = dialog;
            },
            openConfirmationDialog(selectedVisit){
                this.selectedVisit = selectedVisit;
                this.setConfirmationDialog(true);
            },
            async setSelectedVisit(value){
                this.selectedVisit = value;
            },
            async deleteVisit(){
                await AUTH_API.delete(`/api/v1/client/my-visits/?appointment_id=${this.selectedVisit.appointment_id}`, {
                    data: this.selectedVisit 
                })
                .then( async () => {
                    alert("Twoja wizyta została usunięta");
                    this.setConfirmationDialog(false);
                    await this.getVisits();
                })
                .catch(() => {
                    alert("Coś poszło nie tak");
                    this.setConfirmationDialog(false);
                })
            },
            setConfirmationDialog(val){
                this.confirmationDialog = val;
            },
            async getVisits(){
                await AUTH_API.get(`/api/v1/client/my-visits/?visitType=${this.selectedVisitType}`)
                .then(res => {
                    this.visits = res.data.map(el =>{
                        const business_img = appendMimeType(el.business_img)
                        return {
                            ...el,
                            business_img: { ...business_img }
                        };
                    })
                })
            },
            async changeVisitType(visitType){
                this.selectedVisitType = visitType;
                await this.getVisits();
            },
            getSelectedBtnColor(visitType){
                if (visitType === this.selectedVisitType) return "secondary";
                return "success";
            },
        }
    }
</script>