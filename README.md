# swiggy-user-service

This service is used to store the user details while signing up on the swiggy

this service contains 2 APIs in total

**routes information:**
<br/>
/user/signup
this API stores user details in Postgres
bases on role it segregates the data

/user/get-user
this API fetches user details from Postgres


**steps to run**
<br/>
create a .env file following the .env.example file
start the uvicorn server by running the command: uvicorn app.server:app
start using the APIs
