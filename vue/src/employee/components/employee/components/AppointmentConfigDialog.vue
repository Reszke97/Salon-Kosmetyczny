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
                md="6"
                lg="3"
            >
                <div class="flex-centered">
                    <h1>Ustawienia wizyty</h1>
                </div>
                <v-form
                    ref="form"
                    v-model="valid"
                    lazy-validation
                >
                    <div>
                        <h3>Najpóźniejszy dostępny termin wizyty <br> od dnia dzisiejszego</h3>
                        <v-text-field
                            v-model="availabilityConfig.max_weeks_for_registration"
                            dark
                            label="Liczba tygodni"
                            persistent-hint
                            type="number"
                            :rules="numberRules"
                        />
                    </div>
                </v-form>
                <div class="d-flex flex-row mt-2">
                    <v-btn 
                        @click="$emit('closeAppointmentConfigDialog')"
                        color="success"
                    >
                    <v-icon left>
                        mdi-close-circle
                    </v-icon>
                    Zamknij
                    </v-btn>
                    <v-btn 
                        @click="updateAppointmentConfig"
                        class="ml-2"
                        color="success"
                    >
                        <v-icon left>
                            mdi-content-save-outline
                        </v-icon>
                        Zapisz
                    </v-btn>
                </div>
            </v-col>
        </v-row>
    </v-dialog>
</template>

<script>
    import { AUTH_API } from '../../../authorization/AuthAPI';

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
            numberRules: [
                v => (v && !v.includes(['+', '-']))  || 'Błędny format',
                v => (v && +v > 0) || 'Podana liczba musi być większa od 0'
            ],
            valid: true,
            availabilityConfig: {
                max_weeks_for_registration: "",
                min_time_for_registration: "",
            },
        }),
        computed: {
            
        },
        async created(){
            await this.getAppointmentConfig();
        },
        methods: {
            async updateAppointmentConfig(){
                this.$refs.form.validate();
                if(this.valid){
                    const API = await AUTH_API();
                    await API.put("api/v1/employee/availability-config/", {
                        ...this.availabilityConfig,
                        min_time_for_registration: this.availabilityConfig.min_time_for_registration + 'h'
                    })
                        .then(() => {
                            alert("Zapisano zmiany")
                        })
                        .catch(err => {
                            alert(err)
                        })
                }
            },
            async getAppointmentConfig(){
                const API = await AUTH_API();
                await API.get("api/v1/employee/availability-config/")
                    .then(res => {
                        this.availabilityConfig = {
                            max_weeks_for_registration: res.data.max_weeks_for_registration.toString(),
                            min_time_for_registration: res.data.min_time_for_registration.substring(
                                0, res.data.min_time_for_registration.indexOf('h')
                            ) 
                        }
                    });
            }
        }
    }
</script>