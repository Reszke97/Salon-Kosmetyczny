<template>
    <v-row justify="center">
        <v-col
            class="bg-color"
            cols="12"
            sm="12"
            md="6"
            lg="3"
        >
            <v-form
                ref="form"
                v-model="valid"
                lazy-validation
            >
                <h3 style="color:white"> Zmiana hasła </h3>
                <v-text-field
                    v-model="newPassword"
                    :rules="newPasswordRules"
                    label="Nowe hasło"
                    required
                    dark
                    type="password"
                ></v-text-field>
                <v-text-field
                    v-model="repeatPassword"
                    :rules="[...repeatPasswordRules, (repeatPassword == newPassword) || 'Podane hasła się nie zgadzają']"
                    label="Powtórz nowe hasło"
                    required
                    dark
                    type="password"
                ></v-text-field>

                <div>
                    <v-btn
                        color="success"
                        class="mr-4"
                        @click="submit"
                    >
                        Zmień hasło
                    </v-btn>

                </div>
            </v-form>
        </v-col>
        <v-dialog
            :value="showDialog"
            width="500"
        >
            <v-card class="indigo">
                <v-card-title class="text-h5 grey lighten-2">
                    Twoje hasło zostało zmienione.
                </v-card-title>

                <v-divider></v-divider>

                <v-card-actions class="indigo">
                    <v-btn
                        class="indigo"
                        dark
                        text
                        @click="redirectToLogin()"
                    >
                        Zamknij
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-row>
</template>
<script>
    import axios from 'axios'
    export default {
        data: () => ({
            uidb64: null,
            token: null,
            valid: true,
            route: null,
            email: "",
            showDialog: false,
            newPassword: null,
            newPasswordRules: [
                v => !!v || 'Hasło jest wymagane',
            ],
            repeatPassword: null,
            repeatPasswordRules: [
                v => !!v || 'Hasło jest wymagane',
                v => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/.test(v) || 'Hasło musi zawierać co najmniej 8 znaków, 1 dużą literę, 1 małą literę, 1 cyfrę',
            ],
        }),
        
        created(){
            this.route = this.$route.params.activated
            console.log(this.route = this.$route.params.activated)
        },
        methods: {
            submit () {
                const IS_VALID = this.$refs.form.validate()
                if(IS_VALID){
                    this.passwordChange()
                }
            },
            openDialog(){
                this.showDialog = true;
            },
            redirectToLogin(){
                window.location.assign("/employee/login");
            },
            passwordChange(){
                console.log(this.newPassword)
                axios.patch('http://127.0.0.1:8000/api/v1/user/passwordresetcomplete/', {
                    password: this.newPassword, 
                    token: this.token, 
                    uidb64: this.uidb64
                })
                .then(() => {
                    this.openDialog();
                })
                .catch(error =>{
                    console.log(error)
                })
            }
        },
        created(){
            this.uidb64 = this.$route.query.uidb64
            this.token = this.$route.query.token
        }
    }
</script>

<style scoped>
    .w40{
        width: 30%;
        margin-left: auto;
        margin-right: auto;
    }
    .w25{
        width: 25%;
    }
    .mt1{
        margin-top: 1rem;
    }
    .message{
        margin-top: 2rem;
        text-align: center;
        width: 40%;
        padding: 2% 0;
        margin-left: auto;
        margin-right: auto;
        font-size: 0.9rem;
    }
    .top-filter{
    position: sticky;
    top: 0;
    z-index: 2;
    }
</style>