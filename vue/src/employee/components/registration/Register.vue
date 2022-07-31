<template>
    <v-row
        align="center"
        justify="center"
    >
        <v-col
            cols="11"
            sm="9"
            md="6"
            lg="5"
        >
          <v-stepper v-model="stepperPosition" class="indigo" dark>
            <v-stepper-header class="">
                <v-stepper-step
                    :editable="true"
                    step="1"
                >
                    Dane o właścicielu
                </v-stepper-step>
                <v-divider/>
                <v-stepper-step
                    :editable="true"
                    step="2"
                >
                    Dane salonu
                </v-stepper-step>
            </v-stepper-header>
            <v-stepper-items>
                <v-stepper-content 
                    :step="1"
                >
                    <about-owner></about-owner>
                </v-stepper-content>
                <v-stepper-content 
                    :step="2"
                >
                    <business-activity></business-activity>
                </v-stepper-content>
            </v-stepper-items>
          </v-stepper>
        </v-col>
    </v-row>
</template>

<script>
import AboutOwner from "./AboutOwner.vue"
import BusinessActivity from "./BusinessActivity.vue"

export default {
  components: {
    AboutOwner,
    BusinessActivity,
  },
  data() {
    return {
      stepperPosition: 1,
      stepperPositionPrev: 1,
    };
  },
  computed: {
    areNotesAdded() {
      return this.note.some((el) => el.variable.note === "");
    },
  },
  watch: {
    stepperPosition(newVal, oldVal) {
      this.stepperPositionPrev = oldVal;
    },
  },
  methods: {
    createNotes(notes) {
      this.$emit("createNotes", notes);
    },
    nextPosition() {
      if (this.stepperPosition < this.note.length) {
        this.stepperPosition += 1;
      }
    },
    isCompleted(idx) {
      if (this.note[idx].variable.note !== "") {
        return this.stepperPosition !== idx + 1;
      }
      return false;
    },
    previosuPosition() {
      if (this.stepperPosition > 1) {
        this.stepperPosition -= 1;
      }
    },
    addNote() {
      this.$emit("addNote", this.note);
    },
    reset() {
      this.$emit("resetDialog");
    },
  },
};
</script>
<style>
.text-white textarea {
  color: white !important;
}
.label-white label {
  color: white !important;
}
.custom-stepper {
  background: none !important;
  box-shadow: none !important;
}
.custom-header {
  box-shadow: 0 2px 2px -2px rgb(3 13 0) !important;
}
</style>