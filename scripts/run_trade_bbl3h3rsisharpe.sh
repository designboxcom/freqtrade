CONFIG_STD="user_data/config/config.json"
CONFIG_TELEGRAM="user_data/config/config-telegram-bbl3h3rsisharpe.json"
CONFIG_EXCHANGE="user_data/config/config-exchange-binance-notrade.json"

docker-compose run -d freqtrade trade -c $CONFIG_STD -c $CONFIG_TELEGRAM \
-c $CONFIG_EXCHANGE --strategy BBL3H3RSISharpeStrategy \
--logfile /freqtrade/user_data/log/bbl3h3rsisharpe.log
