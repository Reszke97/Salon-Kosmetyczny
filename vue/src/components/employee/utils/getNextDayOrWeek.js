export default {
    methods: {
        getNextMonthDays(date, dayCount, currentMonthDays) {
            const {day, month, year} = date
            if(day + dayCount > currentMonthDays){
                if (month === 12){
                    month = 1
                    year += 1
                } else{
                    month += 1
                }
                day = day + dayCount - currentMonthDays
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