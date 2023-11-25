<template>
  <v-dialog
    :value="dialog"
    dark
    persistent
    width="auto"
  >
  <v-card class="indigo">
    <v-card-title class="text-h5 blue darken-4">
      Pomyślnie zapisano twoją wizytę.
    </v-card-title>
    <v-card-text>
      <div class="d-flex flex-column pt-3">
        <span><span class="font-bold">Firma: </span>{{ summary.business.business_name }}</span>
        <span><span class="font-bold">Usługa: </span>{{ summary.service_name  }}</span>
        <span><span class="font-bold">Data: </span>{{ `${summary.dateTime.date} ${summary.dateTime.start_time} - ${summary.dateTime.end_time}`  }}</span>
        <span><span class="font-bold">Pracownik: </span>{{ `${summary.employee_first_name} ${summary.employee_last_name}`  }}</span>
        <span>
          <span class="font-bold">Adres: </span>
          {{ `${
              summary.business.business_city
            } ${
              summary.business.business_post_code
            } ul. ${
              summary.business.business_street
            }${
              summary.business.business_house_number
            }${summary.business.business_apartment_number ? "/" + summary.business.business_apartment_number : ""}`  
          }}
        </span>
      </div>
    </v-card-text>

    <v-divider></v-divider>

    <v-card-actions class="indigo">
        <v-btn
          class="indigo"
          dark
          text
          @click="$emit('closeSummary')"
        >
          Zamknij
        </v-btn>
    </v-card-actions>
</v-card>
  </v-dialog>
</template>

<script>
    export default {
        name: "",
        components: {
            
        },
        props: {
          dialog: { type: Boolean, required: true },
          summary: { type: Object, required: true },
        },
        emits: [ "closeSummary" ],
        data: () => ({
            
        }),
        computed: {
            
        },
        methods: {
            
        }
    }
</script>