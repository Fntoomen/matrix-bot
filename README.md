# Matrix bot

A bot for the Matrix protocol, which, after joining a room, selects one of the old photos placed in this room every day at the set time and forwards them to this room. The goal may be, for example, the occasional re-joy of an old meme or a reflection on the inevitability of the passage of time.


#### First of all, create the .env file:
```
cp .env-dist .env
```
##### and replace default parameters with your own configuration

#### Create virtual enviroment (optional):
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

#### Note:

- If the room is E2EE then you have to remove the `MINIMAL_AGE` requirement.
    - You can do this by applying a patch: `git apply remove-minimal-age.patch`
