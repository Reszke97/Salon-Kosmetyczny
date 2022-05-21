export default {
    methods: {
        getNextDayOrWeek(date) {
            let {dayOfMonth, month, year, dayCount, monthDays} = date
            if(dayOfMonth + dayCount > monthDays){
                if (month === 12){
                    month = 1
                    year += 1
                } else{
                    month += 1
                }
                dayOfMonth = dayOfMonth + dayCount - monthDays
            } else {
                dayOfMonth += dayCount
            }
            return {
                month,
                year,
                dayOfMonth
            }
        },
    },
};