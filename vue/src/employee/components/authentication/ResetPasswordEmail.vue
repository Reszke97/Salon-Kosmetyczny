<template>
    <div>
        <v-form
            ref="form"
            v-model="valid"
            lazy-validation
            class = "mt1"
        >
            <v-text-field
                v-model="email"
                label="Email"
                required
                class="w40"
            ></v-text-field>

            <div
                class="w40"
            >
                <v-btn
                    color="success"
                    class="mr-4"
                    @click="submit"
                >
                    Wyślij
                </v-btn>

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
            email:'',
            newPasswordRules: [
                v => !!v || 'Hasło jest wymagane',
                // v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],
            oldPassword:'',
            oldPasswordRules: [
                v => !!v || 'Hasło jest wymagane',
                // v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],
        }),
        
        created(){
            this.route = this.$route.params.activated
            console.log(this.route = this.$route.params.activated)
        },
        methods: {
            submit () {
                // const IS_VALID = this.$refs.form.validate()
                // if(IS_VALID){
                //     this.passwordChange()
                // }
                console.log(this.email)
                axios.post('http://127.0.0.1:8000/api/user/requestpasswordreset/',{
                    email: this.email
                })
            },
            async passwordChange(){
                const API = await AUTH_API();
                
                API.put('api/user/passwordchange/', {
                    old_password: this.oldPassword,
                    new_password: this.newPassword
                })
                .then(response => {
                    alert('twoje hasło zostało zmienione')
                    // if(response){
                    //     console.log(response)
                    //     alert('twoje hasło zostało zmienione')
                    // }
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