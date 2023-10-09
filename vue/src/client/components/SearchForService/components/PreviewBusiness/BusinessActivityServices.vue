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
                dark 
                class="accordion-wrapper"
            >
                <v-expansion-panel
                    v-for="(businessActivityCategory, key) in businessActivityCategories"
                    :key="key"
                    style="margin-top:0.25rem"
                    v-if="!!businessActivityCategory[0].service_category_active"
                >
                    <v-expansion-panel-header>
                       <h2>{{key}}</h2>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                        <v-divider dark></v-divider>
                        <div
                            v-for="(businessActivityService) of businessActivityCategory"
                            v-if="businessActivityService.service_active"
                            :key="businessActivityService.service_name"
                            style="display:flex; flex-direction: row; margin: 0.75rem 0 0.75rem 0"
                        >
                            <div
                                style="display:flex; flex-direction: column;width:100%"
                            >
                                <span style="color:#ffba66"><b>{{businessActivityService.service_name}}</b></span>
                                <span>Czas trwania usługi: {{businessActivityService.duration}} min</span>
                                <span>Cena za {{businessActivityService.duration}} min: {{businessActivityService.price}} zł</span>
                                
                            </div>
                            <div 
                                style="display: flex;width:100%; justify-content:end;"
                            >
                                <div 
                                    v-for="(employee, idx) of businessActivityService.employees"
                                    :key="idx"
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
                                                        @click="() => previewEmployee(employee.id, false)"
                                                        dark
                                                        v-on="on"
                                                    >
                                                        mdi-account-circle
                                                    </v-icon>
                                                    <img
                                                        class="avatar"
                                                        v-else
                                                        :src="employee.avatar.image"
                                                        style="width:100%;height: 100%;"
                                                        v-bind="attrs"
                                                        @click="() => previewEmployee(employee.id, false)"
                                                        v-on="on"
                                                    />
                                                </template>
                                                <span>{{ `${employee.user.first_name} ${employee.user.last_name}`}}</span>
                                            </v-tooltip>
                                        </v-avatar>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>
        </v-col>
    </v-row>
    <slot name="employeePreviewDialog" />
  </div>
</template>

<script>
    // import { AUTH_API } from "../../../authorization/AuthAPI";
    
    export default {
        name: "",
        components: {
            
        },
        props: {
            businessActivityCategories: { type: Object, required: true },
            employees: { type: Array, required: true },
            previewEmployee: { type: Function, required: true },
        },
        data: () => ({
        }),
        computed: {
            
        },
        methods: {
        }
    }
</script>

<style>
    .accordion-wrapper .v-expansion-panel {
        background-color: #0844a4!important;
    }
</style>