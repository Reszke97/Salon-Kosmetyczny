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
                    :color="'#5cb85c'"
                >
                    Miesiąc - {{daysData.month.name}} {{daysData.year}}
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
                <v-btn style="width:100%">
                    Dzień
                </v-btn>
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
                    @click="getMonthlyCalendar(false, true)"
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
                    @click="getMonthlyCalendar(true, false)"
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
    import MonthlyCalendar from "../components/MonthlyCalendar.vue"
    export default {
        components: {
            MonthlyCalendar
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
                "day_count": 0,
                "month": {
                    "number": new Date().getMonth() + 1,
                    "name": ""
                },
                "year": new Date().getFullYear()
            }
        }),
        async created(){
            await this.getMonthlyCalendar()
        },
        methods: {
            async getMonthlyCalendar(next = false, prev = false){
                if(next){
                    if(this.daysData.month.number === 12){
                        this.daysData.year += 1
                        this.daysData.month.number = 1
                    } else {
                        this.daysData.month.number += 1
                    }
                } else if (prev) {
                    if(this.daysData.month.number === 1){
                        this.daysData.year -= 1
                        this.daysData.month.number = 12
                    } else {
                        this.daysData.month.number -= 1
                    }
                }
                await AUTH_API.get(
                        `/api/v1/employee/getmonth/?month=${this.daysData.month.number}&year=${this.daysData.year}`
                    )
                    .then((res) => {
                        this.daysData = {...res.data}
                    })
            }
        }
    }
</script>