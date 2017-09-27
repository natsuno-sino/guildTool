import logging
from flask import Flask, jsonify, request,  abort, make_response
import boto3
import requests
from text import Text
from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('gt_stage')

@app.route('/', methods=['POST'])
def hello(event=None, context=None):

    if "token" not in request.form:
        return ""

    if request.form["token"] != "ejEeHZVekon3Rt6hR9VlZYrI":
        return ""

    text = request.form["text"]
    user_name = request.form["user_name"]

    if user_name == "slackbot":
        return ""
    if user_name == "slackbot":
        return ""

    stage = get_stage(user_name)

    if "1" == stage:
        update_stage(user_name,"1_1")
        return create_response(user_name,Text.text1)

    if "1_1" == stage:
        if "1" == text:
            update_stage(user_name,"2_1")
            return create_response(user_name,Text.text2)

        if "2" == text:
            update_stage(user_name,"2_2")
            return create_response(user_name,Text.text3)

        if "3" == text:
            update_stage(user_name,"2_3")
            return create_response(user_name,Text.text4)

        if "4" == text:
            update_stage(user_name,"1")
            return create_response(user_name,Text.text_register)

        return create_response(user_name,Text.text_miss1 +"\r\n"+ Text.text1)

    if "2_1" == stage:
        if "1" == text:
            update_stage(user_name,"1_1")
            return create_response(user_name,Text.text_register +"\r\n"+ Text.text1)

        if "2" == text:
            update_stage(user_name,"1_1")
            return create_response(user_name,Text.text_register +"\r\n"+ Text.text1)

        if "3" == text:
            update_stage(user_name,"1_1")
            return create_response(user_name,Text.text1)

        return create_response(user_name,Text.text_miss1 +"\r\n"+ Text.text2)

    if "2_2" == stage:
        if "#" == text:
            update_stage(user_name,"1_1")
            return create_response(user_name,Text.text1)

        if text.isdigit():
            update_stage(user_name,"1_1")
            return create_response(user_name,Text.text_register +"\r\n"+ Text.text1)

        return create_response(user_name,Text.text_miss2 +"\r\n"+ Text.text3)

    if "2_3" == stage:
        if "1" == text:
            update_stage(user_name,"1_1")
            return create_response(user_name,Text.text_register +"\r\n"+ Text.text1)

        if "2" == text:
            update_stage(user_name,"1_1")
            return create_response(user_name,Text.text_register +"\r\n"+ Text.text1)

        if "3" == text:
            update_stage(user_name,"1_1")
            return create_response(user_name,Text.text_register +"\r\n"+ Text.text1)

        if "4" == text:
            update_stage(user_name,"1_1")
            return create_response(user_name,Text.text_register +"\r\n"+ Text.text1)

        if "5" == text:
            update_stage(user_name,"1_1")
            return create_response(user_name,Text.text_register +"\r\n"+ Text.text1)

        if "6" == text:
            update_stage(user_name,"1_1")
            return create_response(user_name,Text.text_register +"\r\n"+ Text.text1)

        if "7" == text:
            update_stage(user_name,"1_1")
            return create_response(user_name,Text.text_register +"\r\n"+ Text.text1)

        if "8" == text:
            update_stage(user_name,"1_1")
            return create_response(user_name,Text.text_register +"\r\n"+ Text.text1)

        if "9" == text:
            update_stage(user_name,"1_1")
            return create_response(user_name,Text.text1)

        return create_response(user_name,Text.text_miss1 +"\r\n"+ Text.text4)


    return Text.text1

def get_stage(user_id):
    response = table.get_item(Key={"user_id": user_id})
    if "Item" not in response:
        table.put_item(Item={"user_id": user_id,"stage": "1"})
        stage = "1"
    else:
        stage = response["Item"]["stage"]
    return stage

def update_stage(user_id,stage):
    table.update_item(Key={"user_id": user_id}, AttributeUpdates = {"stage": {
                         'Action': 'PUT',
                         'Value': stage
                     }})

def create_response(name, text):
    result = {
        "text": "<@{0}> {1}".format(name, text)
    }
    return make_response(jsonify(result))

if __name__ == '__main__':
    app.run(debug=True)
