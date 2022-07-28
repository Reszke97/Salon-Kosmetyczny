<template>
    <v-row>
        <v-col>
            <v-row style="text-align:center;color:white;" class="">
                <v-col>
                    <h1 style="font-weight:500!important">O aplikacji</h1>
                </v-col>
                <p style="font-weight:500!important" class="px-4">
                    Aplikacja <b>Salon Kosmetyczny dla klienta</b> umożliwia zapisanie się na usługę 
                    do wybranego pracownika salonu kosmetycznego.
                </p>
            </v-row>
            <v-row style="text-align:center;color:white;" justify="center" class="mt-0">
                <v-col :cols="6">
                    <div>
                        Nie masz konta?
                    </div>
                    <div class="pt-2">
                        <v-btn color="primary">
                            Zarejestruj się
                        </v-btn>
                    </div>
                </v-col>
            </v-row>
        </v-col>
    </v-row>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI";
    
    export default {
        name: "",
        components: {
            
        },
        props: {
            
        },
        data: () => ({
            model: 0,
            colors: [
                'primary',
                'secondary',
                'yellow darken-2',
                'red',
                'orange',
            ],
        }),
        computed: {
            
        },
        methods: {
            
        }
    }
</script>