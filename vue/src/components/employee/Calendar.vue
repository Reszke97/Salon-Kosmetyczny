<template>
    <v-container fluid>
        <div 
            style="display:flex"

        >
            <div
                style="background-color:#0892d0;width:100%"
                v-for="(weekDay, idx) of Object.keys(daysData.days)"
                :key="weekDay + idx"
            >
                <div
                    style="
                        width:100%;
                        text-align: center;
                    "
                >
                    <h1>{{weekDay}}</h1>
                </div>
                <div
                    style="
                        flex-direction:row;
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
            await AUTH_API.get('/api/v1/employee/getmonth/')
            .then((res) => {
                this.daysData = res.data
            })
        },
    }
</script>