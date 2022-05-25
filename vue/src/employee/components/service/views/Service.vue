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
                background-color:#BFD7ED;
            "
        >
            <v-toolbar flat
                id="my-tab"
                style="
                    min-height:112px!important
                "
            >
                <!-- <v-app-bar-nav-icon></v-app-bar-nav-icon> -->

                <!-- <v-toolbar-title
                    v-if="tabs === "
                >
                    Twoje usługi
                </v-toolbar-title>
                <v-toolbar-title
                    v-else-if="tabs === "
                >
                    Twoje usługi
                </v-toolbar-title>
                <v-toolbar-title
                    v-else="tabs === "
                >
                    Twoje usługi
                </v-toolbar-title> -->

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
                            Recents
                            <v-icon>mdi-phone</v-icon>
                        </v-tab>

                        <v-tab
                            href="#tab-2"
                            class="primary--text px-3"
                            style="width:100%;"
                        >
                            Favorites
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
                "
            >
                <v-tab-item
                    :value="'tab-1'"
                    style="height:100%"
                >
                    <div>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip 
                        ex ea commodo consequat. Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip 
                        ex ea commodo consequat.Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip 
                    </div>
                </v-tab-item>

                <v-tab-item
                    :value="'tab-2'"
                    style="height:100%"
                >
                    <div>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip 
                        ex ea commodo consequat. Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip 
                        ex ea commodo consequat.Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip 
                    </div>
                </v-tab-item>
                <v-tab-item
                    :value="'tab-3'"
                    style="height:100%"
                >
                    <div>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip 
                        ex ea commodo consequat. Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip 
                        ex ea commodo consequat.Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip 
                    </div>
                </v-tab-item>
            </v-tabs-items>
        </v-col>
    </v-row>
</template>

<script>
    export default {
        name: "Service",
        props: {

        },
        data: () => ({
            tabs: null,
            text: `
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip 
                ex ea commodo consequat. Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
            `,
        })
    }
</script>

<style>
    #my-tab .v-toolbar__extension .v-tabs .v-item-group .v-slide-group__prev{
        display: none!important;
    }
    #my-tab .v-toolbar__extension .v-tabs .v-item-group .v-slide-group__wrapper .v-slide-group__content{
        flex: 0!important;
    }
    #my-tab .v-toolbar__extension .v-tabs .v-item-group .v-slide-group__wrapper{
        justify-content: center;
    }
</style>