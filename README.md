# Matrix bot

## Bot do Matrixa, który po dołączeniu do pokoju codziennie o zadanej godzinie wybiera jedno ze starych zdjęć umieszczonych w tym pokoju i forwarduje je na ten pokój. Celem może być np. okazjonalna ponowna radość ze starego mema albo refleksja na temat nieuniknioności przemijania czasu.


#### First of all, create the .env file:
```shell
cp .env-dist .env
```
##### and replace default parameters with your own configuration

#### Create virtual enviroment (optional):
```shell
virtualenv .venv
source .venv/bin/activate
```

#### Install all required packages:
```shell
pip install -r requirements.txt
```

#### Now you can start the bot:
```shell
./bot.sh
```
