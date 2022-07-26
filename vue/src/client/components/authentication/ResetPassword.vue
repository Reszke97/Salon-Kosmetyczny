<template>
    <div>
        <v-form
            ref="form"
            v-model="valid"
            lazy-validation
            class = "mt1"
        >
            <v-text-field
                v-model="newPassword"
                :rules="newPasswordRules"
                label="Nowe hasło"
                required
                class="w40"
                type="password"
            ></v-text-field>
            <v-text-field
                v-model="repeatPassword"
                :rules="[...repeatPasswordRules, (repeatPassword == newPassword) || 'Podane hasła się nie zgadzają']"
                label="Powtórz nowe hasło"
                required
                class="w40"
                type="password"
            ></v-text-field>

            <div
                class="w40"
            >
                <v-btn
                    color="success"
                    class="mr-4"
                    @click="submit"
                >
                    Zmień
                </v-btn>

            </div>
        </v-form>
    </div>
</template>
<script>
    import axios from 'axios'
    export default {
        data: () => ({
            uidb64: null,
            token: null,
            valid: true,
            route: null,
            email:'',
            newPassword: null,
            newPasswordRules: [
                v => !!v || 'Hasło jest wymagane',
                // v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
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
            passwordChange(){
                console.log(this.newPassword)
                axios.patch('http://127.0.0.1:8000/api/v1/user/passwordresetcomplete/', {
                    password: this.newPassword, 
                    token: this.token, 
                    uidb64: this.uidb64
                })
                .then(response => {
                    // alert('twoje hasło zostało zmienione')
                    console.log(response)
                    // if(response){
                    //     console.log(response)
                    //     alert('twoje hasło zostało zmienione')
                    // }
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