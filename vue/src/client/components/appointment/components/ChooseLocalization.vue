<template>
    <v-dialog
        :value="chooseLocalizationDialogOpen"
        dark
    >
        <div
            :style="{
                backgroundColor:'#0844a4!important',
                display: 'flex',
                flexDirection: 'column',
                width: containerWidth + 'px',
                justifyContent: 'center',
                alignItems: 'center',
                color: 'white',
            }"
        >
            <v-col 
                cols="11"
                sm="9"
                md="6"
                lg="5" 
            >
                <h3>
                    Podaj Lokalizację
                </h3>
            </v-col>
            <v-col 
                cols="11"
                sm="9"
                md="6"
                lg="5" 
            >
                <v-text-field
                    :value="inputVariables.selectedCity"
                    dark
                    :menu-props="{ maxHeight: '400' }"
                    label="Miejscowość"
                    hint="Podaj nazwę miejscowości"
                    persistent-hint
                    @change="(val) => (setInputVariable({ key: 'selectedCity', val: val }))"
                ></v-text-field>
            </v-col>
            <v-col 
                cols="11"
                sm="9"
                md="6"
                lg="5" 
            >
                <v-text-field
                    :value="inputVariables.selectedPostCode"
                    dark
                    :menu-props="{ maxHeight: '400' }"
                    label="Kod Pocztowy"
                    hint="Podaj kod pocztowy"
                    persistent-hint
                    @change="(val) => (setInputVariable({ key: 'selectedPostCode', val: val }))"
                ></v-text-field>
            </v-col>
            <v-col 
                cols="11"
                sm="9"
                md="6"
                lg="5" 
            >
                <v-btn 
                    class="my-2 mx-2"
                    color="success"
                    @click="closeDialogAndSetStarted"
                >
                    Zapisz
                </v-btn>
                <v-btn 
                    class="my-2 mx-2"
                    text
                    dark
                    @click="closeLocalizationDialog"
                >
                    Zamknij
                </v-btn>
            </v-col>
        </div>
    </v-dialog>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI";
    
    export default {
        name: "",
        components: {
            
        },
        props: {
            inputVariables: { type: Object, required: true , }, 
            chooseLocalizationDialogOpen: { type: Boolean, default: true },
            closeLocalizationDialog: { type: Function, default: () => {} },
            setInputVariable: { type: Function, default: () => {} },
            setStarted: { type: Function, default: () => {} },
            containerHeight: { type: Number, required: true },
            containerWidth: { type: Number, required: true },
        },
        data: () => ({
            
        }),
        computed: {
            
        },
        methods: {
            closeDialogAndSetStarted(){
                this.setStarted();
                this.closeLocalizationDialog();
            }
        }
    }
</script>