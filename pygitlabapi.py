#!/usr/bin/python3
# -*- coding: utf-8 -*-
from cryptography.fernet import Fernet
import requests
from json import loads as jsonload
import argparse
import os


'''
pygitlabapi.py is to be used by other python modules to automate gitlab api usage.
it could be called in command line.
See gitlab official references to get the correct Api URL and method to use :
    https://docs.gitlab.com/ee/api/api_resources.html

the API used Personal token to access the gitlab server. See for more information : https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html
API version v4 allowed only. 

By default returns the first page of projects with 100 results per page.

Examples : default /projects
GET /projects : list projects ()       

        python3 pygitlabapi.py

GET /projects/{project_id} : get project details (project_id)

        python3 pygitlabapi.py -api /projects/{project_id}
    
POST /projects : create a project (jsonfile)

        python3 pygitlabapi.py -api /projects -m POST -J project.json

DELETE /projects/{project_id} : delete a project (project_id)

        python3 pygitlabapi.py -api /projects/{project_id} -m DELETE

PUT /projects/{project_id} : update a project (project_id)

        python3 pygitlabapi.py -api /projects/{project_id} -m PUT -J edit_project.json

'''

__version__ = "1.0.1"

ALLOWED_METHODS = ["DELETE", "GET", "POST", "PUT"]
URL = "https://gitlab.com/api/v4" 
NO_CONTENT = 204

def pygitlabApiVersion():
    return f"pygitlabapi version : {__version__}"


class gitlabApi():
    def __init__(self, api, method, url, user, token, jsonfile):
        self.api = api
        self.method = method
        self.json = jsonfile
        self.url = url
        self.user = user
        self.token = gitlabApi.crypted(token)


    def __repr__(self):
        return (f"gitlabApi api: {self.api}, method: {self.method}, url: {self.url}")

    #return the encrypted password/token
    @classmethod
    def crypted(cls, token):
        cls.privkey = Fernet.generate_key()        
        cipher_suite = Fernet(cls.privkey)
        ciphered_text = cipher_suite.encrypt(token.encode())
        cls.token = ciphered_text
        return cls.token

    #return the decrypted password/token
    @classmethod
    def decrypted(cls, token):
        cls.token = token
        cipher_suite = Fernet(cls.privkey)
        decrypted_text = cipher_suite.decrypt(cls.token)
        decrypted_text = decrypted_text.decode()
        return decrypted_text

    #execute the gitlab api using a temp instance
    @staticmethod
    def rungitlabApi(api, method, url, user, token, json):
        if token == None:
            response = jsonload('{"message": "Error : token missing!"}')
            return response 
        tempgitlab = gitlabApi(api, method, url, user, token, json)
        response = tempgitlab.gitlabAuthentication()
        tempgitlab = None
        return response       


    #call private function
    def gitlabAuthentication(self):
        response = self.__gitlabTokenAuth()
        return response

    #internal function that formats the url and calls the gitlab apis
    def __gitlabTokenAuth(self):
        apiurl = self.url + self.api  
        header = {}
        header['Accept'] = 'application/json'
        header['Content-Type'] = 'application/json'
        header['PRIVATE-TOKEN'] = gitlabApi.decrypted(self.token)  
        response = self.__gitlabDispatch(apiurl, header)
        return response

    #internal function that calls the requests
    def __gitlabDispatch(self, apiurl, header):
        response = "{}"        
        try:
            if self.method == "POST":
                contents = open(self.json, 'r')
                response = requests.post(apiurl, headers=header, data=contents)
                contents.close()
            elif self.method == "GET":
                response = requests.get(apiurl, headers=header)
            elif self.method == "PUT":
                if self.json == '':
                    response = requests.put(apiurl, headers=header)
                else:
                    contents = open(self.json, 'r')                    
                    response = requests.put(apiurl, headers=header, data=contents)
                    contents.close()
            elif self.method == "DELETE":
                response = requests.delete(apiurl, headers=header)  
        except requests.exceptions.RequestException as e:  
            raise SystemExit(e)   
        if response.status_code == NO_CONTENT:
            response = "{}"
        elif response.status_code != 200:
            response = jsonload('{"message": "Error : ' + str(response.status_code) + ' ' + response.reason + '"}')            
        else:            
            response = response.json()
        return response

def pygitlabapi(args):
    message = ''
    if args.user == '':
        user = os.environ.get("GITLAB_USER")
    else:
        user = args.user  
    if args.token == '':
        itoken = os.environ.get("GITLAB_TOKEN")
    else:
        itoken = args.token               
    if args.api == '' and args.jsonfile == '':
        api=f"/projects"
    else:
        api=args.api    
    if args.url == '':
        iurl = URL
    else:
        iurl = args.url   
    method = args.method     
    if "POST" in method and args.jsonfile == "":
        message = "Error : Json file required with method POST!"
        print(message)
        return message
    if args.method == 'GET':
        api = api + "?per_page=" + str(args.per_page) + "&page=" + str(args.page)
    json = args.jsonfile        
    message= gitlabApi.rungitlabApi(api=api, method=method, url=iurl, user=user, token=itoken, json=json ) 
    return message


if __name__== "__main__":
    helpmethod = f"should contain one of the method to use : {str(ALLOWED_METHODS)}"
    parser = argparse.ArgumentParser(description="pygitlabapi is a python3 program that call gitlab apis in command line or imported as a module")
    parser.add_argument('-V', '--version', help='Display the version of pygitlabapi', action='version', version=pygitlabApiVersion())
    parser.add_argument('-U', '--user', help='gitlab user', default='', required=False)    
    parser.add_argument('-t', '--token', help='gitlab token', default='', required=False)    
    parser.add_argument('-u', '--url', help='gitlab url', default='', required=False)    
    parser.add_argument('-a', '--api', help='gitlab api should start by a slash', default='', required=False)    
    parser.add_argument('-m', '--method', help = helpmethod, default="GET", required=False)   
    parser.add_argument('-J', '--jsonfile', help='json file needed for POST method', default='', required=False)
    parser.add_argument('-n', '--per_page', help='number of results returned per page', default=100, required=False)
    parser.add_argument('-p', '--page', help='page number', default=1, required=False)
    args = parser.parse_args()
    message = pygitlabapi(args)
    print(message)