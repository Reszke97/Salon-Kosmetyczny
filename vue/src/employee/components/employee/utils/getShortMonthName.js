export const getShortMonthName = (month_number) => {
    let month = ""
    switch(month_number){
        case 1:
            month = "sty"
            break;
        case 2:
            month = "lut"
            break;
        case 3:
            month = "mar"
            break;
        case 4:
            month = "kwi"
            break;
        case 5:
            month = "maj"
            break;
        case 6:
            month = "cze"
            break;
        case 7:
            month = "lip"
            break;
        case 8:
            month = "sie"
            break;
        case 9:
            month = "wrz"
            break;
        case 10:
            month = "paź"
            break;
        case 11:
            month = "lis"
            break;
        case 12:
            month = "gru"
            break;
        default:
            month = "";
            break;
    }
    return month;
}