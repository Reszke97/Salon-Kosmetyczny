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
                        v-model="serviceInfo.service.name"
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
                        v-model="serviceInfo.service.price"
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
                        v-model="serviceInfo.service.duration"
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
                <div 
                    id="image-set"
                    style="display: flex; flex-direction: row"
                >
                    <div 
                        style="display: flex; width:100%"
                        v-for="(img, idx) of serviceInfo.employee_image"
                        :key="idx"
                    >
                        <div style="display: flex; flex-direction: column">
                            <img
                                :src="img.image"
                                style="width:100%;height: 100%"
                            />
                            <div style="display: flex; flex-direction: row; width:100%">
                                <div style="width:100%">
                                    <v-btn
                                        @click="setShowImagePreview(idx)"
                                    >
                                        Podgląd
                                    </v-btn>
                                </div>
                                <div style="width:100%">
                                    <v-btn>
                                        Usuń
                                    </v-btn>
                                </div>
                            </div>
                        </div>
                        <v-dialog
                            id="showImagePreview"
                            v-model="showImagePreview"
                            width="75vw"
                            style="min-height:350px!important"
                            v-if="showImagePreview"
                        >
                            <img
                                :src="serviceInfo.employee_image[imagePreviewIdx].image"
                                style="width:100%;height: 100%"
                            />
                            <v-btn
                                dark
                                @click="setShowImagePreview"
                                class="mr-2"
                            >
                                Zamknij
                            </v-btn>
                        </v-dialog>
                    </div>
                </div>
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
                        @change="() => test()"
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
                service: {
                    name: "",
                    price: 0,
                    duration: "",
                },
                images: [],
            },
            imagePreviewIdx: null,
            images: [],
            showImagePreview: false,
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
        // mounted(){
        //     if(this.preview){
        //         const items = document.querySelectorAll("#image-set div")
        //         for(const item of items){
        //             item.addEventListener("click", () => {

        //             })
        //         }
        //     }
        // },
        methods: {
            test(){
                console.log('sth')
            },
            setShowImagePreview(idx = null){
                this.showImagePreview = !this.showImagePreview;
                this.imagePreviewIdx = idx;
            },
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