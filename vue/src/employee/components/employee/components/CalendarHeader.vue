<template>
    <div>
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
                        @click="setPickDate(false)"
                    >
                        Cancel
                    </v-btn>
                </v-date-picker>
            </div>
        </div>
    </div>
</template>
<script>
    export default {
        props: {
            chooseAndGetCalendarData: {
                type: Function,
                required: true
            },
            calendarHeader: {
                type: String,
                required: true
            },
            pickDate: {
                type: Boolean,
                required: true,
            },
            setPickDate: {
                type: Function,
                required: true
            },
            calendarType: {
                type: String,
                required: true,
            },
            setDate: {
                type: Function,
                required: true,
            },
            daysData: {
                type: Object,
                required: true
            },
            setDayOfMonth: {
                type: Function,
                required: true
            }
        },
        data: () => ({
            
        }),
        computed: {
            fullDate: {
                async set(date) {
                    date = date.split('-')
                    this.setDate(date)
                    if(this.calendarType !== "monthly"){
                        this.setDayOfMonth(date[2])
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
        }
    }

</script>