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
                    :value="inputData.valid"
                    lazy-validation
                    @input="(event) => setInput(event, 'valid')"
                >
                    <v-text-field
                        :value="inputData.name"
                        :rules="nameRules"
                        label="Imię"
                        :counter="50"
                        required
                        @input="(event) => setInput(event, 'name')"
                    ></v-text-field>

                    <v-text-field
                        :value="inputData.lastName"
                        :rules="lastNameRules"
                        label="Nazwisko"
                        :counter="50"
                        required
                        @input="(event) => setInput(event, 'lastName')"
                    ></v-text-field>

                    <v-text-field
                        :value="inputData.email"
                        :rules="emailRules"
                        label="E-mail"
                        required
                        @input="(event) => setInput(event, 'email')"
                    ></v-text-field>

                    <v-text-field
                        :value="inputData.userName"
                        :rules="userNameRules"
                        :counter="10"
                        label="Nazwa użytkownika"
                        required
                        @input="(event) => setInput(event, 'userName')"
                    ></v-text-field>

                    <v-text-field
                        :value="inputData.password1"
                        :rules="password1Rules"
                        label="Hasło"
                        required
                        type="password"
                        @input="(event) => setInput(event, 'password1')"
                    ></v-text-field>

                    <v-text-field
                        :value="inputData.password2"
                        :rules="password2Rules"
                        label="Potwierdź hasło"
                        required
                        type="password"
                        @input="(event) => setInput(event, 'password2')"
                    ></v-text-field>
                </v-form>
            </v-col>
        </v-row>
    </div>
</template>
<script>
    export default {
        props: {
            inputData: {
                type: Object,
                required: true
            },
            setInput: {
                type: Function,
                required: true
            },
        },
        data: () => ({
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
            validate() {
                return this.$refs.form.validate();
            },
            resetValidation(){
                this.$refs.form.resetValidation()
            }
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