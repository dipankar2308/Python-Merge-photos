import logging
import base64
import json
import azure.functions as func


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
        return func.HttpResponse(
                json.dumps({
                    "image1": imageFile1,
                    "image2": imageFile2
                    }))
        # return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
