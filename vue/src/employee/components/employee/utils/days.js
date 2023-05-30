import { formatDate } from "../../../../utils/formatDate";

export const days = (first) => {
    return ([
        {
            gb: "monday",
            pl: "poniedziałek",
            num: 1,
            currentWeekDayDate: formatDate(first),
        },
        {
            gb: "tuesday",
            pl: "wtorek",
            num: 2,
            currentWeekDayDate: formatDate(new Date(first).addDays(first.getDay())),
        },
        {
            gb: "wednesday",
            pl: "środa",
            num: 3,
            currentWeekDayDate: formatDate(new Date(first).addDays(first.getDay() + 1)),
        },
        {
            gb: "thursday",
            pl: "czwartek",
            num: 4,
            currentWeekDayDate: formatDate(new Date(first).addDays(first.getDay() + 2)),
        },
        {
            gb: "friday",
            pl: "piątek",
            num: 5,
            currentWeekDayDate: formatDate(new Date(first).addDays(first.getDay() + 3)),
        },
        {
            gb: "saturday",
            pl: "sobota",
            num: 6,
            currentWeekDayDate: formatDate(new Date(first).addDays(first.getDay() + 4)),
        },
        {
            gb: "sunday",
            pl: "niedziela",
            num: 0,
            currentWeekDayDate: formatDate(new Date(first).addDays(first.getDay() + 5)),
        },
    ])
}