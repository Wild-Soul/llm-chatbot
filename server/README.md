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


* I want you to build the backend APIs for above feature, using Python and FastAPI. As for data storage and persistence prefer to use PostgreSQL, come up with a data-model for this.
* Be minimalistic with additional dependencies.
* For chatbot response I would say that this is going to be forwared to another microservice maybe through a message bus like rabbitMQ. And this other service is going to generate and send the response, for now let it be a static response to any message: "Work in progress, stay tuned!".
* Additonally make sure to cover up all edge cases.
