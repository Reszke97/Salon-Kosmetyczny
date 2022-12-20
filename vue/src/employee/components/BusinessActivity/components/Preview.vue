<template>
    <div 
        style="
            display: flex;
            flex-direction: row;
            width:100%;
            align-items:center;
        "
    >   
        <template v-if="!businessInfoView">
            <div>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            fab
                            small
                            dark
                            v-bind="attrs"
                            v-on="on"
                            @click="selectView({ businessViewSelected: true })"
                        >
                            <v-icon>mdi-arrow-left-bold</v-icon>
                        </v-btn>
                    </template>
                    <span>O firmie</span>
                </v-tooltip>
            </div>
            <business-activity-services

            >

            </business-activity-services>
        </template>
        <template v-else-if="businessInfoView">
            <div style="display: flex; flex-direction: column; width:100%">
                <back-to-first-tab
                    :set-tab="setTab"
                />
                <v-row
                    align="center"
                    justify="center"
                >
                    <v-col
                        cols="11"
                        sm="10"
                        md="10"
                        lg="10"
                    >
                        <img
                            v-if="businessActivity.image"
                            id="b-activity-img"
                            :src="businessActivity.image"
                            style="width:100%;height: 100%;"
                        />
                        <h3 style="color:white"> {{ businessActivity.name }} </h3>
                        <div 
                            style="
                                display: flex;
                                flex-direction: row;
                                width:100%;
                            "
                            class="mt-4"
                        >
                            <div 
                                style="
                                    display: flex;
                                    width: 100%;
                                    min-height: 300px;
                                    border: 1px solid rgb(8, 68, 164);
                                    border-radius: 1rem;
                                    background-color: rgb(8, 68, 164);
                                    color: white;
                                "
                            >
                                <div style="padding: 0.75rem">
                                    <div>
                                        <h4> O firmie </h4>
                                        <p style="padding: 0.4rem"> {{ businessActivity.about }} </p>
                                    </div>
                                    <div style="display: flex; flex-direction: column">
                                        <h4> Adres </h4>
                                        <span style="padding: 0.4rem 0.4rem 0 0.4rem"> Miasto: {{ `${businessActivity.city} ${businessActivity.post_code}` }} </span>
                                        <span style="padding: 0 0.4rem"> Ulica: {{ 
                                            `${businessActivity.street} ${businessActivity.house_number}${
                                                businessActivity.apartment_number ? '/' + businessActivity.apartment_number : ""
                                            }` 
                                        }} </span>
                                    </div>
                                </div>
                            </div>
                            <div
                                class="ml-2"
                                style="
                                    display: flex;
                                    flex-direction: column;
                                    width: 100%;
                                    min-height: 300px;
                                    border: 1px solid rgb(8, 68, 164);
                                    border-radius: 1rem;
                                    background-color: rgb(8, 68, 164);
                                    padding: 0.75rem;
                                "
                            >
                                <div style="color: white;">
                                    <h4> Pracownicy </h4>
                                </div>
                                <div 
                                    v-for="employee of employees"
                                    :key="employee.user.id"
                                    style="
                                        display: flex; 
                                        color: white;
                                        margin-top: 0.5rem;
                                        margin-bottom: 0.5rem;
                                    "
                                >
                                    <div 
                                        style="
                                            display: flex;
                                            margin: 0px 1rem 0rem 0rem;
                                        "
                                    >
                                        <v-avatar 
                                            color="#0844a4"
                                            size="40"
                                        >
                                            <v-tooltip bottom>
                                                <template v-slot:activator="{ on, attrs }">
                                                    <v-icon
                                                        :id="`employee-${employee.id}`"
                                                        style="font-size:40px"
                                                        v-if="!employee.avatar.image"
                                                        @click="() => previewEmployee(employee.id)"
                                                        dark
                                                    >
                                                        mdi-account-circle
                                                    </v-icon>
                                                    <img
                                                        class="avatar"
                                                        v-else
                                                        :src="employee.avatar.image"
                                                        style="width:100%;height: 100%;"
                                                        v-bind="attrs"
                                                        @click="() => previewEmployee(employee.id)"
                                                        v-on="on"
                                                    />
                                                </template>
                                                <span>Podgląd</span>
                                            </v-tooltip>
                                        </v-avatar>
                                    </div>
                                    <div 
                                        style="
                                            display: flex;
                                            flex-direction:column;
                                        "
                                    >
                                        <div>
                                            <span>
                                                {{ `${employee.user.first_name} ${employee.user.last_name}` }}
                                            </span>
                                        </div>
                                        <div>
                                            <span>
                                                {{ `${employee.spec.name}` }}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </v-col>
                </v-row>
                <v-dialog
                    class="serviceDialog"
                    id="serviceDialog"
                    v-model="employeeViewDialog"
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
            </div>
            <div>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            fab
                            small
                            dark
                            v-bind="attrs"
                            v-on="on"
                            @click="selectView({ businessViewSelected: false })"
                        >
                            <v-icon>mdi-arrow-right-bold</v-icon>
                        </v-btn>
                    </template>
                    <span>Usługi</span>
                </v-tooltip>
            </div>
        </template>
    </div>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI";
    import { appendMimeType } from "../../../utils/appendMimeType";
    import ManageServices from "../../service/components/ManageServices.vue";
    import BusinessActivityServices from "./BusinessActivityServices.vue";
    import BackToFirstTab from "./BackToFirstTab.vue";
    
    export default {
        name: "",
        components: {
            ManageServices,
            BusinessActivityServices,
            BackToFirstTab,
        },
        props: {
            setTab: { type: Function, required: true },
            getServices: { type: Function, required: true },
            getBusinessActivityData: { type: Function, required: true },
            services: { type: Object, default: () => {{}} },
        },
        data: () => ({
            businessActivity: {},
            employees: [],
            employeeViewDialog: false,
            businessInfoView: true,
        }),
        inject: ["screenSize"],
        computed: {
            
        },
        async created(){
            new Promise((resolve) => {
                this.getBusinessActivityData(resolve);
            })
            .then(res => {
                const { image } = res;
                delete res.image;
                this.businessActivity = res;
                if(image){
                    this.businessActivity.image = appendMimeType(image).image
                } else this.businessActivity.image = null;
            })
            .then( async () => {
                await this.getEmployees()
            })
        },
        methods: {
            async getEmployees(){
                const API = await AUTH_API();
                await API.get("api/v1/employee/business-activity-employees/")
                .then(res => {
                    this.employees = res.data.map(el => {
                        return {
                            ...el,
                            avatar: appendMimeType(el.avatar)
                        }
                    })
                })
            },
            async previewEmployee(employeeId){
                await this.getServices(employeeId);
                this.openEmployeeViewDialog();
            },

            openBusinessInfoView(){
                this.businessInfoView = true;
            },

            closeBusinessInfoView(){
                this.businessInfoView = false;
            },

            selectView({ businessViewSelected }){
                if(businessViewSelected) this.openBusinessInfoView();
                else this.closeBusinessInfoView();
            },

            openEmployeeViewDialog(){
                this.employeeViewDialog = true;
            },

            closeEmployeeViewDialog(){
                this.employeeViewDialog = false;
            },
        }
    }
</script>

<style>
    .avatar {
        cursor: pointer;
    }
</style>