<template>
    <v-row class="fill-height">
        <v-col>
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
                            <v-btn 
                                class="mx-2" color="secondary"
                                @click="openAppointmentConfigDialog"
                            >
                                Ustawienia wizyty
                            </v-btn>
                            <v-btn 
                                color="secondary"
                                @click="openAvailabilityDialog"
                            >
                                Dyspozycyjność
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
                            >{{ getWorkTimeForGivenDate(date)}}</div>
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
                            >{{ getWorkTimeForGivenDate(date)}}</div>
                        </div>
                    </template>
                <!-- <template #event="{ event }">
                    <h1>{{ event.name }}</h1>
                </template> -->
                </v-calendar>
                <!-- <v-menu
                    v-model="selectedOpen"
                    :close-on-content-click="false"
                    :activator="selectedElement"
                    offset-x
                >
                    <v-card
                        color="grey lighten-4"
                        min-width="350px"
                        flat
                    >
                        <v-toolbar
                            :color="selectedEvent.color"
                            dark
                        >
                            <v-btn icon>
                                <v-icon>mdi-pencil</v-icon>
                            </v-btn>
                            <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
                            <v-spacer></v-spacer>
                            <v-btn icon>
                                <v-icon>mdi-heart</v-icon>
                            </v-btn>
                            <v-btn icon>
                                <v-icon>mdi-dots-vertical</v-icon>
                            </v-btn>
                        </v-toolbar>
                        <v-card-text>
                            <span v-html="selectedEvent.details"></span>
                        </v-card-text>
                        <v-card-actions>
                            <v-btn
                                text
                                color="secondary"
                                @click="selectedOpen = false"
                            >
                                Cancel
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-menu> -->
            </v-sheet>
        </v-col>
    </v-row>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI";
    import { weekdays } from '../../../../utils'
    import AvailabilityDialog from '../components/AvailabilityDialog.vue'
    import AppointmentConfigDialog from '../components/AppointmentConfigDialog.vue'
    import { formatDate } from "../../../../utils/formatDate";
    import { getShortMonthName } from "../utils/getShortMonthName"

    export default {
        components: {
            AvailabilityDialog,
            AppointmentConfigDialog
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
            weekdays: weekdays,
            availabilityDialog: false,
            appointmentConfigDialog: false,
            focus: '',
            type: 'month',
            typeToLabel: {
                "month": 'Miesiąc',
                "week": 'Tydzień',
                "day": 'Dzień',
                "4day": "4 Dni",
            },
            selectedEvent: {},
            selectedElement: null,
            selectedOpen: false,
            categorizedEvents: [],
            events: [],
            colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1'],
            names: ['Meeting', 'Holiday', 'PTO', 'Travel', 'Event', 'Birthday', 'Conference', 'Party'],
        }),
        inject: ["screenSize"],
        async mounted () {
            this.$refs.calendar.checkChange();
        },
        computed: {
        },
        methods: {
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
                    await API.post("/api/v1/employee/appointments/?operation=get", { ...days })
                    .then(res => {
                        this.categorizedEvents = res.data.events
                        this.events = res.data.events.reduce((prev, el) => {
                            if(el.is_free && !el.is_holiday){
                                prev.push({
                                    name: "Wolne",
                                    start: el.date,
                                    end: el.date,
                                    color: "grey"
                                })
                            } else if(el.is_free && el.is_holiday){
                                prev.push({
                                    name: "Święto",
                                    start: el.date,
                                    end: el.date,
                                    color: "red"
                                })
                            } else if(!el.is_free && el.is_default){
                                el.breaks.forEach(el2 => {
                                    prev.push({
                                        name: "Przerwa",
                                        start: el.date + ' ' + el2.start_time,
                                        end: el.date + ' ' + el2.end_time,
                                        color: "green",
                                    })
                                })
                            } else if(el.is_appointment){
                                el.day_appointments.forEach(el2 => {
                                    prev.push({
                                        name: "Usługa",
                                        start: el.date + ' ' + el2.time_start,
                                        end: el.date + ' ' + el2.end_time,
                                        color: "blue",
                                    })
                                })
                            } else if(!el.is_default && el.is_free && !el.is_holiday && !el.is_appointment){
                                prev.push({
                                    name: "Wolne",
                                    start: el.date,
                                    end: el.date,
                                })
                            } else {
                                el.breaks.forEach(el2 => {
                                    prev.push({
                                        name: "Przerwa",
                                        start: el.date + ' ' + el2.start_time,
                                        end: el.date + ' ' + el2.end_time,
                                        color: "green",
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
                console.log(date)
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
            // updateRange ({ start, end }) {
            //     // console.log(start)
            //     // console.log(end)
            //     const events = []

            //     const min = new Date(`${start.date}T00:00:00`)
            //     const max = new Date(`${end.date}T23:59:59`)
            //     const days = (max.getTime() - min.getTime()) / 86400000
            //     const eventCount = this.rnd(days, days + 20)

            //     for (let i = 0; i < eventCount; i++) {
            //         const allDay = this.rnd(0, 3) === 0
            //         const firstTimestamp = this.rnd(min.getTime(), max.getTime())
            //         const first = new Date(firstTimestamp - (firstTimestamp % 900000))
            //         const secondTimestamp = this.rnd(2, allDay ? 288 : 8) * 900000
            //         const second = new Date(first.getTime() + secondTimestamp)

            //         events.push({
            //             name: this.names[this.rnd(0, this.names.length - 1)],
            //             start: first,
            //             end: second,
            //             color: this.colors[this.rnd(0, this.colors.length - 1)],
            //             timed: !allDay,
            //         })
            //     }
            //     this.events = events
            // },
            rnd (a, b) {
                return Math.floor((b - a + 1) * Math.random()) + a
            },
        }
    }
</script>

<style>
    .theme--light.v-calendar-weekly .v-calendar-weekly__head-weeknumber{
        background-color: rgb(42, 99, 255)!important;
        border-right: 1px solid rgb(70, 139, 255)!important;
    }
    .v-calendar-weekly__head-weekday.v-present.v-outside.success--text{
        background-color: rgb(40, 53, 147)!important;
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