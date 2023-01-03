<template>
    <v-row
        style="height:100%"
        justify="center"
    >
        <v-col 
            cols="11"
            sm="9"
            md="6"
            lg="5" 
            style="background-color:#3f51b5;"
        >
            <v-row style="min-height:95px" >
                <v-col :cols="4">
                    <v-text-field
                        dark
                        v-model="selectedEmployee"
                        :menu-props="{ maxHeight: '400' }"
                        label="Kogo szukasz?"
                        hint="Podaj nazwę zawodu"
                        persistent-hint
                    ></v-text-field>
                </v-col>
                <v-col :cols="4">
                    <v-text-field
                        dark
                        v-model="selectedEmployee"
                        :menu-props="{ maxHeight: '400' }"
                        label="Miejscowość"
                        hint="Podaj nazwę miejscowości"
                        persistent-hint
                    ></v-text-field>
                </v-col>
                <v-col :cols="4">
                    <v-text-field
                        dark
                        v-model="selectedEmployee"
                        :menu-props="{ maxHeight: '400' }"
                        label="Kod Pocztowy"
                        hint="Podaj kod pocztowy"
                        persistent-hint
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-row style="min-height:95px">
                <v-col :cols="4">
                    <v-text-field
                        dark
                        v-model="selectedEmployee"
                        :menu-props="{ maxHeight: '400' }"
                        label="Szukana usługa"
                        hint="Podaj nazwę usługi"
                        persistent-hint
                    ></v-text-field>
                </v-col>
                <v-col :cols="4">
                    <v-text-field
                        dark
                        v-model="selectedEmployee"
                        :menu-props="{ maxHeight: '400' }"
                        label="Nazwa Salonu"
                        hint="Podaj nazwę salonu"
                        persistent-hint
                    ></v-text-field>
                </v-col>
                <v-col :cols="4">
                    
                </v-col>
            </v-row>
            <v-row>
                <v-col :cols="12">
                    <p>
                        map longititude - {{ mapCoordinates.lng }}
                    </p>
                    <p>
                        map latitude - {{ mapCoordinates.lat }}
                    </p>
                    <p>
                    my longititude - {{ coordinates.lng }}
                    </p>
                    <p>
                        my latitude - {{ coordinates.lat }}
                    </p>
                    <v-btn
                        @click="geocode"
                    >
                        Click
                    </v-btn>
                    <GmapMap
                        :center="coordinates"
                        :zoom="7"
                        style="height:360px"
                        ref="gMap"
                    >
                        <GmapMarker
                            :position="coordinates"
                            :clickable="true"
                            @click="center=m.position"
                        />
                    </GmapMap>
                </v-col>
            </v-row>
            <!-- <v-row style="height:calc(100% - 240px)">
                <v-col :cols="12" >

                </v-col>
            </v-row>
            <v-row 
                style="min-height:50px"
            >
                <v-col 
                    :cols="12"
                    class="d-flex justify-end"
                >
                    <v-btn
                        color="primary"
                    >
                        Szukaj
                    </v-btn>
                </v-col>
            </v-row> -->
        </v-col>
    </v-row>
</template>
<!-- <v-col :cols="4" style="height:80px" class="search">
                    <v-text-field
                        dark
                        style="background-color:"
                        v-model="searchPhrase"
                        label="Szukaj"
                        outlined
                        append-icon="mdi-magnify"
                    ></v-text-field>
                </v-col> -->

<script>
    import axios from "axios"
    import { AUTH_API } from "../../../authorization/AuthAPI";
    import { filters } from "../utils"
    import { About } from "../components"
    import { gmapApi } from 'vue2-google-maps'
    
    export default {
        name: "Appointment",
        components: {
            About
        },
        props: {
            
        },
        data: () => ({
            items: [{}],
            searchPhrase: "",
            selectedFilters: filters(),
            selectedEmployee: "",
            filters: filters(),
            map: null,
            geoCoded: null,
            coordinates: {
                lat: 57.9023,
                lng: 98.9122,
            }
        }),
        computed: {
            filteredItems(){

            },
        },

        async created(){
            if(
                this.$store.state.allBusinessActivities.length < 1 
                || this.$store.state.distinctServices.length < 1
                || this.$store.state.distinctEmployeeSpecs.length < 1
            ){
                this.$store.dispatch('getBusinessActivitesAndServices')
            }
            // await this.getUserLocation();
        },
        
        mounted(){
            this.$nextTick(() => {
                //Wywołuje watcher, który nasłuchuje zmiany współrzędnych przy wykorzystaniu computed: mapCoordinates
                this.$refs.gMap.$mapPromise.then(map => this.map = map);
            })
        },

        computed: {
            mapCoordinates(){
                if(!this.map){
                    return {
                        lat: 0,
                        lng: 0,
                    }
                }
                return {
                    lat: this.map.getCenter().lat().toFixed(4),
                    lng:this.map.getCenter().lng().toFixed(4),
                }
            },
            google: gmapApi
        },

        methods: {
            async getUserLocation(){
                this.$getLocation({})
                .then(coordinates => {
                    this.coordinates = coordinates;
                })
                .catch(() => {
                    alert("no access to localization")
                });
            },
            async geocode(){
                const self = this;
                const geocoder = new this.google.maps.Geocoder();
                geocoder.geocode( { 'address': "Wejherowo"}, function(results, status) {
                    if (status == 'OK') {
                        self.coordinates.lat = results[0].geometry.location.lat()
                        self.coordinates.lng = results[0].geometry.location.lng()
                    } else {
                        alert('Geocode was not successful for the following reason: ' + status);
                    }
                });
            }
        }
    }
</script>

<style>
    .search .v-input__slot {
        /* background: white!important; */
    }
</style>