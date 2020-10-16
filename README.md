# Insomnia Python Developer hiring assignment
## Task
Create simple REST API in Flask :
 * healtcheck endpoint 
 * endpoint, which will integrate itself into TronGrid HTTP API (https://developers.tron.network/reference) and return current balance of Tron wallet (wallet address as parameter), use any request/response model 

### Should have
Application should have a config file, which will include among other things a static API key used for authorization request with the 2nd endpoint. Healthcheck can be without authorization. Take care of common errors with standard status codes.

# Solution

Solution is packaged in the docker. 
* I used python:3.8-slim image as many comparissons show advantages compared to alpine, e.g. https://megamorf.gitlab.io/2020/05/06/why-it-s-better-not-to-use-alpine-linux-for-python-projects/
* I used combination of Nginx web server, Gunicorn WSGI and Python Flask Restfull
  * Nginx + Gunicorn = possibility to scale with more docker containers, kubernetes, etc., e.g. https://www.nginx.com/blog/docker-swarm-load-balancing-nginx-plus/ 
   * I used supervisord to manage multiple services in 1 docker (not needed in case you separate the services to containers)
   * Gunicorn is configured to use threading (concurency in workers), see supervisord.conf "--threads", I did not have time/resources to test pseudo-thrads (gevent) - https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7 
  * Flask Restfull - REST API
    * Flask uses asyncio & aiohttp for concurrency/thread
* I used Sphinx for documentation, see usage in section "Documentation"
* I used jsonschema for input validation - Sphinx has issues with code that uses open(FILE) so I included the schema in code and in /pp/validation
* I made health check according to microservices recommendations (memory, disk space, etc.) : https://microservices.io/patterns/observability/health-check-api.html
* improve security with HTTPBasicAuth + werkzeug.security(generate_password_hash, check_password_hash) + https

## Docker

To deploy the docker use either following script of commands in the Appendix section.
```
# deploy container locally
deploy_local.bat
```

## Usage

### windows powershell
```
# endpoints
curl -Method Get -ContentType 'application/json' http://localhost/api/health
curl -Method Get -H @{'apikey' = 'test_key'} -ContentType 'application/json' http://localhost/api/wallet -Body '{"address": "TU7Qu3vRSufcetba8qa4CrJuqRY2Sc7TCQ" }'
```
### bash
```
# endpoints
curl --request GET --header "Content-Type: application/json" --url http://localhost/api/health
curl --request GET --header "key: test_key" --header "Content-Type: application/json" --url http://localhost/api/wallet --data '{"address": "TU7Qu3vRSufcetba8qa4CrJuqRY2Sc7TCQ" }'
```

## Monitoring, Debugging and Logging

### Monitoring

#### Number of request
* Flask-profiler:
 * web: http://127.0.0.1:5000/flask-profiler/ 
 * as JSON: http://127.0.0.1:5000/flask-profiler/api/measurements?sort=elapsed,desc

### Logs
* Supervisord: /var/log/supervisor/supervisord.log
* Nginx: /var/log/nginx/access.log & /var/log/nginx/error.log
* Gunicorn: /app/logs/gunicorn.log
* Flask: /app/logs/main.log

### Debugging
* possible debugging with pdb library and pdb.set_trace() - library imported but not used in code

## Coding style
* by adhering to pep8 conventions (whenever possible ;) )

## Documentation

Automatic documentation is created from docstrings by sphinx.
```
pip install sphinx
pip install sphinx_rtd_theme
```
generate new documenation (app\docs):  
1. add new file to be documented under index.rst
2. run sphinx script (make.bat windows, MakeFile linux)
```
make html
```
[HTTP server documentation](https://htmlpreview.github.io/?https://github.com/5uperpalo/insomnia-http-server-assignment/blob/master/app/docs/_build/html/index.html)

## Testing
Testing is done using PyTest module. Example tests are included in app/tests/test_example.py.
PyTest runs by default every .py file that contains "test" in its name (note : tests_ etc. is not included).
Tests can be run in bash:

```
# add -m parameter if you want to run test with path context of current run folder:  
python -m pytest
# run all tests:  
pytest
# run pep8 check
pytest --pep8
# run flake8 check
pytest --flakes
# run testcoverage test - checks how much of the code is covered by tests
pytest --cov
```

# Appendix
## Usefull commands:

```

# build dockerfile - must be runned from folder with dockerfile definition
docker build -t insomnia .

# show list of images
docker images

# show list of containers
docker container ls
docker ps

# remove container (add -f parameter for forced remove)
docker rm insomnia -f

# remove image
docker image remove insomnia

# start/stop container
docker start/stop insomnia

# run container with port forwarding
docker run -p container_port:local_port imagename

# mount local directory to/over the container directory by [-v] parameter - changes will be removed after reset of container (for dev/testing purpose)
docker run -v app:/app -p 80:80 --name insomnia insomnia & ^

# run linux bash in container
docker exec -it insomnia /bin/bash

```