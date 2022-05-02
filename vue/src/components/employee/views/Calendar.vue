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
                    @click="getMonthlyCalendar(undefined, undefined, undefined, 'monthly')"
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
                    @click="getMonthlyCalendar(undefined, undefined, undefined, 'weekly')"
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
                    @click="getMonthlyCalendar(undefined, undefined, undefined, 'daily')"
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
                        v-model="date"
                        type="month"
                        no-title
                        scrollable
                        @change="getPickedMonthCalendar"
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
                    @click="getMonthlyCalendar(false, true, true)"
                >
                    <v-icon large>
                        mdi-chevron-left
                    </v-icon>
                </v-btn>
            </div>
            <monthly-weekly-calendar
                style="
                    display:flex;
                    width:95%;
                "
                :days-data="daysData"
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
                    @click="getMonthlyCalendar(true, false, true)"
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
    import MonthlyWeeklyCalendar from "../components/MonthlyWeeklyCalendar.vue"
    export default {
        components: {
            MonthlyWeeklyCalendar
        },
        mixins: [
            getMonthName
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
                "week": 0,
                "year": 0,
                "day": 0,
            },
            activePicker: null,
            date: "",
            pickDate: false,
        }),
        async created(){
            const today = new Date()
            this.daysData.month.number = today.getMonth() + 1
            this.daysData.year = today.getFullYear()
            this.daysData.day = today.getDay()
            const monthNumber = this.daysData.month.number >= 10 
                ? this.daysData.month.number: 0 + this.daysData.month.number.toString()
            await this.getMonthlyCalendar(undefined, undefined, true)
            this.date = `${this.daysData.year}-${monthNumber}`
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
            calendarHeader(){
                return (this.calendarType === "monthly" 
                    ? `${this.daysData.month.name} - ${this.daysData.year}` 
                    :  this.calendarType === "weekly" 
                    ?  `${this.daysData.week} - ${this.daysData.year}`
                    : this.calendarType === "daily"
                    ? `Dzień`
                    : null
                )
            }
        },
        methods: {
            async getPickedMonthCalendar(){
                const date = this.date.split('-')
                this.daysData.month.number = date[1] !== "10" ? date[1].replace('0', ''): date[1]
                this.daysData.year = date[0]
                await this.getMonthlyCalendar(undefined, undefined, true, "monthly")
            },
            async getMonthlyCalendar(next = false, prev = false, sameView = false, calendarType = ""){
                if(!calendarType) calendarType = this.calendarType
                if(next){
                    if(this.daysData.month.number === 12){
                        this.daysData.year += 1
                        this.daysData.month.number = 1
                        this.date = `${this.daysData.year}-0${this.daysData.month.number}`
                    } else {
                        this.daysData.month.number += 1
                        this.date = this.daysData.month.number >= "10" 
                            ? `${this.daysData.year}-${this.daysData.month.number}`
                            : `${this.daysData.year}-0${this.daysData.month.number}`
                    }
                } else if (prev) {
                    if(this.daysData.month.number === 1){
                        this.daysData.year -= 1
                        this.daysData.month.number = 12
                        this.date = `${this.daysData.year}-${this.daysData.month.number}`
                    } else {
                        this.daysData.month.number -= 1
                        this.date = this.daysData.month.number >= "10" 
                            ? `${this.daysData.year}-${this.daysData.month.number}`
                            : `${this.daysData.year}-0${this.daysData.month.number}`
                    }
                }
                let url = ``
                if(calendarType === "monthly"){
                    url = `/api/v1/employee/getmonth/?month=${this.daysData.month.number}&year=${this.daysData.year}&calendarType=monthly`
                } else if(calendarType === "weekly"){
                    url = `/api/v1/employee/getmonth/?year=${this.daysData.year}&calendarType=weekly&day=30&month=5`
                } else if(calendarType === "daily"){

                }
                await AUTH_API.get(url)
                    .then((res) => {
                        this.daysData = {...res.data}
                        //this.date zupadtetować tyź
                    })
                if(!sameView) this.$router.push({ path: `/calendar/${calendarType}` })
            }
        }
    }
</script>