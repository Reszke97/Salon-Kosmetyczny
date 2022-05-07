export default {
    methods: {
        getNextDayOrWeek(date) {
            let {day, month, year, dayCount, monthDays} = date
            if(day + dayCount > monthDays){
                if (month === 12){
                    month = 1
                    year += 1
                } else{
                    month += 1
                }
                day = day + dayCount - monthDays
            } else {
                day += dayCount
            }
            return {
                month,
                year,
                day
            }
        },
    },
};