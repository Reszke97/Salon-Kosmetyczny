<template>
    <v-dialog
        id="availability-dialog"
        :value="availabilityDialog"
        persistent
        width="100%"
        style="box-shadow:none!important"
    >
        <v-row 
            class="fill-height" 
            justify="center"
            :style="{
                height: `${screenSize.screenHeight - 75}px`,
            }"
        >
            <v-col
                style="background-color: #0844a4!important"
                cols="12"
                sm="12"
                md="8"
                lg="6"
            >
                <h1>Hello</h1>
                <v-btn @click="$emit('closeAvailabilityDialog')">
                    Zamknij
                </v-btn>
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
        emits: [ "closeAvailabilityDialog" ],
        inject: ["screenSize"],
        props: {
            availabilityDialog: { type: Boolean, default: false },
        },
        data: () => ({
            
        }),
        computed: {
            
        },
        methods: {
            
        }
    }
</script>