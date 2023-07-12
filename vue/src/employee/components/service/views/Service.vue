<template>
    <v-row
        id="services-main-container"
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
                        @change="(val) => getDataAfterTabChange(val)"
                    >
                        <v-tabs-slider ></v-tabs-slider>
                        <v-tab
                            href="#tab-1"
                            class="primary--text px-3"
                            style="width:100%;"
                        >
                            Dodaj usługę
                            <v-icon>mdi-phone</v-icon>
                        </v-tab>

                        <v-tab
                            href="#tab-2"
                            class="primary--text px-3"
                            style="width:100%;"
                        >
                            Lista usług
                            <v-icon>mdi-heart</v-icon>
                        </v-tab>
                        <v-tab
                            href="#tab-3"
                            class="primary--text px-3"
                            style="width:100%;"
                        >
                            Podgląd
                            <v-icon>mdi-eye</v-icon>
                        </v-tab>
                    </v-tabs>
                </template>
            </v-toolbar>

            <v-tabs-items 
                v-model="tabs"
                :style="`
                    height: ${'calc(100% - 112px)'} ;
                    background-color:#3f51b5!important
                `"
            >
                <v-tab-item
                    :value="'tab-1'"
                    style="height:100%"
                >
                    <add-or-update-service />
                </v-tab-item>

                <v-tab-item
                    :value="'tab-2'"
                    style="height:100%"
                >
                    <services
                        :services="services.service_info"
                        :get-services="getServices"
                    />
                </v-tab-item>
                <v-tab-item
                    :value="'tab-3'"
                    id="tab-3"
                    style="height:100%;overflow:auto;"
                >
                    
                    <v-dialog
                        :value="tabs === 'tab-3'"
                    >
                        <manage-services
                            v-if="tabs === 'tab-3'"
                            :get-services="getServices"
                            :services="services"
                            :preview-all-services="previewAllServices"
                            :edit-mode="editMode"
                        >
                            <template #header>
                                <div
                                    v-if="previewAllServices"
                                    style="
                                        display: flex;
                                        justify-content: end;
                                    "
                                >
                                    <div
                                        class="mr-8"
                                        :style="`
                                            display: flex;
                                            flex-direction: ${screenSize.screenWidth <= 400 ? 'column' : 'row'}
                                        `"
                                    >
                                        <v-tooltip bottom>
                                            <template v-slot:activator="{ on, attrs }">
                                                <v-chip
                                                    style=" background: rgb(8, 68, 164)!important;"
                                                    class="ma-2"
                                                    color="primary"
                                                    @click="closePreviewTab('tab-1')"
                                                    v-bind="attrs"
                                                    v-on="on"
                                                >
                                                    <v-icon left>
                                                        mdi-keyboard-backspace 
                                                    </v-icon>
                                                    Powrót
                                                </v-chip>
                                            </template>
                                            <span>Powrót</span>
                                        </v-tooltip>
                                        <v-checkbox
                                            class="mt-2 ml-2"
                                            v-model="editMode"
                                            label="Tryb edycji"
                                            dark
                                        ></v-checkbox>
                                    </div>
                                </div>
                            </template>
                        </manage-services>
                    </v-dialog>
                </v-tab-item>
            </v-tabs-items>
        </v-col>
    </v-row>
</template>

<script>
    import AddOrUpdateService from "../components/AddOrUpdateService.vue";
    import Services from "../components/Services.vue";
    import ManageServices from "../components/ManageServices.vue";
    import { AUTH_API } from "../../../authorization/AuthAPI";

    export default {
        name: "Service",
        props: {

        },
        components: {
            AddOrUpdateService,
            Services,
            ManageServices,
        },
        data: () => ({
            tabs: null,
            services: { avatar: {}, service_info: [] },
            previewAllServices: false,
            editMode: false,
        }),
        provide(){
            return {
                getServices: this.getServices
            }
        },
        inject: ["screenSize"],
        methods: {
            closePreviewTab(val){
                this.setTabs(val);
                this.previewAllServices = !this.previewAllServices;
            },
            setTabs(val){
                this.tabs = val;
            },
            async getDataAfterTabChange(val){
                if(val === "tab-3"){
                    this.previewAllServices = true
                    await this.getServices();
                }
                else if(val === "tab-2"){
                    this.previewAllServices = false
                    await this.getServices();
                } return
            },
            groupByCategory(employeeConfig){
                let groupedServices = {
                    employee_info: employeeConfig.employee_info,
                    avatar: employeeConfig.avatar,
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
                        is_active: category.is_active,
                        services: [...items]
                    });
                    categoryIdx += 1;
                } return groupedServices
            },
            async getServices(){
                const API = await AUTH_API();
                await API.get(`/api/v1/employee/service/?preview=${this.previewAllServices}`)
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
                        const employee_info = {
                            name: res.data.employee_info.first_name,
                            last_name: res.data.employee_info.last_name,
                            spec_name: res.data.employee_info.spec_name,
                        }
                        this.services = {... res.data, employee_info: {...employee_info} };
                    })
                this.mapImagesType(this.services);
                if(this.previewAllServices === true){
                    this.services = { ...this.groupByCategory(this.services) }
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
                    this.services.service_info[idx].employee_image = service.employee_image.map((el) => {
                        return this.appendMimeType(el)
                    });
                })
                if(this.previewAllServices && this.services.avatar) this.services.avatar = { ...this.appendMimeType(services.avatar) }
            }
        },
    }
</script>

<style type="text/css">
</style>