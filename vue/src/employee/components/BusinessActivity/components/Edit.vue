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
                    <a
                        v-if="businessActivity.image"
                        @click="openImg(businessActivity.image)"
                    >
                        <v-img
                            id="b-activity-img"
                            :src="businessActivity.image"
                            style="width:100%;height: 100%"
                        />
                    </a>
                    <v-checkbox
                        dark
                        v-model="businessActivity.is_active"
                        label="Działalność aktywna"
                        type="checkbox"
                    >
                        
                    </v-checkbox>
                    <v-file-input
                        v-model="uploadImg"
                        accept=".png, .jpg"
                        label="Załącznik"
                        placeholder="Dodaj zdjęcia"
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
                    <v-text-field
                        v-model="businessActivity.name"
                        label="Nazwa działalności"
                        placeholder="Podaj nazwę działalności"
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
                    <v-col cols=8>
                        <v-text-field
                            v-model="businessActivity.city"
                            label="Miejscowość"
                            placeholder="Podaj miejscowość"
                            dark
                        ></v-text-field>
                    </v-col>
                    <v-col cols=4>
                        <v-text-field
                            v-model="businessActivity.post_code"
                            label="Kod pocztowy"
                            placeholder="Podaj kod pocztowy"
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
                <v-row>
                    <v-col>
                        <v-text-field
                            v-model="businessActivity.street"
                            label="Ulica"
                            placeholder="Podaj ulicę"
                            dark
                        ></v-text-field>
                    </v-col>
                    <v-col>
                        <v-text-field
                            v-model="businessActivity.house_number"
                            label="Nr domu"
                            placeholder="Podaj nr domu"
                            dark
                        ></v-text-field>
                    </v-col>
                    <v-col>
                        <v-text-field
                            v-model="businessActivity.apartment_number"
                            label="Nr mieszkania"
                            placeholder="Podaj nr mieszkania"
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
                <v-row>
                    <v-col>
                        <div class="d-flex">
                            <div style="width:80px!important">
                                <v-text-field
                                    label="Kierunkowy"
                                    dark
                                    :value="'+48'"
                                    readonly
                                />
                            </div>
                            <div class="w-100">
                                <v-text-field
                                    class="ml-2"
                                    v-model="businessActivity.contact_phone"
                                    placeholder="Nr telefonu"
                                    dark
                                ></v-text-field>
                            </div>
                        </div>
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
                <div class="d-flex justify-end">
                    <slot name="closeDialog" />
                    <v-btn
                        @click="updateBusinessInfo"
                        color="success"
                    >Zapisz zmiany</v-btn>
                </div>
                </v-col>
            </v-row>
            <v-dialog
                id="showImagePreview"
                v-model="showImagePreview"
                style="overflow: hidden!important;"
                v-if="showImagePreview"
            >
                <v-img
                    :src="selectedImg"
                    style="width:auto;height: auto"
                />
                <v-btn
                    dark
                    color="secondary"
                    @click="closeImg"
                    class="mr-2"
                >
                    Zamknij
                </v-btn>
            </v-dialog>
        </v-col>
    </v-row>
</template>

<script>
    import { appendMimeType } from "../../../utils/appendMimeType";
    import { jsonToFormData } from "../../../utils/jsonToFormData";
    import { AUTH_API } from "../../../authorization/AuthAPI";
    export default {
        name: "Edit",
        props: {
            getBusinessActivityData: { type: Function, required: true }
        },
        components: {
        },
        data: () => ({
            showImagePreview: false,
            selectedImg: "",
            businessActivity: {},
            uploadImg: null
        }),
        async created(){
            new Promise( async (resolve) => {
                await this.getBusinessActivityData(resolve);
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
            closeImg(){
                this.showImagePreview = false;
            },
            openImg(dataUrl){
                this.selectedImg = dataUrl;
                this.showImagePreview = true;
            },
            async displayImages(event){
                if(event){
                    const reader  = new FileReader();
                    reader.onload = async (e) => { 
                        e.persist = () => {}
                        await this.handleChange(e)
                    }
                    await this.getDataUrl(reader, this.uploadImg)
                } else this.businessActivity.image = null;
            },
            async handleChange (e){
                await new Promise((resolve) => {
                    this.businessActivity.image = e.target.result;
                    this.businessActivity = { ...this.businessActivity }
                    resolve()
                })
            },

            async getDataUrl(reader, image){
                await reader.readAsDataURL(image);
            },

            async updateBusinessInfo(){
                const API = await AUTH_API();
                await API.put("api/v1/employee/business-activity/",
                    jsonToFormData({
                        data: {
                            apartment_number: this.businessActivity.apartment_number,
                            city: this.businessActivity.city,
                            contact_phone: this.businessActivity.contact_phone,
                            house_number: this.businessActivity.house_number,
                            id: this.businessActivity.id,
                            name: this.businessActivity.name,
                            post_code: this.businessActivity.post_code,
                            street: this.businessActivity.street,
                            is_active: this.businessActivity.is_active,
                        },
                        images: this.uploadImg,
                        arrayOfImages: false,
                    }),
                    {
                        headers: {
                            "content-type": "multipart/form-data",
                        },
                    }
                )
                .then(() => {
                    alert("Zapisano zmiany")
                })
                .catch((err) => {
                    alert(err)
                })
            }
        }
    }
</script>