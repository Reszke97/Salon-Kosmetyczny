<template>
    
</template>




<script>
    import axios from 'axios'
    export default {
        data: () => ({
            }),
        created(){
            axios.post('/api/v1/user/logout/', {
                refresh_token: localStorage.getItem('clientRefreshToken'),
            })
            .then(response => {
                this.$store.commit('userLogout')
                window.location.href = '/client/login'
            })
            .catch(error => {
                this.$store.commit('userLogout')
                window.location.href = '/client/login'
            })
        },
    }
</script>