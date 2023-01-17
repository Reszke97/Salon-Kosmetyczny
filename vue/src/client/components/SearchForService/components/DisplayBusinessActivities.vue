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
                <div style="display: flex">
                    <div style="display: flex">
                        {{ `${item.city} ${item.post_code}` }}
                    </div>
                    <div class="mx-2" style="display: flex">
                        {{ `ul. ${item.street} ${item.house_number}` }}
                    </div>
                    
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
                            <div
                                v-for="(item, jdx) of category"
                                :key="jdx"
                                style="display: flex; flex-direction: column"
                            >
                                <h4>{{ item.service_name }}</h4>
                                <span>{{ `Czas trwania - ${item.duration} min` }}</span>
                                <span>{{ `Cena - ${item.price} PLN` }}</span>
                                <div
                                    style="display: flex; flex-direction: row"
                                >
                                    <div style="display: flex; width:100%; color: orange">
                                        Umów wizytę
                                    </div>
                                    <div style="display: flex; width:100%; justify-content: end;">
                                        <v-icon
                                            dark
                                            right
                                        >
                                            mdi-plus
                                        </v-icon>
                                    </div>
                                </div>
                                <v-divider dark class="my-2" />
                            </div>
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