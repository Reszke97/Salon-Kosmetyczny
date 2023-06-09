<template>
  <v-dialog
    :value="signUpForVisitDialog"
    dark
    persistent
    :width="componentDims.width"
  >
    <v-row 
      class="bg-color white-text"
      :style="{ minHeight: `400px` }"
    >
      <v-col
        cols="12"
      >
        <div class="flex-centered">
          <h2>
            <span>
              Zapis na usługę 
            </span>
            <span style="color: orange!important">
              {{ selectedService.service_name }}
            </span>
          </h2>
        </div>
        <div>
          <v-btn 
            @click="closeSignUpForVisitDialog"
            color="success"
          >
            <v-icon left>
              mdi-close-circle
            </v-icon>
            Zamknij
          </v-btn>
        </div>
      </v-col>
    </v-row>
  </v-dialog>
</template>

<script>
    export default {
        name: "",
        components: {
            
        },
        props: {
          signUpForVisitDialog: { type: Boolean, required: true },
          selectedService: { type: Object, required: true },
          componentDims: { type: Object, required: true },
          closeSignUpForVisitDialog: { type: Function, required: true },
        },
        data: () => ({
            
        }),
        computed: {
            
        },
        methods: {
            
        }
    }
</script>

<style>
  @import "../../../../../styles/globalStyles.css";
</style>