<template>
  <div style="display: flex; flex-direction: column; width:100%">
    <div class="mb-2" style="display: flex">
      <div style="width:100px">
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
      <div style="display: flex; justify-content: end; width: calc(100% - 100px)">
        <slot name="header" />
      </div>
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
              <div 
                v-if="editMode" 
                style="display: flex; flex-direction: column"
                class="my-2"
              >
                <template 
                  v-for="comment of service.employee_comment"
                >
                  <div style="display:flex" class="pb-2" :key="`c-${comment.id}`">
                    <h4 class="comment">
                      {{ comment.text }}
                      <v-tooltip top color="success">
                        <template v-slot:activator="{ on, attrs }">
                          <v-icon
                            dark
                            right
                            v-bind="attrs"
                            v-on="on"
                            @click="dialogAction(service.service.service_id, comment.id)"
                          >
                            mdi-pencil
                          </v-icon>
                        </template>
                        <span>Edytuj</span>
                      </v-tooltip>
                      <v-tooltip top color="success">
                        <template v-slot:activator="{ on, attrs }">
                          <v-icon
                            color="red"
                            right
                            v-bind="attrs"
                            v-on="on"
                            @click="deleteComment(comment.id)"
                          >
                            mdi-delete 
                          </v-icon>
                        </template>
                        <span>Usuń</span>
                      </v-tooltip>
                    </h4>
                  </div>
                </template>
                <div>
                  <v-btn
                    class="m-0"
                    rounded
                    color="success"
                    @click="dialogAction(service.service.service_id)"
                  >
                    <v-icon left>
                      mdi-plus-circle-outline
                    </v-icon>
                    Dodaj Komentarz
                  </v-btn>
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
          <div 
            v-if="editMode" 
            style="display: flex;"
            class="my-2"
          >
            <div 
              v-for="comment of service.employee_comment"
              :key="`c-${comment.id}`"
            >
              <template 
                v-for="comment of service.employee_comment"
              >
                <div style="display:flex" class="pb-2" :key="`c-${comment.id}`">
                  <h4 class="comment">
                    {{ comment.text }}
                    <v-tooltip top color="success">
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon
                          dark
                          right
                          v-bind="attrs"
                          v-on="on"
                          @click="dialogAction(service.service.service_id, comment.id)"
                        >
                          mdi-pencil
                        </v-icon>
                      </template>
                      <span>Edytuj</span>
                    </v-tooltip>
                    <v-tooltip top color="success">
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon
                          color="red"
                          right
                          v-bind="attrs"
                          v-on="on"
                          @click="deleteComment(comment.id)"
                        >
                          mdi-delete 
                        </v-icon>
                      </template>
                      <span>Usuń</span>
                    </v-tooltip>
                  </h4>
                </div>
              </template>
            </div>
            <v-btn
              class="m-0"
              rounded
              color="success"
              small
              @click="dialogAction(service.service.service_id)"
            >
              <v-icon left>
                mdi-plus-circle-outline
              </v-icon>
              Dodaj Komentarz
            </v-btn>
          </div>
        </div>
      </div>
    </div>
    <v-row>
      <v-col>
        <comment
          v-if="dialog"
          :dialog="dialog"
          :service_id="selectedServiceId"
          :dialog-action="dialogAction"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script>
  import { AUTH_API } from "../../../authorization/AuthAPI";
  import draggable from "vuedraggable";
  import Comment from "./Comment.vue";
  export default {
    name: "",
    components: {
      draggable, Comment
    },
    props: {
      getServices: { type: Function, required: true },
      services: { type: Object, required: true },
      previewAllServices: { type: Boolean, required: true },
      editMode: { type: Boolean, default: false },
    },
    data: () => ({
      draggingEnabled: true,
      draggingInProgress: false,
      dialog: false,
      selectedServiceId: null,
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
      dialogAction(id = null){
        this.dialog = !this.dialog;
        this.selectedServiceId = id;
      }
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
  .comment i:hover{
    cursor: pointer;
  }
</style>