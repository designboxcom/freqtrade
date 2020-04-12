# freqtrade

## Create docker image

docker-compose pull
docker-compose build

## Running

docker-compose run -d freqtrade trade --strategy strategy_name
docker-compose run freqtrade hyperopt --hyperopt HyperOptBBRSI -e 100 --strategy strategy_name
ftbg trade --config /freqtrade/user_data/config-ft_bbrsi_bot.json --logfile /freqtrade/user_data/log/dryrun_bb3rsi.log --strategy BB3RSIStrategy
