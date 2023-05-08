<template>
    <v-dialog
        id="availability-dialog"
        :value="availabilityDialog"
        persistent
        width="100%"
    >
        <v-row 
            class="fill-height white-text"
            justify="center"
            :style="{
                maxHeight: `${screenSize.screenHeight - 60}px`,
            }"
        >
            <v-col
                class="bg-color"
                cols="12"
                sm="12"
                md="8"
                lg="5"
            >
                <div class="flex-centered">
                    <h1>Zapisana dyspozycyjność</h1>
                </div>
                <div class="d-flex flex-row">
                    <div 
                        class="px-2"
                        style="
                            max-width: 150px;
                            border-right: 1px solid;
                            border-left: 1px solid;
                            border-top: 1px solid;
                            border-bottom: 1px solid;
                            border-color: hsla(0,0%,100%,.12);
                        "
                    >
                        <span>Domyślna dyspozycyjność</span>
                    </div>
                    <div 
                        class="w-100 px-2"
                        style="
                            border-right: 1px solid;
                            border-top: 1px solid;
                            border-bottom: 1px solid;
                            border-color: hsla(0,0%,100%,.12);
                        "
                    >
                        <span>
                            Dodatkowe zdarzenia
                        </span>
                    </div>
                </div>
                <div class="flex-centered w-100 flex-col">
                    <div
                        v-for="item in availability"
                        class="w-100 flex px-2"
                        style="
                            min-height: 50px!important;
                            border: 1px solid;
                            border-top: 0;
                            border-color: hsla(0,0%,100%,.12);
                        "
                    >
                        <div 
                            class="w-100 d-flex"
                        >
                            <div 
                                style="
                                    max-width: 141px;
                                    border-right: 1px solid hsla(0,0%,100%,.12);
                                "
                            >
                                <div
                                    class="d-flex"
                                >
                                    <h4 class="mr-1">
                                        {{ item.default.day.pl.charAt(0).toUpperCase() + item.default.day.pl.substring(1)  }}
                                    </h4>
                                    <v-tooltip bottom>
                                        <template v-slot:activator="{ on, attrs }">
                                            <v-icon
                                                style="font-size:20px"
                                                dark
                                                v-bind="attrs"
                                                v-on="on"
                                                @click="setActionDataAndOpenDialog({
                                                    day: item.default.day,
                                                    isDefault: true,
                                                    data: [ item.default ],
                                                })"
                                            >
                                                mdi-pencil
                                            </v-icon>
                                        </template>
                                        <span>Edytuj</span>
                                    </v-tooltip>
                                </div>
                                <div 
                                    style="
                                        min-width: 141px;
                                        border-right: 1px solid hsla(0,0%,100%,.12);
                                    "
                                >
                                    <template v-if="!!!item.default.is_free">
                                        <div
                                            v-for="defaultWorkHours in item.default.work_hours"
                                        >
                                            <span>
                                                {{ `${defaultWorkHours.start_time} - ${defaultWorkHours.end_time}` }}
                                            </span>
                                        </div>
                                    </template>
                                    <template v-else>
                                        <span style="color: greenyellow">
                                            Wolne
                                        </span>
                                    </template>
                                    <template v-if="item.default.work_hours.length && !!!item.default.is_free">
                                        <span>
                                            Przerwy
                                        </span>
                                        <div
                                            v-for="defaultBreaks in item.default.breaks"
                                        >
                                            {{ `${defaultBreaks.start_time} - ${defaultBreaks.end_time}` }}
                                        </div>
                                    </template>
                                </div>
                            </div>
                            <div class="flex-centered flex-row w-100">
                                <div class="w-100 flex-centered flex-col">
                                    <template v-for="extra in item.extra">
                                        <div 
                                            v-if="extra.date >= now" style="color: orange" 
                                            class="w-100 px-2 d-flex"
                                        >
                                            <span>
                                                {{ extra.date }}
                                            </span>
                                        </div>
                                    </template>
                                </div>
                                <div class="w-100 d-flex justify-end">
                                    <v-tooltip bottom>
                                        <template v-slot:activator="{ on, attrs }">
                                            <v-icon
                                                style="font-size:20px"
                                                dark
                                                v-bind="attrs"
                                                v-on="on"
                                            >
                                                mdi-pencil
                                            </v-icon>
                                        </template>
                                        <span>Edytuj</span>
                                    </v-tooltip>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <v-btn 
                        @click="$emit('closeAvailabilityDialog')"
                        class="mt-2"
                        color="success"
                    >
                        Zamknij
                    </v-btn>
                </div>
            </v-col>
        </v-row>
        <edit-action
            v-if="showEditAction"
            :show-edit-action="showEditAction"
            :selected-action-data="selectedActionData"
            @closeEditAction="closeEditAction"
            @addBreak="addBreak"
            @editAvailabilityProp="editAvailabilityProp"
            @deleteBreak="deleteBreak"
        />
    </v-dialog>
</template>

<script>
    import { AUTH_API } from '../../../authorization/AuthAPI';
    import { defaultAvailability } from "../utils/defaultAvailability";
    import { days } from "../utils/days";
    import { formatDate } from "../../../../utils/formatDate"
    import EditAction from "./EditAction.vue"

    export default {
        name: "",
        components: {
            EditAction
        },
        emits: [ "closeAvailabilityDialog" ],
        inject: ["screenSize"],
        props: {
            availabilityDialog: { type: Boolean, default: false },
        },
        data: () => ({
            availability: [],
            maxWeeksForRegistration: 2,
            minTimeForRegistration: "60min",
            now: formatDate(new Date()),
            showEditAction: false,
            selectedActionData: {},
        }),
        computed: {
            today(){
                const todayNum = new Date(this.now).getDay();
                return days.find(el => el.num === todayNum);
            }
        },
        async created(){
            const API = await AUTH_API();
            await API.get("api/v1/employee/availability")
                .then(res => {
                    if(res.data){
                        this.mapAvailablility(res.data)
                        this.maxWeeksForRegistration = res.data[0].max_weeks_for_registration;
                        this.minTimeForRegistration = res.data[0].min_time_for_registration;
                    } else {
                        this.availability = [...defaultAvailability]
                    }
                })
        },
        methods: {
            closeEditAction(){
                this.showEditAction = false;
            },
            openEditAction(){
                this.showEditAction = true;
            },
            setActionData({ day, isDefault, data, date }){
                this.selectedActionData = {
                    day: day,
                    is_default: isDefault,
                    data: data,
                    date: date,
                }
            },

            getSelectedWeekItemDate(day){
                if(day.pl === this.today.pl){
                    return this.now
                } else {
                    const chosenDay = day.num === 0 ? 7 : day.num;
                    const todayNum = this.today.num === 0 ? 7 : this.today.num;
                    const daysEquation = todayNum - chosenDay;
                    if(daysEquation > 0){
                        return formatDate(new Date(this.now).substractDays(daysEquation))
                    } else {
                        return formatDate(new Date(this.now).addDays(daysEquation * (-1)))
                    }
                }
            },

            setActionDataAndOpenDialog({ day, isDefault, data }){
                const date = isDefault ? this.getSelectedWeekItemDate(day) : "";
                this.setActionData({ day, isDefault, data, date });
                this.openEditAction();
            },
            mapAvailablility(items){
                for(const day of days){
                    const itemsGrpedByDay = items.filter(item => item.weekday === day.gb)
                    const objectToAppend = {
                        default: {},
                        extra: []
                    };
                    for(const item of itemsGrpedByDay){
                        if(item.is_default){
                            if(Object.keys(objectToAppend["default"]).length === 0){
                                objectToAppend["default"].day = day;
                                objectToAppend["default"].is_free = item.is_free;
                                objectToAppend["default"].is_holiday = item.is_holiday;
                                objectToAppend["default"].breaks = [];
                                objectToAppend["default"].work_hours = [];
                            }
                            this.appendItemToDefaultOrExtra({
                                objectToModify: objectToAppend,
                                item: item,
                                keyToAppend: "default"
                            });
                        } else {
                            if(objectToAppend.length === 0){
                                this.createAndAppendNewExtraItem({data: item, itemToModify: objectToAppend});
                            } else {
                                const foundIdx = objectToAppend.extra.findIndex(el => el.date === item.date)
                                if(foundIdx !== -1){
                                    this.appendItemToDefaultOrExtra({
                                        objectToModify: objectToAppend.extra[foundIdx],
                                        item: item,
                                        keyToAppend: "extra"
                                    })
                                } else {
                                    this.createAndAppendNewExtraItem({data: item, itemToModify: objectToAppend});
                                }
                            }
                        }
                    }
                    this.availability.push(objectToAppend);
                }
            },
            appendItemToDefaultOrExtra({ objectToModify, item, keyToAppend }){
                let secondKeyToAppend = "work_hours";
                if(item.is_break){
                    secondKeyToAppend = "breaks";
                }
                if(keyToAppend === "default"){
                    if(item.is_free === 0 && item.start_time){
                        objectToModify[keyToAppend][secondKeyToAppend].push({
                            start_time: item.start_time,
                            end_time: item.end_time,
                        }) 
                    }
                } else {
                    if(item.is_free === 0){
                        objectToModify[secondKeyToAppend].push({
                            start_time: item.start_time,
                            end_time: item.end_time,
                        }) 
                    }
                }
            },
            createAndAppendNewExtraItem({data, itemToModify}){
                const extraItems = {
                    date: data.date,
                    is_free: data.is_free,
                    is_holiday: data.is_holiday,
                    breaks: [],
                    work_hours: [],
                }
                this.appendItemToDefaultOrExtra({
                    objectToModify: extraItems,
                    item: data,
                    keyToAppend: "extra"
                })
                itemToModify.extra.push(extraItems);
            },
            getAvailabilityIdx({ day }){
                return this.availability.findIndex(avail => avail.default.day.pl === day.pl)
            },
            addBreak({ isDefault, day, date}){
                const availabilityIdx = this.getAvailabilityIdx({ day: day });
                if(isDefault){
                    this.availability[availabilityIdx].default.breaks.push({
                        end_time: "",
                        start_time: "",
                    })
                } else {

                }
            },
            getExtraDateIdx({ availabilityIdx, dayType, date }){
                return this.availability[availabilityIdx][dayType].findIndex( extra => extra.date === date)
            },
            checkIfPropIsArray(prop){
                if(["date", "is_free", "is_holiday"].includes(prop)){
                    return false
                } else return true
            },
            editAvailabilityProp({ date, day, eventIdx, eventType, isDefault, prop, value }){
                const availabilityIdx = this.getAvailabilityIdx({ day: day });
                const dayType = isDefault ? "default" : "extra";
                const isPropArray = this.checkIfPropIsArray(prop);
                if(isDefault){
                    if(isPropArray){
                        this.availability[availabilityIdx][dayType][eventType][eventIdx][prop] = value;
                    } else {
                        this.availability[availabilityIdx][dayType][prop] = value;
                    }
                } else {
                    const extraDateIdx = this.getExtraDateIdx({ availabilityIdx: availabilityIdx, dayType: dayType, date: date })
                    if(isPropArray){
                        this.availability[availabilityIdx][dayType][extraDateIdx][eventType][eventIdx][prop] = value;
                    } else {
                        this.availability[availabilityIdx][dayType][extraDateIdx][prop] = value;
                    }
                }
            },
            deleteBreak({ day, isDefault, date, eventIdx, }){
                const availabilityIdx = this.getAvailabilityIdx({ day: day });
                const dayType = isDefault ? "default" : "extra";
                if(isDefault){
                    console.log('yeah')
                    this.availability[availabilityIdx][dayType]["breaks"].splice(eventIdx, 1);
                } else {
                    const extraDateIdx = this.getExtraDateIdx({ availabilityIdx: availabilityIdx, dayType: dayType, date: date })
                    this.availability[availabilityIdx][dayType][extraDateIdx]["breaks"].splice(eventIdx, 1);
                }
            },
        }
    }
</script>

<style>
    @import "../../../../styles/globalStyles.css";
    .v-dialog {
        box-shadow:none!important
    }

</style>