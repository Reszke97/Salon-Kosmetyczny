<template>
    <v-row
        style="
            height:100%
        "
        align="center"
        justify="center"
    >
        <v-col
            cols="12"
            sm="10"
            md="8"
            lg="6"
            style="
                height:100%;
                background-color:#3f51b5;
            "
        >
            <div
                v-if="previewAllServices"
                style="
                    display: flex;
                    justify-content: end;
                "
            >
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-icon 
                            style="position: absolute; z-index: 1"
                            @click="closePreviewTab('tab-1')"
                            v-bind="attrs"
                            v-on="on"
                        >
                            mdi-keyboard-backspace 
                        </v-icon>
                    </template>
                    <span>Powrót</span>
                </v-tooltip>
            </div>
            <v-toolbar 
                v-else
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
                style="
                    height: calc(100% - 112px);
                    background-color:#3f51b5!important
                "
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
                    style="height:100%"
                >
                    <manage-services
                        :get-services="getServices"
                        :services="services"
                        :preview-all-services="previewAllServices"
                    >
                    </manage-services>
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
        }),
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
                } return
            },
            groupByCategory(employeeConfig){
                let groupedServices = {
                    avatar: employeeConfig.avatar,
                    categories: [],
                }
                const uniqueCategories = [
                    ...new Map(employeeConfig.service_info.map(item =>[item.service.service_category.category_id, item.service.service_category])).values()
                ];

                let categoryIdx = 0;
                for(const category of uniqueCategories){
                    const items = employeeConfig.service_info.filter(el => el.service.service_category.category_id === category.category_id)
                    groupedServices.categories.push({
                        name: category.name,
                        category_id: category.category_id,
                        id: category.category_display_order,
                        services: [...items]
                    });
                    categoryIdx += 1;
                } return groupedServices
            },
            async getServices(){
                const API = await AUTH_API();
                let employeeConfig = {};
                await API.get(`/api/v1/employee/getemployeeservices/?preview=${this.previewAllServices}`)
                    .then(res => {
                        res.data.service_info = res.data.service_info.map(el => {
                            return { ...el, id: el.service.service_display_order }
                        })
                        employeeConfig = { ...res.data };
                        this.services = {... res.data };
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
                if(this.previewAllServices) this.services.avatar = { ...this.appendMimeType(services.avatar) }
            }
        },
    }
</script>

<style>
    /* #my-tab .v-toolbar__extension .v-tabs .v-item-group .v-slide-group__prev{
        display: none!important;
    }
    #my-tab .v-toolbar__extension .v-tabs .v-item-group .v-slide-group__wrapper .v-slide-group__content{
        flex: 0!important;
    }
    #my-tab .v-toolbar__extension .v-tabs .v-item-group .v-slide-group__wrapper{
        justify-content: center;
    } */
</style>