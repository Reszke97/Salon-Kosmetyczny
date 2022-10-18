<template>
    <v-container>
        <h1>Patryk literka 1</h1>
    </v-container>
</template>




<script>
    import { AUTH_API } from '../../authorization/AuthAPI'
    export default {
        data: () => ({
        }),
        async created(){
            const API = await AUTH_API();
            await API.get('/api/v1/employee/get-images/');
        },
    }
</script>