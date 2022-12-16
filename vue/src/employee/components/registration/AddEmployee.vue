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
                        :counter="50"
                        required
                        dark
                    ></v-text-field>

                    <v-text-field
                        v-model="employeeInfo.lastName"
                        :rules="lastNameRules"
                        label="Nazwisko"
                        :counter="50"
                        required
                        dark
                    ></v-text-field>

                    <v-autocomplete
                        v-if="!isNewSpec"
                        v-model="employeeInfo.selectedSpec"
                        :items="defaultSpecializations"
                        item-text="label"
                        item-value="value"
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
                        v-if="isNewSpec"
                        v-model="employeeInfo.selectedSpec"
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
                        :counter="10"
                        label="Nazwa użytkownika"
                        required
                        dark
                    ></v-text-field>

                    <v-text-field
                        v-model="employeeInfo.password1"
                        :rules="password1Rules"
                        label="Hasło"
                        required
                        type="password"
                        dark
                    ></v-text-field>

                    <v-text-field
                        v-model="employeeInfo.password2"
                        :rules="password2Rules"
                        label="Potwierdź hasło"
                        required
                        type="password"
                        dark
                    ></v-text-field>

                    <v-row
                        
                    >
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
                                Validate
                            </v-btn>
                        </v-col>
                        <v-col
                            cols="6"
                            sm="4"
                        >
                            <v-btn
                                color="error"
                                style="width:100%!important"
                                @click="reset"
                            >
                                Reset Form
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
                password: "",
                password1: "",
            },
            valid: true,
            activation: false,
            // defaultSpecializations: employeeSpecs(),
            // specs => api/v1/employee/all-specs/
            isNewSpec: false,

            emailRules: [
                v => !!v || 'E-mail jest wymagany',
                v => /.+@.+\..+/.test(v) || 'E-mail musi być poprawny przykład:\n example@mail.com',
            ],

            userNameRules: [
                v => !!v || 'Nazwa użytkownika jest wymagana',
                // v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],

            password1Rules: [
                v => !!v || 'Hasło jest wymagane',
                // v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],

            password2Rules: [
                v => !!v || 'Potwierdzenie Hasła jest wymagane',
                // v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],
            
            nameRules: [
                v => !!v || 'Name is required',
                v => (v && v.length <= 10) || 'Name must be less than 10 characters',
            ],
            
            lastNameRules: [
                v => !!v || 'Nazwisko jest wymagane',
                // v => (v && v.length <= 10) || 'Name must be less than 10 characters',
            ],
        }),
        computed: {
            
        },
        methods: {
            
        }
    }
</script>