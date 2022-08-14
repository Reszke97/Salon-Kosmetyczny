<template>
    <v-row
        style="
            height:100%
        "
        align="center"
        justify="center"
    >
        <v-col
            cols="12"
            sm="10"
            md="8"
            lg="6"
            style="
                height:100%;
                background-color:#3f51b5;
            "
        >
            <v-toolbar flat
                id="my-tab"
                style="
                    min-height:112px!important;
                    background-color:#3f51b5;
                "
            >
                <v-spacer></v-spacer>

                <template v-slot:extension>
                    <v-tabs
                        v-model="tabs"
                        centered
                        icons-and-text
                    >
                        <v-tabs-slider ></v-tabs-slider>
                        <v-tab
                            href="#tab-1"
                            class="primary--text px-3"
                            style="width:100%;"
                        >
                            Dodaj usługę
                            <v-icon>mdi-phone</v-icon>
                        </v-tab>

                        <v-tab
                            href="#tab-2"
                            class="primary--text px-3"
                            style="width:100%;"
                        >
                            Lista usług
                            <v-icon>mdi-heart</v-icon>
                        </v-tab>
                        <v-tab
                            href="#tab-3"
                            class="primary--text px-3"
                            style="width:100%;"
                        >
                            Nearby
                            <v-icon>mdi-account-box</v-icon>
                        </v-tab>
                    </v-tabs>
                </template>
            </v-toolbar>

            <v-tabs-items 
                v-model="tabs"
                style="
                    height: calc(100% - 112px);
                    background-color:#3f51b5!important
                "
            >
                <v-tab-item
                    :value="'tab-1'"
                    style="height:100%"
                >
                    <add-new-service />
                </v-tab-item>

                <v-tab-item
                    :value="'tab-2'"
                    style="height:100%"
                >
                    <get-services
                        :services="services"
                    />
                </v-tab-item>
                <v-tab-item
                    :value="'tab-3'"
                    style="height:100%"
                >
                </v-tab-item>
            </v-tabs-items>
        </v-col>
    </v-row>
</template>

<script>
    import AddNewService from "../components/AddNewService.vue"
    import GetServices from "../components/GetServices.vue"
    import { AUTH_API } from "../../../authorization/AuthAPI";

    export default {
        name: "Service",
        props: {

        },
        components: {
            AddNewService,
            GetServices
        },
        data: () => ({
            tabs: null,
            services: []
        }),
        async created(){
            setTimeout( async () => {
                const API = await AUTH_API();
                API.get("/api/v1/employee/getemployeeservices/")
                .then(res => {
                    this.services = res.data
                })
            }, 100)
        },
    }
</script>

<style>
    /* #my-tab .v-toolbar__extension .v-tabs .v-item-group .v-slide-group__prev{
        display: none!important;
    }
    #my-tab .v-toolbar__extension .v-tabs .v-item-group .v-slide-group__wrapper .v-slide-group__content{
        flex: 0!important;
    }
    #my-tab .v-toolbar__extension .v-tabs .v-item-group .v-slide-group__wrapper{
        justify-content: center;
    } */
</style>