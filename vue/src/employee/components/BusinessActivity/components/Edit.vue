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
                    <img
                        v-if="businessActivity.image"
                        id="b-activity-img"
                        :src="businessActivity.image"
                        style="width:100%;height: 100%"
                    />
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
                        <v-text-field
                            v-model="businessActivity.contact_phone"
                            label="Telefon kontaktowy"
                            placeholder="Podaj nr telefonu"
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
                <div class="d-flex justify-end">
                    <slot name="closeDialog" />
                    <v-btn
                        color="success"
                    >Zapisz zmiany</v-btn>
                </div>
                </v-col>
            </v-row>
        </v-col>
    </v-row>
</template>

<script>
    import { appendMimeType } from "../../../utils/appendMimeType";
    export default {
        name: "Edit",
        props: {
            getBusinessActivityData: { type: Function, required: true }
        },
        components: {
        },
        data: () => ({
            businessActivity: {},
            uploadImg: null
        }),
        async created(){
            new Promise((resolve) => {
                this.getBusinessActivityData(resolve);
            })
            .then(res => {
                const { image } = res;
                delete res.image;
                this.businessActivity = res;
                if(image){
                    this.businessActivity.image = appendMimeType(image)
                } else this.businessActivity.image = null;
            })
        },
        methods: {
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
        }
    }
</script>