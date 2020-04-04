# freqtrade

## Create docker image

docker-compose pull
docker-compose build

## Running

docker-compose run -d freqtrade trade --strategy strategy_name
docker-compose run freqtrade hyperopt --hyperopt HyperOptBBRSI -e 100 --strategy strategy_name
