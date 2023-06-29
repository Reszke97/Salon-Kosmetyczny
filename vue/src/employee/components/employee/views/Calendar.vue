<template>
    <v-row class="fill-height">
        <v-col>
            <availability-dialog
                v-if="availabilityDialog"
                @closeAvailabilityDialog="closeAvailabilityDialog"
                :availability-dialog="availabilityDialog"
                :non-working-dates="nonWorkingDates"
            />
            <appointment-config-dialog
                v-if="appointmentConfigDialog"
                @closeAppointmentConfigDialog="closeAppointmentConfigDialog"
                :appointment-config-dialog="appointmentConfigDialog"
            />
            <v-sheet height="64">
                <v-toolbar
                    flat
                >
                    <v-btn
                        outlined
                        class="mr-4"
                        color="grey darken-2"
                        @click="setToday"
                    >
                        Dzisiaj
                    </v-btn>
                    <v-btn
                        fab
                        text
                        small
                        color="grey darken-2"
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
                        color="grey darken-2"
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
                                color="grey darken-2"
                                v-bind="attrs"
                                v-on="on"
                            >
                                <span>{{ typeToLabel[type] }}</span>
                                <v-icon right>
                                    mdi-menu-down
                                </v-icon>
                            </v-btn>
                            <v-btn 
                                class="mx-2" color="success"
                                @click="openAppointmentConfigDialog"
                            >
                                Ustawienia wizyty
                            </v-btn>
                            <v-btn 
                                color="success"
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
            <v-sheet :height="screenSize.screenHeight - 112">
                <v-calendar
                    ref="calendar"
                    v-model="focus"
                    color="dark"
                    :weekdays="weekdays"
                    :events="events"
                    :event-color="getEventColor"
                    :type="type"
                    @click:event="showEvent"
                    @click:more="viewDay"
                    @click:date="viewDay"
                    @change="updateRange"
                ></v-calendar>
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
    import axios from "axios";
    import { AUTH_API } from "../../../authorization/AuthAPI";
    import { weekdays } from '../../../../utils'
    import AvailabilityDialog from '../components/AvailabilityDialog.vue'
    import AppointmentConfigDialog from '../components/AppointmentConfigDialog.vue'

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
            nonWorkingDates: [],
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
            events: [],
            colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1'],
            names: ['Meeting', 'Holiday', 'PTO', 'Travel', 'Event', 'Birthday', 'Conference', 'Party'],
        }),
        inject: ["screenSize"],
        async created(){
            await this.getNonWorkingDates();
        },
        async mounted () {
            this.$refs.calendar.checkChange();
            await this.getAppointments(this.$refs.calendar.$children[0].days);
        },
        computed: {
        },
        methods: {
            setCalendarType(val){
                this.type = val;
            },
            async setCalendarTypeAndGetAppointments(val){
                this.setCalendarType(val)
                this.$nextTick( async () => {
                    await this.getAppointments(this.$refs.calendar.$children[0].days);
                });
            },
            async getNonWorkingDates(){
                const today = new Date();
                await axios.get(`http://127.0.0.1:8000/api/v1/employee/non-working-days/?year=${today.getFullYear()}`)
                    .then(res => {
                        this.nonWorkingDates = res.data;
                    })
            },
            async getAppointments(days){
                const API = await AUTH_API();
                await API.post("/api/v1/employee/appointments/?operation=get", { ...days })
                .then(res => {

                })
                .catch(err => {

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
                this.type = 'day'
            },
            getEventColor (event) {
                return event.color
            },
            setToday () {
                this.focus = ''
            },
            async prev () {
                this.$refs.calendar.prev();
                this.$nextTick( async () => {
                    await this.getAppointments(this.$refs.calendar.$children[0].days);
                });
            },
            async next () {
                this.$refs.calendar.next();
                this.$nextTick( async () => {
                    await this.getAppointments(this.$refs.calendar.$children[0].days);
                });
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
            updateRange ({ start, end }) {
                console.log(start)
                console.log(end)
                const events = []

                const min = new Date(`${start.date}T00:00:00`)
                const max = new Date(`${end.date}T23:59:59`)
                const days = (max.getTime() - min.getTime()) / 86400000
                const eventCount = this.rnd(days, days + 20)

                for (let i = 0; i < eventCount; i++) {
                    const allDay = this.rnd(0, 3) === 0
                    const firstTimestamp = this.rnd(min.getTime(), max.getTime())
                    const first = new Date(firstTimestamp - (firstTimestamp % 900000))
                    const secondTimestamp = this.rnd(2, allDay ? 288 : 8) * 900000
                    const second = new Date(first.getTime() + secondTimestamp)

                    events.push({
                        name: this.names[this.rnd(0, this.names.length - 1)],
                        start: first,
                        end: second,
                        color: this.colors[this.rnd(0, this.colors.length - 1)],
                        timed: !allDay,
                    })
                }
                this.events = events
            },
            rnd (a, b) {
                return Math.floor((b - a + 1) * Math.random()) + a
            },
        }
    }
</script>