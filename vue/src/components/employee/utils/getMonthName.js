export default {
    methods: {
        getMonthName(month_number) {
            switch(month_number){
                case month_number == 1:
                    return "Styczeń"
                case month_number == 2:
                    return "Luty"
                case month_number == 3:
                    return "Marzec"
                case month_number == 4:
                    return "Kwiecień"
                case month_number == 5:
                    return "Maj"
                case month_number == 6:
                    return "Czerwiec"
                case month_number == 7:
                    return "Lipiec"
                case month_number == 8:
                    return "Sierpień"
                case month_number == 9:
                    return "Wrzesień"
                case month_number == 10:
                    return "Październik"
                case month_number == 11:
                    return "Listopad"
                case month_number == 12:
                    return "Grudzień"
                default:
                    return ""
            }
        },
    },
};