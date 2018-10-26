### Project MESBack

A CanionLabs project

[![Build Status](https://travis-ci.org/canionlabs/MONARBack.svg?branch=master)](https://travis-ci.org/canionlabs/MONARBack)


### Decouple Schema
| Name       | Type | Sample                                  |
| ---------- | ---  | --------------------------------------- |
| SECRET_KEY | str  | super-secret-password                   |
| DEBUG      | bool | True                                    |
| DB_URL     | str  | postgres://USER:PASSWORD@HOST:PORT/NAME |

### Run tests
```
docker-compose run -e DJANGO_SETTINGS_MODULE=monar_back.settings.tests --no-deps --rm web py.test
```

### Run locally
```
docker-compose up --build
```