<template>
    <v-dialog
        :value="activationDialog"
        width="500"
    >
        <v-card>
            <v-card-title class="text-h5 grey lighten-2">
                Na podany email został przesłany link do aktywacji konta.
            </v-card-title>

            <v-divider></v-divider>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    color="primary"
                    text
                    @click="$emit('closeActivateDialog')"
                >
                    Zamknij
                </v-btn>
                <v-btn
                    color="primary"
                    text
                >
                    Przejdź do logowania
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
    export default {
        name: "",
        components: {
            
        },
        props: {
            activationDialog: { type: Boolean, default: false },
        },
        emits: [ "closeActivateDialog" ],
        data: () => ({
            
        }),
        computed: {
            
        },
        methods: {
            
        }
    }
</script>