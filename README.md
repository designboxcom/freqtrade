# freqtrade

## Create docker image

docker-compose pull
docker-compose build

## Running

docker-compose run -d freqtrade trade --strategy strategy_name
docker-compose run freqtrade hyperopt --hyperopt HyperOptBBRSI -e 100 --strategy strategy_name
ftbg trade --config /freqtrade/user_data/config-ft_bbrsi_bot.json --logfile /freqtrade/user_data/log/dryrun_bb3rsi.log --strategy BB3RSIStrategy
docker-compose run freqtrade hyperopt --strategy BB3RSIForHyperoptsStrategy --hyperopt HyperOptBBRSI --logfile /freqtrade/user_data/log/hyperopt_bbrsi.log --hyperopt-loss SharpeHyperOptLoss -e 50

## Sending a status when the daemon finishes

. .env/bin/activate
docker wait <instance> && python scripts/telegram-send.py --config user_data/config/config-telegram-simu.json "computation complete" &
