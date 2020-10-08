# user_focused_locust_boilerplate
Locust is an easy to use, scriptable and scalable performance testing tool. This boilerplate is barebones for testing user behavior focused load testing. This can act as a starting point for testing server that have user focused test/use cases. 

### Structure 
1. ```base_user.py``` contains the barebone code for log_in, logging_response, validating_response and handling user's pool. 
2. Extend the base_user.py to implement api for login
3. Use methods postfix with *hook* to add or update cookies or locally store token for api calls to follow. 
4. Update validate_resp ```is_valid_response_data``` as per your api needs. 
5. You will probably need to generate dummy users. Those will be imported into memory from file named ```USER_CREDENTIALS_FILE_NAME```. This script will try to log them in with ```USER_API_PASSWORD``` as password. 
6. Because locust uses the local copy of code provided to slave nodes. For distributed testing, branch your code and divide your users per machine. 

### Setup & Requirements
1. Setup virtual env
2. ``` python > 3.7  ```
3. ``` pip3 install requirements.txt ```
4. run command ``` locust -f locust_files/your_user.py ```

