<template>
    <v-row justify="center">
        <v-col
            class="bg-color"
            cols="12"
            sm="12"
            md="6"
            lg="3"
        >
            <v-card
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
                    dark
                    v-model="user_name"
                    label="Login"
                ></v-text-field>

                <v-text-field
                    dark
                    v-model="password1"
                    label="Hasło"
                    type="password"
                ></v-text-field>

                <div
                    class="flexible"
                >
                    <div
                        style="color:white;"
                        class="flex; flex-row"
                    >
                        <p>Nie pamiętasz hasła? <a class="font-bold" href="http://localhost:8080/employee/passwordresetemailsend">Zresetuj hasło</a></p>
                        <p>Nie masz konta? <a class="font-bold" href="http://localhost:8080/employee/register">Zarejestruj się</a></p>
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
        </v-col>
    </v-row>
</template>
<script>
    import axios from 'axios'
    export default {
        data: () => ({
            valid: true,
            route: null,
            user_name: "",
            password1: "",
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
                axios.post('http://127.0.0.1:8000/api/v1/employee/token/', {
                    user_name: this.user_name,
                    password: this.password1,
                    type: 'login'
                })
                .then(response => {
                    localStorage.setItem( 'employeeToken', response.data.access );
                    localStorage.setItem( 'employeeRefreshToken', response.data.refresh );
                    window.location.href = '/employee'
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