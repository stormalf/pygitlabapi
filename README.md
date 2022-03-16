# pygitlabapi
python3 module to call gitlab api V4 in command line or inside a module

## pygitlabapi.py

It's a python module that you can include in your python module example with test.py

    python3 pygitlabapi.py -V
    pygitlabapi version : 1.0.0

    python3 pygitlabapi.py --help
    usage: pygitlabapi.py [-h] [-V] [-U USER] [-t TOKEN] [-u URL] [-a API] [-m METHOD] [-J JSONFILE] [-n PER_PAGE]
                        [-p PAGE]

    pygitlabapi is a python3 program that call gitlab apis in command line or imported as a module

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         Display the version of pygitlabapi
    -U USER, --user USER  gitlab user
    -t TOKEN, --token TOKEN
                            gitlab token
    -u URL, --url URL     gitlab url
    -a API, --api API     gitlab api should start by a slash
    -m METHOD, --method METHOD
                            should contain one of the method to use : ['DELETE', 'GET', 'POST', 'PUT']
    -J JSONFILE, --jsonfile JSONFILE
                            json file needed for POST method
    -n PER_PAGE, --per_page PER_PAGE
                            number of results returned per page
    -p PAGE, --page PAGE  page number


## examples

By default if nothing is specified, it will call the api /projects

    GET /projects : list projects ()       

            python3 pygitlabapi.py

Getting  project details 

    GET /projects/{project_id} : get project details (project_id)

            python3 pygitlabapi.py -api /projects/{project_id}
        
Creating a new project

    POST /projects : create a project (jsonfile)

            python3 pygitlabapi.py -api /projects -m POST -J project.json

Deleting a project

    DELETE /projects/{project_id} : delete a project (project_id)

            python3 pygitlabapi.py -api /projects/{project_id} -m DELETE

Updating an existing project

    PUT /projects/{project_id} : update a project (project_id)

            python3 pygitlabapi.py -api /projects/{project_id} -m PUT -J edit_project.json

## release notes

pygitlabapi.py

1.0.0 initial version