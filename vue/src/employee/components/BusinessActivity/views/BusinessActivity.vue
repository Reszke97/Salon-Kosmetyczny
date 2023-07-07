<template>
    <v-row
        id="b-activity-main-container"
        style="
            height:100%
        "
        align="center"
        justify="center"
    >
        <v-col
            cols="12"
            sm="12"
            md="8"
            lg="6"
            style="
                height:100%;
                background-color:#3f51b5;
            "
        >
            <v-toolbar
                v-if="toolbarVisible"
                id="my-tab"
                flat
                style="
                    min-height:112px!important;
                    background-color:#3f51b5;
                "
            >
                <v-spacer></v-spacer>

                <template v-slot:extension>
                    <v-tabs
                        v-model="tabs"
                        centered
                        icons-and-text
                        @change="(val) => setView(val)"
                    >
                        <v-tabs-slider ></v-tabs-slider>
                        <v-tab
                            href="#tab-1"
                            class="primary--text px-3"
                            style="width:100%;"
                        >
                            Edycja
                            <v-icon>mdi-pencil</v-icon>
                        </v-tab>
                        <v-tab
                            href="#tab-2"
                            class="primary--text px-3"
                            style="width:100%;"
                        >
                            Podgląd
                            <v-icon>mdi-eye</v-icon>
                        </v-tab>
                        <v-tab
                            href="#tab-3"
                            class="primary--text px-3"
                            style="width:100%;"
                        >
                            Dodaj pracownika
                            <v-icon>mdi-account-plus </v-icon>
                        </v-tab>
                    </v-tabs>
                </template>
            </v-toolbar>

            <v-tabs-items 
                v-model="tabs"
                :style="`
                    height: ${tabs == 'tab-2' ? '100%' : 'calc(100% - 112px)'} ;
                    background-color:#3f51b5!important
                `"
            >
                <v-tab-item
                    :value="'tab-1'"
                    style="height:100%;overflow-y:auto;overflow-x:hidden"
                >
                    <edit
                        :get-business-activity-data="getBusinessActivityData"
                    >
                    </edit>
                </v-tab-item>

                <v-tab-item
                    :value="'tab-2'"
                    style="height:100%;overflow-y:auto;overflow-x:hidden"
                >
                    <preview
                        :get-business-activity-data="getBusinessActivityData"
                        :set-tab="setTab"
                        :get-services="getServices"
                        :services="employeeServices"
                    >
                    </preview>
                </v-tab-item>
                <v-tab-item
                    :value="'tab-3'"
                    id="tab-3"
                    style="height:100%;overflow-y:auto;overflow-x:hidden"
                >
                    <add-employee
                    />
                </v-tab-item>
            </v-tabs-items>
        </v-col>
    </v-row>
</template>

<script>
    import Edit from "../components/Edit.vue";
    import Preview from "../components/Preview.vue";
    import AddEmployee from "../../registration/AddEmployee.vue";
    import { AUTH_API } from "../../../authorization/AuthAPI";
    
    export default {
        name: "BusinessActivity",
        props: {

        },
        components: {
            Edit,
            Preview,
            AddEmployee,
        },
        data: () => ({
           tabs: null,
           businessActivity: {},
           toolbarVisible: true,
           employeeServices: {},
           employees: [],
        }),
        provide(){
        },
        inject: ["screenSize"],
        methods: {
            async getBusinessActivityData(resolve){
                const API = await AUTH_API();
                await API.get("api/v1/employee/business-activity/")
                    .then(res => {
                        this.employees = res.data.employees
                        resolve(res.data)
                    })
            },

            setTab(val){
                this.toolbarVisible = true;
                this.tabs = val;
            },

            setView(val){
                if(val === "tab-2"){
                    this.toolbarVisible = false;
                }
                else{
                    this.toolbarVisible = true;
                }
            },

            appendMimeType(image){
                let type;
                switch (image.file_type) {
                    case "PNG":
                        type = "data:image/png;base64,";
                    break;
                    case "JPG":
                        type = "data:image/jpg;base64,";
                    break;
                    case "JPEG":
                        type = "data:image/jpeg;base64,";
                    break;
                    default:
                        type = "";
                }
                return { ...image, image: type + image.image, isFromDB: true };
            },

            mapImagesType(services){
                services.service_info.forEach((service, idx) => {
                    this.employeeServices.service_info[idx].employee_image = service.employee_image.map((el) => {
                        return this.appendMimeType(el)
                    });
                })
                if(this.employeeServices.avatar) this.employeeServices.avatar = { ...this.appendMimeType(services.avatar) }
            },

            groupByCategory(employeeConfig){
                let groupedServices = {
                    avatar: employeeConfig.avatar,
                    employee_info: employeeConfig.employee_info,
                    categories: [],
                }
                const uniqueCategories = [
                    ...new Map(employeeConfig.service_info.map(item =>[item.category.category_id, item.category])).values()
                ];

                let categoryIdx = 0;
                for(const category of uniqueCategories){
                    const items = employeeConfig.service_info.filter(el => el.category.category_id === category.category_id)
                    groupedServices.categories.push({
                        name: category.name,
                        category_id: category.category_id,
                        id: category.category_display_order,
                        services: [...items]
                    });
                    categoryIdx += 1;
                } return groupedServices
            },

            async getServices(employeeId){
                const API = await AUTH_API();
                await API.get(`/api/v1/employee/service/?preview=${employeeId}`)
                    .then(res => {
                        res.data.service_info = res.data.service_info.map(el => {
                            const { service } = el
                            const { service_category } = service
                            delete service.service_category
                            return { 
                                employee_image: el.employee_image,
                                employee_comment: el.employee_comments,
                                employee_service_config_id: el.employee_service_config_id,
                                image_set_id: el.image_set_id,
                                service: { ...service }, 
                                category: { ...service_category, is_new: false, category: service_category.category_id, }
                            }
                        })
                        const _employee = this.employees.find(el => el.employee_id === employeeId);
                        this.employeeServices = {... res.data, employee_info: {
                            "name": _employee.first_name,
                            "last_name": _employee.last_name,
                            "spec_name": _employee.spec_name,
                        }};
                    })
                this.mapImagesType(this.employeeServices);
                this.employeeServices = { ...this.groupByCategory(this.employeeServices) }
            },
        },
    }
</script>

<style type="text/css">
</style>