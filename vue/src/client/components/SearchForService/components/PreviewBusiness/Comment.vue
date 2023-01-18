<template>
    <v-dialog
        :width="`${screenSize.screenWidth <= 500 ? screenSize.screenWidth - 20 + 'px': '400px'}`"
        v-model="dialog"
    >
        <div 
            style="
                backgroundColor:#3f51b5!important;
            "
        >
            <div 
                class="px-2 py-2" 
                style="display: flex; flex-direction: column"
            >
                <div class="px-2">
                    <h3 style="color:white;">{{ header }}</h3>
                </div>
                <div id="comment-field" class="mx-2">
                    <v-textarea
                        dark
                        v-model="comment"
                    >
                    </v-textarea>
                </div>
                <div style="display:flex;flex-direction:row">
                    <v-btn 
                        class="my-2 mx-2"
                        color="success"
                        @click="postComment"
                    >
                        Zapisz
                    </v-btn>
                    <v-btn 
                        class="my-2 mx-2"
                        text
                        dark
                        @click="dialogAction(null)"
                    >
                        Zamknij
                    </v-btn>
                </div>
            </div>
        </div>
    </v-dialog>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI";
    
    export default {
        name: "",
        components: {
            
        },
        props: {
            dialog: { type: Boolean, default: false },
            service_id: { type: Number, default: null },
            dialogAction: { type: Function, default: () => {} },
            selectedComment: { type: Object, default: null }
        },
        data: () => ({
            comment: "",
            header: "Dodawanie komentarza",
        }),
        inject: ["screenSize"],
        computed: {},
        created(){
            if(this.selectedComment) {
                this.header = "Edycja komentarza"
                this.comment = this.selectedComment.text
            }
        },
        methods: {
            async postComment(){
                let action = "post";
                self = this;
                let object = {
                    text: this.comment,
                    service_id: this.service_id
                };
                if(this.selectedComment) {
                    action = "put";
                    object = {...object, srvCommentId: this.selectedComment.id}
                }
                const API = await AUTH_API();
                await API[action]("/api/v1/employee/comment/", object)
                .then(() => {
                    self.$emit("commentActionSuccess");
                })
            }
        }
    }
</script>