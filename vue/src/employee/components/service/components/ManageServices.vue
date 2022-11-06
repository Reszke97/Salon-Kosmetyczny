<template>
  <div style="display: flex; flex-direction: column; width:100%">
    <div class="mb-2">
      <v-avatar 
        color="#0844a4"
        size="100"
      >
        <img
          v-if="services.avatar"
          :src="services.avatar.image"
          style="width:100%;height: 100%"
        />
      </v-avatar>
    </div>
    <div v-if="screenSize.screenWidth >= 570" style="display: flex; flex-direction: column">
      <div
        style="display: flex; flex-direction: row"
        v-for="(group, idx) of servicesGroupedByScreenSize.lteMedium"
        :key="idx"
      >
         <div
          style="display: flex; flex-direction: column; width: 100%;"
          v-for="(category, idx) of group"
          :key="idx"
        >
          <h3>{{ category.name }}</h3>
          <div 
            v-for="(service, jdx) of category.services"
            :key="jdx + 'i'"
          >
            <div>
              <h3> Usługa - {{ service.service.name }} </h3>
              <p> Cena - {{ service.service.price }} PLN</p>
              <p> Czas trwania - {{ service.service.duration }} </p>
              <div style="display: flex;">
                <div
                  style="width:100%"
                  class="mx-2"
                  v-for="(image, jdx) of service.employee_image"
                  :key="jdx + 'i'"
                >
                  <img
                    :src="image.image"
                    :style="{
                      height: 'auto',
                      maxHeight: screenSize.screenWidth <= 680 ? '80px' : '100px',
                      maxWidth: screenSize.screenWidth <= 680 ? '80px' : '100px',
                    }"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div> 
    </div>
    <div v-else style="display: flex; flex-direction: column">
      <div
        style="display:flex; flex-direction: column; width: 100%"
        v-for="(category, idx) of services.categories"
        :key="idx"
      >
        <h3>{{ category.name }}</h3>
        <div 
          v-for="(service, jdx) of category.services"
          :key="jdx + 'i'"
        >
          <div>
            <h3> Usługa - {{ service.service.name }} </h3>
            <p> Cena - {{ service.service.price }} PLN</p>
            <p> Czas trwania - {{ service.service.duration }} </p>
            <div style="display: flex; flex-direction: row">
              <div
                style="width:100%;"
                class="mx-2"
                v-for="(image, jdx) of service.employee_image"
                :key="jdx + 'i'"
              >
                <img
                  :src="image.image"
                  style="height: auto; max-height:80px; max-width:80px"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { AUTH_API } from "../../../authorization/AuthAPI";
  import draggable from 'vuedraggable'
  export default {
    name: "",
    components: {
      draggable
    },
    props: {
      getServices: { type: Function, required: true },
      services: { type: Object, required: true },
      previewAllServices: { type: Boolean, required: true }
    },
    data: () => ({
      draggingEnabled: true,
      draggingInProgress: false,
    }),
    inject: ["screenSize"],
    computed: {
      openDialog(){
        if(this.previewAllServices) return true
        return false
      },
      draggingInfo() {
        return this.dragging ? "under drag" : "";
      },
      servicesGroupedByScreenSize(){
        if(this.services.hasOwnProperty("categories")){
          let groupedServices = { gtMedium: [this.services.categories], lteMedium: [] }
          let rowCount = 1;
          let groupNo = -1;
          groupedServices.lteMedium = this.services.categories.reduce((prev, current) => {
            if(rowCount == 2){
              prev[groupNo].push(current)
              rowCount += 1;
            } else {
              prev.push(new Array(current))
              if(rowCount > 2) rowCount = 1;
              groupNo += 1;
              rowCount += 1;
            }
            return prev
          }, [])
          return groupedServices
        } return { gtMedium: [], lteMedium: [] };
      },
    },

    methods: {
    }
  }
</script>

<style>
  .ghost {
    opacity: 0.5;
    background: #c8ebfb;
  }
  /* #items-container .list-group div {
    cursor: move;
  } */
  #items-container {
    width: 100%;
  }
</style>