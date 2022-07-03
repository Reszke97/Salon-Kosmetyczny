<template>
    <v-row
        class="pt-5"
    >
        <v-col>
            <v-row
                align="center"
                justify="center"
            >
                <v-col
                    cols="11"
                    sm="10"
                    md="8"
                    lg="6"
                >
                    <v-text-field
                        v-model="serviceName"
                        label="Nazwa usługi"
                        placeholder="Podaj nazwę usługi"
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-row
                align="center"
                justify="center"
            >
                <v-col
                    cols="11"
                    sm="10"
                    md="8"
                    lg="6"
                >
                    <v-text-field
                        v-model="price"
                        label="Cena [PLN]"
                        placeholder="Podaj cenę"
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-row
                align="center"
                justify="center"
            >
                <v-col
                    cols="11"
                    sm="10"
                    md="8"
                    lg="6"
                >
                    <v-text-field
                        v-model="timeSpan"
                        label="Czas trwania usługi"
                        placeholder="Podaj czas trwania"
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-row
                align="center"
                justify="center"
            >
                <v-col
                    cols="11"
                    sm="10"
                    md="8"
                    lg="6"
                >
                    <v-btn
                        @click="postNewService"
                    >Dodaj usługę</v-btn>
                </v-col>
            </v-row>
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
            
        },
        data: () => ({
            serviceName: "",
            price: 0,
            timeSpan: ""
        }),
        computed: {
            
        },
        methods: {
            async postNewService(){
                await AUTH_API.post("/api/v1/employee/postnewservice/", {
                    name: this.serviceName,
                    price: this.price,
                    duration: this.timeSpan
                })
                .then(() => {
                    console.log("hurra!")
                })
                .catch((err) => {
                    console.log(err)
                })
            }
        }
    }
</script>