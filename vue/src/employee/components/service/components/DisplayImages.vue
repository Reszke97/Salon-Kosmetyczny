<template>
    <v-row 
        id="sth"
        ref="container"
        style="height:175px"
    >
        <v-col 
            cols=4
            style=""
            v-for="(img, idx) of imgs"
            :id="`img-container-${idx}`"
            :key="idx"
        >
            <div style="display: flex; flex-direction: column">
                <div style="display: flex; flex-direction: row; width:100%">
                    <div v-if="!creatingNewService" style="width:100%">
                        <v-btn>
                            Usuń
                        </v-btn>
                    </div>
                </div>
                <img
                    :id="`img-${idx}`"
                    :src="img.image"
                    style=" width: 100%;height: auto; max-height:150px"
                />
            </div>
            <v-dialog
                id="showImagePreview"
                v-model="showImagePreview"
                width="75vw"
                style="min-height:350px!important"
                v-if="showImagePreview"
            >
                <img
                    :src="images[imagePreviewIdx].image"
                    style="width:100%;height: 100%"
                />
                <v-btn
                    dark
                    @click="setShowImagePreview"
                    class="mr-2"
                >
                    Zamknij
                </v-btn>
            </v-dialog>
        </v-col>
    </v-row>
</template>

<script>
    export default {
        name: "",
        components: {
            
        },
        props: {
            images: {
                type: Array,
                default: () => ([])
            },
            creatingNewService: {
                type: Boolean,
                default: true
            },
            imagesCount: {
                type: Number,
                required: true
            }
        },
        data: () => ({
            showImagePreview: false,
            imagePreviewIdx: null,
        }),
        computed: {
            imgs(){
                console.log(this.$refs)
                if(this.imagesCount > 0 && this.imagesCount == this.images.length){
                    this.$nextTick(() => {
                        this.images.forEach((el, idx) =>{
                            const img = document.getElementById(`img-${idx}`)
                            img.addEventListener("click", this.setShowImagePreview)
                        })
                    })
                    return this.images
                } else return []
            },
        },

        methods: {
            setShowImagePreview({ target }){
                const id = target.id.split('-')[1]
                this.showImagePreview = !this.showImagePreview;
                this.imagePreviewIdx = id;
            },
        },
    }
</script>