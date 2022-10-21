<template>
    <div>
        <v-row
            class="py-8"
            align="center"
            justify="center"
        >
            <v-col cols="10">
                <v-avatar 
                    color="#0844a4"
                    size="100"
                >
                    <v-icon
                        v-if="!employeeInfo.avatar.image"
                        dark
                    >
                        mdi-account-circle
                    </v-icon>
                    <img
                        v-else
                        id="user-avatar"
                        :src="employeeInfo.avatar.image"
                        style="width:100%;height: 100%"
                    />
                </v-avatar>
                <v-text-field
                    v-model="employeeInfo.email"
                    label="Email"
                    required
                    dark
                ></v-text-field>
                <v-text-field
                    v-model="employeeInfo.user_name"
                    label="Nazwa użytkownika"
                    required
                    class="w40"
                    type="text"
                    dark
                ></v-text-field>
                <v-text-field
                    v-model="employeeInfo.first_name"
                    label="Imię"
                    required
                    class="w40"
                    type="text"
                    dark
                ></v-text-field>
                <v-text-field
                    v-model="employeeInfo.last_name"
                    label="Nazwisko"
                    required
                    class="w40"
                    type="text"
                    dark
                ></v-text-field>
                <v-autocomplete
                    v-if="!isNewSpec"
                    v-model="employeeInfo.employee_spec"
                    :items="existingSpecs"
                    item-text="name"
                    item-value="id"
                    label="Specjalność"
                    placeholder="Wybierz specjalność"
                    hint="Kliknij na ikonę aby dodać własną specjalność."
                    persistent-hint
                    dark
                >
                    <template #append-outer>
                        <v-btn
                            icon
                            @click="toggleSpecInput"
                        >
                            <v-icon>
                                mdi-swap-horizontal
                            </v-icon>
                        </v-btn>
                    </template>
                </v-autocomplete>
                <v-text-field
                    v-if="isNewSpec"
                    v-model="employeeInfo.employee_spec"
                    label="Specjalność"
                    placeholder="Podaj specjalność"
                    hint="Kliknij na ikonę aby wybrać specjalność z listy."
                    persistent-hint
                    dark
                >
                    <template #append-outer>
                        <v-btn
                            icon
                            @click="toggleSpecInput"
                        >
                            <v-icon>
                                mdi-keyboard-backspace 
                            </v-icon>
                        </v-btn>
                    </template>
                </v-text-field>
                <v-text-field
                    v-model="employeeInfo.phone_number"
                    label="Telefon"
                    required
                    class="w40"
                    type="text"
                    dark
                ></v-text-field>
                <v-file-input
                    v-model="newAvatar"
                    accept=".png, .jpg"
                    label="Avatar"
                    placeholder="Dodaj zdjęcie"
                    prepend-icon="mdi-paperclip"
                    :show-size="1000"
                    counter
                    dark
                    @change="changeAvatar"
                >
                    <template #selection="{ text }">
                    <v-chip
                        small
                        label
                        color="success"
                    >
                        {{ text }}
                    </v-chip>
                    </template>
                </v-file-input>
                <v-btn
                    color="secondary"
                    @click="setDialog(true)"
                >
                    Zapisz zmiany
                </v-btn>
                <v-btn
                    class="mx-2"
                    color="secondary"
                    @click="getEmployeeInfo"
                >
                    Cofnij Zmiany
                </v-btn>
            </v-col>
        </v-row>
        <Dialog
            v-if="confirmDialog"
            :dialog="confirmDialog"
            :onConfirmAction="onConfirmAction"
            :setDialog="setDialog"
        />
    </div>
</template>

<script>
    import { AUTH_API } from "../../../authorization/AuthAPI";
    import { Dialog } from "../../../../utils";
    
    export default {
        name: "",
        components: {
            Dialog
        },
        props: {
            
        },
        data: () => ({
            employeeInfo: {
                first_name: "",
                last_name: "",
                phone_number: "",
                user_name: "",
                email: "",
                employee_spec: "",
                avatar: { file_type: "", image: "" },
            },
            newAvatar: null,
            isNewSpec: false,
            confirmDialog: false,
            existingSpecs: [],
        }),
        computed: {
            
        },
        methods: {
            toggleSpecInput(){
                this.isNewSpec = !this.isNewSpec;
                this.employeeInfo.employee_spec = "";
            },
            async updateAvatar(){
                const formData = new FormData();
                formData.append('avatar', this.newAvatar);
                const API = await AUTH_API();
                await API.put('api/v1/employee/update-employee-avatar/', 
                    formData,
                    {
                        headers: {
                            "content-type": "multipart/form-data",
                        },
                    }
                )
            },
            async updateEmployeeData(){
                const requestData = {
                    ...this.employeeInfo,
                    employee_spec: this.isNewSpec 
                        ? { isNew: true, value: this.employeeInfo.employee_spec } 
                        : { isNew: false, value: this.employeeInfo.employee_spec.id}
                }
                const API = await AUTH_API();
                await API.put("api/v1/employee/update-employee-info/", requestData)
            },
            async updateInfo(){
                if(this.newAvatar) await this.updateAvatar();
                await this.updateEmployeeData();
            },
            async onConfirmAction(value){
                await this.updateInfo()
                this.setDialog(false)
            },
            setDialog(value){
                this.confirmDialog = value
            },
            appendMimeType(image){
                let type;
                switch (image.file_type) {
                    case "PNG":
                        type = "data:image/png;base64,";
                    break;
                    case "JPG":
                        type = "data:image/jpg;base64,";
                    break;
                    case "JPEG":
                        type = "data:image/jpeg;base64,";
                    break;
                    default:
                        type = "";
                }
                return { ...image, image: type + image.image, isFromDB: true };
            },
            changeAvatar(image){
                if(image){
                    const url = URL.createObjectURL(image)
                    this.employeeInfo.avatar.image = url
                    this.employeeInfo.avatar.file_type = image.type
                } else this.employeeInfo.avatar = { file_type: "", image: "" }
            },
            async getEmployeeInfo(){
                const API = await AUTH_API();
                await API.get('api/v1/employee/get-employee-info/')
                    .then((res) => {
                        this.employeeInfo = res.data.employee_info;
                        this.existingSpecs = res.data.existing_specs;
                        if(this.employeeInfo.avatar){
                            this.employeeInfo.avatar = this.appendMimeType(this.employeeInfo.avatar)
                        }
                    })
                this.isNewSpec = false;
            } 
        },

        async created() {
            await this.getEmployeeInfo()
        }
    }
</script>