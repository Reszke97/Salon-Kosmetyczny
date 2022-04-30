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
                >{{day.number}}</div>
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
    }
}
</script>
