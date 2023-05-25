import streamlit as st
from functions import ideator
import json
import os
import sys
from datetime import datetime
import redis



def main():
    redis_host = os.environ.get("REDIS_1_HOST")
    redis_port = 25061
    redis_password = os.environ.get("REDIS_1_PASSWORD")
    rd = redis.Redis(host=redis_host, port=redis_port, password=redis_password, ssl=True, ssl_ca_certs="/etc/ssl/certs/ca-certificates.crt")

    system_prompt = rd.get("matej@closersintoleaders.com-systemprompt-01").decode('utf-8')

    # Create a title for the chat interface
    st.title("Pat - Closers.io")
    st.write("This bot is still in alpha. To test, first click the button below.")
    
    if st.button('Click to Start or Restart'):
        st.write("Hey [NAME] - Pat here from Cole Gordon's Remote Closing Academy. I saw you were potentially considering getting into remote closing. Are you still looking into doing that? Let me know, I might have a few resources I can send over or help point you in the right direction. If you don't want me to text you, just reply 'stop' and I'll cease all communication moving forward :)")
        restart_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('database.jsonl', 'r') as db, open('archive.jsonl','a') as arch:
        # add reset 
            arch.write(json.dumps({"restart": restart_time}) + '\n')
        #copy each line from db to archive
            for line in db:
                arch.write(line)

        #clear database to only first two lines
        with open('database.jsonl', 'w') as f:
        # Override database with initial json files
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "assistant", "content": "Hey [NAME] - Pat here from Cole Gordon's Remote Closing Academy. I saw you were potentially considering getting into remote closing. Are you still looking into doing that? Let me know, I might have a few resources I can send over or help point you in the right direction. If you don't want me to text you, just reply 'stop' and I'll cease all communication moving forward :)"}            ]
            f.write(json.dumps(messages[0])+'\n')
            f.write(json.dumps(messages[1])+'\n')



    #initialize messages list and print opening bot message
    #st.write("Hi! This is Tara. Seems like you need help coming up with an idea! Let's do this. First, what's your job?")

    # Create a text input for the user to enter their message and append it to messages
    userresponse = st.text_input("Enter your message")
    

    # Create a button to submit the user's message
    if st.button("Send"):
        #prep the json
        newline = {"role": "user", "content": userresponse}

        #append to database
        with open('database.jsonl', 'a') as f:
        # Write the new JSON object to the file
            f.write(json.dumps(newline) + '\n')

        #extract messages out to list
        messages = []

        with open('database.jsonl', 'r') as f:
            for line in f:
                json_obj = json.loads(line)
                messages.append(json_obj)

        #generate OpenAI response
        messages = ideator(messages)

        #append to database
        with open('database.jsonl', 'a') as f:
        # Write the new JSON object to the file
            f.write(json.dumps(messages[-1]) + '\n')



        # Display the response in the chat interface
        string = ""

        for message in messages[1:]:
            string = string + message["role"] + ": " + message["content"] + "\n\n"
        st.write(string)
            

if __name__ == '__main__':
    main()


    
