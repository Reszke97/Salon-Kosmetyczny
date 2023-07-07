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
                                    <template v-if="!!!item.default.is_free && !item.default.day.isHoliday">
                                        <div
                                            v-for="defaultWorkHours in item.default.work_hours"
                                        >
                                            <span>
                                                {{ `${defaultWorkHours.start_time} - ${defaultWorkHours.end_time}` }}
                                            </span>
                                        </div>
                                    </template>
                                    <template v-else-if="item.default.day.isHoliday">
                                        <span class="font-bold" style="color: rgb(255, 87, 76)">
                                            Święto
                                        </span>
                                    </template>
                                    <template v-else>
                                        <span class="font-bold" style="color: greenyellow">
                                            Wolne
                                        </span>
                                    </template>
                                    <template v-if="item.default.work_hours.length && !!!item.default.is_free && !item.default.day.isHoliday">
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
                                                @click="setActionDataAndOpenDialog({
                                                    day: item.default.day,
                                                    isDefault: false,
                                                    data: item.extra,
                                                })"
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
            :first-day-of-the-week-date="firstDayOfTheWeekDate"
            @closeEditAction="closeEditAction"
            @addBreak="addBreak"
            @editAvailabilityProp="editAvailabilityProp"
            @deleteBreak="deleteBreak"
            @addExtraDay="addExtraDay"
            @deleteDay="deleteDay"
            @saveData="saveDataAndRefresh"
        />
    </v-dialog>
</template>

<script>
    import axios from "axios";
    import { AUTH_API } from '../../../authorization/AuthAPI';
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
            firstDayOfTheWeekDate: "",
            maxWeeksForRegistration: 2,
            minTimeForRegistration: "60min",
            now: formatDate(new Date()),
            showEditAction: false,
            selectedActionData: {},
            itemsToDelete: [],
            nonWorkingDates: [],
        }),
        computed: {
            today(){
                const todayNum = new Date(this.now).getDay();
                return (
                    days({ first: this.firstDayOfTheWeekDate, nonWorkingDates: this.nonWorkingDates })
                        .find(el => el.num === todayNum)
                );
            }
        },
        async created(){
            const _now = new Date(this.now)
            this.firstDayOfTheWeekDate = new Date(_now).substractDays(_now.getDay() - 1)
            await this.getNonWorkingDates();
            await this.getAvailability();
        },
        methods: {
            async getNonWorkingDates(){
                const today = new Date();
                await axios.get(`http://127.0.0.1:8000/api/v1/employee/non-working-days/?year=${today.getFullYear()}`)
                    .then(res => {
                        this.nonWorkingDates = res.data;
                    })
            },
            async getAvailability(){
                this.availability = [];
                const API = await AUTH_API();
                await API.get("api/v1/employee/availability/")
                    .then(res => {
                        this.mapAvailablility(res.data)
                        this.maxWeeksForRegistration = res.data[0].max_weeks_for_registration;
                        this.minTimeForRegistration = res.data[0].min_time_for_registration;
                        
                    })
            },
            async deleteItems(){
                const uniqueItemsToDelete = [...new Set(this.itemsToDelete.map((el) => el))];
                const itemsForRequest = uniqueItemsToDelete.filter(el => el !== null && el !== "new");
                const API = await AUTH_API();
                await API.delete("api/v1/employee/availability/", { data: itemsForRequest })
            },
            async postData(){
                const API = await AUTH_API();
                await API.post("api/v1/employee/availability/", this.availability)
                    .then( () => {
                        alert("Zapisano zmiany");
                    })
            },
            async saveData(){
                if(this.itemsToDelete.length) await this.deleteItems();
                await this.postData();
            },
            async saveDataAndRefresh(){
                await this.saveData();
                await this.getAvailability();
                this.showEditAction = false;
                this.selectedActionData = {};
                this.itemsToDelete = [];
            },
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
                    return day.currentWeekDayDate
                    // const chosenDay = day.num === 0 ? 7 : day.num;
                    // const todayNum = this.today.num === 0 ? 7 : this.today.num;
                    // const daysEquation = todayNum - chosenDay;
                    // if(daysEquation > 0){
                    //     return formatDate(new Date(this.now).substractDays(daysEquation))
                    // } else {
                    //     return formatDate(new Date(this.now).addDays(daysEquation * (-1)))
                    // }
                }
            },

            setActionDataAndOpenDialog({ day, isDefault, data }){
                const date = isDefault ? this.getSelectedWeekItemDate(day) : "";
                this.setActionData({ day, isDefault, data, date });
                this.openEditAction();
            },

            mapAvailablility(items){
                for(const day of days({ first: this.firstDayOfTheWeekDate, nonWorkingDates: this.nonWorkingDates })){
                    const itemsGrpedByDay = items.filter(item => item.weekday === day.gb)
                    const objectToAppend = {
                        default: {},
                        extra: []
                    };
                    for(const item of itemsGrpedByDay){
                        if(item.is_default){
                            if(Object.keys(objectToAppend["default"]).length === 0){
                                objectToAppend["default"].day = day;
                                objectToAppend["default"].is_free = !!item.is_free;
                                objectToAppend["default"].is_holiday = !!item.is_holiday;
                                objectToAppend["default"].breaks = [];
                                objectToAppend["default"].is_break = !!item.is_break;
                                objectToAppend["default"].work_hours = [];
                                objectToAppend["default"].id = null;
                                if(!objectToAppend["default"].is_break) {
                                    objectToAppend["default"].id = item.id;
                                }
                            }
                            this.appendItemToDefaultOrExtra({
                                objectToModify: objectToAppend,
                                item: item,
                                keyToAppend: "default"
                            });
                        } else {
                            if(objectToAppend.extra.length === 0){
                                this.createAndAppendNewExtraItem({data: item, itemToModify: objectToAppend});
                            } else {
                                const foundIdx = objectToAppend.extra.findIndex(el => el.date === item.date)
                                if(foundIdx !== -1){
                                    if(!!!item.is_break) objectToAppend.extra[foundIdx].id = item.id;
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
                const objectToPush = {
                    start_time: item.start_time,
                    end_time: item.end_time
                }
                if(secondKeyToAppend === "breaks") objectToPush.id = item.id;
                if(keyToAppend === "default"){
                    if(item.is_free === 0 && item.start_time){
                        objectToModify[keyToAppend][secondKeyToAppend].push(objectToPush);
                    }
                } else {
                    if(item.is_free === 0){
                        objectToModify[secondKeyToAppend].push(objectToPush) ;
                    }
                }
            },
            createAndAppendNewExtraItem({data, itemToModify}){
                const extraItems = {
                    date: data.date,
                    is_free: !!data.is_free,
                    is_holiday: !!data.is_holiday,
                    is_break: false,
                    breaks: [],
                    work_hours: [],
                    id: null,
                }
                if(!!!data.is_break) extraItems.id = data.id;
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
            addBreak({ isDefault, day, extraDateIdx}){
                const availabilityIdx = this.getAvailabilityIdx({ day: day });
                if(isDefault){
                    this.availability[availabilityIdx].default.breaks.push({
                        end_time: "",
                        start_time: "",
                        id: "new",
                    })
                } else {
                    this.availability[availabilityIdx]["extra"][extraDateIdx]["breaks"].push({
                        end_time: "",
                        start_time: "",
                        id: "new",
                    })
                }
            },
            checkIfPropIsArray(prop){
                if(["date", "is_free", "is_holiday"].includes(prop)){
                    return false
                } else return true
            },
            checkiIfDayIsCorrect({ givenDate, dialogDay, givenDayEvents, prop }){
                if(prop === "date"){
                    const newDate = new Date(givenDate);
                    const dayAlreadyDefined = givenDayEvents.some(el => el.date === givenDate);
                    if(dayAlreadyDefined){
                        alert(`Wybrana data została już zdefiniowana ${givenDate}`)
                        return false
                    }
                    if(newDate.getDay() !== dialogDay.num){
                        alert(`Wybrano inny dzień niż ${dialogDay.pl}`)
                        return false
                    }
                } return true
            },
            editAvailabilityProp({ day, eventIdx, eventType, isDefault, prop, value, extraDateIdx }){
                const availabilityIdx = this.getAvailabilityIdx({ day: day });
                const dayType = isDefault ? "default" : "extra";
                const isPropArray = this.checkIfPropIsArray(prop);
                if(prop === "is_free") this.setFreeEvent({ day: day, extraDateIdx: extraDateIdx, isDefault: isDefault });
                if(isDefault){
                    if(isPropArray){
                        this.availability[availabilityIdx][dayType][eventType][eventIdx][prop] = value;
                    } else {
                        this.availability[availabilityIdx][dayType][prop] = value;
                    }
                } else {
                    if(isPropArray){
                        this.availability[availabilityIdx][dayType][extraDateIdx][eventType][eventIdx][prop] = value;
                    } else {
                        if(this.checkiIfDayIsCorrect({ 
                            givenDate: value, 
                            dialogDay: day, 
                            givenDayEvents: [...this.availability[availabilityIdx][dayType]],
                            prop: prop
                        })){
                            this.availability[availabilityIdx][dayType][extraDateIdx][prop] = value;
                        }
                    }
                }
            },
            deleteBreak({ day, isDefault, eventIdx, extraDateIdx }){
                const availabilityIdx = this.getAvailabilityIdx({ day: day });
                const dayType = isDefault ? "default" : "extra";
                if(isDefault){
                    this.itemsToDelete.push(this.availability[availabilityIdx][dayType]["breaks"][eventIdx]["id"]);
                    this.availability[availabilityIdx][dayType]["breaks"].splice(eventIdx, 1);
                } else {
                    this.itemsToDelete.push(this.availability[availabilityIdx][dayType][extraDateIdx]["breaks"][eventIdx]["id"]);
                    this.availability[availabilityIdx][dayType][extraDateIdx]["breaks"].splice(eventIdx, 1);
                }
            },
            deleteDay({ day, extraDateIdx }){
                const availabilityIdx = this.getAvailabilityIdx({ day: day });
                this.itemsToDelete.push(this.availability[availabilityIdx]["extra"][extraDateIdx]["id"]);
                this.availability[availabilityIdx]["extra"][extraDateIdx]["breaks"].forEach(el => {
                    this.itemsToDelete.push(el.id)
                })
                this.availability[availabilityIdx]["extra"].splice(extraDateIdx, 1);
            },
            setFreeEvent({ day, extraDateIdx, isDefault }){
                const availabilityIdx = this.getAvailabilityIdx({ day: day });
                const dayType = isDefault ? "default" : "extra";
                if(isDefault){
                    this.availability[availabilityIdx][dayType]["is_free"] = true;
                    this.availability[availabilityIdx][dayType]["work_hours"][0] = {
                        start_time: null,
                        end_time: null,
                    }
                    this.availability[availabilityIdx][dayType]["breaks"].forEach(el => {
                        this.itemsToDelete.push(el.id);
                    });
                    this.availability[availabilityIdx][dayType]["breaks"] = [];
                } else {
                    this.availability[availabilityIdx]["extra"][extraDateIdx]["is_free"] = true;
                    this.availability[availabilityIdx]["extra"][extraDateIdx]["work_hours"][0] = {
                        start_time: null,
                        end_time: null,
                    };
                    this.availability[availabilityIdx]["extra"][extraDateIdx]["breaks"].forEach(el => {
                        this.itemsToDelete.push(el.id);
                    });
                    this.availability[availabilityIdx]["extra"][extraDateIdx]["breaks"] = [];
                }

            },
            addExtraDay({ day }){
                const availabilityIdx = this.getAvailabilityIdx({ day: day });
                this.availability[availabilityIdx]["extra"].push({
                    breaks: [],
                    date: "",
                    is_free: false,
                    is_holiday: false,
                    id: "new",
                    work_hours: [{
                        end_time: "",
                        start_time: "",
                    }],
                })
            }
        }
    }
</script>

<style>
    @import "../../../../styles/globalStyles.css";
    .v-dialog {
        box-shadow:none!important
    }

</style>