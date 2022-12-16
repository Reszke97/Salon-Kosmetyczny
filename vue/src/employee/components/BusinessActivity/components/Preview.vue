<template>
    <div style="display: flex; flex-direction: column; width:100%">
        <div style="display: flex; justify-content: end; width:100%">
            <div
                style="
                    display: flex;
                    justify-content: end;
                "
            >
                <div
                    class="mr-8"
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
        <v-row
            align="center"
            justify="center"
        >
            <v-col
                cols="11"
                sm="10"
                md="10"
                lg="10"
            >
                <img
                    v-if="businessActivity.image"
                    id="b-activity-img"
                    :src="businessActivity.image"
                    style="width:100%;height: 100%;"
                />
                <h3 style="color:white"> {{ businessActivity.name }} </h3>
                <div 
                    style="
                        display: flex;
                        flex-direction: row;
                        width:100%;
                    "
                    class="mt-4"
                >
                    <div 
                        style="
                            display: flex;
                            width: 100%;
                            min-height: 300px;
                            border: 1px solid rgb(8, 68, 164);
                            border-radius: 1rem;
                            background-color: rgb(8, 68, 164);
                            color: white;
                        "
                    >
                        <div style="padding: 0.75rem">
                            <div>
                                <h4> O firmie </h4>
                                <p style="padding: 0.4rem"> {{ businessActivity.about }} </p>
                            </div>
                            <div style="display: flex; flex-direction: column">
                                <h4> Adres </h4>
                                <span style="padding: 0.4rem 0.4rem 0 0.4rem"> Miasto: {{ `${businessActivity.city} ${businessActivity.post_code}` }} </span>
                                <span style="padding: 0 0.4rem"> Ulica: {{ 
                                    `${businessActivity.street} ${businessActivity.house_number}${
                                        businessActivity.apartment_number ? '/' + businessActivity.apartment_number : ""
                                    }` 
                                }} </span>
                            </div>
                        </div>
                    </div>
                    <div
                        class="ml-2"
                        style="
                            display: flex;
                            justify-content: end;
                            width: 100%;
                            min-height: 300px;
                            border: 1px solid rgb(8, 68, 164);
                            border-radius: 1rem;
                            background-color: rgb(8, 68, 164);
                        "
                    >
                        employees
                    </div>
                </div>
            </v-col>
        </v-row>
    </div>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI";
    import { appendMimeType } from "../../../utils/appendMimeType";
    import { jsonToFormData } from "../../../utils/jsonToFormData";
    
    export default {
        name: "",
        components: {
            
        },
        props: {
            setTab: { type: Function, required: true },
            getBusinessActivityData: { type: Function, required: true },
        },
        data: () => ({
            businessActivity: {},
        }),
        inject: ["screenSize"],
        computed: {
            
        },
        async created(){
            new Promise((resolve) => {
                this.getBusinessActivityData(resolve);
            })
            .then(res => {
                const { image } = res;
                delete res.image;
                this.businessActivity = res;
                if(image){
                    this.businessActivity.image = appendMimeType(image).image
                } else this.businessActivity.image = null;
            })
        },
        methods: {
            
        }
    }
</script>