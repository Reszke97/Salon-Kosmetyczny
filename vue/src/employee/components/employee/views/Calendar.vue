<template>
    <v-row class="fill-height">
        <v-col
            id="calendar"
        >
            <availability-dialog
                v-if="availabilityDialog"
                @closeAvailabilityDialog="closeAvailabilityDialog"
                :availability-dialog="availabilityDialog"
            />
            <appointment-config-dialog
                v-if="appointmentConfigDialog"
                @closeAppointmentConfigDialog="closeAppointmentConfigDialog"
                :appointment-config-dialog="appointmentConfigDialog"
            />
            <v-sheet
                id="calendar-header"
                height="64"
            >
                <v-toolbar
                    flat
                >
                    <v-btn
                        outlined
                        class="mr-4"
                        color="white"
                        @click="setToday"
                    >
                        Dzisiaj
                    </v-btn>
                    <v-btn
                        fab
                        text
                        small
                        color="white"
                        @click="prev"
                    >
                        <v-icon small>
                            mdi-chevron-left
                        </v-icon>
                    </v-btn>
                    <v-btn
                        fab
                        text
                        small
                        color="white"
                        @click="next"
                    >
                        <v-icon small>
                            mdi-chevron-right
                        </v-icon>
                    </v-btn>
                    <v-toolbar-title v-if="$refs.calendar">
                        {{ $refs.calendar.title }}
                    </v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-menu
                        v-if="$store.state.role === 'owner'"
                        bottom
                        right
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                outlined
                                color="white"
                                v-bind="attrs"
                                v-on="on"
                                class="mr-1"
                            >
                                <span>{{ selectedEmployee.name }}</span>
                                <v-icon right>
                                    mdi-menu-down
                                </v-icon>
                            </v-btn>
                            <v-tooltip bottom>
                                <template v-slot:activator="{ on, attrs }">
                                    <v-btn
                                        icon
                                        class="mr-1"
                                        color="primary"
                                        @click="openAppointmentConfigDialog"
                                        :disabled="!canEdit"
                                    >
                                        <v-icon
                                            v-on="on"
                                        >mdi-cog</v-icon>     
                                    </v-btn>
                                </template>
                                <span>Ustawienia wizyty</span>
                            </v-tooltip>
                            <v-tooltip bottom>
                                <template v-slot:activator="{ on, attrs }">
                                    <v-btn 
                                        icon
                                        color="primary"
                                        @click="openAvailabilityDialog"
                                        :disabled="!canEdit"
                                    >
                                        <v-icon
                                            v-on="on"
                                        >mdi-clock-edit-outline</v-icon>     
                                    </v-btn>
                                </template>
                                <span>Dyspozycyjność</span>
                            </v-tooltip>
                        </template>
                        <v-list>
                            <v-list-item
                                v-for="employee of employees"
                                @click="setEmployeeAndGetNewData(employee)"
                            >
                                <v-list-item-title>{{ employee.name }}</v-list-item-title>
                            </v-list-item>
                        </v-list>
                    </v-menu>
                    <v-menu
                        bottom
                        right
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                outlined
                                color="white"
                                v-bind="attrs"
                                v-on="on"
                            >
                                <span>{{ typeToLabel[type] }}</span>
                                <v-icon right>
                                    mdi-menu-down
                                </v-icon>
                            </v-btn>
                        </template>
                        <v-list>
                            <v-list-item @click="setCalendarTypeAndGetAppointments('day')">
                                <v-list-item-title>Dzień</v-list-item-title>
                            </v-list-item>
                            <v-list-item @click="setCalendarTypeAndGetAppointments('week')">
                                <v-list-item-title>Tydzień</v-list-item-title>
                            </v-list-item>
                            <v-list-item @click="setCalendarTypeAndGetAppointments('month')">
                                <v-list-item-title>Miesiąc</v-list-item-title>
                            </v-list-item>
                            <v-list-item @click="setCalendarTypeAndGetAppointments('4day')">
                                <v-list-item-title>4 dni</v-list-item-title>
                            </v-list-item>
                        </v-list>
                    </v-menu>
                </v-toolbar>
            </v-sheet>
            <v-sheet 
                id="calendar-body"
                :height="screenSize.screenHeight - 112"
            >
                <v-calendar
                    v-model="focus"
                    ref="calendar"
                    color="success"
                    show-week
                    event-more
                    event-more-text="więcej"
                    :short-intervals="false"
                    :weekdays="weekdays"
                    :events="events"
                    :event-color="getEventColor"
                    :type="type"
                    @click:event="showEvent"
                    @click:more="viewDay"
                    @change="getAppointments"
                >
                    <!-- monthly -->
                    <template #day-label="{date, day, month}" >
                        <div class="d-flex flex-column">
                            <div 
                                style="color:white!important; font-size:small;"
                            >
                                <v-btn
                                    fab
                                    :icon="getDayColor(date) ? false : true"
                                    height="40px"
                                    width="40px"
                                    :color="getDayColor(date)"
                                    @click="viewDay(date)"
                                >
                                    {{ getDayName(day, month) }}
                                </v-btn>
                            </div>
                            <div 
                                style="color:white!important; font-size:small;"
                                class="flex-centered"
                            >
                                {{ getWorkTimeForGivenDate(date)}}
                                <v-tooltip bottom v-if="!isHolidayOrFree(date) && canEdit">
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-icon
                                            v-on="on"
                                            color="success"
                                            @click="openNewVisitDialog(date)"
                                        >
                                            mdi-plus-circle
                                        </v-icon>
                                    </template>
                                    <span>Dodaj wizytę</span>
                                </v-tooltip>
                            </div>
                        </div>
                    </template>
                    <!-- else than monthly -->
                    <template #day-label-header="{date, day, month}">
                        <div class="d-flex flex-column">
                            <div 
                                style="color:white!important; font-size:small;"
                            >
                                <v-btn
                                    fab
                                    :icon="getDayColor(date) ? false : true"
                                    height="40px"
                                    width="40px"
                                    :color="getDayColor(date)"
                                    @click="viewDay(date)"
                                >
                                    {{ getDayName(day, month) }}
                                </v-btn>
                            </div>
                            <div 
                                style="color:white!important; font-size:small;"
                                class="flex-centered"
                            >
                                {{ getWorkTimeForGivenDate(date)}}
                                <v-tooltip bottom v-if="!isHolidayOrFree(date) && canEdit">
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-icon
                                            v-on="on"
                                            color="success"
                                            @click="openNewVisitDialog(date)"
                                        >
                                            mdi-plus-circle
                                        </v-icon>
                                    </template>
                                    <span>Dodaj wizytę</span>
                                </v-tooltip>
                            </div>
                        </div>
                    </template>
                </v-calendar>
                <v-menu
                    v-model="selectedOpen"
                    :close-on-content-click="false"
                    :activator="selectedElement"
                    offset-x
                >
                    <v-card
                        color="grey lighten-4"
                        min-width="300px"
                        max-width="350px"
                        flat
                    >
                        <v-toolbar
                            :color="selectedEvent.color"
                            dark
                        >   <div class="flex-centered w-100">
                                <div class="w-100">
                                    <v-toolbar-title> {{ `${selectedEvent.name}` }} </v-toolbar-title>
                                </div>
                                <div>
                                    <v-tooltip bottom>
                                        <template v-slot:activator="{ on, attrs }">
                                            <v-btn
                                                dark
                                                icon
                                                v-on="on"
                                                @click="selectedOpen = false"
                                            >
                                                <v-icon>
                                                    mdi-close-circle
                                                </v-icon>
                                            </v-btn>
                                        </template>
                                        <span>Zamknij</span>
                                    </v-tooltip>
                                </div>
                            </div>
                            <v-spacer></v-spacer>
                        </v-toolbar>
                        <v-card-text class="bg-color" style="color:white!important">
                            <div class="d-flex flex-column">
                                <template v-if="!selectedEvent.is_holiday && !selectedEvent.is_free">
                                    <span>
                                        <span style="color: orange!important" class="font-bold">Data: </span><span>{{ `${selectedEvent.date}` }}</span>
                                    </span>
                                    <span>
                                        <span style="color: orange!important" class="font-bold">Godzina: </span><span>{{ `${selectedEvent.time}` }}</span>
                                    </span>
                                    <template v-if="selectedEvent.is_appointment">
                                        <span>
                                            <span style="color: orange!important" class="font-bold">Imię klienta: </span><span>{{ `${selectedEvent.client_name ? selectedEvent.client_name : selectedEvent.non_user_client} ${selectedEvent.client_last_name ? selectedEvent.client_last_name : ""}` }}</span>
                                        </span>
                                        <span>
                                            <span style="color: orange!important" class="font-bold">E-mail klienta: </span><span>{{ `${selectedEvent.client_mail ? selectedEvent.client_mail : "-"}` }}</span>
                                        </span>
                                    </template>
                                </template>
                            </div>
                        </v-card-text>
                        <v-card-actions class="bg-color">
                            <v-tooltip bottom v-if="selectedEvent.is_appointment && canEdit">
                                <template v-slot:activator="{ on, attrs }">
                                    <v-btn 
                                        dark
                                        v-on="on"
                                        icon
                                        @click="openChangeVisitDialogAndSetSelectedAppointment(selectedEvent)"
                                    >
                                        <v-icon
                                        >mdi-pencil</v-icon>
                                    </v-btn>
                                </template>
                                <span>Przenieś wizytę</span>
                            </v-tooltip>
                            <v-tooltip bottom v-if="selectedEvent.is_appointment && canEdit">
                                <template v-slot:activator="{ on, attrs }">
                                    <v-btn 
                                        dark
                                        v-on="on"
                                        icon
                                        @click="openReasonDialog(selectedEvent)"
                                    >
                                        <v-icon
                                            color="red"
                                        >mdi-trash-can</v-icon>
                                    </v-btn>
                                </template>
                                <span>Usuń wizytę</span>
                            </v-tooltip>
                        </v-card-actions>
                    </v-card>
                </v-menu>
            </v-sheet>
        </v-col>
        <SignUpForVisit
            v-if="changeVisitDialog"
            :signUpForVisitDialog="changeVisitDialog"
            :selectedService="selectedAppointment"
            :componentDims="componentDims"
            :closeSignUpForVisitDialog="closeChangeVisitDialog"
            :type="signUpForVisitType"
            @refreshData="getAppointments"
        />
        <NewVisitDialog
            v-if="newVisitDialog"
            :componentDims="componentDims"
            :newVisitDialog="newVisitDialog"
            :newVisitData="newVisitData"
            @closeNewVisitDialog="closeNewVisitDialog"
            @updateNewVisitData="updateNewVisitData"
            @closeNewVisitDialogAndGetNewData="closeNewVisitDialogAndGetNewData"
        />
        <v-dialog
            v-model="reasonDialog"
            persistent
            dark
            :width="'300px'"
        >   
            <div class="bg-color px-4">
                <v-text-field
                    v-model="reason"
                    label="Podaj powód"
                />
                <div class="d-flex pb-2">
                    <v-btn
                        @click="deleteVisit"
                        class="mr-2 indigo"
                    >
                        Usuń wizytę
                    </v-btn>
                    <v-btn
                        class="indigo"
                        @click="closeReasonDialog"
                    >
                        Zamknij
                    </v-btn>
                </div>
            </div>
        </v-dialog>
    </v-row>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI";
    import { weekdays } from '../../../../utils'
    import { formatDate } from "../../../../utils/formatDate";
    import { getShortMonthName } from "../utils/getShortMonthName"
    import { appendMimeType } from "../../../../client/utils";
    import AvailabilityDialog from '../components/AvailabilityDialog.vue'
    import AppointmentConfigDialog from '../components/AppointmentConfigDialog.vue'
    import SignUpForVisit from "./SignForService/SignUpForVisit.vue";
    import NewVisitDialog from "./SignForService/NewVisitDialog.vue"

    const _newVisitData = {
        date: "", 
        user_does_not_exists: false,
        employee_id: null,
        client_id: null,
        non_existent_user: "",
        service_id: null,
        chosen_time: {
            start: "",
            end: ""
        }
    }

    export default {
        components: {
            AvailabilityDialog,
            AppointmentConfigDialog,
            SignUpForVisit,
            NewVisitDialog,
        },
        mixins: [
        ],
        props: {
            calendarType: {
                type: String,
                default: "monthly",
            },
        },
        data: () => ({
            newVisitData: {..._newVisitData},
            newVisitDialog: false,
            componentDims: { height: 0, width: 0 },
            weekdays: weekdays,
            availabilityDialog: false,
            appointmentConfigDialog: false,
            focus: '',
            type: 'month',
            employees: [],
            typeToLabel: {
                "month": 'Miesiąc',
                "week": 'Tydzień',
                "day": 'Dzień',
                "4day": "4 Dni",
            },
            signUpForVisitType: "swap",
            selectedEmployee: { name: "", employee_id: null },
            selectedEvent: {},
            selectedElement: null,
            selectedOpen: false,
            categorizedEvents: [],
            events: [],
            appointmentDialog: false,
            selectedAppointment: {},
            changeVisitDialog: false,
            deleteData: {},
            reason: "",
            reasonDialog: false,
        }),
        inject: ["screenSize"],
        async mounted () {
            this.$refs.calendar.checkChange();
            this.setComponentDims();
        },
        async created(){
            if(this.$store.state.role === "owner"){
                this.selectedEmployee = { 
                    name: `${this.$store.state.name} ${this.$store.state.last_name}`, 
                    employee_id: this.$store.state.employee_id 
                };
                const API = await AUTH_API();
                await API.get("/api/v1/employee/owner-employees/")
                .then(res => {
                    this.employees = res.data.map(el => {
                        return {
                            employee_id: el.pk,
                            user_id: el.user.id,
                            name: `${el.user.first_name} ${el.user.last_name}`,
                        }
                    })
                })
            }
        },
        computed: {
            canEdit(){
                return this.$store.state.role !== "owner" || (this.$store.state.role === "owner" && this.$store.state.employee_id === this.selectedEmployee.employee_id);
            },
        },
        methods: {
            async deleteVisit(){
                const API = await AUTH_API();
                if(this.reason){
                    API.delete(`/api/v1/client/visit/?appointment_id=${this.deleteData.appointment_id}`, { data: { reason: this.reason } })
                    .then( async () => {
                        this.reason = "";
                        this.deleteData = {};
                        this.closeReasonDialog();
                        alert("Usunięto wizytę")
                        await this.getAppointments();
                    })
                } else {
                    alert("Podaj powód")
                }
            },
            openReasonDialog(data){
                this.deleteData.appointment_id = data.appointment_id;
                this.reasonDialog = true;
            },
            closeReasonDialog(){
                this.reasonDialog = false;
            },
            async closeNewVisitDialogAndGetNewData(){
                this.closeNewVisitDialog();
                await this.getAppointments();
            },
            updateNewVisitData({ key, val }){
                this.newVisitData[key] = val;
            },
            refreshNewVisitDialog(){
                this.newVisitData = {..._newVisitData};
            },
            openNewVisitDialog(date){
                this.refreshNewVisitDialog();
                this.newVisitData.date = date;
                this.newVisitData.employee_id = this.selectedEmployee.employee_id;
                this.newVisitDialog = true;
            },
            closeNewVisitDialog(){
                this.newVisitDialog = false;
            },
            async getCompleteServiceInfo(appointmentInfo){
                const API = await AUTH_API();
                await API.post(`/api/v1/employee/change-visit/?operation=get&employee=${this.selectedEmployee.employee_id}`, {...appointmentInfo})
                .then(res => {
                    this.selectedAppointment = {
                        ...res.data,
                        date: appointmentInfo.date,
                        time: appointmentInfo.time,
                        service_name: appointmentInfo.name,
                        client_name: appointmentInfo.client_name,
                        client_last_name: appointmentInfo.client_last_name,
                        appointment_id: appointmentInfo.appointment_id,
                    }
                    this.selectedAppointment.employees.forEach((el, idx) =>{
                        let img = this.selectedAppointment.employees[idx].avatar;
                        if(Object.hasOwn(this.selectedAppointment.employees[idx].avatar, "image")){
                            img = appendMimeType(el.avatar)
                        }
                        this.selectedAppointment.employees[idx].avatar = {...img};
                    })
                })
            },
            setComponentDims(){
                const minW = 600;
                const width = document.getElementById('calendar').offsetWidth/2.5;
                this.componentDims = {
                    height: `${document.getElementById('calendar').offsetHeight - 350}px`,
                    width: width < minW ? minW + "px" : width + "px",
                }
            },
            openChangeVisitDialog(){
                this.changeVisitDialog = true;
            },
            closeChangeVisitDialog(){
                this.changeVisitDialog = false;
            },
            setSignUpForVisitType(type){
                this.signUpForVisitType = type;
            },
            async openChangeVisitDialogAndSetSelectedAppointment(appointment){
                await this.getCompleteServiceInfo(appointment);
                this.setSignUpForVisitType("swap");
                this.openChangeVisitDialog();
            },
            openAppointmentDialog(){
                this.appointmentDialog = true;
            },
            closeAppointmentDialog(){
                this.appointmentDialog = false;
            },
            setEmployee(employee){
                this.selectedEmployee = employee;
            },
            async setEmployeeAndGetNewData(employee){
                this.setEmployee(employee);
                await this.getAppointments();
            },
            getDayName(day, month){
                if(day === 1){
                    return getShortMonthName(month) + ' ' + day;
                } else return day;
            },
            getDayColor(date){
                const dateNow = new Date();
                const formattedDate = formatDate(dateNow)
                if(date === formattedDate){
                    return "success"
                } return ""
            },
            setCalendarType(val){
                this.type = val;
            },
            isHolidayOrFree(date){
                const foundItemIdx = this.categorizedEvents.findIndex(
                    el => el.date === date && (el.is_free || el.is_holiday)
                );
                if(foundItemIdx >= 0) {
                    return true
                }
                return false
            },
            getWorkTimeForGivenDate(date){
                const foundItemIdx = this.categorizedEvents.findIndex(
                    el => el.date === date && !el.is_appointment && !el.is_free && !el.is_holiday
                );
                if(foundItemIdx >= 0) {
                    return`${this.categorizedEvents[foundItemIdx].work_time.start_time} - ${this.categorizedEvents[foundItemIdx].work_time.end_time}`;
                }
                return ""
            },
            async setCalendarTypeAndGetAppointments(val){
                this.setCalendarType(val)
                this.$nextTick( async () => {
                    await this.getAppointments();
                });
            },
            async getAppointments(){
                this.$nextTick( async () => {
                    const days = this.$refs.calendar.$children[0].days;
                    const API = await AUTH_API();
                    await API.post(`/api/v1/employee/appointments/?operation=get&employee=${this.selectedEmployee.employee_id}`, { ...days })
                    .then(res => {
                        this.categorizedEvents = res.data.events
                        this.events = res.data.events.reduce((prev, el) => {
                            if(el.is_free && !el.is_holiday){
                                prev.push({
                                    name: "Wolne",
                                    start: el.date,
                                    end: el.date,
                                    color: "grey",
                                    is_appointment: false,
                                    is_free: true,
                                    is_holiday: false,
                                })
                            } else if(el.is_free && el.is_holiday){
                                prev.push({
                                    name: "Święto",
                                    start: el.date,
                                    end: el.date,
                                    color: "red",
                                    is_appointment: false,
                                    is_free: false,
                                    is_holiday: true,
                                })
                            } else if(!el.is_free && el.is_default){
                                el.breaks.forEach(el2 => {
                                    prev.push({
                                        name: "Przerwa",
                                        start: el.date + ' ' + el2.start_time,
                                        end: el.date + ' ' + el2.end_time,
                                        color: "green",
                                        is_appointment: false,
                                        is_free: false,
                                        is_holiday: false,
                                        time: `${el2.start_time} - ${el2.end_time}`,
                                        date: el.date,
                                    })
                                })
                            } else if(el.is_appointment){
                                el.day_appointments.forEach(el2 => {
                                    prev.push({
                                        appointment_id: el2.appointment_id,
                                        name: el2.service_name,
                                        start: el.date + ' ' + el2.time_start,
                                        end: el.date + ' ' + el2.end_time,
                                        color: "blue",
                                        client_name: el2.client_name,
                                        client_last_name: el2.client_last_name,
                                        client_mail: el2.client_mail,
                                        non_user_client: el2.non_user_client,
                                        time: `${el2.time_start} - ${el2.end_time}`,
                                        date: el.date,
                                        is_appointment: true,
                                        is_free: false,
                                        is_holiday: false,
                                    })
                                })
                            } else if(!el.is_default && el.is_free && !el.is_holiday && !el.is_appointment){
                                prev.push({
                                    name: "Wolne",
                                    start: el.date,
                                    end: el.date,
                                    is_appointment: false,
                                    is_free: true,
                                    is_holiday: false,
                                })
                            } else {
                                el.breaks.forEach(el2 => {
                                    prev.push({
                                        name: "Przerwa",
                                        start: el.date + ' ' + el2.start_time,
                                        end: el.date + ' ' + el2.end_time,
                                        color: "green",
                                        is_appointment: false,
                                        is_free: false,
                                        is_holiday: false,
                                        time: `${el2.start_time} - ${el2.end_time}`,
                                        date: el.date,
                                    })
                                })
                            }
                            return prev
                        }, [])
                    })
                    .catch(err => {
                        console.log(err)
                    })
                })
            },

            openAppointmentConfigDialog(){
                this.appointmentConfigDialog = true;
            },
            closeAppointmentConfigDialog(){
                this.appointmentConfigDialog = false;
            },
            openAvailabilityDialog(){
                this.availabilityDialog = true;
            },
            closeAvailabilityDialog(){
                this.availabilityDialog = false;
            },
            viewDay ({ date }) {
                this.focus = date
                this.type = "day"
            },
            getEventColor (event) {
                return event.color
            },
            async setToday () {
                this.focus = ""
            },
            async prev () {
                this.$refs.calendar.prev();
            },
            async next () {
                this.$refs.calendar.next();
            },
            showEvent ({ nativeEvent, event }) {
                const open = () => {
                    this.selectedEvent = event
                    this.selectedElement = nativeEvent.target
                    requestAnimationFrame(() => requestAnimationFrame(() => this.selectedOpen = true))
                }

                if (this.selectedOpen) {
                    this.selectedOpen = false
                    requestAnimationFrame(() => requestAnimationFrame(() => open()))
                } else {
                    open()
                }
                nativeEvent.stopPropagation()
            },
        }
    }
</script>

<style>
    .v-event-more.pl-1{
        color: black!important;
    }
    .theme--light.v-calendar-weekly .v-calendar-weekly__head-weekday.v-outside {
        background-color: rgb(63, 81, 181)!important;
    }
    .theme--light.v-calendar-weekly .v-calendar-weekly__head-weeknumber{
        background-color: rgb(42, 99, 255)!important;
        border-right: 1px solid rgb(70, 139, 255)!important;
    }
    .v-calendar-weekly__day.v-present.v-outside{
        background-color: rgb(40, 53, 147)!important;
    }
    .theme--light.v-calendar-weekly .v-calendar-weekly__weeknumber{
        background-color: rgb(42, 99, 255)!important;
        border-right: 1px solid rgb(70, 139, 255)!important;
        border-bottom: 1px solid rgb(70, 139, 255)!important;
        color: white!important;
    }
    .theme--light.v-calendar-weekly{
        border-top: 1px solid rgb(70, 139, 255)!important;
        border-left: 1px solid rgb(70, 139, 255)!important;
    }
    .theme--light.v-calendar-weekly .v-calendar-weekly__head-weekday{
        border-right: 1px solid rgb(70, 139, 255)!important;
    }
    .theme--light.v-calendar-weekly .v-calendar-weekly__day{
        border-right: 1px solid rgb(70, 139, 255)!important;
        border-bottom: 1px solid rgb(70, 139, 255)!important;
    }

    #calendar-body  .v-calendar-monthly.v-calendar-weekly.v-calendar.theme--light.v-calendar-events{
        background-color: rgb(40, 53, 147)!important;
    }
    .v-calendar-weekly__day.v-past.v-outside {
        background-color: rgb(63, 81, 181)!important;
        color: white!important;
    }
    .v-calendar-weekly__day.v-future.v-outside{
        background-color: rgb(63, 81, 181)!important;
        color: white!important;
    }
    .v-calendar-weekly__head-weekday.v-past.v-outside{
        background-color: rgb(63, 81, 181)!important;
        color: #d0d0d0!important;
    }
    .v-calendar-weekly__head-weekday.v-past{
        color: white!important;
    }
    .v-calendar-weekly__head-weekday.v-present.success--text{
        color: orange!important;
        font-weight: bold;
    }
    .v-calendar-weekly__head-weekday.v-future{
        color: white!important;
        font-weight: bold!important;
    }
    .v-calendar-weekly__day-label .v-btn{
        color: white!important;
    }
    #calendar-header header{
        background-color: rgb(42, 99, 255)!important;
    }
    .v-toolbar__title{
        color: white;
    }
    /*4days*/
    #calendar-body .v-calendar.v-calendar-daily.theme--light.v-calendar-events{
        background-color: rgb(40, 53, 147)!important;
    }
    #calendar-body .v-calendar-daily__head{
        color: white!important;
    }
    #calendar-body .v-calendar-daily_head-day-label .v-btn{
        color: white!important;
    }
    #calendar-body .v-calendar-daily_head-day.v-past .v-calendar-daily_head-weekday{
        color: #d0d0d0!important;
    }
    #calendar-body .v-calendar-daily_head-day.v-future .v-calendar-daily_head-weekday{
        color: white!important;
        font-weight: white!important;
    }
    #calendar-body .v-calendar-daily_head-day.v-present .v-calendar-daily_head-weekday{
        color: orange!important;
        font-weight: white!important;
    }
    #calendar-body .theme--light.v-calendar-daily .v-calendar-daily__intervals-body .v-calendar-daily__interval-text{
        color: white!important;
    }
    #calendar-body .v-calendar.v-calendar-daily.theme--light.v-calendar-events{
        border-top: 1px solid rgb(70, 139, 255)!important;
        border-left: 1px solid rgb(70, 139, 255)!important;
    }
    #calendar-body .theme--light.v-calendar-daily .v-calendar-daily__intervals-head{
        border-right: 1px solid rgb(70, 139, 255)!important;
    }
    #calendar-body .theme--light.v-calendar-daily .v-calendar-daily_head-day{
        border-right: 1px solid rgb(70, 139, 255)!important;
        border-bottom: 1px solid rgb(70, 139, 255)!important;
    }
    #calendar-body .v-calendar-daily__intervals-body{
        border-right: 1px solid rgb(70, 139, 255)!important;
    }
    #calendar-body .v-calendar-daily__day.v-past{
        border-right: 1px solid rgb(70, 139, 255)!important;
        border-bottom: 1px solid rgb(70, 139, 255)!important;
    }
    #calendar-body .theme--light.v-calendar-daily .v-calendar-daily__day{
        border-right: 1px solid rgb(70, 139, 255)!important;
        border-bottom: 1px solid rgb(70, 139, 255)!important;
    }
    #calendar-body .theme--light.v-calendar-daily .v-calendar-daily__interval:after{
        border-top: 1px solid rgb(70, 139, 255)!important;
    }
    #calendar-body .theme--light.v-calendar-daily .v-calendar-daily__day-interval{
        border-top: 1px solid rgb(70, 139, 255)!important;
    }
    #calendar-body .theme--light.v-calendar-daily .v-calendar-daily__intervals-head:after{
        background: linear-gradient(90deg,transparent,rgb(70, 139, 255));
    }
</style>