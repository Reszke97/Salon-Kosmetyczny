<template>
    <v-row
        :style="{
            height: screenSize.screenHeight + 'px',
            paddingTop: '8px',
            paddingBottom: '8px',
        }"
        justify="center"
    >
        <v-col 
            id="appointment"
            cols="11"
            sm="9"
            md="6"
            lg="5" 
            :style="{
                backgroundColor:'#3f51b5',
                height: '100%'
            }"
        >
            <v-row 
                v-if="!started"
                style="color: white"
            >
                <v-col>
                    <h2>
                        Zapis na wizytę do specjalisty
                    </h2>
                    <p style="text-align: justify;">
                        <span>
                            Tutaj znajdziesz informację o firmię, usługach i jej pracownikach, z możliwością zapisu się na wizytę do wybranego specjalisty.
                        </span>
                        <span>
                            Kliknij w guzik <b>"Rozpocznij"</b> aby rozpocząć wyszykiwanie.
                        </span>
                    </p>
                    <v-btn 
                        class="my-2 mx-2"
                        color="success"
                        @click="openLocalizationDialog"
                    >
                        Rozpocznij
                    </v-btn>
                </v-col>
            </v-row>
            <template v-else>
                <v-expansion-panels 
                    v-model="panel"
                    dark 
                    class="accordion-wrapper"
                    id="filters"
                >
                    <v-expansion-panel
                        style="background-color:#3f51b5;"
                    >
                        <v-expansion-panel-header>
                        <h2>Filtry</h2>
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                            <v-row style="min-height:95px" >
                                <v-col :cols="4">
                                    <v-text-field
                                        dark
                                        v-model="inputVariables.selectedSpec"
                                        :menu-props="{ maxHeight: '400' }"
                                        label="Kogo szukasz?"
                                        hint="Podaj nazwę zawodu"
                                        persistent-hint
                                    ></v-text-field>
                                </v-col>
                                <v-col :cols="4">
                                    <v-text-field
                                        dark
                                        v-model="inputVariables.selectedService"
                                        :menu-props="{ maxHeight: '400' }"
                                        label="Szukana usługa"
                                        hint="Podaj nazwę usługi"
                                        persistent-hint
                                    ></v-text-field>
                                </v-col>
                                <v-col :cols="4">
                                    <v-text-field
                                        dark
                                        v-model="inputVariables.selectedBEntity"
                                        :menu-props="{ maxHeight: '400' }"
                                        label="Nazwa Salonu"
                                        hint="Podaj nazwę salonu"
                                        persistent-hint
                                    ></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row style="min-height:95px; align-items: center;">
                                <v-col :cols="4">
                                    <v-text-field
                                        dark
                                        v-model="inputVariables.selectedCity"
                                        :menu-props="{ maxHeight: '400' }"
                                        label="Miejscowość"
                                        hint="Podaj nazwę miejscowości"
                                        persistent-hint
                                        disabled
                                    ></v-text-field>
                                </v-col>
                                <v-col :cols="4">
                                    <v-text-field
                                        dark
                                        v-model="inputVariables.selectedPostCode"
                                        :menu-props="{ maxHeight: '400' }"
                                        label="Kod Pocztowy"
                                        hint="Podaj kod pocztowy"
                                        persistent-hint
                                        disabled
                                    ></v-text-field>
                                </v-col>
                                <div id="edit-loc" class="mx-2">
                                    <v-tooltip bottom color="success">
                                        <template v-slot:activator="{ on, attrs }">
                                            <v-icon
                                                dark
                                                right
                                                v-bind="attrs"
                                                v-on="on"
                                                @click="openLocalizationDialog"
                                            >
                                                mdi-pencil
                                            </v-icon>
                                        </template>
                                        <span>Edytuj Lokalizację</span>
                                    </v-tooltip>
                                </div>
                            </v-row>
                            <v-row style="min-height:95px">
                                <v-col>
                                    <v-btn 
                                        class="my-2 mx-2"
                                        color="success"
                                        @click="getBusinessActivities"
                                    >
                                        <v-icon>mdi-magnify</v-icon> Wyszukaj
                                    </v-btn>
                                </v-col>
                            </v-row>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-expansion-panels>
                <!-- here -->
                <display-business-activities
                    :items="items"
                    :businessesHeight="businessesHeight"
                />
            </template>
        </v-col>
        <ChooseLocalization
            :input-variables="inputVariables"
            :container-height="containerHeight"
            :container-width="containerWidth"
            :choose-localization-dialog-open="chooseLocalizationDialogOpen"
            :close-localization-dialog="closeLocalizationDialog"
            :set-input-variable="setInputVariable"
            :set-started="setStarted"
            :get-business-activities="getBusinessActivities"
        />
    </v-row>
</template>

<script>
    import axios from "axios"
    import { appendMimeType } from "../../../utils"
    import { ChooseLocalization, DisplayBusinessActivities } from "../components"
    
    export default {
        name: "AllBusinesses",
        components: {
            ChooseLocalization,
            DisplayBusinessActivities,
        },
        props: {
            
        },
        data: () => ({
            items: {},
            inputVariables: {
                selectedSpec: "",
                selectedService: "",
                selectedBEntity: "",
                selectedCity: "",
                selectedPostCode: "",
            },
            containerHeight: 0,
            containerWidth: 0,
            businessesHeight: 0,
            chooseLocalizationDialogOpen: false,
            started: false,
            panel: 0
        }),
        inject: ["screenSize"],
        computed: {
            filteredItems(){

            },
        },

        async created(){

        },
        
        mounted(){
            this.$nextTick(() => {
                this.watchScreenHeightResize()
                this.watchScreenWidthResize()
            })
        },

        computed: {
        },

        methods: {
            watchScreenHeightResize() {
                const observer = new ResizeObserver((entries) => {
                    this.containerHeight = document.getElementById("appointment").offsetHeight;
                    if(this.started){
                        this.businessesHeight = this.screenSize.screenHeight - document.getElementById("filters").offsetHeight - 40;
                    } else this.businessesHeight = this.screenSize.screenHeight;
                });
                observer.observe(document.getElementById("appointment"));
            },
            watchScreenWidthResize() {
                const observer = new ResizeObserver((entries) => {
                    this.containerWidth = document.getElementById("appointment").offsetWidth
                });
                observer.observe(document.getElementById("appointment"));
            },
            closeLocalizationDialog(){
                this.chooseLocalizationDialogOpen = false;
            },
            openLocalizationDialog(){
                this.chooseLocalizationDialogOpen = true;
            },
            setInputVariable({ key, val }){
                this.inputVariables[key] = val;
            },
            setStarted(){
                this.started = !this.started;
                this.$nextTick(() => {
                    if(this.started){
                        this.businessesHeight = this.screenSize.screenHeight - document.getElementById("filters").offsetHeight - 40;
                    }
                })
            },
            async getBusinessActivities(){
                await axios.get('http://127.0.0.1:8000/api/v1/client/business-activities/')
                .then(res => {
                    Object.keys(res.data).forEach(bActivity => {
                        Object.keys(res.data[bActivity]).forEach(el => {
                            if(el == "image"){
                                res.data[bActivity].image = appendMimeType(res.data[bActivity].image)
                            } else if(el == "categories"){
                                Object.keys(res.data[bActivity].categories).forEach(category => {
                                    res.data[bActivity].categories[category].forEach((item, idx) => {
                                        item.employees.forEach((emp, jdx) => {
                                            res.data[bActivity]["categories"][category][idx]["employees"][jdx].avatar = appendMimeType(
                                                res.data[bActivity]["categories"][category][idx]["employees"][jdx].avatar
                                            )
                                        })
                                    })
                                })
                            }
                        })
                    })
                    this.items = res.data
                })
            },
        }
    }
</script>

<style>
    .search .v-input__slot {
        /* background: white!important; */
    }
    #edit-loc i:hover{
        cursor: pointer;
    }
</style>