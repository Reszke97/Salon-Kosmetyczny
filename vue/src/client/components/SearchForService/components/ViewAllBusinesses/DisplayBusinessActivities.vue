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
            v-for="(business, key) in items"
            :key="key"
            :cols="6"
            class="px-2"
        >
            <div
                style="
                    display: flex;
                    flex-direction: column;
                    border: solid;
                    border-radius: 10px;
                    border-color: rgb(8, 68, 164);
                    border-width: 3px;
                    padding: 10px;
                "
            >
                <div style="display: flex; flex-direction: row">
                    <div style="display: flex; width:100%">
                        <h3>{{ key }}</h3>
                    </div>
                    <div style="display: flex; width:100%; justify-content: end;">
                        <v-tooltip top color="success">
                            <template v-slot:activator="{ on, attrs }">
                                <v-icon
                                    dark
                                    right
                                    v-bind="attrs"
                                    v-on="on"
                                    @click="previewBusinessActivity(business)"
                                >
                                    mdi-information 
                                </v-icon>
                            </template>
                            <span>Szczegóły firmy</span>
                        </v-tooltip>
                    </div>
                </div>
                <div style="display: flex">
                    <div style="display: flex">
                        {{ `${business.city} ${business.post_code}` }}
                    </div>
                    <div class="mx-2" style="display: flex">
                        {{ `ul. ${business.street} ${business.house_number}` }}
                    </div>
                    
                </div>
                <div
                    style="height:200px"
                    v-if="business.image"
                >
                    <img
                        :src="business.image.image"
                        style="max-height:200px; width: 100%"
                    />
                </div>
                <v-expansion-panels 
                    dark 
                    class="accordion-wrapper"
                >
                    <v-expansion-panel
                        v-for="(category, idx) of business.categories"
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
                                        <v-tooltip top color="success">
                                            <template v-slot:activator="{ on, attrs }">
                                                <v-icon
                                                    dark
                                                    right
                                                    v-bind="attrs"
                                                    v-on="on"
                                                    @click="openSignUpForVisitDialog({
                                                        ...item,
                                                        business: {
                                                            business_city: business.city,
                                                            business_post_code: business.post_code,
                                                            business_street: business.street,
                                                            business_house_number: business.house_number,
                                                            business_name: key,
                                                        }
                                                    })"
                                                >
                                                    mdi-plus
                                                </v-icon>
                                            </template>
                                            <span>Umów wizytę</span>
                                        </v-tooltip>
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
    
    export default {
        name: "",
        components: {
            
        },
        props: {
            items: { type: Object, required: true },
            businessesHeight: { type: Number, default: 0 },
            openSignUpForVisitDialog: { type: Function, default: () => {} },
            previewBusinessActivity: { type: Function, default: () => {} },
        },
        data: () => ({
            
        }),
        inject: ["screenSize"],
        computed: {
            
        },
        methods: {
            
        }
    }
</script>