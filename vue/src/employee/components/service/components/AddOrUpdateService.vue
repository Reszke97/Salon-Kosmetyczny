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
                    <v-autocomplete
                        v-if="!serviceInfo.category.is_new"
                        v-model="serviceInfo.category.category"
                        :items="availableCategories"
                        id="category-list"
                        item-text="name"
                        item-value="id"
                        label="Nazwa kategorii"
                        placeholder="Podaj nazwę kategorii"
                        hint="Kliknij na ikonę aby dodać własną Kategorię."
                        persistent-hint
                        dark
                        item-color="black"
                    >
                        <template #append-outer>
                            <v-btn
                                icon
                                @click="setCategoryInput"
                            >
                                <v-icon>
                                    mdi-swap-horizontal
                                </v-icon>
                            </v-btn>
                        </template>
                    </v-autocomplete>
                    <v-text-field
                        v-if="serviceInfo.category.is_new"
                        v-model="serviceInfo.category.category"
                        label="Nazwa kategorii"
                        placeholder="Podaj nazwę kategorii"
                        hint="Kliknij na ikonę aby wybrać specjalność z listy."
                        persistent-hint
                        dark
                    >
                        <template #append-outer>
                            <v-btn
                                icon
                                @click="setCategoryInput"
                            >
                                <v-icon>
                                    mdi-keyboard-backspace 
                                </v-icon>
                            </v-btn>
                        </template>
                    </v-text-field>
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
                            type="number"
                        ></v-text-field>
                    </v-col>
                    <v-col>
                        <v-text-field
                            v-model="serviceInfo.service.duration"
                            label="Czas trwania [min]"
                            placeholder="Podaj czas"
                            dark
                            type="number"
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
                        @click:clear="(event) => clearImgs()"
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
                        :images-count="imagesCount"
                        :delete-image="deleteImage"
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
                        @click="prepareAndPostRequest(false)"
                    >{{ preview ? "Zapisz zmiany" : "Dodaj usługę" }}</v-btn>
                    <v-btn
                        dark
                        class="ml-2"
                        v-if="preview"
                        color="red"
                        @click="prepareAndPostRequest(true)"
                    >
                        Usuń
                    </v-btn>
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
            },
            getServices: {
                type: Function,
                default: () => {}
            },
            closeDialog: {
                type: Function,
                default: () => {}
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
                    is_new: true,
                    category: "",
                },
                employee_image: []
            },
            availableCategories: [],
            images: [],
        }),
        computed: {
            imagesCount(){
                return this.serviceInfo.employee_image.length + this.images.length
            }
        },
        async created(){
            this.assignServiceInfoData();
            await this.getCategories();
        },
        methods: {
            clearImgs(){
                this.serviceInfo.employee_image = this.serviceInfo.employee_image.filter(el => el.isFromDB === true);
            },
            async getCategories(){
                const API = await AUTH_API();
                const res = await API.get("/api/v1/employee/employee-category/")
                const key = "name";
                this.availableCategories = [...new Map(res.data.map(item =>[item[key], item])).values()];
            },
            resetForm(){
                this.serviceInfo = {
                    service: {
                        name: "",
                        price: 0,
                        duration: "",
                    },
                    category: {
                        is_new: true,
                        category: "",
                    },
                    employee_image: []
                }
            },
            assignServiceInfoData(){
                if(this.preview){
                    Object.keys(this.serviceToEdit).forEach(key => {
                        this.serviceInfo[key] = this.serviceToEdit[key];
                    })
                }
            },
            async deleteImage({ image_id }){
                const API = await AUTH_API();
                await API.delete(`/api/v1/employee/images/?image_id=${image_id}`)
                    .then( async () => {
                        alert("Usunięto zdjęcie");
                        await this.getServices();
                        this.assignServiceInfoData();
                    })
            },
            setCategoryInput(){
                this.serviceInfo.category.is_new = !this.serviceInfo.category.is_new
            },
            async displayImages(event = []){
                if(event.length || this.preview){
                    for(const image of this.images){
                        const reader  = new FileReader();
                        reader.onload = async (e) => { 
                            e.persist = () => {}
                            await this.handleChange(e)
                        }
                        await this.getDataUrl(reader, image)
                    }
                } else {
                    this.serviceInfo.employee_image = [];
                }
            },
            async handleChange (e){
                await new Promise((resolve) => {
                    this.serviceInfo.employee_image.push({image:(e.target.result), isFromDB: false})
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
                    alert('Zapisano zmiany');
                })
                .catch((err) => {
                    console.log(err);
                })
            },
            async prepareAndPostRequest(isDelete = false){
                let actionType = "post";
                if(this.preview){
                    if(isDelete) {
                        actionType = "delete";
                        const API = await AUTH_API();
                        await API.delete("/api/v1/employee/service/", {
                            data: {
                                category: this.serviceInfo.category,
                                service: this.serviceInfo.service
                            }
                        })
                        .then(() => {
                            alert("Usunięto usługę")
                        })
                    }
                    else actionType = "put";
                }
                if(!isDelete){
                    await this.postData(actionType);
                }
                if(actionType === "post"){
                    this.resetForm();
                } if(actionType === "post" || actionType === "delete"){
                    await this.getCategories();
                }
                if(actionType === "put" || actionType === "delete"){
                    this.closeDialog();
                }
            }
        }
    }
</script>

<style>
    .v-list v-select-list v-sheet{
        background-color: red!important;
    }
</style