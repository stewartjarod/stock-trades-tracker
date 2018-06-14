#!/usr/bin/env python
#

# <bitbar.title>Stock Trades</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Jarod Stewart</bitbar.author>
# <bitbar.author.github>stewartjarod</bitbar.author.github>
# <bitbar.desc>Add and track your stock trades. Shows suggested stop loss and sell points, alerts when meeting either stop or sell price.</bitbar.desc>
# <bitbar.image>https://raw.githubusercontent.com/stewartjarod/stock-trades-tracker/master/screenshot.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>

import json, urllib2, os, subprocess, sys
icon = "iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAMAAADzapwJAAAAAXNSR0IArs4c6QAAAAlwSFlzAAAPYQAAD2EBqD+naQAAActpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx4bXA6Q3JlYXRvclRvb2w+QWRvYmUgSW1hZ2VSZWFkeTwveG1wOkNyZWF0b3JUb29sPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KKS7NPQAAAW5QTFRFAAAAAAAAAAAAAACAAICAgICAVVVVQEBAMzMzMzNmK1VVM01NLkZGM0REOkJKOEBINEFIOD5LN0NJNUBKN0FGN0FLNUJKOUFJOEBIOEJJNkFHNkFLOEJJOEFIOUJIOEFLN0FKNkJINkFJOEJKN0JKN0FJNkBHNkBKOEJJN0FJNkBIOEJJOEFIOEFKNkFIN0BJNkFINkFKOEBJN0JIN0FINkFJNkBJOEBJOEBIOEJIOEJKN0FJNkJJOEFJN0JJNkFIN0JJN0FKNkFJNkBJOEBJN0FIN0FJN0FJNkBIOEFKN0FJN0FINkFJOEFJN0FIOEFKN0FKNkBJOEBJN0JJN0BJN0FKNkFJOEFJN0FJN0FJN0FJN0FJN0FJNkFJN0FJN0FJN0FJN0FJN0FJN0FJNkFJN0FJN0FJOEFJN0FJN0FJN0FJN0FJOEJKOURMOkRMOkRNOkVNOkVOO0VOO0ZOO0ZPPEdPPEdQPUhQPUhRQUxWN2zrtgAAAGx0Uk5TAAECAgICAwQFBQYKCw8fICcpKjAzMz4/QElLS01OUVJTVV5gYWJkZGVmZ2lubnFzdXV3eHl6e3t8fICChImLjZCRlpeXmJmam5yeoqSlpqqtrq6vuru8vMjLzM3P09vf5Obo7u/w8fj5+/z+f4t3XAAAAUtJREFUGBlVwWcjQmEYgOH7abxvZYvI3mTvvbJDZkbnJNnbCQn/XtEHroscwd3V5Ub4T5hLp+cQ/hEwLcsEIUfIUjTc3TWgyBJQOEC0DeJxsGkBB4oMpwZqTx4fT2oB7SSjOVIFVBymrZsbK31QCVRFmjkPhnT90fvTvi8W8+0/vR/V69D8ObGLs9PX28kSiEahZPL27fTsMkZpeDG8GyzAjmlipyC4F17aKiVjzFszhcIwUEzVeMfIcFO2CiuFYBhQtAyr5bhxMLwZ6NzpAMOAlp1Ax1Y/Cqgb7O4Z8oNhIuNrC0sr03ngpOn+OXldDYYJs6m3l48QP7x9vcWAaQKNofVWQchRcHxMjpClXC6Xw+ZPJPyiPMqphT+ilhXlL8Ezs72ReHhIbGzPeBB+2cm/+vpMJZOpz6+rPOz8EnTbxMDI6OjIwES7RoBv8fI7D+ewmsIAAAAASUVORK5CYII="

stocks_file = '/tmp/trade-tracker/stocks.json'
if not os.path.isdir('/tmp/trade-tracker'):
    os.mkdir('/tmp/trade-tracker')

def displayNotification(message,title=None,soundname=None):
    """
        Display an OSX notification with message title an subtitle
        sounds are located in /System/Library/Sounds or ~/Library/Sounds
    """
    titlePart = ''
    if(not title is None):
        titlePart = 'with title "{0}"'.format(title)
    # subtitlePart = ''
    # if(not subtitle is None):
    #     subtitlePart = 'subtitle "{0}"'.format(subtitle)
    soundnamePart = ''
    if(not soundname is None):
        soundnamePart = 'sound name "{0}"'.format(soundname)
    # icon = 'with icon {0}'.format('caution')

    appleScriptNotification = 'display notification "{0}" {1} {2}'.format(message, titlePart, soundnamePart)
    subprocess.call("osascript -e '{0}'".format(appleScriptNotification), shell=True)

def get_stock_quotes(stocks):
    list = []
    for stock in stocks:
        list.append(stock['stock'])
    response = urllib2.urlopen('https://api.iextrading.com/1.0/stock/market/batch?symbols={0}&types=quote'.format(','.join(list)))
    return json.loads(response.read())

def prompt(text='', defaultAnswer='', icon='note', buttons=('Cancel','Ok'), defaultButton=1):
    try:
        d = locals()
        d['buttonsStr'] = ', '.join('"%s"' % button for button in buttons)
        d['defaultButtonStr'] = isinstance(defaultButton, int) and buttons[defaultButton] or defaultButton
        return subprocess.check_output(['osascript', '-l', 'JavaScript', '-e', '''
            const app = Application.currentApplication()
            app.includeStandardAdditions = true
            const response = app.displayDialog("{text}", {{
                defaultAnswer: "{defaultAnswer}",
                withIcon: "{icon}",
                buttons: [{buttonsStr}],
                defaultButton: "{defaultButtonStr}"
            }})
            response.textReturned
        '''.format(**d)]).rstrip()
    except subprocess.CalledProcessError:
        pass

def entry(title='---', **kwargs):
    args = ' '.join('{}=\'{}\''.format(k,v) for k,v in kwargs.items() if v is not None)
    if args: args = '|' + args
    print(title + args)

def create_stocks_file():
    with open(stocks_file, 'wt') as f:
        f.write('{}')

def read_stocks_file():
    with open(stocks_file, 'rt') as f:
        return json.loads(f.read())

def add_stock_to_stocks_file(stock):
    stocks = read_stocks_file()
    stocks[stock['stock']] = stock
    with open(stocks_file, 'wt') as f:
        f.write(json.dumps(stocks))

def remove_stock_from_stocks_file(ticker):
    stocks = read_stocks_file()
    stocks.pop(ticker, None)
    with open(stocks_file, 'wt') as f:
        f.write(json.dumps(stocks))

def create_output_string(quote, stockObj):
    output = stockObj['stock']
    output += ": $"
    output += "{:0.2f} ".format(quote["latestPrice"])
    pl = (quote["latestPrice"] - stockObj['price']) * stockObj['shares']
    output += "(${:0.2f}) ".format(pl)

    output += " L: {:0.2f} ".format(stockObj['stop'])
    output += " S: {:0.2f} ".format(stockObj['sell'])

    color = "red" if quote["changePercent"] < 0 else "green"
    quote_url = 'https://swingtradebot.com/equities/' + stockObj['stock']
    output += " | color=" + color + " href=" + quote_url
    return output

def PLNow(stocks):
    totalPL=0
    finalOutput = ''

    if len(stocks) > 0:
        quotes = get_stock_quotes(stocks)
        for stockObj in stocks:
            quote = quotes[stockObj['stock']]['quote']
            stockObj['stop'] = (stockObj['price'] * 0.99)
            stockObj['sell'] = (stockObj['price'] * 1.05)

            if quote['latestPrice'] >= stockObj['sell']:
                sellTitle = "SELL: {}".format(stockObj['stock'])
                sellMessage = "Sell Price: {:0.2f}".format(stockObj['sell'])
                displayNotification(sellMessage, sellTitle, "Pop")
            elif quote['latestPrice'] <= stockObj['stop']:
                stopTitle = "STOP LOSS: {}".format(stockObj['stock'])
                stopMessage = "Stop Price: {:0.2f}".format(stockObj['stop'])
                displayNotification(stopMessage, stopTitle, "Ping")

            totalPL += (quote['latestPrice'] - stockObj['price']) * stockObj['shares']
            finalOutput += create_output_string(quote, stockObj) + '\r\n'

        print '{}${:0.2f} | color={}'.format(':chart_with_downwards_trend:' if totalPL < 0 else ':chart_with_upwards_trend:', totalPL, "red" if totalPL < 0 else "green")
        print '---'
        print finalOutput

if len(sys.argv) == 1:
    entry('|templateImage=\'%s\'' % icon)
    entry('---')
    entry('Add a trade...', bash=__file__, param1='add', terminal='false', refresh='true')
    entry('---')
    if os.path.isfile(stocks_file):
        stocks = read_stocks_file()
        if len(stocks) > 0:
            stockObjects = []
            for ticker, stock in stocks.iteritems():
                stockObjects.append(stock)
            PLNow(stockObjects)
            entry('---')
            entry('Remove stocks:')
            for ticker, stock in stocks.iteritems():
                entry('{}'.format(ticker), bash=__file__, param1='remove', param2=ticker, terminal='false', refresh='true')
    else:
        create_stocks_file()
    entry('---')
    entry('Data provided for free by IEX.')
elif len(sys.argv) == 2 and sys.argv[1] == 'add':
    stock = prompt('Stock symbol')
    price = float(prompt('Price paid per share'))
    shares = int(prompt('How many shares?', '100'))
    add_stock_to_stocks_file({'stock': stock, 'price': price, 'shares': shares})
elif len(sys.argv) == 3 and sys.argv[1] == 'remove':
    remove_stock_from_stocks_file(sys.argv[2])
