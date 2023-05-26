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
                class = "mt1"
            >
                <v-card
                    v-if="showMessage"
                    class = "message mb-2 px-2"
                    color = "#FFFEE9"
                >
                    Instrukcję do zmiany hasła zostały przesłane, na podany adres e-mail.
                </v-card>
                <h3 style="color:white">
                    Resetowanie hasła
                </h3>
                <v-text-field
                    dark
                    v-model="email"
                    label="Email"
                    required
                ></v-text-field>

                <div>
                    <v-btn
                        color="success"
                        class="mr-4"
                        @click="submit"
                    >
                        Wyślij
                    </v-btn>

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
            email: "",
            showMessage: false,
        }),
        
        created(){
            this.route = this.$route.params.activated
        },
        methods: {
            submit () {
                console.log(this.email)
                axios.post('http://127.0.0.1:8000/api/v1/user/requestpasswordreset/',{
                    email: this.email
                })
                .then(() => {
                    this.showMessage = true;
                })
            },
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
        text-align: justify;
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