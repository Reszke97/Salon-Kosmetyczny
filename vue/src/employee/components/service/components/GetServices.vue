<template>
    <div>
        <v-row class="my-2">
            <v-col cols="12">
                <v-expansion-panels dark class="accordion-wrapper">
                    <v-expansion-panel
                        v-for="service of services"
                        :key="service.id"
                    >
                    <v-expansion-panel-header>
                        {{ service.service.name }}
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                        <p><b>Czas Trwania: </b>{{ service.service.duration }}</p>
                        <p><b>Cena: </b>{{ service.service.price }}</p>
                    </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-expansion-panels>
            </v-col>
            
        </v-row>
    </div>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI";
    
    export default {
        name: "",
        components: {
            
        },
        props: {
            services: {
                type: Array,
                default: () => ([])
            }
        },
        data: () => ({
            
        }),
        computed: {
            
        },
        
        methods: {
            
        }
    }
</script>

<style>
    .accordion-wrapper .v-expansion-panel {
        background-color: #0844a4!important;
        color: red;
    }
</style>