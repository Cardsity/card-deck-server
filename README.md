# card-deck-server
[![Build Status](https://travis-ci.org/Cardsity/card-deck-server.svg?branch=master)](https://travis-ci.org/Cardsity/card-deck-server)
[![Coverage Status](https://coveralls.io/repos/github/Cardsity/card-deck-server/badge.svg?branch=master)](https://coveralls.io/github/Cardsity/card-deck-server?branch=master)
[![GitHub license](https://img.shields.io/github/license/Cardsity/card-deck-server.svg)](https://github.com/Cardsity/card-deck-server/blob/master/LICENSE)  
The cardsity deck :flower_playing_cards: server.

## Installation
The deck server can be started quite easily using docker. The docker image can be get from the GitHub packages of the Cardsity organization.  
To pull the latest image, type: `docker.pkg.github.com/cardsity/card-deck-server/cardsity-deck-server:latest`.
**Note:** To pull this image, you need to [authenticate to GitHub packages](https://help.github.com/en/packages/using-github-packages-with-your-projects-ecosystem/configuring-docker-for-use-with-github-packages#authenticating-to-github-packages).  
The image can then be run. It will expose the post `8020`.  
### Environment variables
- **SECRET_KEY**: The django secret key. Choose a long, randomly generated password for this.
- **ALLOWED_HOSTS**: A list of allowed hosts separated by `,`, e.g.: `127.0.0.1,localhost`
- **DATABASE_URL**: The database url. For more information, see [the `db_url` type of django-environ](https://github.com/joke2k/django-environ#supported-types).
- **DJANGO_AUTOMATIC_MIGRATE**: If this environment variable is set, django will automatically migrate the database on every start.
- **DJANGO_COLLECTSTATIC**: If this environment variable is set, django will automatically collect the static files on every start.
### Creating a superuser
To create a superuser, all of this three environment variables have to be supplied:
- **DJANGO_SUPERUSER_USERNAME**: The username
- **DJANGO_SUPERUSER_EMAIL**: The email
- **DJANGO_SUPERUSER_PASSWORD**: The password

## Different settings
The application itself gives the option to use multiple configurations for the settings. Here is a comparison of them:  
|                      | dev                         | prod                                            |
|----------------------|-----------------------------|-------------------------------------------------|
| Module               | carddeckserver.settings.dev | carddeckserver.settings.prod                    |
| django-debug-toolbar | :heavy_check_mark:          | :x:                                             |
| Secret key           | Fixed secret key            | Loaded from environment                         |
| Debug                | :heavy_check_mark:          | :x:                                             |
| Database             | db.sqlite3 in project root  | Uses the database from the environment variable |

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.  
Please make sure to update tests as appropriate.

## License
[GNU GPL v3.0](LICENSE)