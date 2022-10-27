<template>
    <v-row
        class="pt-5"
        :style="{
            backgroundColor:'#3f51b5!important',
            height: '100%',
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
                        v-model="serviceInfo.category.category"
                        label="Nazwa kategorii"
                        placeholder="Podaj nazwę kategorii"
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
                <v-row>
                    <v-col cols=6>
                        <v-text-field
                            v-model="serviceInfo.service.price"
                            label="Cena [PLN]"
                            placeholder="Podaj cenę"
                            dark
                        ></v-text-field>
                    </v-col>
                    <v-col>
                        <v-text-field
                            v-model="serviceInfo.service.duration"
                            label="Czas trwania"
                            placeholder="Podaj czas"
                            dark
                        ></v-text-field>
                    </v-col>
                </v-row>
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
                        dark
                        @change="(event) => displayImages(event)"
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
                    <display-images
                        v-if="imagesCount > 0"
                        :images="serviceInfo.employee_image"
                        :imagesCount="imagesCount"
                    />
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
                        color="success"
                        @click="prepareAndPostRequest"
                    >{{ preview ? "Zapisz zmiany" : "Dodaj usługę" }}</v-btn>
                </div>
                </v-col>
            </v-row>
        </v-col>
    </v-row>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI";
    import DisplayImages from "./DisplayImages.vue";
    export default {
        name: "",
        components: {
            DisplayImages
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
                category: {
                    isNew: true,
                    category: "",
                },
                employee_image: []
            },
            images: [],
            imagesCount: 0
        }),
        computed: {
            
        },
        created(){
            if(this.preview){
                Object.keys(this.serviceToEdit).forEach(key => {
                    this.serviceInfo[key] = this.serviceToEdit[key];
                })
            }
        },
        methods: {
            async displayImages(event){
                if(event.length){
                    for(const image of this.images){
                        const reader  = new FileReader();
                        reader.onload = async (e) => { 
                            e.persist = () => {}
                            await this.handleChange(e)
                        }
                        await this.getDataUrl(reader, image)
                        this.imagesCount = this.images.length
                    }
                } else {
                    this.serviceInfo.employee_image = [];
                    this.imagesCount = 0
                }
            },
            async handleChange (e){
                await new Promise((resolve) => {
                    this.serviceInfo.employee_image.push({image:(e.target.result)})
                    resolve()
                })
            },
            async getDataUrl(reader, image){
                await reader.readAsDataURL(image);
            },
            setShowImagePreview(idx = null){
                this.showImagePreview = !this.showImagePreview;
                this.imagePreviewIdx = idx;
            },
            buildFormData(formData, data, parentKey) {
                if (data && typeof data === 'object' && !(data instanceof Date) && !(data instanceof File)) {
                    Object.keys(data).forEach(key => {
                        this.buildFormData(formData, data[key], parentKey ? `${parentKey}[${key}]` : key);
                    });
                } else {
                    const value = data == null ? '' : data;

                    formData.append(parentKey, value);
                }
            },
            jsonToFormData(data) {
                const formData = new FormData();
                this.buildFormData(formData, data);
                for (let i = 0; i < this.images.length; i += 1) {
                    formData.append('files', this.images[i]);
                }
                return formData;
            },
            async postData (actionType){
                const API = await AUTH_API();
                const formData = new FormData();
                Object.keys(this.serviceInfo).forEach(key => formData.append(key, this.serviceInfo[key]));
                const _serviceInfo = {...this.serviceInfo}
                delete _serviceInfo.employee_image
                await API[actionType]("/api/v1/employee/service/",
                    this.jsonToFormData(_serviceInfo),
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
            async prepareAndPostRequest(){
                let actionType = "post";
                if(this.preview){
                    actionType = "put"
                }
                await this.postData(actionType);
            }
        }
    }
</script>