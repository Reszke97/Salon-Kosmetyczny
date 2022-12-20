<template>
    <div style="display: flex; justify-content: end; width:100%">
        <div
            style="
                display: flex;
                justify-content: end;
            "
        >
            <div
                class="mr-15"
                :style="`
                    display: flex;
                    flex-direction: ${screenSize.screenWidth <= 400 ? 'column' : 'row'}
                `"
            >
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-chip
                            style=" background: rgb(8, 68, 164)!important;"
                            class="ma-2"
                            color="primary"
                            @click="setTab('tab-1')"
                            v-bind="attrs"
                            v-on="on"
                        >
                            <v-icon left>
                                mdi-keyboard-backspace 
                            </v-icon>
                            Powrót
                        </v-chip>
                    </template>
                    <span>Powrót</span>
                </v-tooltip>
            </div>
        </div>
    </div>
</template>

<script>
    
    export default {
        name: "",
        components: {},
        props: {
            setTab: { type: Function, required: true }
        },
        data: () => ({}),
        inject: ["screenSize"],
    }
</script>