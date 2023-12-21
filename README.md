# cyber-defender-backend


el bot le envía al backend dos campos: la lista de los responsables y la lista de los chatsId, como:
>{
  responsables: [adulto_id1, adulto_id2],
  chats: [chatId1, chatId2, chatId3]
}
 
el backend le responde 
>{
  message: "success",
  details: []
  statusCode: 200
}

>{
  message: "failed",
  details: ["Bad request"],
  statusCode:400
}

Cuando haya un nuevo mensaje, el bot le envía un payload al backend con el texto
>{
  text: "texto del chat",
  chatId: "chat_id"
}

El backend le responde: 
>{
  class: "NO"
}

>{
  class: "OFP"
  responsables: [adulto_id1, adulto_id2, ..., adulto_idN],
}
