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
                        :style="
                            day.number === today.getDate()
                            ?
                            {
                                borderWidth: '1px',
                                border: 'solid',
                                borderRadius: '100%',
                                padding: '8px 2px 8px 2px',
                                display: 'inline-flex',
                                justifyContent: 'center',
                                alignItems: 'center',
                                minWidth: '50px',
                                minHeight: '50px',
                                borderColor: '#5cb85c',
                                backgroundColor: '#5cb85c'
                            }
                            : 
                            {
                                display: 'inline-flex',
                                justifyContent: 'center',
                                alignItems: 'center',
                                minHeight: '50px',
                                padding: '8px 2px 8px 2px',
                            }
                        "
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
    }
}
</script>
