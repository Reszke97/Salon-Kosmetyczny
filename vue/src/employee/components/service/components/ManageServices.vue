<template>
  <div class="col-6">
    <v-row style="">
      <v-col>
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
      </v-col>
    </v-row>
    <v-row id="items-container">
      <draggable
        :list="services.categories"
        :disabled="!draggingEnabled"
        class="list-group"
        ghost-class="ghost"
        @start="draggingInProgress = true"
        @end="draggingInProgress = false"
      >
        <v-col
          class="list-group-item"
          cols="12"
          v-for="(category, idx) of services.categories"
          :key="idx"
        >
          <h3>{{ category.name }}</h3>
          <v-row 
            v-for="(service, jdx) of category.services"
            :key="jdx + 'i'"
          >
            <v-col>
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
                    style="width: 100%;height: auto; max-height:150px;"
                  />
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-col>
      </draggable>
    </v-row>
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
      draggingInProgress: false
    }),
    computed: {
      openDialog(){
        if(this.previewAllServices) return true
        return false
      },
      draggingInfo() {
        return this.dragging ? "under drag" : "";
      }
    },
    methods: {
      // add: function() {
      //   this.list.push({ name: "Juan " + id, id: id++ });
      // },
      // replace: function() {
      //   this.list = [{ name: "Edgard", id: id++ }];
      // },
      // checkMove: function(e) {
      //   window.console.log("Future index: " + e.draggedContext.futureIndex);
      // }
    }
  }
</script>

<style>
  .ghost {
    opacity: 0.5;
    background: #c8ebfb;
  }
  #items-container .list-group div {
    cursor: move;
  }
</style>