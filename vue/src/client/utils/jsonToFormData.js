function buildFormData(formData, data, parentKey) {
    if (data && typeof data === 'object' && !(data instanceof Date) && !(data instanceof File)) {
        Object.keys(data).forEach(key => {
            buildFormData(formData, data[key], parentKey ? `${parentKey}[${key}]` : key);
        });
    } else {
        const value = data == null ? '' : data;
        formData.append(parentKey, value);
    }
}

export function jsonToFormData({ data, images, arrayOfImages = true }) {
    const formData = new FormData();
    buildFormData(formData, data);
    if(arrayOfImages){
        for (let i = 0; i < this.images.length; i += 1) {
            formData.append('files', images[i]);
        }
    } else {
        formData.append('files', images);
    }
    return formData;
}