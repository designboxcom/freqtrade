CONFIG_STD="user_data/config/config.json"
CONFIG_TELEGRAM="user_data/config/config-telegram-bbrsi.json"
CONFIG_EXCHANGE="user_data/config/config-exchange-binance-notrade.json"

docker-compose run freqtrade trade -c $CONFIG_STD -c $CONFIG_TELEGRAM \
-c $CONFIG_EXCHANGE --strategy BB3RSIStrategy\
--logfile /freqtrade/user_data/log/bb3rsi.log
