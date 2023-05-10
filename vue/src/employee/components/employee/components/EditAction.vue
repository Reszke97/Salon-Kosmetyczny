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
                <v-form
                    ref="form"
                    v-model="valid"
                    lazy-validation
                >
                    <v-expansion-panels dark class="accordion-wrapper"
                        v-model="panel"
                    >
                        <v-expansion-panel
                            v-for="(currentDateData, panelIdx) of selectedActionData.data"
                            :key="panelIdx"
                        >
                            <v-expansion-panel-header>
                                <template #actions>
                                    <div>
                                        <v-tooltip bottom>
                                            <template v-slot:activator="{ on, attrs }">
                                                <v-icon
                                                    dark
                                                    v-bind="attrs"
                                                    v-on="on"
                                                >
                                                    mdi-menu-down
                                                </v-icon>
                                            </template>
                                            <span>{{ `${panel === panelIdx ? "Zwiń" : "Rozwiń"}` }}</span>
                                        </v-tooltip>
                                    </div>
                                </template>
                                <div class="d-flex">
                                    <div class="w-100">
                                        <v-menu
                                            ref="menu"
                                                :close-on-content-click="false"
                                                transition="scale-transition"
                                                offset-y
                                                max-width="290px"
                                                min-width="auto"
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
                                                @change="val => $emit('editAvailabilityProp', {
                                                    value: val,
                                                    day: selectedActionData.day,
                                                    isDefault: selectedActionData.is_default,
                                                    date: val,
                                                    prop: 'date',
                                                    eventType: '',
                                                    eventIdx: null,
                                                    extraDateIdx: panelIdx,
                                                })"
                                            ></v-date-picker>
                                        </v-menu>
                                    </div>
                                    <div 
                                        v-if="!!!selectedActionData.is_default"
                                        class="pt-6 mr-3"
                                    >
                                        <v-tooltip bottom>
                                            <template v-slot:activator="{ on, attrs }">
                                                <v-icon
                                                    color="red"
                                                    dark
                                                    v-bind="attrs"
                                                    v-on="on"
                                                    @click="$emit('deleteDay', { day:selectedActionData.day, extraDateIdx: panelIdx })"
                                                >
                                                    mdi-trash-can
                                                </v-icon>
                                            </template>
                                            <span>Usuń dzień</span>
                                        </v-tooltip>
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
                                            :input-value="currentDateData.is_free"
                                            label="Wolne"
                                            @change="val => $emit('editAvailabilityProp', {
                                                value: val,
                                                day: selectedActionData.day,
                                                isDefault: selectedActionData.is_default,
                                                date: selectedActionData.is_default ? '' : currentDateData.date,
                                                prop: 'is_free',
                                                eventType: '',
                                                eventIdx: null,
                                                extraDateIdx: selectedActionData.isDefault ? null : panelIdx,
                                            })"
                                        />
                                    </div>
                                </div>
                                <template v-if="!!!currentDateData.is_free">
                                    <div
                                        v-for="(item, idx) of currentDateData.work_hours"
                                    >
                                        <v-text-field
                                            :value="item.start_time"
                                            label="Godzina rozpoczęcia"
                                            type="time"
                                            dark
                                            required
                                            :rules="[...startHourRules]"
                                            @input="val => $emit('editAvailabilityProp', {
                                                value: val,
                                                day: selectedActionData.day,
                                                isDefault: selectedActionData.is_default,
                                                date: selectedActionData.is_default ? '' : currentDateData.date,
                                                prop: 'start_time',
                                                eventType: 'work_hours',
                                                eventIdx: idx,
                                                extraDateIdx: selectedActionData.is_default ? null : panelIdx
                                            })"
                                        />
                                        <v-text-field
                                            :value="item.end_time"
                                            label="Godzina zakończenia"
                                            type="time"
                                            dark
                                            required
                                            :rules="[
                                                ...endHourRules, 
                                                (item.end_time > item.start_time) || 'Godzina zakończenia musi być większa od godziny rozpoczęcia']
                                            "
                                            @input="val => $emit('editAvailabilityProp', {
                                                value: val,
                                                day: selectedActionData.day,
                                                isDefault: selectedActionData.is_default,
                                                date: selectedActionData.is_default ? '' : currentDateData.date,
                                                prop: 'end_time',
                                                eventType: 'work_hours',
                                                eventIdx: idx,
                                                extraDateIdx: selectedActionData.is_default ? null : panelIdx
                                            })"
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
                                                                        eventIdx: idx,
                                                                        extraDateIdx: selectedActionData.is_default ? null : panelIdx
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
                                                    required
                                                    :rules="[...startHourRules]"
                                                    type="time"
                                                    @input="val => $emit('editAvailabilityProp', {
                                                        value: val,
                                                        day: selectedActionData.day,
                                                        isDefault: selectedActionData.is_default,
                                                        date: selectedActionData.is_default ? '' : currentDateData.date,
                                                        prop: 'start_time',
                                                        eventType: 'breaks',
                                                        eventIdx: idx,
                                                        extraDateIdx: selectedActionData.is_default ? null : panelIdx
                                                    })"
                                                />
                                                <v-text-field
                                                    :value="item.end_time"
                                                    label="Godzina zakończenia"
                                                    type="time"
                                                    dark
                                                    required
                                                    :rules="[
                                                        ...endHourRules, 
                                                        (item.end_time > item.start_time) || 'Godzina zakończenia musi być większa od godziny rozpoczęcia']
                                                    "
                                                    @input="val => $emit('editAvailabilityProp', {
                                                        value: val,
                                                        day: selectedActionData.day,
                                                        isDefault: selectedActionData.is_default,
                                                        date: selectedActionData.is_default ? '' : currentDateData.date,
                                                        prop: 'end_time',
                                                        eventType: 'breaks',
                                                        eventIdx: idx,
                                                        extraDateIdx: selectedActionData.is_default ? null : panelIdx
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
                                                            extraDateIdx: selectedActionData.is_default ? null : panelIdx,
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
                </v-form>
                <div
                    class="d-flex flex-row mt-3"
                >
                    <div v-if="!selectedActionData.is_default" class="">
                        <v-btn
                            @click="$emit('addExtraDay', { day: selectedActionData.day })"
                        >
                            Dodaj dzień
                            <v-icon
                                dark
                                right
                            >
                                mdi-plus-circle
                            </v-icon>
                        </v-btn>
                    </div>
                    <div class="ml-2">
                        <v-btn
                            :disabled="!valid"
                        >
                            Zapisz
                            <v-icon
                                color=""
                                right
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
    
    export default {
        name: "",
        components: {
            
        },
        emits: [ "closeEditAction", "addBreak", "editAvailabilityProp", "deleteBreak", "addExtraDay", "deleteDay" ],
        inject: ["screenSize"],
        props: {
            showEditAction: { type: Boolean, default: false },
            selectedActionData: { type: Object, default: () => ({}) }
        },
        data: () => ({
            showDatePickerMenu: false,
            panel: undefined,
            startHourRules: [
                v => !!v || 'Godzina rozpoczęcia jest wymagana'
            ],
            endHourRules: [
                v => !!v || 'Godzina zakończenia jest wymagana'
            ],
            valid: true,
        }),
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