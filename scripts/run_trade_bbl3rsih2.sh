CONFIG_STD="user_data/config/config.json"
CONFIG_TELEGRAM="user_data/config/config-telegram-bbl3rsih2.json"
CONFIG_EXCHANGE="user_data/config/config-exchange-binance-notrade.json"

docker-compose run -d freqtrade trade -c $CONFIG_STD -c $CONFIG_TELEGRAM \
-c $CONFIG_EXCHANGE --strategy BBL3RSIH2Strategy \
--logfile /freqtrade/user_data/log/bbl3rsih2.log
