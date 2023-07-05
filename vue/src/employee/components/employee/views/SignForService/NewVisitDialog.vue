<template>
    <v-dialog
      :value="newVisitDialog"
      dark
      persistent
      :width="componentDims.width"
    >
      <v-row 
        class="bg-color white-text"
      >
        <v-col
          cols="12"
        >
            <h3>Tworzenie nowej wizyty dnia <span style="color:orange;">{{ newVisitData.date }}</span></h3>
            <v-select
                label="Wybór usługi"
            >

            </v-select>
            <div class="d-flex">
                <v-text-field
                    v-if="newVisitData.user_does_not_exists"
                    label="Podaj nazwę użytkownika"
                    :value="newVisitData.non_existent_user"
                    @change="val => $emit('updateNewVisitData', { key: 'non_existent_user', val: val })"
                >

                </v-text-field>
                <v-autocomplete
                    v-else
                    label="Wybór użytkownika"
                >

                </v-autocomplete>
                <v-checkbox
                    label="Brak użytkownika w liście"
                    :input-value="newVisitData.user_does_not_exists"
                    @change="val => $emit('updateNewVisitData', { key: 'user_does_not_exists', val: val })"
                >

                </v-checkbox>
            </div>
            <div class="d-flex">

                <v-btn
                    class="indigo"
                    dark
                    text
                    @click="$emit('closeNewVisitDialog')"
                >
                    Wybór godziny
                </v-btn>
                <v-btn
                    class="indigo ml-2"
                    dark
                    text
                    @click="$emit('closeNewVisitDialog')"
                >
                    Zamknij
                </v-btn>
            </div>
            <template name="signUpForVisit"/>
        </v-col>
      </v-row>
    </v-dialog>
</template>

<script>
    import { AUTH_API } from "../../../../authorization/AuthAPI"
    export default {
        name: "",
        components: {
            
        },
        props: {
            componentDims: { type: Object, required: true },
            newVisitDialog: { type: Boolean, required: true },
            newVisitData: { type: Object, required: true },
        },
        emits: [ "closeNewVisitDialog", "updateNewVisitData" ],
        data: () => ({
            chooseTimeDialog: false,
        }),
        computed: {
            
        },
        methods: {
            async getWorkHoursForGivenDate(){
                const API = await AUTH_API();
                //employee
                //date
                API.get("/api/v1/employee/new-visit/")
                .then(res => {

                })
                .catch(err => {
                    alert(err);
                })
            }
        }
    }
</script>