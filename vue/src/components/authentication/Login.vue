<template>
    <div
        class="w40"
    >
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
            class = "mt1 w100"
        >
            <v-text-field
                v-model="email"
                :rules="emailRules"
                label="E-mail"
                required
            ></v-text-field>

            <v-text-field
                v-model="password1"
                :rules="password1Rules"
                label="Hasło"
                required
                type="password"
            ></v-text-field>

            <div
                class="flexible"
            >
                <div
                    class="buttonContainer"
                >
                    <p>Nie pamiętasz hasła?</p>
                </div>
            </div>
            <div
                class="flexible"
            >
                <div
                    class="buttonContainer"
                >
                    <v-btn
                        class="success"
                        @click="submit"
                    >
                        Zaloguj
                    </v-btn>
                </div>
            </div>
        </v-form>
    </div>
</template>
<script>
    import { AUTH_API } from '../../authorization/AuthAPI'
    import axios from 'axios'
    export default {
        data: () => ({
            valid: true,
            route: null,
            email: '',
            emailRules: [
                v => !!v || 'E-mail jest wymagany',
                v => /.+@.+\..+/.test(v) || 'E-mail musi być poprawny przykład:\n example@mail.com',
            ],
            password1:'',
            password1Rules: [
                v => !!v || 'Hasło jest wymagane',
            ],
        }),
        
        created(){
            this.route = this.$route.params.activated
        },
        methods: {
            submit () {
                const IS_VALID = this.$refs.form.validate()
                if(IS_VALID){
                    this.login()
                }
            },
            login(){
                axios.post('http://127.0.0.1:8000/api/v1/token/', {
                    email: this.email,
                    password: this.password1,
                    type: 'login'
                })
                .then(response => {
                    this.$store.commit('setToken', {
                        access: response.data.access,
                        refresh: response.data.refresh
                    })
                    this.$store.commit('setIsAuthenticated', true)
                    
                })
                .then(()=>{
                    AUTH_API.get('/api/v1/user/getuserrole/')
                    .then(response=>{
                        this.$store.commit('setRole', response.data.role)
                        this.$router.push({name: 'Home' })
                    })
                })
                .catch(error =>{
                    if(error.response.data.detail === 'No active account found with the given credentials'){
                        alert('Podano błędny login lub hasło.')
                    }
                })
            },
        },
    }
</script>

<style scoped>
    .w40{
        width: 30%;
        min-width: 230px;
        display: flex;
        margin-left: auto;
        margin-right: auto;
    }
    .flexible{
        width: 100%;
        display: flex;
        margin-left: auto;
        margin-right: auto;
    }
    .w100{
        width: 100%;
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
    .buttonContainer{
        display: flex;
        width: 100%;
        height: 2rem
    }
    .top-filter{
    position: sticky;
    top: 0;
    z-index: 2;
    }
</style>