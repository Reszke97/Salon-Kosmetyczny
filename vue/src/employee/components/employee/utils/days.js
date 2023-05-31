import { formatDate } from "../../../../utils/formatDate";

export const days = ({ first, nonWorkingDates }) => {
    const _days = [
        {
            gb: "monday",
            pl: "poniedziałek",
            num: 1,
            currentWeekDayDate: formatDate(first),
            isHoliday: false,
        },
        {
            gb: "tuesday",
            pl: "wtorek",
            num: 2,
            currentWeekDayDate: formatDate(new Date(first).addDays(first.getDay())),
            isHoliday: false,
        },
        {
            gb: "wednesday",
            pl: "środa",
            num: 3,
            currentWeekDayDate: formatDate(new Date(first).addDays(first.getDay() + 1)),
            isHoliday: false,
        },
        {
            gb: "thursday",
            pl: "czwartek",
            num: 4,
            currentWeekDayDate: formatDate(new Date(first).addDays(first.getDay() + 2)),
            isHoliday: false,
        },
        {
            gb: "friday",
            pl: "piątek",
            num: 5,
            currentWeekDayDate: formatDate(new Date(first).addDays(first.getDay() + 3)),
            isHoliday: false,
        },
        {
            gb: "saturday",
            pl: "sobota",
            num: 6,
            currentWeekDayDate: formatDate(new Date(first).addDays(first.getDay() + 4)),
            isHoliday: false,
        },
        {
            gb: "sunday",
            pl: "niedziela",
            num: 0,
            currentWeekDayDate: formatDate(new Date(first).addDays(first.getDay() + 5)),
            isHoliday: false,
        },
    ]
    _days.forEach((day, key) => {
        if(nonWorkingDates.includes(day.currentWeekDayDate.substring(5))){
            _days[key]["isHoliday"] = true;
        }
    })
    return _days;
}