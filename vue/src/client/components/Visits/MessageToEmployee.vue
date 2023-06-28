<template>
    <v-dialog
        :value="showDialog"
        dark
        persistent
        :width="componentDims.width"
    >
        <v-row 
            class="bg-color white-text"
            :style="{ minHeight: '360px' }"
        >
            <v-col
                cols="12"
            >
                <div>
                    <h3>Utwórz wiadomość mailową do pracownika</h3>
                </div>
                <v-form
                    ref="form"
                    v-model="valid"
                >
                    <v-textarea
                        v-model="message"
                        class="mt-2"
                        outlined
                        name="input-7-4"
                        label="Wiadomość do pracownika"
                        clearable
                        rows="8"
                        :rules="messageRules"
                    ></v-textarea>
                </v-form>
                <div>
                    <v-btn
                        @click="$emit('closeDialog')"
                        color="success"
                    >
                        Zamknij
                        <v-icon right>
                            mdi-close-circle
                        </v-icon>
                    </v-btn>
                    <v-btn
                        class="ml-2"
                        @click="sendMessage"
                        color="success"
                    >
                        Wyślij
                        <v-icon right>
                            mdi-send 
                        </v-icon>
                    </v-btn>
                </div>
            </v-col>
        </v-row>
    </v-dialog>
</template>

<script>
    export default {
        props: {
            selectedVisit: { type: Object, default: () => {{}} },
            showDialog: { type: Boolean, required: true },
            componentDims: { type: Object, required: true },
        },
        emits: ["closeDialog", "sendMessage"],
        data: () => ({
            message: "",
            messageRules: [
                v => !!v || 'Pole wymagane'
            ],
            valid: true,
        }),
        methods: {
            sendMessage(){
                this.valid = this.$refs.form.validate();
                if (this.valid) this.$emit("sendMessage", this.message);
            }
        }
    }
</script>