import logging
import base64
import json
import azure.functions as func
from PIL import Image
from io import BytesIO

def base64_pil(base64_str):
    image = base64.b64decode(base64_str)
    image = BytesIO(image)
    image = Image.open(image)
    return image

def pil_base64(image):
    img_buffer = BytesIO()
    image.save(img_buffer, format='JPEG')
    byte_data = img_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    if req_body:
        try:
            name = req_body.get('name')
            if not name:
                return func.HttpResponse("Name not found", status_code=400)
            imageFile1 = req_body.get('sweater')
            if not imageFile1:
                return func.HttpResponse("Sweater photo not found", status_code=400)
            imageFile2 = req_body.get('empPhoto')
            if not imageFile2:
                return func.HttpResponse("Employee photo not found", status_code=400)
        except ValueError:
            pass

    if req_body:

        sweaterImage = base64_pil(imageFile1)
        empimage = base64_pil(imageFile2)

        # sweaterImage.show()
        # empimage.show()

        sweaterImage = sweaterImage.resize((400,400))
        sweater_size = sweaterImage.size
        emp_size = empimage.size

        mergedImage = Image.new('RGB', (sweater_size[0], sweater_size[1]+emp_size[1]), (250,250,250))
        mergedImage.paste(empimage, (0,0))
        mergedImage.paste(sweaterImage, (0,emp_size[1]))
        mergedImage.show()

        merged_base64 = pil_base64(mergedImage)

        # print(merged_base64)

        return func.HttpResponse(
                json.dumps({
                    "image1": imageFile1,
                    "image2": imageFile2,
                    "mergedImage": merged_base64.decode('utf-8')
                    }))
        # return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
