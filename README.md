# Matrix bot

A bot for the Matrix protocol, which, after joining a room, selects one of the old photos placed in this room every day at the set time and forwards them to this room. The goal may be, for example, the occasional re-joy of an old meme or a reflection on the inevitability of the passage of time.


#### First of all, create the .env file:
```
cp .env-dist .env
```
##### and replace default parameters with your own configuration
`TIMESTAMP` is the maximal media [timestamp (in milliseconds since the unix epoch) on originating homeserver when this event was sent.](https://spec.matrix.org/v1.8/client-server-api/#definition-clientevent
)
Bot doesn't include media that have a timestamp greater than the one in `.env`, i.e. they are younger.

#### Create virtual enviroment (recommended - if not used you may encounter issues related to conflicting dependencies):
```
virtualenv .venv
source .venv/bin/activate
```

#### Install all required packages:
```
pip install -r requirements.txt
```

#### Now you can start the bot:
```
./bot.sh
```
