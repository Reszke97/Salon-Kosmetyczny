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
                <display-business-activities
                    :items="items"
                    :businessesHeight="businessesHeight"
                    :open-sign-up-for-visit-dialog="openSignUpForVisitDialog"
                    :preview-business-activity="previewBusinessActivity"
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
            :started="started"
        />
        <BusinessActivityPreview
            :business-activity-preview="businessActivityPreview"
            :business-activity-preview-data="businessActivityPreviewData"
            :close-preview="closePreview"
        />
        <SignUpForVisit
            v-if="signUpForVisitDialog"
            :sign-up-for-visit-dialog="signUpForVisitDialog"
            :close-sign-up-for-visit-dialog="closeSignUpForVisitDialog"
            :selected-service="selectedService"
            :component-dims="componentDims"
        />
    </v-row>
</template>

<script>
    import axios from "axios";
    import { appendMimeType } from "../../../utils";
    import { ChooseLocalization, DisplayBusinessActivities, SignUpForVisit } from "../components";
    import BusinessActivityPreview from "./BusinessActivityPreview.vue";
    
    export default {
        name: "AllBusinesses",
        components: {
            ChooseLocalization,
            DisplayBusinessActivities,
            BusinessActivityPreview,
            SignUpForVisit,
        },
        props: {
            
        },
        data: () => ({
            selectedService: {},
            signUpForVisitDialog: false,
            componentDims: {},
            items: {},
            inputVariables: {
                selectedSpec: "",
                selectedService: "",
                selectedBEntity: "",
                selectedCity: "",
                selectedPostCode: "",
            },
            servicesBoxWatcherSet: false,
            containerHeight: 0,
            containerWidth: 0,
            businessesHeight: 0,
            chooseLocalizationDialogOpen: false,
            started: false,
            panel: 0,
            businessActivityPreview: false,
            businessActivityPreviewData: {},
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
            openSignUpForVisitDialog(item){
                this.componentDims = {
                    height: `${document.getElementById('appointment').offsetHeight - 200}px`,
                    width: `${document.getElementById('appointment').offsetWidth}px`,
                }
                this.selectedService = item;
                this.signUpForVisitDialog = true;
            },
            closeSignUpForVisitDialog(){
                this.signUpForVisitDialog = false;
                this.selectedService = {};
                this.componentDims = {};
            },
            openPreview(){
                this.businessActivityPreview = true;
            },
            closePreview(){
                this.businessActivityPreview = false;
            },
            previewBusinessActivity(businessInfo){
                this.businessActivityPreviewData = { ...businessInfo };
                this.openPreview();
            },
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
                    if(this.started && !this.servicesBoxWatcherSet){
                        const observer = new ResizeObserver((entries) => {
                            this.businessesHeight = this.screenSize.screenHeight - document.getElementById("filters").offsetHeight - 40;
                        });
                        observer.observe(document.getElementById("filters"));
                    }
                })
            },
            async getBusinessActivities(){
                await axios.get(`http://127.0.0.1:8000/api/v1/client/business-activities/?selectedBEntity=${
                    this.inputVariables.selectedBEntity
                }&selectedCity=${
                    this.inputVariables.selectedCity
                }&selectedPostCode=${
                    this.inputVariables.selectedPostCode
                }&selectedService=${
                    this.inputVariables.selectedService
                }&selectedSpec=${
                    this.inputVariables.selectedSpec
                }`)
                .then(res => {
                    Object.keys(res.data).forEach(bActivity => {
                        Object.keys(res.data[bActivity]).forEach(el => {
                            if(el == "image"){
                                if(res.data[bActivity].image){
                                    res.data[bActivity].image = appendMimeType(res.data[bActivity].image)
                                }
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
                            } else if(el == "employees"){
                                res.data[bActivity][el].forEach((img, idx) => {
                                    res.data[bActivity][el][idx]["avatar"] = appendMimeType(
                                        img.avatar
                                    )
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