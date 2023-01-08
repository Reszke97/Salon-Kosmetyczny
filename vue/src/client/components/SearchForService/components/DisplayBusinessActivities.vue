<template>
    <v-row 
        :style="{
            color: 'white', 
            overflow: 'auto', 
            height: businessesHeight + 'px'
        }"
        class="mt-2"
    >
        <v-col
            v-for="(item, key) in items"
            :key="key"
            :cols="6"
        >
            <div
                style="
                    display: flex;
                    flex-direction: column;
                "
            >
                <div>
                    <h3>{{ key }}</h3>
                </div>
                <div
                    style="height:200px"
                    v-if="item.image.image"
                >
                    <img
                        :src="item.image.image"
                        style="max-height:200px; width: 100%"
                    />
                </div>
                <v-expansion-panels 
                    dark 
                    class="accordion-wrapper"
                >
                    <v-expansion-panel
                        v-for="(category, idx) of item.categories"
                        :key="idx"
                        style="background-color:#3f51b5;"
                    >
                        <v-expansion-panel-header>
                            <h3>{{idx}}</h3>
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-expansion-panels>
            </div>
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
            items: { type: Object, required: true },
            businessesHeight: { type: Number, default: 0 },
        },
        data: () => ({
            
        }),
        computed: {
            
        },
        methods: {
            
        }
    }
</script>