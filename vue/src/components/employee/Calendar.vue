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
                    width:5%;
                "
            >
                <v-icon large>
                    mdi-chevron-left
                </v-icon>
            </div>
            <div
                style="
                    width:90%;
                "
                v-for="(weekDay, idx) of Object.keys(daysData.days)"
                :key="weekDay + idx"
            >
                <div
                    style="
                        width:100%;
                        text-align: center;
                    "
                >
                    <div><b>{{weekDay}}</b></div>
                </div>
                <div
                    style="
                        width:100%;
                        justify-content: center;
                        text-align: center;
                    "
                    v-for="day in daysData.days[weekDay]"
                    :key="day.number"
                >
                    <div
                        class="py-5"
                    >{{day.number}}</div>
                </div>
            </div>
            <div 
                id="next-month"
                style="
                    display:flex;
                    align-items:center;
                    width:5%;
                "
            >
                <v-icon large>
                    mdi-chevron-right
                </v-icon>
            </div>
        </div>
    </v-container>
</template>




<script>
    import { AUTH_API } from '../../authorization/AuthAPI'
    import axios from 'axios'
    export default {
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
            }
        }),
        async created(){
            // await AUTH_API.get(`/api/v1/employee/getmonth/`)
            await AUTH_API.get(`/api/v1/employee/getmonth/?month=${5}`)
            .then((res) => {
                this.daysData = res.data
            })
        },
    }
</script>