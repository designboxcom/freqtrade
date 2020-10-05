#!/bin/bash
CONFIG_STD="user_data/config/config.json"
CONFIG_TELEGRAM="user_data/config/config-telegram-simu.json"
CONFIG_EXCHANGE="user_data/config/config-exchange-binance-notrade-for-simu.json"
NBDAYS=90
EPOCHS=10

docker-compose run freqtrade $@ -c $CONFIG_STD -c $CONFIG_TELEGRAM -c $CONFIG_EXCHANGE
