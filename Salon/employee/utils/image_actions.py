from django.conf import settings
from ...serializers import EmployeeImageSerializer, EmployeeImageSet
from ...models import EmployeeImage, EmployeeImageSet
from rest_framework import status
import base64

def map_images(image, image_list = None, id = None):
    content = str(image.content).replace("/", "\\")
    file_type = content[content.find('.') + 1::].upper()
    # Note: The "rb" option stands for "read binary".
    with open(settings.MEDIA_ROOT + "\\" + content, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
        encoded_image = {
            "image": image_data,
            "file_type": file_type,
            "image_id": id,
        }
        if(image_list != None):
            image_list.append(encoded_image)
        return encoded_image

def create_image(images):
    images_serializer = EmployeeImageSerializer(data=images)
    if images_serializer.is_valid():
        images_serializer.save()
        return { "status": status.HTTP_201_CREATED, "errors": "" }
    else:
        return { "status": status.HTTP_400_BAD_REQUEST, "errors": images_serializer.errors }

def prepare_and_create_images(files, employee, img_set = None):
    if img_set == None:
        img_set = EmployeeImageSet.objects.create().id
    for key in files:
        object = {
            "content": key,
            "employee": employee,
            "image_set": img_set
        }
        response = create_image(object)
        response["image_set"] = img_set
    return response

def append_images(employee_config):
    for config in employee_config:
        images = EmployeeImage.objects.filter(image_set = config["image_set_id"])
        image_list = []
        for image in images:
            map_images(image, image_list, image.pk)
        config["employee_image"] = image_list


