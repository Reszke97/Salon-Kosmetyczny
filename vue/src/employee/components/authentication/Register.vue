<template>
    <div>
        <v-row 
            align="center"
            justify="center"
        >
            <v-col
                cols="11"
                sm="9"
                md="6"
                lg="3"
            >
                <v-form
                    ref="form"
                    v-model="valid"
                    lazy-validation
                >
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
                    <v-row>
                        <v-col
                            cols="3"
                            sm="3"
                        >
                            <v-select
                                :items="countriesWithImages"
                                v-model="selectedCountry"
                                label="Kraj"
                                @change="handleInput()"
                            >
                                <template slot="selection" slot-scope="data">
                                    <v-img
                                        class="mr-1"
                                        max-height="15"
                                        max-width="20"
                                        :src="data.item.src"
                                    ></v-img>
                                    {{ data.item.phone }}
                                </template>
                                <template 
                                    slot="item" 
                                    slot-scope="data"
                                >
                                    <v-img
                                        class="mr-1"
                                        max-height="15"
                                        max-width="20"
                                        :src="data.item.src"
                                    ></v-img>
                                    {{ data.item.phone }}
                                </template>
                            </v-select>
                        </v-col>
                        <v-col
                            cols="9"
                            sm="9"
                        >
                            <v-text-field
                                label="Nr telefonu"
                                required
                                :rules="selectedCountry.rule"
                                v-model="phone"
                            ></v-text-field>

                        </v-col>
                    </v-row>

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
            selectedCountry: '',
            imgSrc: '',
        }),
        computed: {
            ...mapState({
                countries: state => state.countries,
                rules: state => state.rules,
            }),
            countriesWithImages(){
                let _countries = this.countries
                _countries[0].src = require('../../assets/images/countries_flags/pl.svg')
                _countries[1].src = require('../../assets/images/countries_flags/de.svg')
                _countries[2].src = require('../../assets/images/countries_flags/gb.svg')
                return _countries
            }
        },
        methods: {
            submit () {
                const IS_VALID = this.$refs.form.validate()
                if(IS_VALID){
                    this.sendForm()
                }
            },
            assingFlag(head){
                switch(head){
                    case '+48':
                        this.imgSrc=require('../../assets/images/countries_flags/pl.svg')
                    break
                    
                    case '+49':
                        this.imgSrc=require('../../assets/images/countries_flags/de.svg')
                    break
                    case '+44':
                        this.imgSrc=require('../../assets/images/countries_flags/gb.svg')
                    break
                }
            },
            handleInput(){
                this.assingFlag(this.selectedCountry.phone)
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
                let _phone = ''
                if(this.phone !== '' && this.phone.length > 3){
                    _phone = this.selectedCountry.phone + ' ' + this.phone
                }
                else{
                    _phone = ''
                }
                axios.post('http://127.0.0.1:8000/api/v1/user/register/', {
                    'email': this.email,
                    'user_name': this.userName,
                    'password': this.password1,
                    'first_name': this.name,
                    'last_name': this.lastName,
                    'phone_number': _phone === '' ? null : _phone,
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