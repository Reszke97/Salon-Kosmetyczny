<template>
    <v-row
        style="height:100%"
        justify="center"
    >
        <v-col :cols="8">
            <v-row style="background-color:#3f51b5;" >
                <v-col :cols="4">
                    <v-text-field
                        dark
                        v-model="selectedEmployee"
                        :menu-props="{ maxHeight: '400' }"
                        label="Kogo szukasz?"
                        hint="Pick your favorite states"
                        persistent-hint
                    ></v-text-field>
                </v-col>
                <v-col :cols="4">
                    <v-text-field
                        dark
                        v-model="selectedEmployee"
                        :menu-props="{ maxHeight: '400' }"
                        label="Miejscowość?"
                        hint="Pick your favorite states"
                        persistent-hint
                    ></v-text-field>
                </v-col>
                <v-col :cols="4">
                    <v-text-field
                        dark
                        v-model="selectedEmployee"
                        :menu-props="{ maxHeight: '400' }"
                        label="Kod Pocztowy"
                        hint="Pick your favorite states"
                        persistent-hint
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-row style="background-color:#3f51b5;">
                <v-col :cols="4">
                    <v-text-field
                        dark
                        v-model="selectedEmployee"
                        :menu-props="{ maxHeight: '400' }"
                        label="Kogo szukasz?"
                        hint="Pick your favorite states"
                        persistent-hint
                    ></v-text-field>
                </v-col>
                <v-col :cols="4">
                    <v-text-field
                        dark
                        v-model="selectedEmployee"
                        :menu-props="{ maxHeight: '400' }"
                        label="Miejscowość?"
                        hint="Pick your favorite states"
                        persistent-hint
                    ></v-text-field>
                </v-col>
                <v-col :cols="4">
                    <v-text-field
                        dark
                        v-model="selectedEmployee"
                        :menu-props="{ maxHeight: '400' }"
                        label="Miejscowość?"
                        hint="Pick your favorite states"
                        persistent-hint
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-row style="height:60%">
                <v-col :cols="12">

                </v-col>
            </v-row>
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
    import { AUTH_API } from "../../../authorization/AuthAPI";
    import { filters } from "../utils"
    import { About } from "../components"
    
    export default {
        name: "",
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
            filters: filters()
        }),
        computed: {
            filteredItems(){

            },
        },
        methods: {
            
        }
    }
</script>

<style>
    .search .v-input__slot {
        /* background: white!important; */
    }
</style>