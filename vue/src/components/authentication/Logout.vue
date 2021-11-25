<template>
    
</template>




<script>
    import { AUTH_API } from '../../authorization/AuthAPI'
    import axios from 'axios'
    export default {
        data: () => ({
            }),
        created(){
            axios.post('/api/v1/user/logout/', {
                refresh_token: localStorage.getItem('refreshToken'),
            })
            .then(response => {
                this.$store.commit('userLogout')
                window.location.href = '/login'
            })
            .catch(error => {
                this.$store.commit('userLogout')
                window.location.href = '/login'
            })
        },
    }
</script>