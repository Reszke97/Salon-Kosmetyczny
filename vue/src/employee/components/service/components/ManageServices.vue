<template>
  <div 
    :style="
      isInDialog ? {
        display: 'flex', 
        flexDirection: 'column',
        width: '100%', 
        backgroundColor: '#3f51b5',
        padding: '1rem',
        color: 'white',
        minWidth: '600px',
      }
      :
      {
        display: 'flex', 
        flexDirection: 'column',
        width: '100%', 
        backgroundColor: '#3f51b5',
        color: 'white',
        padding: '1rem',
        minWidth: '600px',
      }
    "
  >
    <div class="mb-2" style="display: flex;">
      <div class="d-flex flex-column" style="min-width:250px">
        <div v-if="services.employee_info" class="d-flex flex-column">
          <span>{{ services.employee_info.name }} {{ services.employee_info.last_name }}</span>
          <span><span class="font-bold">Spec.</span><span class="font-bold" style="color:orange"> {{ services.employee_info.spec_name }}</span></span>
        </div>
        <v-avatar 
          color="#0844a4"
          size="100"
        >
          <v-img
            v-if="services.avatar"
            :src="services.avatar.image"
            style="width:100%;height: 100%"
          />
          <v-icon
            v-else
            style="font-size:100px"
            dark
          >
            mdi-account-circle
          </v-icon>
        </v-avatar>
      </div>
      <div style="display: flex; justify-content: end;">
        <slot name="header" />
      </div>
    </div>
    <div style="display: flex; flex-direction: column">
      <div
        style="display: flex; flex-direction: row"
        v-for="(group, idx) of servicesGroupedByScreenSize.lteMedium"
        :key="idx"
      >
         <div
          style="display: flex; flex-direction: column; width: 100%;min-width:250px"
          v-for="(category, idx) of group"
          :key="idx"
        >
          <h3>{{ category.name }}</h3>
          <div
            class="mx-2"
            v-for="(service, jdx) of category.services"
            :key="jdx + 'i'"
          >
            <div class="pb-3">
              <h4> Usługa - {{ service.service.name }} </h4>
              <div class="d-flex flex-column ">
                <span style="color:orange"> Cena - {{ service.service.price }} PLN</span>
                <span style="color:orange"> Czas trwania - {{ service.service.duration }} </span>
              </div>
              <div style="display: flex; width:50%;" class="mb-2">
                <div
                  style="width:100%"
                  class="mx-1"
                  v-for="(image, jdx) of service.employee_image"
                  :key="jdx + 'i'"
                >
                  <a
                    @click="openImg(image.image)"
                  >
                    <v-img
                      :src="image.image"
                      :style="{
                        height: 'auto',
                        maxHeight: '80px',
                        maxWidth: '80px',
                      }"
                      
                    />
                  </a>
                </div>
              </div>
              <div 
                style="display: flex; flex-direction: column; border: solid 1px; border-radius: 10px; border-color:rgb(70, 139, 255);"
                class="px-2 py-2"
              >
                <div>
                  <h4>
                    Komentarze do usługi:
                  </h4>
                </div>
                <template 
                  v-for="comment of service.employee_comment"
                >
                  <div style="display:flex" class="pb-2" :key="`c-${comment.id}`">
                    <span class="comment">
                      - {{ comment.text }}
                    </span>
                    <template v-if="editMode">
                      <v-tooltip top color="success">
                        <template v-slot:activator="{ on, attrs }">
                          <v-icon
                            dark
                            right
                            v-bind="attrs"
                            v-on="on"
                            @click="dialogAction(service.service.service_id, comment)"
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
                            @click="deleteComment(service.service.service_id, comment.id)"
                          >
                            mdi-delete 
                          </v-icon>
                        </template>
                        <span>Usuń</span>
                      </v-tooltip>
                    </template>
                  </div>
                </template>
                <div v-if="editMode">
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
    <v-row>
      <v-col>
        <comment
          v-if="dialog"
          :dialog="dialog"
          :service_id="selectedServiceId"
          :dialog-action="dialogAction"
          :selected-comment="selectedComment"
          @commentActionSuccess="closeComment"
        />
      </v-col>
    </v-row>
    <v-dialog
      id="showImagePreview"
      v-model="showImagePreview"
      style="overflow: hidden!important;"
      v-if="showImagePreview"
    >
      <v-img
        :src="selectedImg"
        style="width:auto;height: auto"
      />
      <v-btn
        dark
        color="secondary"
        @click="closeImg"
        class="mr-2"
      >
        Zamknij
      </v-btn>
    </v-dialog>
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
      editMode: { type: Boolean, default: false },
      isInDialog: { type: Boolean, default: false },
    },
    data: () => ({
      showImagePreview: false,
      selectedImg: "",
      draggingEnabled: true,
      draggingInProgress: false,
      dialog: false,
      selectedServiceId: null,
      selectedComment: null,
    }),
    inject: ["screenSize"],
    computed: {
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
      closeImg(){
        this.showImagePreview = false;
      },
      openImg(dataUrl){
        this.selectedImg = dataUrl;
        this.showImagePreview = true;
      },
      async deleteComment(service_id, comment_id){
        const API = await AUTH_API();
        await API.delete(`/api/v1/employee/comment/?service_id=${service_id}&comment_id=${comment_id}`)
        .then( async () => {
          alert("Usunięto komentarz");
          await this.closeComment()
        })
      },
      async closeComment(){
        this.dialog = false;
        await this.getServices()
      },
      setSelectedComment(comment){
        this.selectedComment = comment;
      },
      dialogAction(id = null, comment = null){
        this.setSelectedComment(comment);
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