You need to develop a chat widget that allows users to send messages to a chatbot. The widget should support the following actions:
* Send a message
    * The chatbot should respond with a message
        * you can decide how ot implement this chatbot. It could be as simple or as complex as you'd like. Ultimately, sending a message to the chatbot should return a response.
* Delete message
    * The user can delete a message that they've sent
    * They should only eb able to delete any sent message.
* Edit message
    * the user can edit the message they've sent
    * They shoudl only be able to edit any message.
    * If they edit a message then it should trigger a new response from the bot.

* Hint:
    * You can follow RESTful api endpoints for this
* The chatbot should persist the state, ie. it should maintain a continuous conversation state.


- Running postgres (not detached):
```
docker run \
  -e POSTGRES_PASSWORD="password" \
  -p 5432:5432 \
  --name my_postgres \
  postgres:16.7-alpine3.21
```

- Running pgAdmin (not detached):
```
docker run \
  -p 80:80 \
  --name pgadmin \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="admin" \
  --link my_postgres:postgres \
  dpage/pgadmin4:9.0.0
```
