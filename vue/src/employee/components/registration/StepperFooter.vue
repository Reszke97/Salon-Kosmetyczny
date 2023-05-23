<template>
    <v-row
        class="v-stepper__content"
    >
        <v-col
            cols="11"
            sm="9"
            md="6"
            lg="5"
        >
            <v-btn
                color="success"
                @click="$emit('submit')"
                style="width:100%!important"
            >
                Zapisz
            </v-btn>
        </v-col>
    </v-row>
</template>

<script>
    export default {
        name: "",
        components: {
            
        },
        props: {
            valid: { type: Boolean, default: true }
        },
        emits: [ "reset", "submit" ],
        data: () => ({
            
        }),
        computed: {
            
        },
        methods: {
            
        }
    }
</script>