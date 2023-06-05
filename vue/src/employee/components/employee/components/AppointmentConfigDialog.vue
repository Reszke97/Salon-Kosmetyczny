<template>
    <v-dialog
        id="appointment-config-dialog"
        :value="appointmentConfigDialog"
        persistent
        width="100%"
    >
        <v-row 
            class="fill-height white-text"
            justify="center"
            :style="{
                maxHeight: `${screenSize.screenHeight - 60}px`,
            }"
        >
            <v-col
                class="bg-color"
                cols="12"
                sm="12"
                md="8"
                lg="5"
            >
                <div class="flex-centered">
                    <h1>Ustawienia wizyty</h1>
                </div>
                <div>
                    <v-btn 
                        @click="$emit('closeAppointmentConfigDialog')"
                        class="mt-2"
                        color="success"
                    >
                        Zamknij
                    </v-btn>
                </div>
            </v-col>
        </v-row>
    </v-dialog>
</template>

<script>
    export default {
        name: "",
        components: {
            
        },
        emits: [ "closeAppointmentConfigDialog" ],
        inject: ["screenSize"],
        props: {
            appointmentConfigDialog: { type: Boolean, required: true }
        },
        data: () => ({
            
        }),
        computed: {
            
        },
        methods: {
            
        }
    }
</script>