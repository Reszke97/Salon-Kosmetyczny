export default {
    methods: {
        getPrevDayOrWeek(date) {
            let {dayOfMonth, month, year, dayCount, monthDays} = date
            if(dayOfMonth - dayCount <= 0){
                if (month === 1){
                    month = 12
                    year -= 1
                } else{
                    month -= 1
                }
                // Aby uzyskać odpowiedni dzień zeszłego miesiąca
                // najpierw od przekazanego dnia odejmuje ilość dni
                // a następnie zamieniam na liczbę dodatnią
                let daysToSubstract = (dayOfMonth - dayCount) * (-1) 
                dayOfMonth = monthDays - daysToSubstract
            } else {
                dayOfMonth -= dayCount
            }
            return {
                month,
                year,
                dayOfMonth
            }
        },
    },
};