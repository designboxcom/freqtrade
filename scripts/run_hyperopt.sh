#!/bin/bash
CONFIG_STD="user_data/config/config.json"
CONFIG_TELEGRAM="user_data/config/config-telegram-simu.json"
CONFIG_EXCHANGE="user_data/config/config-exchange-binance-notrade.json"

source .env/bin/activate
python scripts/telegram-send.py --config user_data/config/config-telegram-simu.json "computation started" && docker-compose run freqtrade download-data -c $CONFIG_STD -c $CONFIG_TELEGRAM -c $CONFIG_EXCHANGE -t 1h --days 90 --exchange binance && docker-compose run -d freqtrade hyperopt -c $CONFIG_STD -c $CONFIG_TELEGRAM -c $CONFIG_EXCHANGE --strategy BBL3RSIH2Strategy --hyperopt HyperOptBBL3RSIH2 --logfile /freqtrade/user_data/log/hyperopt_bbrsi.log --hyperopt-loss SharpeHyperOptLoss -e 50 | xargs docker wait && python scripts/telegram-send.py --config user_data/config/config-telegram-simu.json "computation complete" &
