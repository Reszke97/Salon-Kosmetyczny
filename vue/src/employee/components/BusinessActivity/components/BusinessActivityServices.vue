<template>
  <div>
    text
  </div>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI";
    
    export default {
        name: "",
        components: {
            
        },
        props: {
            
        },
        data: () => ({
            
        }),
        computed: {
            
        },
        async created(){
            await this.getBusinessActivityServices();
        },
        methods: {
            async getBusinessActivityServices(){
                const API = await AUTH_API();
                await API.get("api/v1/employee/business-activity-services/")
            }
        }
    }
</script>