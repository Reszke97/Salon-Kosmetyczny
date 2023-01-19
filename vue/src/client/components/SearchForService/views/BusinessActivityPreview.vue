<template>
    <v-dialog
        :value="businessActivityPreview"
        dark
        hide-overlay
        fullscreen
        persistent
        transition="dialog-bottom-transition"
    >
        <v-card
            style="background-color: #0844a4"
        >
            <v-toolbar
                dark
                style="background-color: #3f51b5"
            >
                <v-btn
                    icon
                    @click="closePreview"
                >
                    <v-icon>mdi-close</v-icon>
                </v-btn>
                <v-toolbar-title>Podgląd firmy - {{businessActivityPreviewData.name}}</v-toolbar-title>
            </v-toolbar>
            <v-row
                justify="center"
                :style="{
                    height: `${screenSize.screenHeight + footerSize.footerHeight}px`,
                    paddingTop: '8px',
                    paddingBottom: '8px',
                }"
                class="mt-0 ml-0 mr-0"
            >
                <v-col 
                    id="appointment"
                    cols="11"
                    sm="9"
                    md="6"
                    lg="5" 
                    :style="{
                        backgroundColor:'#3f51b5',
                        height: '100%'
                    }"
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
                            :employees="employees"
                            :preview-employee="previewEmployee"
                        >
                        <template #employeePreviewDialog>
                            <manage-services-dialog
                                :employee-view-dialog="employeeViewDialog"
                                :get-services="getServices"
                                :services="services"
                                :closeEmployeeViewDialog="closeEmployeeViewDialog"
                            />
                        </template>
                        </business-activity-services>
                    </template>
                    <template v-else-if="businessInfoView">
                        <div style="display: flex; flex-direction: column; width:100%">
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
                                        v-if="Object.keys(businessActivityPreviewData).length"
                                        id="b-activity-img"
                                        :src="businessActivityPreviewData.image.image"
                                        style="width:100%;height: 100%;"
                                    />
                                    <h3 style="color:white"> {{ businessActivityPreviewData.name }} </h3>
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
                                                    <p style="padding: 0.4rem"> {{ businessActivityPreviewData.about }} </p>
                                                </div>
                                                <div style="display: flex; flex-direction: column">
                                                    <h4> Adres </h4>
                                                    <span style="padding: 0.4rem 0.4rem 0 0.4rem"> 
                                                        Miasto: {{ `${businessActivityPreviewData.city} ${businessActivityPreviewData.post_code}` }}
                                                    </span>
                                                    <span style="padding: 0 0.4rem"> Ulica: {{ 
                                                        `${businessActivityPreviewData.street} ${businessActivityPreviewData.house_number}${
                                                            businessActivityPreviewData.apartment_number ? '/' + businessActivityPreviewData.apartment_number : ""
                                                        }` 
                                                    }} </span>
                                                </div>
                                            </div>
                                        </div>
                                        <!-- <div
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
                                        </div> -->
                                    </div>
                                </v-col>
                            </v-row>
                            <manage-services-dialog
                                :employee-view-dialog="employeeViewDialog"
                                :get-services="getServices"
                                :services="services"
                                :closeEmployeeViewDialog="closeEmployeeViewDialog"
                            />
                        </div>
                        <!-- <div>
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
                        </div> -->
                    </template>
                </v-col>
            </v-row>
        </v-card>
    </v-dialog>
</template>

<script>
    import { ManageServicesDialog, BusinessActivityServices } from "../components"
    export default {
        name: "",
        components: {
            BusinessActivityServices,
            ManageServicesDialog,
        },
        props: {
            getServices: { type: Function, default: () => { } },
            services: { type: Object, default: () => {{}} },

            //here
            closePreview: { type: Function, default: () => {} },
            businessActivityPreview: { type: Boolean, default: () => false },
            businessActivityPreviewData: { type: Object, default: () => {{}} },
        },
        data: () => ({
            employeeViewDialog: false,
            businessInfoView: true,
        }),
        inject: ["screenSize", "navBarSize", "footerSize"],
        computed: {
            
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