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
                    ref="businessForm"
                    lazy-validation
                >
                    <v-text-field
                        :value="salonInfo.name"
                        label="Nazwa salonu"
                        required
                        @change="val => $emit('setSalonInfo', { prop: 'name', val: val })"
                    ></v-text-field>
                    <v-row>
                        <v-col cols="6">

                        </v-col>
                        <v-col cols="6">

                        </v-col>
                    </v-row>
                    <v-text-field
                        :value="salonInfo.street"
                        label="Ulica"
                        required
                        @change="val => $emit('setSalonInfo', { prop: 'street', val: val })"
                    ></v-text-field>
                    <v-text-field
                        :value="salonInfo.house_number"
                        label="Nr domu"
                        required
                        @change="val => $emit('setSalonInfo', { prop: 'house_number', val: val })"
                    ></v-text-field>
                    <v-text-field
                        :value="salonInfo.apartment_number"
                        label="Nr lokalu"
                        @change="val => $emit('setSalonInfo', { prop: 'apartment_number', val: val })"
                    ></v-text-field>
                </v-form>
            </v-col>
        </v-row>
    </div>
</template>
<script>
    export default {
        props: {
            salonInfo: { type: Object, default: () => ({}) },
        },
        emits: [ "setSalonInfo" ],
        data: () => ({
        }),
        methods: {
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
</template>