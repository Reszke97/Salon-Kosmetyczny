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
            style="
                background-color: #0844a4;
                overflow: hidden;
            "
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
                        height: '100%',
                        overflow: 'auto'
                    }"
                >
                    <div style="display: flex; flex-direction: row">
                        <div style="display: flex; width: 100%">
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
                                    :employees="businessActivityPreviewData.employees"
                                    :business-activity-categories="businessActivityPreviewData.categories"
                                    :preview-employee="previewEmployee"
                                >
                                    <template #employeePreviewDialog>
                                        <manage-services-dialog
                                            :employee-view-dialog="employeeViewDialog"
                                            :services="services"
                                            :closeEmployeeViewDialog="closeEmployeeViewDialog"
                                        />
                                    </template>
                                </business-activity-services>
                            </template>
                            <template v-else-if="businessInfoView">
                                <div style="display: flex; flex-direction: row; width:100%">
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

                                        <a
                                            v-if="Object.keys(businessActivityPreviewData).length && businessActivityPreviewData.image"
                                            @click="openImg(businessActivityPreviewData.image.image)"
                                        >
                                            <img
                                                id="b-activity-img"
                                                :src="businessActivityPreviewData.image.image"
                                                style="width:100%;height: 100%;"
                                            />
                                        </a>
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
                                                        v-for="employee of businessActivityPreviewData.employees"
                                                        :key="employee.user_id"
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
                                                                            @click="() => previewEmployee(employee)"
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
                                                                            @click="() => previewEmployee(employee)"
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
                                                                    {{ `${employee.first_name} ${employee.last_name}` }}
                                                                </span>
                                                            </div>
                                                            <div>
                                                                <span>
                                                                    {{ `${employee.spec_name}` }}
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </v-col>
                                    </v-row>
                                    <manage-services-dialog
                                        v-if="businessInfoView"
                                        :employee-view-dialog="employeeViewDialog"
                                        :services="services"
                                        :closeEmployeeViewDialog="closeEmployeeViewDialog"
                                    />
                                </div>
                                <div style="display: flex; align-items: center;">
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
                    </div>
                </v-col>
                <v-dialog
                    id="showImagePreview"
                    v-model="showImagePreview"
                    style="overflow: hidden!important;"
                    v-if="showImagePreview"
                >
                    <v-img
                        :src="selectedImg"
                        style="width:auto;height: auto"
                    />
                    <v-btn
                        dark
                        color="secondary"
                        @click="closeImg"
                        class="mr-2"
                    >
                        Zamknij
                    </v-btn>
                </v-dialog>
            </v-row>
        </v-card>
    </v-dialog>
</template>

<script>
    import axios from "axios";
    import { ManageServicesDialog, BusinessActivityServices } from "../components"
    export default {
        name: "",
        components: {
            BusinessActivityServices,
            ManageServicesDialog,
        },
        props: {
            closePreview: { type: Function, default: () => {} },
            businessActivityPreview: { type: Boolean, default: () => false },
            businessActivityPreviewData: { type: Object, default: () => {{}} },
        },
        data: () => ({
            showImagePreview: false,
            selectedImg: "",
            employeeViewDialog: false,
            businessInfoView: true,
            services: {},
        }),
        inject: ["screenSize", "navBarSize", "footerSize"],
        computed: {
            
        },
        methods: {
            closeImg(){
                this.showImagePreview = false;
            },
            openImg(dataUrl){
                this.selectedImg = dataUrl;
                this.showImagePreview = true;
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
                    this.services.service_info[idx].employee_image = service.employee_image.map((el) => {
                        return this.appendMimeType(el)
                    });
                })
                if(services.avatar) this.services.avatar = { ...this.appendMimeType(services.avatar) }
            },
            groupByCategory(employeeConfig){
                let groupedServices = {
                    avatar: employeeConfig.avatar,
                    categories: [],
                    employee_info: employeeConfig.employee_info
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
            async getServices(employee, def){
                const empId = def ? employee.employee_id : employee
                await axios.get(`http://127.0.0.1:8000/api/v1/client/employee-preview/?empId=${empId}`)
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
                        if(typeof employee === "number"){
                            const _employee = this.businessActivityPreviewData.employees.find(el => el.employee_id === employee);
                            this.services = {... res.data, employee_info: {
                                "name": _employee.first_name,
                                "last_name": _employee.last_name,
                                "spec_name": _employee.spec_name,
                            }};
                        } else{
                            this.services = {... res.data, employee_info: {
                                "name": employee.first_name,
                                "last_name": employee.last_name,
                                "spec_name": employee.spec_name,
                            }};
                        }
                    })
                this.mapImagesType(this.services);
                this.services = { ...this.groupByCategory(this.services) }
            },
            async previewEmployee(employee, def = true){
                await this.getServices(employee, def);
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