#!/usr/bin/env python
#

# <bitbar.title>Stock Trades</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Jarod Stewart</bitbar.author>
# <bitbar.author.github>stewartjarod</bitbar.author.github>
# <bitbar.desc>Add and track your stock trades. Shows suggested stop loss and sell points, alerts when meeting either stop or sell price.</bitbar.desc>
# <bitbar.image>https://raw.githubusercontent.com/stewartjarod/stock-trades-tracker/master/screenshot.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>

import json
import os
import subprocess
import sys
import time
import urllib2

scales_icon = "iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAMAAADzapwJAAAAAXNSR0IArs4c6QAAAAlwSFlzAAAPYQAAD2EBqD+naQAAActpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx4bXA6Q3JlYXRvclRvb2w+QWRvYmUgSW1hZ2VSZWFkeTwveG1wOkNyZWF0b3JUb29sPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KKS7NPQAAAW5QTFRFAAAAAAAAAAAAAACAAICAgICAVVVVQEBAMzMzMzNmK1VVM01NLkZGM0REOkJKOEBINEFIOD5LN0NJNUBKN0FGN0FLNUJKOUFJOEBIOEJJNkFHNkFLOEJJOEFIOUJIOEFLN0FKNkJINkFJOEJKN0JKN0FJNkBHNkBKOEJJN0FJNkBIOEJJOEFIOEFKNkFIN0BJNkFINkFKOEBJN0JIN0FINkFJNkBJOEBJOEBIOEJIOEJKN0FJNkJJOEFJN0JJNkFIN0JJN0FKNkFJNkBJOEBJN0FIN0FJN0FJNkBIOEFKN0FJN0FINkFJOEFJN0FIOEFKN0FKNkBJOEBJN0JJN0BJN0FKNkFJOEFJN0FJN0FJN0FJN0FJN0FJNkFJN0FJN0FJN0FJN0FJN0FJN0FJNkFJN0FJN0FJOEFJN0FJN0FJN0FJN0FJOEJKOURMOkRMOkRNOkVNOkVOO0VOO0ZOO0ZPPEdPPEdQPUhQPUhRQUxWN2zrtgAAAGx0Uk5TAAECAgICAwQFBQYKCw8fICcpKjAzMz4/QElLS01OUVJTVV5gYWJkZGVmZ2lubnFzdXV3eHl6e3t8fICChImLjZCRlpeXmJmam5yeoqSlpqqtrq6vuru8vMjLzM3P09vf5Obo7u/w8fj5+/z+f4t3XAAAAUtJREFUGBlVwWcjQmEYgOH7abxvZYvI3mTvvbJDZkbnJNnbCQn/XtEHroscwd3V5Ub4T5hLp+cQ/hEwLcsEIUfIUjTc3TWgyBJQOEC0DeJxsGkBB4oMpwZqTx4fT2oB7SSjOVIFVBymrZsbK31QCVRFmjkPhnT90fvTvi8W8+0/vR/V69D8ObGLs9PX28kSiEahZPL27fTsMkZpeDG8GyzAjmlipyC4F17aKiVjzFszhcIwUEzVeMfIcFO2CiuFYBhQtAyr5bhxMLwZ6NzpAMOAlp1Ax1Y/Cqgb7O4Z8oNhIuNrC0sr03ngpOn+OXldDYYJs6m3l48QP7x9vcWAaQKNofVWQchRcHxMjpClXC6Xw+ZPJPyiPMqphT+ilhXlL8Ezs72ReHhIbGzPeBB+2cm/+vpMJZOpz6+rPOz8EnTbxMDI6OjIwES7RoBv8fI7D+ewmsIAAAAASUVORK5CYII="  # NOQA

# file_path = '' # TODO let user set path, suggest using dropbox...
stocks_file = '/tmp/trade-tracker/stocks.json'
trade_history = '/tmp/trade-tracker/trades.json'


def display_notification(message, title=None, sound_name=None):
    """
        Display an OSX notification with message title an subtitle
        sounds are located in /System/Library/Sounds or ~/Library/Sounds
    """
    title_part = ''
    if (not title is None):
        title_part = 'with title "{0}"'.format(title)
    # subtitlePart = ''
    # if(not subtitle is None):
    #     subtitlePart = 'subtitle "{0}"'.format(subtitle)
    sound_name_part = ''
    if not sound_name is None:
        sound_name_part = 'sound name "{0}"'.format(sound_name)
    # icon = 'with icon {0}'.format('caution')

    apple_script_notification = 'display notification "{0}" {1} {2}'.format(message, title_part, sound_name_part)
    subprocess.call("osascript -e '{0}'".format(apple_script_notification), shell=True)


def get_stock_quotes(stocks):
    list = []
    for stock in stocks:
        list.append(stock['stock'])
    response = urllib2.urlopen(
        'https://api.iextrading.com/1.0/stock/market/batch?symbols={0}&types=quote'.format(','.join(list)))
    return json.loads(response.read())


def prompt(text='', default_answer='', icon='note', buttons=('Cancel', 'Ok'), default_button=1):
    try:
        d = locals()
        d['buttonsStr'] = ', '.join('"%s"' % button for button in buttons)
        d['defaultButtonStr'] = isinstance(default_button, int) and buttons[default_button] or default_button
        return subprocess.check_output(['osascript', '-l', 'JavaScript', '-e', '''
            const app = Application.currentApplication()
            app.includeStandardAdditions = true
            const response = app.displayDialog("{text}", {{
                defaultAnswer: "{default_answer}",
                withIcon: "{icon}",
                buttons: [{buttonsStr}],
                defaultButton: "{defaultButtonStr}"
            }})
            response.textReturned
        '''.format(**d)]).rstrip()
    except subprocess.CalledProcessError:
        pass


def entry_string(title='---', **kwargs):
    args = ' '.join('{}=\'{}\''.format(k, v) for k, v in kwargs.items() if v is not None)
    if args: args = '|' + args
    return title + args


def entry(title='---', **kwargs):
    args = ' '.join('{}=\'{}\''.format(k, v) for k, v in kwargs.items() if v is not None)
    if args: args = '|' + args
    print(title + args)


def toggle_alert_for_ticker(ticker):
    stocks = read_stocks_file()
    stock = stocks[ticker]
    stock['alert'] = not stock.get('alert', True)
    stocks[ticker] = stock
    with open(stocks_file, 'wt') as f:
        f.write(json.dumps(stocks))


def create_file(file, data):
    with open(file, 'wt') as f:
        f.write(data)


def read_stocks_file():
    with open(stocks_file, 'rt') as f:
        return json.loads(f.read())


def add_stock_to_stocks_file(stock):
    stocks = read_stocks_file()
    stock['buy_time'] = time.time()
    stocks[stock['stock']] = stock
    with open(stocks_file, 'wt') as f:
        f.write(json.dumps(stocks))


def record_trade(ticker, sell_price):
    stocks = read_stocks_file()
    trade = stocks[ticker]
    trade['sell_price'] = sell_price
    trade['sell_time'] = time.time()
    trade['profit_loss'] = ((trade['sell_price'] - trade['buy_price']) * trade['shares'])

    with open(trade_history, 'rt') as f:
        trades = json.loads(f.read())
    trades.append(trade)
    with open(trade_history, 'wt') as f:
        f.write(json.dumps(trades))


def update_stock_in_stocks_file(stock):
    stocks = read_stocks_file()
    stocks[stock['stock']] = stock
    with open(stocks_file, 'wt') as f:
        f.write(json.dumps(stocks))


def remove_stock_from_stocks_file(ticker):
    stocks = read_stocks_file()
    stocks.pop(ticker, None)
    with open(stocks_file, 'wt') as f:
        f.write(json.dumps(stocks))


def create_output_string(quote, stock):
    pl = (quote["latestPrice"] - stock['buy_price']) * stock['shares']
    color = "red" if pl < 0 else "green"
    quote_url = 'https://swingtradebot.com/equities/' + stock['stock']
    return entry_string(
        '{}: ${:0.2f} {:0.2f} [STOP: {:0.2f} / SELL: {:0.2f}]'.format(
            stock['stock'],
            quote["latestPrice"],
            pl,
            stock['stop'],
            stock['sell']
        ),
        color=color,
        href=quote_url
    )


def overall_PL():
    OverallPL = 0
    with open(trade_history, 'rt') as f:
        trades = json.loads(f.read())
        for trade in trades:
           OverallPL += trade['profit_loss']
    entry('Total P/L: ${:0.2f}'.format(OverallPL))

def pl_totals(stocks):
    total_pl = 0
    final_output = ''

    if len(stocks) > 0:
        quotes = get_stock_quotes(stocks)
        for stock in stocks:
            quote = quotes[stock['stock']]['quote']
            stock['stop'] = (stock['buy_price'] * 0.99)
            stock['sell'] = (stock['buy_price'] * 1.05)

            if quote['latestPrice'] >= stock['sell']:
                sell_title = "SELL: {}".format(stock['stock'])
                sell_message = "Sell Price: {:0.2f}".format(stock['sell'])
                if stock.get('alert', True):
                    display_notification(sell_message, sell_title, "Pop")
            elif quote['latestPrice'] <= stock['stop']:
                stop_title = "STOP LOSS: {}".format(stock['stock'])
                stop_message = "Stop Price: {:0.2f}".format(stock['stop'])
                if stock.get('alert', True):
                    display_notification(stop_message, stop_title, "Ping")

            total_pl += (quote['latestPrice'] - stock['buy_price']) * stock['shares']
            final_output += create_output_string(quote, stock) + '\r\n'

        print '{} Active Trades Current P/L ${:0.2f} | color={}'.format(
            ':chart_with_downwards_trend:' if total_pl < 0 else ':chart_with_upwards_trend:', total_pl,
            "red" if total_pl < 0 else "green")
        print '---'
        print final_output


def initialize():
    entry('|templateImage=\'%s\'' % scales_icon)
    entry('---')
    entry('Add a trade...', bash=__file__, param1='add', terminal='false', refresh='true')
    entry('---')
    overall_PL()
    stocks = read_stocks_file()
    if len(stocks) > 0:
        stockObjects = []
        for ticker, stock in stocks.iteritems():
            stockObjects.append(stock)
        pl_totals(stockObjects)
        entry('---')
        entry('Toggle Alerts:')
        for ticker, stock in stocks.iteritems():
            alert_icon = ":bell:" if stock.get('alert', True) is True else ":no_bell:"
            entry('{} {}'.format(alert_icon, ticker), bash=__file__, param1='toggleAlert', param2=ticker,
                  terminal='false', refresh='true')
        entry('---')
        entry('Remove stocks:')
        for ticker, stock in stocks.iteritems():
            entry('{}'.format(ticker), bash=__file__, param1='remove', param2=ticker, terminal='false',
                  refresh='true')
    entry('---')
    entry('Data provided for free by IEX.')


def check_files():
    if not os.path.isdir('/tmp/trade-tracker'):
        os.mkdir('/tmp/trade-tracker')
    if not os.path.isfile(stocks_file):
        create_file(stocks_file, '{}')
    if not os.path.isfile(trade_history):
        create_file(trade_history, '[]')


check_files()
if len(sys.argv) == 1:
    initialize()
elif len(sys.argv) == 2 and sys.argv[1] == 'add':
    stock = prompt('Stock symbol')
    price = float(prompt('Price paid per share'))
    shares = int(prompt('How many shares?', '100'))
    add_stock_to_stocks_file({'stock': stock, 'buy_price': price, 'shares': shares})
elif len(sys.argv) == 3 and sys.argv[1] == 'remove':
    sell_price = float(prompt('Price sold per share?'))
    record_trade(sys.argv[2], sell_price)
    remove_stock_from_stocks_file(sys.argv[2])
elif len(sys.argv) == 3 and sys.argv[1] == 'toggleAlert':
    toggle_alert_for_ticker(sys.argv[2])
