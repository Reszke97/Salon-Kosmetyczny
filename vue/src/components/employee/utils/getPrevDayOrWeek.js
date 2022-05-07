export default {
    methods: {
        getPrevDayOrWeek(date) {
            let {day, month, year, dayCount, monthDays} = date
            if(day - dayCount <= 0){
                if (month === 1){
                    month = 12
                    year -= 1
                } else{
                    month -= 1
                }
                // Aby uzyskać odpowiedni dzień zeszłego miesiąca
                // najpierw od przekazanego dnia odejmuje ilość dni
                // a następnie zamieniam na liczbę dodatnią
                let daysToSubstract = (day - dayCount) * (-1) 
                day = monthDays - daysToSubstract
            } else {
                day -= dayCount
            }
            return {
                month,
                year,
                day
            }
        },
    },
};