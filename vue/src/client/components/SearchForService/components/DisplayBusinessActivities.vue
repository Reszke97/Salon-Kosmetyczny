<template>
    <v-row 
        style="color: white"
    >
        <v-col
            v-for="(item, key) of items"
            :key="key"
            :cols="6"
        >
            <div>
                aaaa
            </div>
            <!-- <v-expansion-panels 
                dark 
                class="accordion-wrapper"
            >
                <v-expansion-panel
                    style="background-color:#3f51b5;"
                >
                    <v-expansion-panel-header>
                    <h2>Filtry</h2>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels> -->
        </v-col>
    </v-row>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI";
    
    export default {
        name: "",
        components: {
            
        },
        props: {
            items: { type: Object, required: true }
        },
        data: () => ({
            
        }),
        computed: {
            
        },
        methods: {
            
        }
    }
</script>