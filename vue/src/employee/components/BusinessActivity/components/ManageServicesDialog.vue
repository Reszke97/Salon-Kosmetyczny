<template>
    <v-dialog
        class="serviceDialog"
        id="serviceDialog"
        v-model="employeeViewDialog"
        width="auto"
    >
        <manage-services
            :get-services="getServices"
            :services="services"
            :isInDialog="true"
        >
            <template #header>
                <div
                    style="
                        display: flex;
                        justify-content: end;
                    "
                >
                    <div
                        class="mr-8"
                        :style="`
                            display: flex;
                        `"
                    >
                        <v-btn
                            style=" background: rgb(8, 68, 164)!important;"
                            class="mr-0"
                            color="primary"
                            @click="closeEmployeeViewDialog"
                        >
                            Zamknij
                        </v-btn>
                    </div>
                </div>
            </template>
        </manage-services>
    </v-dialog>
</template>

<script>
    import ManageServices from "../../service/components/ManageServices.vue";
    export default {
        name: "",
        components: {
            ManageServices,
        },
        props: {
            employeeViewDialog: { type: Boolean, default: false },
            getServices: { type: Function, required: true },
            closeEmployeeViewDialog: { type: Function, required: true },
            services: { type: Object, default: () => {{}} },
        },
        data: () => ({
            
        }),
        computed: {
            
        },
        methods: {
            
        }
    }
</script>