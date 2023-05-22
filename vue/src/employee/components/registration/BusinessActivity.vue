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
                        :rules="[ v => !!v || 'Pole wymagane', ]"
                        label="Nazwa salonu"
                        required
                        @change="val => $emit('setSalonInfo', { prop: 'name', val: val })"
                    ></v-text-field>
                    <v-text-field
                        :value="salonInfo.street"
                        :rules="[ v => !!v || 'Pole wymagane', ]"
                        label="Ulica"
                        required
                        @change="val => $emit('setSalonInfo', { prop: 'street', val: val })"
                    ></v-text-field>
                    <v-text-field
                        :value="salonInfo.house_number"
                        :rules="[ v => !!v || 'Pole wymagane', ]"
                        label="Nr domu"
                        required
                        @change="val => $emit('setSalonInfo', { prop: 'house_number', val: val })"
                    ></v-text-field>
                    <v-text-field
                        :value="salonInfo.apartment_number"
                        label="Nr lokalu"
                        @change="val => $emit('setSalonInfo', { prop: 'apartment_number', val: val })"
                    ></v-text-field>
                    <v-text-field
                        :value="salonInfo.city"
                        :rules="[ v => !!v || 'Pole wymagane', ]"
                        required
                        label="Miasto"
                        @change="val => $emit('setSalonInfo', { prop: 'city', val: val })"
                    ></v-text-field>
                    <div :style="
                        (!salonInfo.post_code_part2 || !salonInfo.post_code_part1) && !valid
                        ? { color:'#f44336 !important' } 
                        : { color: 'inherit' }"
                    > Kod pocztowy </div>
                    <div class="d-flex flex-row">
                        <div style="width:50px" class="mr-2">
                            <v-text-field
                                :value="salonInfo.post_code_part1"
                                :counter="2"
                                :rules="[ v => !!v || '', ]"
                                required
                                @change="val => $emit('setSalonInfo', { prop: 'post_code_part1', val: val })"
                            ></v-text-field>
                        </div>
                        <div 
                            class="flex-centered"
                            :style="
                                (!salonInfo.post_code_part2 || !salonInfo.post_code_part1) && !valid
                                ? { color:'#f44336 !important' } 
                                : { color: 'inherit' }
                            "
                        ><span>-</span></div>
                        <div style="width:50px" class="ml-2 d-flex justify-end">
                            <v-text-field
                                :value="salonInfo.post_code_part2"
                                :counter="3"
                                :rules="[ v => !!v || '', ]"
                                required
                                @change="val => $emit('setSalonInfo', { prop: 'post_code_part2', val: val })"
                            ></v-text-field>
                        </div>
                    </div>
                    <template
                        v-if="(!salonInfo.post_code_part2 || !salonInfo.post_code_part1) && !valid" 
                    >
                        <div id="postcode-error" class="mt-1">
                            <v-divider />
                        </div>
                        <div 
                            class="v-text-field__details mt-2"
                        >
                            <div class="v-messages theme--dark error--text" role="alert">
                                <div class="v-messages__wrapper">
                                    <div class="v-messages__message">Pola wymagane</div>
                                </div>
                            </div>
                        </div>
                    </template>
                </v-form>
            </v-col>
        </v-row>
    </div>
</template>
<script>
    export default {
        props: {
            salonInfo: { type: Object, default: () => ({}) },
            valid: { type: Boolean, default: true },
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
    #postcode-error .theme--dark.v-divider {
        border-color: #f44336 !important;
    }
</style>
</template>