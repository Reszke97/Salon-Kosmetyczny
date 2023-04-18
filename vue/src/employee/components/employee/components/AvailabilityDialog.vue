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
                height: `${screenSize.screenHeight - 70}px`,
            }"
        >
            <v-col
                class="bg-color"
                cols="12"
                sm="12"
                md="8"
                lg="6"
            >
                <div class="flex-centered">
                    <h1>Zapisana dyspozycyjność</h1>
                </div>
                <div class="flex-centered flex-row">
                    
                </div>
                <div>
                    <v-btn @click="$emit('closeAvailabilityDialog')">
                        Zamknij
                    </v-btn>
                </div>
            </v-col>
        </v-row>
    </v-dialog>
</template>

<script>
    import { AUTH_API } from '../../../authorization/AuthAPI';
    import { defaultAvailability } from "../utils/defaultAvailability";
    import { days } from "../utils/days";
    export default {
        name: "",
        components: {
            
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
        }),
        computed: {
            
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
                    objectToModify[keyToAppend][secondKeyToAppend].push({
                        start_time: item.start_time,
                        end_time: item.end_time,
                    }) 
                } else {
                    if(item.is_free === 0)
                    objectToModify[secondKeyToAppend].push({
                        start_time: item.start_time,
                        end_time: item.end_time,
                    }) 
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