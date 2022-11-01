<template>
    <div>
        <v-row class="my-2">
            <v-col cols="12">
                <v-expansion-panels dark class="accordion-wrapper">
                    <v-expansion-panel
                        v-for="service of services"
                        :key="service.service.id"
                    >
                        <v-expansion-panel-header>
                            <h2>Usługa {{ service.service.name }}</h2>
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                            <p><b>Czas Trwania: </b>{{ service.service.duration }}</p>
                            <p><b>Cena: </b>{{ service.service.price }}</p>
                            <v-btn
                                color="red lighten-2"
                                dark
                                @click="OpenDialog"
                            >
                                Edytuj
                            </v-btn>
                            <v-row
                                v-if="openDialog"
                                justify="end"
                            >
                                <v-col cols=2>
                                    <v-dialog
                                        class="serviceDialog"
                                        id="serviceDialog"
                                        v-model="openDialog"
                                        width="50vw"
                                        style="min-height:350px!important"
                                    >
                                        <add-or-update-service
                                            ref="editDialog"
                                            min-height="400px"
                                            :preview="true"
                                            :service-to-edit="service"
                                            :get-services="getServices"
                                        >
                                            <template #closeDialog>
                                                <v-btn
                                                    dark
                                                    @click="closeDialog"
                                                    class="mr-2"
                                                >
                                                    Zamknij
                                                </v-btn>
                                            </template>
                                        </add-or-update-service>
                                    </v-dialog>
                                </v-col>
                            </v-row>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-expansion-panels>
            </v-col>
        </v-row>
    </div>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI";
    import AddOrUpdateService from './AddOrUpdateService.vue';
    
    export default {
        name: "",
        components: {
            AddOrUpdateService
        },
        props: {
            services: {
                type: Array,
                default: () => ([])
            },
            getServices: {
                type: Function,
                required: true
            },
        },
        data: () => ({
            openDialog: false
        }),
        computed: {
            
        },
        
        methods: {
            async closeDialog(){
                this.openDialog = false;
                await this.getServices();
            },
            async OpenDialog(){
                this.openDialog = true;
                this.$nextTick( async () => {
                    await this.$refs.editDialog[0].displayImages();
                })
            },
        },
    }
</script>

<style>
    @import "../../../../styles/globalStyles.css";
    .accordion-wrapper .v-expansion-panel {
        background-color: #0844a4!important;
        color: red;
    }
    .v-window__container {
        height: 100%!important;
    }
</style>