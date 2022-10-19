<template>
  <v-row style="">
    <v-col>
      <v-avatar 
        color="#0844a4"
        size="100"
      >
        <!-- <v-icon dark>
          mdi-account-circle
        </v-icon> -->
        <img
          :src="services.avatar.image"
          style="width:100%;height: 100%"
        />
      </v-avatar>
    </v-col>
    <v-col
      cols="12"
      v-for="(service, idx) of services.service_info"
      :key="idx"
    >
      <h3> Usługa - {{ service.service.name }} </h3>
      <p> Cena - {{ service.service.price }} PLN</p>
      <p> Czas trwania - {{ service.service.duration }} </p>
      <v-row>
        <v-col
          v-for="(image, jdx) of service.employee_image"
          :key="jdx + 'i'"
        >
          <img
            :src="image.image"
            style="width:100%;height: 100%"
          />
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
  import { AUTH_API } from "../../../authorization/AuthAPI";
  export default {
    name: "",
    components: {
        
    },
    props: {
      getServices: { type: Function, required: true },
      services: { type: Object, required: true },
      previewAllServices: { type: Boolean, required: true }
    },
    data: () => ({

    }),
    computed: {
      openDialog(){
        if(this.previewAllServices) return true
        return false
      },
    },
    methods: {
        
    }
  }
</script>

<style>
</style>