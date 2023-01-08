export function appendMimeType(image){
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
    return { ...image, image: type + image.image };
}