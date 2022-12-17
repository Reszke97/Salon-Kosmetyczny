<template>
    <div
        style="width:100%"
    >
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
                <v-form
                    ref="form"
                    v-model="valid"
                    lazy-validation
                >
                    <v-text-field
                        v-model="employeeInfo.name"
                        :rules="nameRules"
                        label="Imię"
                        required
                        dark
                    ></v-text-field>

                    <v-text-field
                        v-model="employeeInfo.lastName"
                        :rules="lastNameRules"
                        label="Nazwisko"
                        required
                        dark
                    ></v-text-field>

                    <v-autocomplete
                        v-if="!employeeInfo.isNewSpec"
                        v-model="employeeInfo.employee_spec"
                        :items="defaultSpecializations"
                        item-text="name"
                        item-value="id"
                        label="Specjalność"
                        placeholder="Wybierz specjalność"
                        hint="Kliknij na ikonę aby dodać własną specjalność."
                        persistent-hint
                        dark
                    >
                        <template #append-outer>
                            <v-btn
                                icon
                                @click="toggleSpecInput"
                            >
                                <v-icon>
                                    mdi-swap-horizontal
                                </v-icon>
                            </v-btn>
                        </template>
                    </v-autocomplete>
                    <v-text-field
                        v-if="employeeInfo.isNewSpec"
                        v-model="employeeInfo.employee_spec"
                        label="Specjalność"
                        placeholder="Podaj specjalność"
                        hint="Kliknij na ikonę aby wybrać specjalność z listy."
                        persistent-hint
                        dark
                    >
                        <template #append-outer>
                            <v-btn
                                icon
                                @click="toggleSpecInput"
                            >
                                <v-icon>
                                    mdi-keyboard-backspace 
                                </v-icon>
                            </v-btn>
                        </template>
                    </v-text-field>

                    <v-text-field
                        v-model="employeeInfo.email"
                        :rules="emailRules"
                        label="E-mail"
                        required
                        dark
                    ></v-text-field>

                    <v-text-field
                        v-model="employeeInfo.userName"
                        :rules="userNameRules"
                        label="Nazwa użytkownika"
                        required
                        dark
                    ></v-text-field>

                    <v-row>
                        <v-col
                            cols="6"
                            sm="4"
                        >
                            <v-btn
                                :disabled="!valid"
                                color="success"
                                @click="submit"
                                style="width:100%!important"
                            >
                                Zapisz
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-col>
        </v-row>
    </div>
</template>


<script>
    import { AUTH_API } from "../../authorization/AuthAPI";
    
    export default {
        name: "",
        components: {
            
        },
        props: {
            
        },
        data: () => ({
            employeeInfo: {
                name: "",
                lastName: "",
                selectedSpec: "",
                email: "",
                userName: "",
                phoneNumber: "",
                isNewSpec: false,
            },
            valid: true,
            activation: false,
            defaultSpecializations: [],

            emailRules: [
                v => !!v || 'E-mail jest wymagany',
                v => /.+@.+\..+/.test(v) || 'E-mail musi być poprawny przykład:\n example@mail.com',
            ],

            userNameRules: [
                v => !!v || 'Nazwa użytkownika jest wymagana',
            ],
            
            nameRules: [
                v => !!v || 'Name is required',
            ],
            
            lastNameRules: [
                v => !!v || 'Nazwisko jest wymagane',
            ],
        }),
        async created(){
            await this.getAllSpecs();
        },
        computed: {
            
        },
        methods: {
            async getAllSpecs(){
                const API = await AUTH_API();
                await API.get("api/v1/employee/all-specs/")
                .then(res => {
                    this.defaultSpecializations = res.data
                })
            },
            async submit () {
                const IS_VALID = this.$refs.form.validate()
                if(IS_VALID){
                   await this.sendForm()
                }
            },
            async sendForm(){
                const API = await AUTH_API();
                await API.post('api/v1/employee/create-employee/', this.employeeInfo)
                .then(response => {
                })
                .catch(error => {
                    alert(error)
                })
            },
            toggleSpecInput(){
                this.employeeInfo.isNewSpec = !this.employeeInfo.isNewSpec;
                this.employeeInfo.employee_spec = "";
            },
        }
    }
</script>