<template>
    <v-dialog
        id="action-dialog"
        :value="showEditAction"
        persistent
        width="100%"
    >
    <v-row 
        class="fill-height white-text"
        justify="center"
    >
        <v-col
            class="bg-color"
            cols="12"
            sm="12"
            md="6"
            lg="3"
        >
            <div
                class="flex-col"
            >
                <div class="d-flex mb-2">
                    <div class="w-100">
                        <h4>
                            <span 
                                v-if="selectedActionData.is_default"
                            >
                                Domyślna dyspozycyjność:
                            </span>
                            <span 
                                v-else="selectedActionData.is_default"
                            >
                                Dodatkowe zdarzenia:
                            </span>
                            <span style="color: orange">
                                {{ selectedActionData.day.pl.charAt(0).toUpperCase() + selectedActionData.day.pl.substring(1) }}
                            </span>
                        </h4>
                    </div>
                    <div>
                        <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                                <v-icon
                                    dark
                                    v-bind="attrs"
                                    v-on="on"
                                    @click="$emit('closeEditAction')"
                                >mdi-close-circle</v-icon>
                            </template>
                            <span>Zamknij</span>
                        </v-tooltip>
                    </div>
                </div>
                <v-expansion-panels dark class="accordion-wrapper"
                    v-model="panel"
                >
                    <v-expansion-panel
                        v-for="(currentDateData, panelIdx) of selectedActionData.data"
                        :key="panelIdx"
                    >
                        <v-expansion-panel-header>
                            <div class="d-flex">
                                <div class="w-100">
                                    <v-menu
                                        ref="menu"
                                            v-model="showDatePickerMenu"
                                            :close-on-content-click="false"
                                            transition="scale-transition"
                                            offset-y
                                            max-width="290px"
                                            min-width="auto"
                                            @click.native.stop
                                        >
                                        <template v-slot:activator="{ on, attrs }">
                                            <v-text-field
                                                :value="selectedActionData.is_default ? selectedActionData.date : currentDateData.date"
                                                label="Data"
                                                persistent-hint
                                                prepend-icon="mdi-calendar"
                                                v-bind="attrs"
                                                @blur="date = formatDate(selectedActionData.is_default ? selectedActionData.date : currentDateData.date)"
                                                v-on="on"
                                                :disabled="selectedActionData.is_default"
                                            ></v-text-field>
                                        </template>
                                        <v-date-picker
                                            :value="selectedActionData.is_default ? selectedActionData.date : currentDateData.date"
                                            no-title
                                            @input="showDatePickerMenu = false"
                                        ></v-date-picker>
                                    </v-menu>
                                    <!-- @click.native.stop -->
                                </div>
                            </div>
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                            <div class="d-flex align-center">
                                <div class="w-100">
                                    Godziny pracy:
                                </div>
                                <div id="is-free">
                                    <v-checkbox
                                        :value="!!selectedActionData.is_free"
                                        label="Wolne"
                                        @change="val => $emit('editAvailabilityProp', {
                                            value: val,
                                            day: selectedActionData.day,
                                            isDefault: selectedActionData.is_default,
                                            date: selectedActionData.is_default ? '' : currentDateData.date,
                                            prop: 'is_free',
                                            eventType: '',
                                            eventIdx: null
                                        })"
                                    />
                                </div>
                            </div>
                            <template v-if="!!!currentDateData.is_free">
                                <div
                                    v-for="item of currentDateData.work_hours"
                                >
                                    <v-text-field
                                        :value="item.start_time"
                                        label="Godzina rozpoczęcia"
                                        type="time"
                                        dark
                                    />
                                    <v-text-field
                                        :value="item.end_time"
                                        label="Godzina zakończenia"
                                        type="time"
                                        dark
                                    />
                                </div>
                                <div 
                                    class="d-flex flex-col"
                                >
                                    <template
                                        v-if="currentDateData.breaks.length"
                                    >
                                        <div 
                                            v-for="(item, idx) of currentDateData.breaks"
                                        >
                                            <div class="d-flex">
                                                <span>
                                                    {{ `Przerwa ${idx + 1}` }}
                                                </span>
                                                <div>
                                                    <v-tooltip bottom>
                                                        <template v-slot:activator="{ on, attrs }">
                                                            <v-icon
                                                                style="font-size:20px; cursor: pointer"
                                                                dark
                                                                v-bind="attrs"
                                                                v-on="on"
                                                                color="red"
                                                                @click="$emit('deleteBreak', {
                                                                    day: selectedActionData.day,
                                                                    isDefault: selectedActionData.is_default,
                                                                    date: selectedActionData.is_default ? '' : currentDateData.date,
                                                                    eventIdx: idx
                                                                })"
                                                            >
                                                                mdi-trash-can
                                                            </v-icon>
                                                        </template>
                                                        <span>Usuń przerwę</span>
                                                    </v-tooltip>
                                                </div>
                                            </div>
                                            <v-text-field
                                                :value="item.start_time"
                                                label="Godzina rozpoczęcia"
                                                dark
                                                type="time"
                                                @input="val => $emit('editAvailabilityProp', {
                                                    value: val,
                                                    day: selectedActionData.day,
                                                    isDefault: selectedActionData.is_default,
                                                    date: selectedActionData.is_default ? '' : currentDateData.date,
                                                    prop: 'start_time',
                                                    eventType: 'breaks',
                                                    eventIdx: idx
                                                })"
                                            />
                                            <v-text-field
                                                :value="item.end_time"
                                                label="Godzina zakończenia"
                                                type="time"
                                                dark
                                                @input="val => $emit('editAvailabilityProp', {
                                                    value: val,
                                                    day: selectedActionData.day,
                                                    isDefault: selectedActionData.is_default,
                                                    date: selectedActionData.is_default ? '' : currentDateData.date,
                                                    prop: 'end_time',
                                                    eventType: 'breaks',
                                                    eventIdx: idx
                                                })"
                                            />
                                        </div>
                                    </template>
                                    <div class="d-flex flex-row mt-2">
                                        <div>
                                            <v-btn
                                                light
                                                @click="$emit('addBreak', { 
                                                        isDefault: selectedActionData.is_default,
                                                        day: selectedActionData.day,
                                                        date: selectedActionData.is_default ? '' : currentDateData.date,
                                                    }
                                                )"
                                            >
                                                Dodaj przerwę
                                            </v-btn>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-expansion-panels>
                <div
                    class="d-flex flex-row mt-2"
                >
                    <div v-if="!selectedActionData.is_default" class="">
                        <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                                <v-icon
                                    dark
                                    v-bind="attrs"
                                    v-on="on"
                                >mdi-plus-circle</v-icon>
                            </template>
                            <span>Dodaj dzień</span>
                        </v-tooltip>
                    </div>
                    <div class="mt-2">
                        <v-btn>
                            Zapisz zmiany
                            <v-icon
                                color=""
                            >
                                mdi-content-save
                            </v-icon>

                        </v-btn>
                    </div>
                </div>
            </div>
        </v-col>
    </v-row>
    </v-dialog>
</template>

<script>
    import { formatDate } from '../../../../utils/formatDate';
    import { AUTH_API } from '../../../authorization/AuthAPI';
    
    export default {
        name: "",
        components: {
            
        },
        emits: [ "closeEditAction", "addBreak", "editAvailabilityProp", "deleteBreak" ],
        inject: ["screenSize"],
        props: {
            showEditAction: { type: Boolean, default: false },
            selectedActionData: { type: Object, default: () => ({}) }
        },
        data: () => ({
            showDatePickerMenu: false
        }),
        computed: {
            panel: {
                get: function (){
                    if(this.selectedActionData.is_default) return 0;
                    return undefined;
                },
                set: function (value){
                    return value
                }
            }
        },
        methods: {
            formatDate(date){
                return formatDate(date)
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