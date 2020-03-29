FROM freqtradeorg/freqtrade:master

RUN curl https://raw.githubusercontent.com/freqtrade/freqtrade/develop/requirements-plot.txt -o requirements-plot.txt
RUN pip install -r requirements-plot.txt --no-cache-dir
