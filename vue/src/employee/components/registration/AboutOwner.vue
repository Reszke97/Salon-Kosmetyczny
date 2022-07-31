<template>
    <div
        style="width:100%"
    >
        <v-row 
            align="center"
            justify="center"
        >
            <v-col
                cols="12"
            >
                <v-form
                    ref="form"
                    v-model="valid"
                    lazy-validation
                >
                    <v-text-field
                        v-model="name"
                        :rules="nameRules"
                        label="Imię"
                        :counter="50"
                        required
                    ></v-text-field>

                    <v-text-field
                        v-model="lastName"
                        :rules="lastNameRules"
                        label="Nazwisko"
                        :counter="50"
                        required
                    ></v-text-field>

                    <v-autocomplete
                        v-if="!isNewSpec"
                        v-model="selectedSpec"
                        :items="defaultSpecializations"
                        item-text="label"
                        item-value="value"
                        label="Specjalność"
                        placeholder="Wybierz specjalność"
                        hint="Kliknij na ikonę aby dodać własną specjalność."
                        persistent-hint
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
                        v-model="selectedSpec"
                        label="Specjalność"
                        placeholder="Podaj specjalność"
                        hint="Kliknij na ikonę aby wybrać specjalność z listy."
                        persistent-hint
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
                        v-model="email"
                        :rules="emailRules"
                        label="E-mail"
                        required
                    ></v-text-field>

                    <v-text-field
                        v-model="userName"
                        :rules="userNameRules"
                        :counter="10"
                        label="Nazwa użytkownika"
                        required
                    ></v-text-field>

                    <v-text-field
                        v-model="password1"
                        :rules="password1Rules"
                        label="Hasło"
                        required
                        type="password"
                    ></v-text-field>

                    <v-text-field
                        v-model="password2"
                        :rules="password2Rules"
                        label="Potwierdź hasło"
                        required
                        type="password"
                    ></v-text-field>

                    <v-checkbox
                        v-model="checkbox"
                        :rules="checkboxRules"
                        value="1"
                        label="Zgadzam się na przetwarzanie danych"
                        type="checkbox"
                        required
                    ></v-checkbox>

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
        <v-dialog
            v-model="activation"
            width="500"
        >
            <v-card>
                <v-card-title class="text-h5 grey lighten-2">
                    Na podany email został przesłany link do aktywacji konta.
                </v-card-title>

                <v-divider></v-divider>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="primary"
                        text
                        @click="activation = false"
                    >
                        Zamknij
                    </v-btn>
                    <v-btn
                        color="primary"
                        text
                    >
                        Przejdź do logowania
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>
<script>
    import axios from 'axios'
    import { mapState} from 'vuex';
    import { employeeSpecs } from "../../../utils"
    export default {
        data: () => ({
            valid: true,
            activation: false,
            email: '',
            emailRules: [
                v => !!v || 'E-mail jest wymagany',
                v => /.+@.+\..+/.test(v) || 'E-mail musi być poprawny przykład:\n example@mail.com',
            ],
            userName:'',
            userNameRules: [
                v => !!v || 'Nazwa użytkownika jest wymagana',
                // v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],
            password1:'',
            password1Rules: [
                v => !!v || 'Hasło jest wymagane',
                // v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],
            password2:'',
            password2Rules: [
                v => !!v || 'Potwierdzenie Hasła jest wymagane',
                // v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],
            name: '',
            nameRules: [
                v => !!v || 'Name is required',
                v => (v && v.length <= 10) || 'Name must be less than 10 characters',
            ],
            lastName:'',
            lastNameRules: [
                v => !!v || 'Nazwisko jest wymagane',
                // v => (v && v.length <= 10) || 'Name must be less than 10 characters',
            ],
            phone: '',
            checkbox: false,
            checkboxRules : [
                v => !!v || 'Aby kontynuować konieczna jest zgoda!'
            ],
            defaultSpecializations: employeeSpecs(),
            selectedSpec: "",
            isNewSpec: false,
        }),
        computed: {

        },
        methods: {
            submit () {
                const IS_VALID = this.$refs.form.validate()
                if(IS_VALID){
                    this.sendForm()
                }
            },
            toggleSpecInput() {
                this.isNewSpec = !this.isNewSpec
            },
            reset () {
                this.selectedCountry = ''
                this.phone = ''
                this.checkbox = false
                this.imgSrc = ''
                this.lastName = ''
                this.password2 = ''
                this.password1 = ''
                this.userName = ''
                this.email = ''
                this.activation = ''
                this.valid = ''
                this.name = ''
                this.$refs.form.resetValidation()
            },
            sendForm(){
                axios.post('http://127.0.0.1:8000/api/v1/user/register/', {
                    'email': this.email,
                    'user_name': this.userName,
                    'password': this.password1,
                    'first_name': this.name,
                    'last_name': this.lastName,
                })
                .then(response => {
                    this.activation = true
                })
                .catch(error => {
                    alert(error)
                })
            },
        },
    }
</script>

<style scoped>
    .w40{
    width: 40%;
    margin-left: auto;
    margin-right: auto;
    }
    .w25{
        width: 25%;
    }
    .top-filter{
        position: sticky;
        top: 0;
        z-index: 2;
    }
    .mt1{
        margin-top: 1rem;
    }
</style>