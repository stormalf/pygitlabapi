import os
from pygitlabapi import gitlabApi

iurl = "https://gitlab.com/api/v4"
ijson = "project.json"
imethod="POST"
iapi = "/projects"
iuser= os.environ.get("GITLAB_USER")
itoken = os.environ.get("GITLAB_TOKEN")
message= gitlabApi.rungitlabApi(api=iapi, method=imethod, url=iurl, user=iuser, token=itoken, json=ijson )
print(message)