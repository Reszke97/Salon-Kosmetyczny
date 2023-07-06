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
      }
      :
      {
        display: 'flex', 
        flexDirection: 'column',
        width: '100%', 
        backgroundColor: '#3f51b5',
        color: 'white',
      }
    "
  >
    <div class="mb-2" style="display: flex;">
      <div class="d-flex flex-column" style="min-width:250px">
        <div class="d-flex flex-column">
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
              <h3> Usługa - {{ service.service.name }} </h3>
              <div class="d-flex flex-column ">
                <span style="color:orange"> Cena - {{ service.service.price }} PLN</span>
                <span style="color:orange"> Czas trwania - {{ service.service.duration }} </span>
              </div>
              <div style="display: flex; width:50%">
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
                style="display: flex; flex-direction: column; border: solid 1px; border-radius: 10px;"
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
                  </div>
                </template>
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
  </div>
</template>

<script>
  import draggable from "vuedraggable";
  import Comment from "./Comment.vue";
  export default {
    name: "",
    components: {
      draggable, Comment
    },
    props: {
      services: { type: Object, required: true },
      editMode: { type: Boolean, default: false },
      isInDialog: { type: Boolean, default: false },
    },
    data: () => ({
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
      async deleteComment(){
      },
      async closeComment(){
        this.dialog = false;
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