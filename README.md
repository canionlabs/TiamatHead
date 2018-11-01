### Project TiamatHead

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a0f66b65b3d8432bb3689c59b1afb02f)](https://app.codacy.com/app/caiovictormc/TiamatHead?utm_source=github.com&utm_medium=referral&utm_content=canionlabs/TiamatHead&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.org/canionlabs/TiamatHead.svg?branch=master)](https://travis-ci.org/canionlabs/TiamatHead)

A CanionLabs project

<p align="center">
<img src="https://i.pinimg.com/originals/44/da/a5/44daa5b97de51186fea3e6ee765919f7.jpg" height="300" width="250" >
</p>


### Decouple Schema
| Name       | Type | Sample                                  |
| ---------- | ---  | --------------------------------------- |
| SECRET_KEY | str  | super-secret-password                   |
| DEBUG      | bool | True                                    |
| DB_URL     | str  | postgres://USER:PASSWORD@HOST:PORT/NAME |

### Run tests
```
docker-compose run -e DJANGO_SETTINGS_MODULE=tiamat_head.settings.tests --no-deps --rm web py.test
```

### Run locally
```
docker-compose up --build
```