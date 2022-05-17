<template>
    <div 
    >
        <div
            style="
                width:100%;
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
                :key="day.number + day.month_in_words"
            >
                <div
                    class="py-5"
                >
                    <span
                        :style="colorHolidaysAndToday(day, weekDay)"
                    >
                        {{day.number}}
                    </span>

                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        daysData: {
            type: Object,
            required: true
        },
        today: {
            type: Date,
            required: true
        }
    },
    methods: {
        colorHolidaysAndToday(day, weekDay){
            console.log(weekDay)
            let style;
            if(
                day.number === this.today.getDate() 
                && day.month === this.today.getMonth() + 1 
                && this.daysData.year === this.today.getFullYear()
            ){
                style =  {
                    display: 'inline-flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    minHeight: '50px',
                    padding: '8px 2px 8px 2px',
                    borderWidth: '1px',
                    border: 'solid',
                    borderRadius: '100%',
                    minWidth: '50px',
                    borderColor: '#5cb85c',
                    backgroundColor: '#5cb85c'
                }
            } else{
                style =  {
                    display: 'inline-flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    minHeight: '50px',
                    padding: '8px 2px 8px 2px',
                }
            }
            if(weekDay == "Niedziela" || day.holiday){
                style.color = 'red'
                style.fontWeight = 'bold'
            }
            return style
        }
    },
    computed: {
        
    }
}
</script>
