import json
from flask import jsonify, request
import requests
from app import app, DEBUG, API_GPT
from utils import get_responsibles, create_table, register


@app.route('/register', methods=['POST'])
def register_user():
    #   request contiene la informacion entregada en la request { responsables: [adulto_id1, adulto_id2], chats: [chatId1, chatId2, chatId3] }

    json_data = request.json
    responsables = json_data.get('responsables')
    chats = json_data.get('chats')

    if responsables and chats:
        print("responsables", responsables)
        print("chats", chats)
        create_table()
        details = register(chats, responsables)     
        details = ["registered using bdd functions"]
        return jsonify({ 'message': "success", 'details': details, 'statusCode': 200 })
    
    else:
        print('==============================')
        print('error al recibir informacion del bot')
        print('==============================')
        return jsonify({ 'message': "failed", 'details': ["Bad request"], 'statusCode': 400 })
    

@app.route('/get-responsables', methods=['POST'])
def responsables():
    #   request contiene la informacion entregada en la request { chatId: "chat_id" }
    json_data = request.json
    chatId = json_data.get('chatId')
    text = json_data.get('text')

    if not (chatId and text):
        print('==============================')
        print('error al recibir informacion del bot')
        print('==============================')
        return jsonify({'class_name': "Error bot"})
    
    apicall = requests.post(API_GPT, json={'message': text})
    if apicall.status_code == 200:
        apicall = json.loads(apicall.content.decode('utf-8'))
        if apicall == "NO":
            return jsonify({'class_name': "NO"})
        responsables = get_responsibles(chatId)
        if not responsables:
            return jsonify({'responsibles': [], 'class_name': apicall["class_name"]})
        return jsonify({'responsibles': responsables, 'class_name': apicall["class_name"]})