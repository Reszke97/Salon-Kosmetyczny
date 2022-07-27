<template>
  <v-row justify="center">
    <v-dialog
      :value="dialog"
      persistent
      max-width="290"
      dark
    >
      <v-card>
        <v-card-title class="text-h5">
          Czy na pewno chcesz potwierdzić?
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            text
            @click="setDialog(false)"
          >
            Nie
          </v-btn>
          <v-btn
            @click="onConfirmAction(true)"
            color="secondary"
          >
            Tak
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
    export default {
        name: "",
        components: {
            
        },
        props: {
            dialog: {
                type: Boolean,
                required: true
            },
            onConfirmAction: {
                type: Function,
                default: () => {{}}
            },
            setDialog: {
                type: Function,
                default: () => {{}}
            }
        },
        data: () => ({
            
        }),
        computed: {
            
        },
        methods: {
            
        }
    }
</script>