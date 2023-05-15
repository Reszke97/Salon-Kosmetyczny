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
                    ref="ownerForm"
                    lazy-validation
                >
                    <v-text-field
                        :value="ownerInfo.name"
                        :rules="nameRules"
                        label="Imię"
                        required
                        @change="val => $emit('setOwnerInfo', { val: val, prop: 'name' })"
                    ></v-text-field>

                    <v-text-field
                        :value="ownerInfo.lastName"
                        :rules="lastNameRules"
                        label="Nazwisko"
                        required
                        @change="val => $emit('setOwnerInfo', { val: val, prop: 'lastName' })"
                    ></v-text-field>
                    <v-autocomplete
                        v-if="!ownerInfo.isNewSpec"
                        :value="ownerInfo.selectedSpec"
                        :items="defaultSpecializations"
                        item-text="label"
                        item-value="value"
                        label="Specjalność"
                        placeholder="Wybierz specjalność"
                        hint="Kliknij na ikonę aby dodać własną specjalność."
                        persistent-hint
                        @change="val => $emit('setOwnerInfo', { val: val, prop: 'selectedSpec' })"
                    >
                        <template #append-outer>
                            <v-btn
                                icon
                                @click="$emit('toggleSpecInput')"
                            >
                                <v-icon>
                                    mdi-swap-horizontal
                                </v-icon>
                            </v-btn>
                        </template>
                    </v-autocomplete>

                    <v-text-field
                        v-if="ownerInfo.isNewSpec"
                        :value="ownerInfo.selectedSpec"
                        label="Specjalność"
                        placeholder="Podaj specjalność"
                        hint="Kliknij na ikonę aby wybrać specjalność z listy."
                        persistent-hint
                        @change="val => $emit('setOwnerInfo', { val: val, prop: 'selectedSpec' })"
                    >
                        <template #append-outer>
                            <v-btn
                                icon
                                @click="$emit('toggleSpecInput')"
                            >
                                <v-icon>
                                    mdi-keyboard-backspace 
                                </v-icon>
                            </v-btn>
                        </template>
                    </v-text-field>

                    <v-text-field
                        :value="ownerInfo.email"
                        :rules="emailRules"
                        label="E-mail"
                        required
                        @change="val => $emit('setOwnerInfo', { val: val, prop: 'email' })"
                    ></v-text-field>

                    <v-text-field
                        :value="ownerInfo.userName"
                        :rules="userNameRules"
                        :counter="10"
                        label="Nazwa użytkownika"
                        required
                        @change="val => $emit('setOwnerInfo', { val: val, prop: 'userName' })"
                    ></v-text-field>

                    <v-text-field
                        :value="ownerInfo.password1"
                        :rules="[
                            ...password1Rules,
                            ownerInfo.password1 === ownerInfo.password2 || 'Podane hasła się nie zgadzają'
                        ]"
                        label="Hasło"
                        required
                        type="password"
                        @change="val => $emit('setOwnerInfo', { val: val, prop: 'password1' })"
                    ></v-text-field>

                    <v-text-field
                        :value="ownerInfo.password2"
                        :rules="[
                            ...password2Rules,
                            ownerInfo.password1 === ownerInfo.password2 || 'Podane hasła się nie zgadzają'
                        ]"
                        label="Potwierdź hasło"
                        required
                        type="password"
                        @change="val => $emit('setOwnerInfo', { val: val, prop: 'password2' })"
                    ></v-text-field>
                </v-form>
            </v-col>
        </v-row>
    </div>
</template>
<script>
    export default {
        props: {
            ownerInfo: { type: Object, required: true },
            defaultSpecializations: { type: Array, default: () => ([]) },
        },
        emits: [ "setOwnerInfo", "toggleSpecInput" ],
        data: () => ({
            emailRules: [
                v => !!v || 'E-mail jest wymagany',
                v => /.+@.+\..+/.test(v) || 'E-mail musi być poprawny przykład:\n example@mail.com',
            ],
            userNameRules: [
                v => !!v || 'Nazwa użytkownika jest wymagana',
            ],
            password1Rules: [
                v => !!v || 'Hasło jest wymagane',
            ],
            password2Rules: [
                v => !!v || 'Potwierdzenie Hasła jest wymagane'
            ],
            nameRules: [
                v => !!v || 'Imię jest wymagane',
            ],
            lastNameRules: [
                v => !!v || 'Nazwisko jest wymagane',
            ],
        }),
        methods: {
            reset () {
                this.$refs.form.resetValidation()
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