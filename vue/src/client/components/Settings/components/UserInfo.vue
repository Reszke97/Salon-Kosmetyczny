<template>
    <div>
        <v-row
            class="py-8"
            align="center"
            justify="center"
        >
            <v-col cols="10">
                <v-text-field
                    v-model="userInfo.email"
                    label="Email"
                    required
                    dark
                ></v-text-field>
                <v-text-field
                    v-model="userInfo.user_name"
                    label="Nazwa użytkownika"
                    required
                    class="w40"
                    type="text"
                    dark
                ></v-text-field>
                <v-text-field
                    v-model="userInfo.first_name"
                    label="Imię"
                    required
                    class="w40"
                    type="text"
                    dark
                ></v-text-field>
                <v-text-field
                    v-model="userInfo.last_name"
                    label="Nazwisko"
                    required
                    class="w40"
                    type="text"
                    dark
                ></v-text-field>
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
                            v-model="userInfo.phone_number"
                            label="Telefon"
                            required
                            class="w40 ml-2"
                            type="text"
                            dark
                        ></v-text-field>
                    </div>
                </div>
                <v-btn
                    color="secondary"
                    @click="setDialog(true)"
                >
                    Zmień
                </v-btn>
            </v-col>
        </v-row>
        <Dialog
            v-if="confirmDialog"
            :dialog="confirmDialog"
            :onConfirmAction="onConfirmAction"
            :setDialog="setDialog"
        />
    </div>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI";
    import { Dialog } from "../../../utils";
    
    export default {
        name: "",
        components: {
            Dialog
        },
        props: {
            
        },
        data: () => ({
            userInfo: {
                first_name: "",
                last_name: "",
                phone_number: "",
                user_name: "",
                email: "",
            },
            confirmDialog: false,
        }),
        computed: {
            
        },
        methods: {
            async updateInfo(){
                const API = await AUTH_API();
                await API.put('api/v1/client/info/', this.userInfo)
            },
            async onConfirmAction(value){
                await this.updateInfo()
                this.setDialog(false)
            },
            setDialog(value){
                this.confirmDialog = value
            },
        },

        async created() {
            const API = await AUTH_API();
            await API.get('api/v1/client/info/')
                .then((res) => {
                    this.userInfo = res.data
                })
        }
    }
</script>