import json
import boto3
import rest_interface


rest_interface.bucket = "twentyrandomquestions"

def handle_get(event):
    # Usually a GET method is intended to retrieve the content of one or more files in S3.
    # If obtain the content of a single file then use s3_get_object.
    # If obtaining content from multiple files then use s3_get_multiple_objects.
    # You may need to use the path parameter or value of a query parameter as the key of the object or the folder name.

    param_name = "color"
    color = rest_interface.get_query_parm(event, param_name)
    key = f"/rhymes/{color}"
    try:
        stanza = rest_interface.s3_get_object(key)
        return {"stanza": stanza}
    except:
        return {"stanza": f"I don't have a rhyme for {color}"}


def handle_post(event):

    body = rest_interface.get_body(event)
    rhymes = body['rhymes']

    for color, stanza in rhymes.items():
        rest_interface.s3_write_obj(f"/rhymes/{color}", stanza)
    response = f"Saved {len(rhymes)} rhymes"

    return response


def lambda_handler(event, context):
    httpMethod = event["httpMethod"]
    if httpMethod == "POST":
        return rest_interface.response(handle_post(event), event=event)
    elif httpMethod == "GET":
        return rest_interface.response(handle_get(event), event=event)
    return rest_interface.response(dict(msg="Unsupported method", method=httpMethod), statusCode=405)
