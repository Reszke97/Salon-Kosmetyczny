<template>
    <div class="mb-3">
        <v-btn  @click="toggleOpenUploadDialog">Dodaj avatar</v-btn>
        <my-upload field="img"
            v-model="openUploadDialog"
            langType="pl"
            noSquare
            :width="300"
            :height="300"
            @src-file-set="setNameAndFileType"
            @crop-success="cropSuccess"
        />
    </div>
</template>

<script>
	import 'babel-polyfill'; // es6 shim
	import myUpload from "vue-image-crop-upload/upload-2.vue";
    export default {
        name: "",
        components: {
            myUpload,
        },
        props: {
            setImgDataUrl: { type: Function, default: () => {} },
            createFormData: { type: Function, default: () => {} }
        },
		data: () => ({
			openUploadDialog: false,
            fileName: "",
            fileType: "",
		}),
		methods: {
			toggleOpenUploadDialog() {
				this.openUploadDialog = !this.openUploadDialog;
			},
            dataURLtoBlob(dataurl) {
                var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
                    bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
                while(n--){
                    u8arr[n] = bstr.charCodeAt(n);
                }
                return new Blob([u8arr], {type:mime});
            },
            setNameAndFileType( fileName, fileType ){
                this.fileName = fileName;
                this.fileType = fileType
            },
			async cropSuccess(imgDataUrl){
                this.setImgDataUrl(imgDataUrl, this.fileType)
                const blob = this.dataURLtoBlob(imgDataUrl);
                this.createFormData(blob, this.fileName);
			},
		}
	};
</script>