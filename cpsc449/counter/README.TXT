README.TXT


Team Members: 


Uday Kumar Reddy Margadi (CWID - 894865609) 
Shrinidhi Pande (CWID - 887347474)


Cookie-based Sessions


In this project, we are going to implement sessions using two ways. 


* Default session implementation using flask
* Using Session Interface which can replace the default session implementation provided by the flask. 


By setting USE_SESSION_STORE to false, the project will implement the default session provided by the flask. By setting to True, will use our custom session implementation written in the session.py.


We have two services running on this project. It was mentioned in the Procfile, how the applications have to run. One is counter service that can access the browser and the other is a key-value store service that can be accessed via HTTP. We are going to use this service to store session details. 


Now, we have left so much to do in the sessions.py file. In KeyValueSessionStore we have to override, set_key, get_key, and delete_key methods. We have to make HTTP calls to the key-value store service in order to set, get, and delete session details. In order to call key-value store service via HTTP, requests method is used. Requests is a simple HTTP library in python.


I’m going to list how we have implemented and handled set_key, get_key, and delete_key methods in KeyValueSessionStore class.


Set_key:


In this method, we get session id and session data as parameters. We have made a POST request to key-value store service with the session id and session data.






Get_key:


In this, we extract session details whenever it is needed. We are making a GET request to key-value store service and return the details of the particular session.


Delete_key:


This method is used to delete the data of the session. For this, we are making DELETE calls to key-value store service.




In order to list down all the session data, We have implemented dump.py which accepts URL as an argument and makes a GET HTTP call to key-value store service(match method) to get all sessions(keys) or else if we make a request with any prefix, it returns sessions(keys) which match the prefix. After getting keys, we are iterating through it, making a GET call to key-value store service to get details of that particular key or a session.