#!/bin/bash
CONFIG_STD="user_data/config/config.json"
CONFIG_TELEGRAM="user_data/config/config-telegram-simu.json"
CONFIG_EXCHANGE="user_data/config/config-exchange-binance-notrade-for-simu.json"
NBDAYS=60
EPOCHS=20000

source .env/bin/activate
python scripts/telegram-send.py --config user_data/config/config-telegram-simu.json "computation started" && docker-compose run freqtrade download-data -c $CONFIG_STD -c $CONFIG_TELEGRAM -c $CONFIG_EXCHANGE -t 1h --days $NBDAYS --exchange binance && docker-compose run -d freqtrade hyperopt -c $CONFIG_STD -c $CONFIG_TELEGRAM -c $CONFIG_EXCHANGE --strategy BBL3H2RSIStdStrategy --hyperopt HyperOptBBL2H1RSI --logfile /freqtrade/user_data/log/hyperopt_bbl3h2rsi.log --hyperopt-loss DefaultHyperOptLoss -e $EPOCHS | xargs docker wait && python scripts/telegram-send.py --config user_data/config/config-telegram-simu.json "computation complete" &
