<template>
    <div>
        <v-card
            elevation="2"
            class = "message"
            color = "#FFFEE9"
            v-if="route"
        >
            Twoje konto zostało aktywowane. Możesz przejść do logowania.
        </v-card>
        <v-form
            ref="form"
            v-model="valid"
            lazy-validation
            class = "mt1"
        >
            <v-text-field
                v-model="oldPassword"
                :rules="oldPasswordRules"
                label="Stare hasło"
                required
                class="w40"
                type="password"
                dark
            ></v-text-field>

            <v-text-field
                v-model="newPassword"
                :rules="newPasswordRules"
                label="Nowe hasło"
                required
                class="w40"
                type="password"
                dark
            ></v-text-field>
            <v-text-field
                v-model="repeatPassword"
                :rules="[...repeatPasswordRules, (repeatPassword == newPassword) || 'Podane hasła się nie zgadzają']"
                label="Powtórz nowe hasło"
                required
                class="w40"
                type="password"
                dark
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
    import { AUTH_API } from '../../../authorization/AuthAPI'
    export default {
        data: () => ({
            valid: true,
            route: null,
            newPassword:'',
            newPasswordRules: [
                v => !!v || 'Hasło jest wymagane',
                v => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/.test(v) || 'Hasło musi zawierać co najmniej 8 znaków, 1 dużą literę, 1 małą literę, 1 cyfrę ',
            ],
            oldPassword:'',
            oldPasswordRules: [
                v => !!v || 'Hasło jest wymagane'
            ],
            repeatPassword:'',
            repeatPasswordRules: [
                v => !!v || 'Hasło jest wymagane',
                v => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/.test(v) || 'Hasło musi zawierać co najmniej 8 znaków, 1 dużą literę, 1 małą literę, 1 cyfrę',
            ],
        }),
        
        created(){
            this.route = this.$route.params.activated
        },
        methods: {
            submit () {
                const IS_VALID = this.$refs.form.validate()
                if(IS_VALID){
                    this.passwordChange()
                }
            },
            async passwordChange(){
                const API = await AUTH_API();
                await API.put('api/v1/user/passwordchange/', {
                    old_password: this.oldPassword,
                    new_password: this.newPassword
                })
                .then(response => {
                    alert('twoje hasło zostało zmienione')
                    this.$emit('passchanged')
                })
                .catch(error =>{
                    if(error.response.status === 400){
                        alert('Stare hasło jest błędne.')
                    }
                })
            }
        },
    }
</script>

<style scoped>
    .w40{
        width: 90%;
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