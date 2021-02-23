#!/bin/bash
CONFIG_STD="user_data/config/config.json"
CONFIG_TELEGRAM="user_data/config/config-telegram-simu.json"
CONFIG_EXCHANGE="user_data/config/config-exchange-binance-notrade-for-simu.json"
NBDAYS=60
EPOCHS=500

docker-compose run --service-ports freqtrade download-data -c $CONFIG_STD -c $CONFIG_TELEGRAM -c $CONFIG_EXCHANGE -t 1h --days $NBDAYS --exchange binance && docker-compose run --service-ports freqtrade hyperopt -c $CONFIG_STD -c $CONFIG_TELEGRAM -c $CONFIG_EXCHANGE --strategy BBL3H2RSIStdStrategy --hyperopt HyperOptBBL2H1RSI --logfile /freqtrade/user_data/log/hyperopt_bbl3h2rsi.log --hyperopt-loss DefaultHyperOptLoss -e $EPOCHS
