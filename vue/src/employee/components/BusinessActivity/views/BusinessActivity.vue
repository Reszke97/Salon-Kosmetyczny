<template>
    <v-row
        id="b-activity-main-container"
        style="
            height:100%
        "
        align="center"
        justify="center"
    >
        <v-col
            cols="12"
            sm="12"
            md="8"
            lg="6"
            style="
                height:100%;
                background-color:#3f51b5;
            "
        >
            <v-toolbar
                id="my-tab"
                flat
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
                            Edycja
                            <v-icon>mdi-phone</v-icon>
                        </v-tab>
                        <v-tab
                            href="#tab-2"
                            class="primary--text px-3"
                            style="width:100%;"
                        >
                            Podgląd
                            <v-icon>mdi-eye</v-icon>
                        </v-tab>
                        <v-tab
                            href="#tab-3"
                            class="primary--text px-3"
                            style="width:100%;"
                        >
                            Dodaj pracownika
                            <v-icon>mdi-phone</v-icon>
                        </v-tab>
                    </v-tabs>
                </template>
            </v-toolbar>

            <v-tabs-items 
                v-model="tabs"
                :style="`
                    height: ${tabs == 'tab-3' ? '100%' : 'calc(100% - 112px)'} ;
                    background-color:#3f51b5!important
                `"
            >
                <v-tab-item
                    :value="'tab-1'"
                    style="height:100%;overflow-y:auto;overflow-x:hidden"
                >
                    <edit
                        :get-business-activity-data="getBusinessActivityData"
                    >
                    </edit>
                </v-tab-item>

                <v-tab-item
                    :value="'tab-2'"
                    style="height:100%"
                >
                </v-tab-item>
                <v-tab-item
                    :value="'tab-3'"
                    id="tab-3"
                    style="height:100%;overflow:auto;"
                >
                    
                </v-tab-item>
            </v-tabs-items>
        </v-col>
    </v-row>
</template>

<script>
    import Edit from "../components/Edit.vue";
    import { AUTH_API } from "../../../authorization/AuthAPI";
    export default {
        name: "BusinessActivity",
        props: {

        },
        components: {
            Edit
        },
        data: () => ({
           tabs: null,
           businessActivity: {},
        }),
        provide(){
        },
        inject: ["screenSize"],
        methods: {
            async getBusinessActivityData(resolve){
                const API = await AUTH_API();
                await API.get("api/v1/employee/business-activity/")
                    .then(res => {
                        resolve(res.data)
                    })
           }
        },
    }
</script>

<style type="text/css">
</style>