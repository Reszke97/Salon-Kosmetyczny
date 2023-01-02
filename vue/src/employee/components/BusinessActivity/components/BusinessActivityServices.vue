<template>
  <div style="display: flex; flex-direction: column; width:100%; color: white">
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
        <h2>Usługi</h2>
            <v-divider dark></v-divider>
        </v-col>
        <v-col
            cols="11"
            sm="10"
            md="10"
            lg="10"
        >
            <v-expansion-panels 
                v-for="(businessActivityCategory, idx) in businessActivityCategories"
                class="accordion-wrapper"
                :key="idx"
                dark 
                
            >
                <v-expansion-panel
                    v-for="businessActivityService of businessActivityCategory"
                    :key="businessActivityService.service_name"
                >
                    <v-expansion-panel-header>
                        <h2>{{businessActivityService.service_name}}</h2>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>
            
        </v-col>
    </v-row>
  </div>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI";
    
    export default {
        name: "",
        components: {
            
        },
        props: {
            employees: { type: Array, required: true }
        },
        data: () => ({
            businessActivityCategories: {},
        }),
        computed: {
            
        },
        async created(){
            await this.getbusinessActivityCategories();
        },
        methods: {

            getEmployeeAvatar(empId){
                return this.employees.find(el => el.id == empId).avatar
            },

            async getbusinessActivityCategories(){
                const API = await AUTH_API();
                await API.get("api/v1/employee/business-activity-services/")
                .then(res => {
                    const uniqueCategories = [...new Set(res.data.map((el) => el.category_name))];
                    for(const category of uniqueCategories){
                        const servicesOfCategory = res.data.filter(el => el.category_name == category)
                        for(const serviceOfCategory of servicesOfCategory){
                            if(this.businessActivityCategories.hasOwnProperty(category)){
                                const serviceIdx = this.businessActivityCategories[category].findIndex(el => el.service_name == serviceOfCategory.service_name)
                                if(serviceIdx != -1){
                                    this.businessActivityCategories[category][serviceIdx].employee_id.push(serviceOfCategory.employee_id);
                                } else {
                                    this.businessActivityCategories[category] = [
                                        { 
                                            ...serviceOfCategory, 
                                            employee_id: [serviceOfCategory.employee_id],
                                            avatars: [this.getEmployeeAvatar(serviceOfCategory.employee_id)]
                                        }
                                    ];
                                }
                            } else {
                                this.businessActivityCategories[category] = [
                                    { 
                                        ...serviceOfCategory, 
                                        employee_id: [serviceOfCategory.employee_id],
                                        avatars: [this.getEmployeeAvatar(serviceOfCategory.employee_id)]
                                    }
                                ];
                            }
                        }
                    }
                    this.businessActivityCategories = {...this.businessActivityCategories}
                })
            }
        }
    }
</script>