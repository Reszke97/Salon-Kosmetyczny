<template>
    <v-container fluid>
        <div 
            id="buttons-wrapper"
            style="
                display:flex;
                flex-direction:row;
            "
        >
            <div
                id="monthly-preview" 
                :style="{
                    width:'100%',
                }"
            >
                <v-btn 
                    style="width:100%"
                    :color="calendarType === 'monthly' ? '#5cb85c' : null"
                    @click="chooseAndGetCalendarData(undefined, undefined, undefined, 'monthly')"
                >
                    Miesiąc
                </v-btn>
            </div>
            <div 
                id="weekly-preview" 
                :style="{
                    width:'100%',
                }"
            >
                <v-btn 
                    style="width:100%"
                    :color="calendarType === 'weekly' ? '#5cb85c' : null"
                    @click="chooseAndGetCalendarData(undefined, undefined, undefined, 'weekly')"
                >
                    Tydzień
                </v-btn>
            </div>
            <div 
                id="daily-preview"
                :style="{
                    width:'100%',
                }"
            >
                <v-btn 
                    style="width:100%"
                    :color="calendarType === 'daily' ? '#5cb85c' : null"
                    @click="chooseAndGetCalendarData(undefined, undefined, undefined, 'daily')"
                >
                    Dzień
                </v-btn>
            </div>
        </div>
            <div
                id="month-info-wrapper"
                style="
                    width:100%;
                    background-color:#0892d0;
                    position:relative;
                "
                class="pt-4 pb-2"
            >
                <div 
                    style="
                        width:100%;
                        display:flex;
                        justify-content:center;
                    "
                >
                    <h1
                        style="cursor: pointer;"
                        id="month-info"
                    >
                        <v-icon
                            large
                        >
                            mdi-calendar
                        </v-icon>
                        {{calendarHeader}}
                    </h1>
                </div>
                <div 
                    style="
                        width:100%;
                        position:absolute;
                        display:flex;
                        justify-content:center;
                    "
                    class="py-2"
                >
                    <v-date-picker
                        v-if="pickDate"
                        v-model="fullDate"
                        :type="calendarType === 'monthly' ? 'month' : 'date'"
                        @change="chooseAndGetCalendarData(undefined, undefined, true, calendarType)"
                        no-title
                        scrollable
                    >
                        <v-spacer></v-spacer>
                        <v-btn
                            text
                            color="primary"
                            @click="pickDate = false"
                        >
                            Cancel
                        </v-btn>
                    </v-date-picker>
                </div>
            </div>
            <div 
                id="calendar-wrapper"
                style="
                    display:flex;
                    flex-direction:row;
                    background-color:#0892d0;
                    width:100%;
                "
            >
            <div 
                id="prev-month"
                style="
                    display:flex;
                    align-items:center;
                    width:2.5%;
                "
            >
                <v-btn
                    style="width:100%"
                    icon
                    @click="chooseAndGetCalendarData(false, true, true, calendarType)"
                >
                    <v-icon large>
                        mdi-chevron-left
                    </v-icon>
                </v-btn>
            </div>
            <monthly-calendar
                style="
                    display:flex;
                    width:95%;
                "
                :days-data="daysData"
                :today="today"
            />
            <div 
                id="next-month"
                style="
                    display:flex;
                    align-items:center;
                    width:2.5%;
                "
            >
                <v-btn
                    style="width:100%" 
                    icon
                    @click="chooseAndGetCalendarData(true, false, true, calendarType)"
                >
                    <v-icon large>
                        mdi-chevron-right
                    </v-icon>
                </v-btn>
            </div>
        </div>
    </v-container>
</template>




<script>
    import { AUTH_API } from '../../../authorization/AuthAPI'
    import axios from 'axios'
    import getMonthName from "../utils/getMonthName"
    import MonthlyCalendar from "../components/MonthlyCalendar.vue"
    import getNextDayOrWeek from "../utils/getNextDayOrWeek"
    import getPrevDayOrWeek from "../utils/getPrevDayOrWeek"

    export default {
        components: {
            MonthlyCalendar
        },
        mixins: [
            getMonthName,
            getNextDayOrWeek,
            getPrevDayOrWeek
        ],
        props: {
            calendarType: {
                type: String,
                default: "monthly",
            },
        },
        data: () => ({
            daysData: {
                "days": {
                    "Poniedziałek": [],
                    "Wtorek": [],
                    "Środa": [],
                    "Czwartek": [],
                    "Piątek": [],
                    "Sobota": [],
                    "Niedziela": []
                },
                "month": {
                    "number": 0,
                    "name": ""
                },
                "day_count": 0,
                "week": 1,
                "year": 0,
                "dayOfMonth": 1,
                "current_month_days": 0,
                "last_month_days": 0,
                "next_month_days": 0,
            },
            activePicker: null,
            pickDate: false,
            today: "",
        }),
        async created(){
            const today = new Date()
            this.today = today;
            this.daysData.month.number = today.getMonth() + 1
            this.daysData.year = today.getFullYear()
            this.daysData.dayOfMonth = today.getDate();
            await this.chooseAndGetCalendarData(undefined, undefined, true)
        },
        mounted(){
            document.getElementById("month-info").addEventListener("click", () => {
                this.pickDate = true;
            })
        },
        watch: {
            menu (val) {
                val && setTimeout(() => (this.activePicker = 'YEAR'))
            },
        },
        computed: {
            fullDate: {
                async set(date) {
                    console.log(date)
                    date = date.split('-')
                    this.daysData.month.number = date[1] !== "10" ? date[1].replace('0', ''): date[1]
                    this.daysData.year = date[0]

                    if(this.calendarType !== "monthly"){
                        this.daysData.dayOfMonth = date[2]
                    }
                },
                get() {
                    if(this.calendarType !== "monthly"){
                        return `${this.daysData.year}-${this.daysData.month.number}-${this.daysData.dayOfMonth}`
                    } else {
                        const monthNumber = this.daysData.month.number >= 10 
                            ? this.daysData.month.number: 0 + this.daysData.month.number.toString()
                        return `${this.daysData.year}-${monthNumber}`
                    }
                },
            },

            calendarHeader(){
                let year = this.daysData.year
                if(this.daysData.month.number === 12 && this.daysData.week === 1){
                     year += 1
                } else if(this.daysData.month.number === 1 && this.daysData.week >= 52){
                    year -= 1
                }
                return (this.calendarType === "monthly" 
                    ? `${this.daysData.month.name} - ${year}` 
                    :  this.calendarType === "weekly" 
                    ?  `${this.daysData.week} - ${year}`
                    : this.calendarType === "daily"
                    ? `Dzień`
                    : null
                )
            }
        },
        methods: {
            prepareDataForNextOrPrevDayOrWeek(dayCount, type){
                return {
                    month: this.daysData.month.number,
                    dayOfMonth: this.daysData.dayOfMonth,
                    year: this.daysData.year,
                    dayCount: dayCount,
                        monthDays: type === "next" 
                            ? this.daysData.current_month_days 
                            : this.daysData.last_month_days
                }
            },
            async chooseAndGetCalendarData(next = false, prev = false, sameView = false, calendarType = ""){
                if(!calendarType) calendarType = this.calendarType
                let url = ``
                if(calendarType === "monthly"){
                    await this.prepareMonthlyDays(next, prev)
                    url = `
                        /api/v1/employee/getmonth/?month=${this.daysData.month.number}
                        &year=${this.daysData.year}&calendarType=monthly`.replace(/\s/g, "")
                    await this.getCalendarData(sameView, calendarType, url)
                } else if(calendarType === "weekly"){
                    let newDate = {}
                    if(next) newDate = this.getNextDayOrWeek(this.prepareDataForNextOrPrevDayOrWeek(7, "next"))
                    else if(prev) newDate = this.getPrevDayOrWeek(this.prepareDataForNextOrPrevDayOrWeek(7, "prev"))
                    if(Object.keys(newDate).length){
                        this.daysData = {
                            ...this.daysData, 
                            month: {...this.daysData.month, number: newDate.month},
                            year: newDate.year,
                            dayOfMonth: newDate.dayOfMonth,
                        }
                    }
                    url = `/api/v1/employee/getmonth/?year=${this.daysData.year}
                        &calendarType=weekly&dayOfMonth=${this.daysData.dayOfMonth}
                        &month=${this.daysData.month.number}`.replace(/\s/g, "")
                    await this.getCalendarData(sameView, calendarType, url)
                }
            },
            async prepareMonthlyDays(next, prev){
                if(next){
                    if(this.daysData.month.number === 12){
                        this.daysData.year += 1
                        this.daysData.month.number = 1
                        this.fullDate = `${this.daysData.year}-0${this.daysData.month.number}`
                    } else {
                        this.daysData.month.number += 1
                        this.fullDate = this.daysData.month.number >= "10" 
                            ? `${this.daysData.year}-${this.daysData.month.number}`
                            : `${this.daysData.year}-0${this.daysData.month.number}`
                    }
                } else if (prev) {
                    if(this.daysData.month.number === 1){
                        this.daysData.year -= 1
                        this.daysData.month.number = 12
                        this.fullDate = `${this.daysData.year}-${this.daysData.month.number}`
                    } else {
                        this.daysData.month.number -= 1
                        this.fullDate = this.daysData.month.number >= "10" 
                            ? `${this.daysData.year}-${this.daysData.month.number}`
                            : `${this.daysData.year}-0${this.daysData.month.number}`
                    }
                }
            },

            async getCalendarData(sameView, calendarType, url){
                await AUTH_API.get(url)
                    .then((res) => {
                        this.daysData = {...res.data}
                        if(calendarType === "monthly" && this.daysData.month.number !== this.today.getMonth() + 1){
                            this.daysData.dayOfMonth = 1
                        }
                    })
                if(!sameView){
                    this.$router.push({ path: `/calendar/${calendarType}` })
                } 
            }
        }
    }
</script>