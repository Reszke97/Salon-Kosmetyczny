import { days } from "./days"
export const defaultAvailability = [
    {
        default: {
            day: days.find(day => day.gb === "monday"),
            is_free: false,
            is_holiday: false,
            breaks: [{
                start_time: "10:00",
                end_time: "10:30",
            }],
            work_hours: [{
                start_time: "8:00",
                end_time: "16:00", 
            }],
        },
        extra: {}
    },
    {
        default:{
            day: days.find(day => day.gb === "tuesday"),
            is_free: false,
            is_holiday: false,
            breaks: [{
                start_time: "10:00",
                end_time: "10:30",
            }],
            work_hours: [{
                start_time: "8:00",
                end_time: "16:00", 
            }],
        },
        
        extra: {}
    },
    {
        default: {
            day: days.find(day => day.gb === "wednesday"),
            is_free: false,
            is_holiday: false,
            breaks: [{
                start_time: "10:00",
                end_time: "10:30",
            }],
            work_hours: [{
                start_time: "8:00",
                end_time: "16:00", 
            }],
        },
        
        extra: {}
    },
    {
        default: {
            day: days.find(day => day.gb === "thursday"),
            is_free: false,
            is_holiday: false,
            breaks: [{
                start_time: "10:00",
                end_time: "10:30",
            }],
            work_hours: [{
                start_time: "8:00",
                end_time: "16:00", 
            }],
        },
        extra: {}
    },
    {
        default: {
            day: days.find(day => day.gb === "friday"),
            is_free: false,
            is_holiday: false,
            breaks: [{
                start_time: "10:00",
                end_time: "10:30",
            }],
            work_hours: [{
                start_time: "8:00",
                end_time: "16:00", 
            }],
        },
        extra: {}
    },
    {
        default: {
            day: days.find(day => day.gb === "saturday"),
            is_free: true,
            is_holiday: false,
            breaks: [{
                start_time: "10:00",
                end_time: "10:30",
            }],
            work_hours: [{
                start_time: "8:00",
                end_time: "16:00", 
            }],
        },
        extra: {}
    },
    {
        default: {
            day: days.find(day => day.gb === "sunday"),
            is_free: true,
            is_holiday: false,
            breaks: [{
                start_time: "10:00",
                end_time: "10:30",
            }],
            work_hours: [{
                start_time: "8:00",
                end_time: "16:00", 
            }],
        },
        extra: [{}]
    },
]

// extra: [{
//     date: "",
//     is_free: "",
//     breaks: {
//         start_time: "",
//         end_time: "",
//     },
//     work_hours: {
//         start_time: "",
//         end_time: "",
//     }
// }]