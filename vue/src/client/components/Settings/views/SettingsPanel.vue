<template>
     <v-row
        style="
            height:100%
        "
        align="center"
        justify="center"
    >
        <v-col
            class="indigo"
            cols="12"
            sm="10"
            md="8"
            lg="6"
            style="
                height:100%;
            "
        >
            <v-toolbar flat
                class="indigo"
                id="my-tab"
                style="
                    min-height:112px!important
                "
            >
                <v-spacer></v-spacer>

                <template v-slot:extension>
                    <v-tabs
                        class="indigo"
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
                            Dane osobowe
                            <v-icon>mdi-account </v-icon>
                        </v-tab>

                        <v-tab
                            href="#tab-2"
                            class="primary--text px-3"
                            style="width:100%;"
                        >
                            Zmiana Hasła
                            <v-icon>mdi-lock-alert </v-icon>
                        </v-tab>
                    </v-tabs>
                </template>
            </v-toolbar>

            <v-tabs-items
                class="primary--text indigo" 
                v-model="tabs"
                style="
                    height: calc(100% - 112px);
                "
            >
                <v-tab-item
                    :value="'tab-1'"
                    style="height:100%"
                >
                    <UserInfo />
                </v-tab-item>

                <v-tab-item
                    :value="'tab-2'"
                    style="height:100%"
                >
                    <PasswordChange />
                </v-tab-item>
            </v-tabs-items>
        </v-col>
    </v-row>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI"
    import UserInfo from "../components/UserInfo.vue"
    import PasswordChange from "../components/PasswordChange.vue"
    
    export default {
        name: "",
        components: {
            UserInfo,
            PasswordChange
        },
        props: {
            
        },
        data: () => ({
            tabs: null,
            text: ` 
            `,
        }),
        computed: {
            
        },
        methods: {
            
        }
    }
</script>