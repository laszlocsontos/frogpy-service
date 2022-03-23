## Getting Started for Local Dev and Deploy

1. Pull this repo
2. Install Python 2.7 and some development tools: `sudo apt-get install python2.7 python-pip python-setuptools python-virtualenv`
3. Install the latest version of Frog locally, check next section for details
4. Install Redis
    + `sudo apt-get install redis-server redis-tools`
    + `systemctl disable redis-server.service`
    + `systemctl start redis-server.service`
5. run `sh init-venv.sh` to initialize a virtual python environment
6/a. run `sh start-server.sh` to start the frog service
6/b. run `sh stop-server.sh` to start the frog service
7. run `sh build.sh` to make a distributable package
8. deploy `frogpy-service.zip` to the target node
    + `scp build/frogpy-service.zip centos@<host>:~`
    + `ssh centos@<host>`
    + `unzip frogpy-service.zip`
    + `cd frogpy-service`
    + `env ENVIRONMENT=<envname> ./start-server.sh`
9. during development test cases can be executed by running `sh runtests.sh`

## Steps Taken to compile Frog from source

- Have a sane C/C++ compiler toolchain installed
    + Use `sudo yum install gcc gcc-c++ autoconf autoconf-archive automake libtool perl-ExtUtils-PkgConfig` on CentOS/RHEL
    + Use `sudo apt-get install gcc g++ autoconf autoconf-archive automake libtool pkg-config` on Debian/Ubuntu
- Compile _ticcutils_
    + https://github.com/LanguageMachines/ticcutils
- Compile _libfolia_
    + https://github.com/LanguageMachines/libfolia
- Compile _ucto_
    + https://github.com/LanguageMachines/ucto
- Compile _timbl_
    + https://github.com/LanguageMachines/timbl
- Compile _mbt_
    + https://github.com/LanguageMachines/mbt
- Compile _frogdata_
    + https://github.com/LanguageMachines/frogdata
- Compile _frog_
    + https://github.com/LanguageMachines/frog

## Sample environment configuration files

Directory env contains sample configuration files for various environments (development, test, production). Currently the following options are supported which have the following default values.

```
FROG_CONFIG=/usr/local/etc/frog/frog.cfg
FROG_OPTIONS="{ \"parser\": \"False\" }"
REDIS_HOST=localhost
REDIS_PORT=6379
AUTH_TOKEN=
HTTP_PORT=5000
```

Please note that `AUTH_TOKEN` must have a value otherwise the server will return HTTP 500 on purpose when processing the `Authorization` header.

## REST API

- Send text to be analysed and store the result in Redis and refresh the entry's TTL (now + 1day) if it already exists

    ```
    curl -H "Authorization: a7638cbc-e455-481e-a139-379af3c1bdd4" -H "Content-Type: text/plain" http://localhost:5000/analyse -XPOST \
    -d "Toerisme, cultuur, bedrijfsleven en de gemeente Utrecht slaan de handen ineen om de de stad beter te verkopen. Na het succes van de Tourstart is het nu tijd om stappen te maken. ,,Utrecht is een sterk merk, maar we moeten het intensiever uitventen,'' zegt Richard Kraan van Toerisme Utrecht."
    ```


- Remove Frog's data from the cache manually if necessary

    ```
    curl -H "Authorization: a7638cbc-e455-481e-a139-379af3c1bdd4" -H "Content-Type: text/plain" http://localhost:5000/analyse -XDELETE \
    -d "Toerisme, cultuur, bedrijfsleven en de gemeente Utrecht slaan de handen ineen om de de stad beter te verkopen. Na het succes van de Tourstart is het nu tijd om stappen te maken. ,,Utrecht is een sterk merk, maar we moeten het intensiever uitventen,'' zegt Richard Kraan van Toerisme Utrecht."
    ```

- Get data from Frog's cache without changing the entry's TTL

    ```
    curl -H "Authorization: a7638cbc-e455-481e-a139-379af3c1bdd4" -H "Content-Type: text/plain" http://localhost:5000/analyse -XGET \
    -d "Toerisme, cultuur, bedrijfsleven en de gemeente Utrecht slaan de handen ineen om de de stad beter te verkopen. Na het succes van de Tourstart is het nu tijd om stappen te maken. ,,Utrecht is een sterk merk, maar we moeten het intensiever uitventen,'' zegt Richard Kraan van Toerisme Utrecht."
    ```
