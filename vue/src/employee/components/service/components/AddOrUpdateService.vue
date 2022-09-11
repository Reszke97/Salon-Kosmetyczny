<template>
    <v-row
        class="pt-5"
        :style="{
            backgroundColor:'#3f51b5!important',
            minHeight: minHeight
        }"
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
                        v-model="serviceInfo.name"
                        label="Nazwa usługi"
                        placeholder="Podaj nazwę usługi"
                        dark
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
                        v-model="serviceInfo.price"
                        label="Cena [PLN]"
                        placeholder="Podaj cenę"
                        dark
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
                        v-model="serviceInfo.duration"
                        label="Czas trwania usługi"
                        placeholder="Podaj czas trwania"
                        dark
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
                    <v-file-input
                        v-model="images"
                        accept=".png, .jpg"
                        label="Załącznik"
                        placeholder="Dodaj zdjęcia"
                        multiple
                        prepend-icon="mdi-paperclip"
                        :show-size="1000"
                        counter
                        dark
                    >
                        <template #selection="{ text }">
                        <v-chip
                            small
                            label
                            color="success"
                        >
                            {{ text }}
                        </v-chip>
                        </template>
                    </v-file-input>
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
                <div class="d-flex justify-end">
                    <slot name="closeDialog" />
                    <v-btn
                        @click="postImages"
                    >{{ preview ? "Zapisz zmiany" : "Dodaj usługę" }}</v-btn>
                </div>
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
            minHeight: {
                type: String,
                default: "auto"
            },
            preview: {
                type: Boolean,
                default: () => false
            },
            serviceToEdit: {
                type: Object,
                default: () => ({})
            }
        },
        data: () => ({
            serviceInfo: {
                name: "",
                price: 0,
                duration: "",
            },
            images: [],
        }),
        computed: {
            
        },
        created(){
            if(this.preview){
                // console.log(this.serviceToEdit)
                Object.keys(this.serviceToEdit).forEach(key => {
                    this.serviceInfo[key] = this.serviceToEdit[key];
                })
            }
        },
        methods: {
            async postImages (){
                const API = await AUTH_API();

                const formData = new FormData();
                for (let i = 0; i < this.images.length; i += 1) {
                    formData.append('files', this.images[i]);
                    // formData.append("employee", 4);
                }

                console.log(...formData)

                let actionType = "post";
                if(this.preview){
                    actionType = "put"
                }
                await API[actionType]("/api/v1/employee/postnewimages/",
                    formData,
                    {
                        headers: {
                            "content-type": "multipart/form-data",
                        },
                    }
                )
                .then(() => {
                    console.log("hurra!")
                })
                .catch((err) => {
                    console.log(err)
                })
            },
            async postService(){
                const API = await AUTH_API();
                let actionType = "post";
                if(this.preview){
                    actionType = "put"
                }
                await API[actionType]("/api/v1/employee/postnewservice/", this.serviceInfo)
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