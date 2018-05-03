from django.shortcuts import render
from Crypto.models import Value
from Crypto.models import CurrencyNews
from django.db import connection
import operator
import matplotlib.pyplot as plt
import numpy as np
from .fusioncharts import FusionCharts
from pylab import *
from django.utils import timezone
from datetime import timedelta
from scipy.stats.stats import pearsonr
import math
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go


stop_word_list = ['credits', 'burst', 'icos', 'zero', 'version', 'purpose', 'tokens', 'ico', 'crypto', 'data', 'social', 'the', 'of', 'to', 'and', 'a', 'in', 'is', 'it', 'you', 'that', 'he', 'was', 'for', 'on', 'are', 'with', 'as', 'I', 'his', 'they', 'be', 'at', 'one', 'have', 'this', 'from', 'or', 'had', 'by', 'hot', 'word', 'but', 'what', 'some', 'we', 'can', 'out', 'other', 'were', 'all', 'there', 'when', 'up', 'use', 'your', 'how', 'said', 'an', 'each', 'she', 'which', 'do', 'their', 'time', 'if', 'will', 'way', 'about', 'many', 'then', 'them', 'write', 'would', 'like', 'so', 'these', 'her', 'long', 'make', 'thing', 'see', 'him', 'two', 'has', 'look', 'more', 'day', 'could', 'go', 'come', 'did', 'number', 'sound', 'no', 'most', 'people', 'my', 'over', 'know', 'water', 'than', 'call', 'first', 'who', 'may', 'down', 'side', 'been', 'now', 'find', 'any', 'new', 'work', 'part', 'take', 'get', 'place', 'made', 'live', 'where', 'after', 'back', 'little', 'only', 'round', 'man', 'year', 'came', 'show', 'every', 'good', 'me', 'give', 'our', 'under', 'name', 'very', 'through', 'just', 'form', 'sentence', 'great', 'think', 'say', 'help', 'low', 'line', 'differ', 'turn', 'cause', 'much', 'mean', 'before', 'move', 'right', 'boy', 'old', 'too', 'same', 'tell', 'does', 'set', 'three', 'want', 'air', 'well', 'also', 'play', 'small', 'end', 'put', 'home', 'read', 'hand', 'port', 'large', 'spell', 'add', 'even', 'land', 'here', 'must', 'big', 'high', 'such', 'follow', 'act', 'why', 'ask', 'men', 'change', 'went', 'light', 'kind', 'off', 'need', 'house', 'picture', 'try', 'us', 'again', 'animal', 'point', 'mother', 'world', 'near', 'build', 'self', 'earth', 'father', 'head', 'stand', 'own', 'page', 'should', 'country', 'found', 'answer', 'school', 'grow', 'study', 'still', 'learn', 'plant', 'cover', 'food', 'sun', 'four', 'between', 'state', 'keep', 'eye', 'never', 'last', 'let', 'thought', 'city', 'tree', 'cross', 'farm', 'hard', 'start', 'might', 'story', 'saw', 'far', 'sea', 'draw', 'left', 'late', 'run', "don't", 'while', 'press', 'close', 'night', 'real', 'life', 'few', 'north', 'open', 'seem', 'together', 'next', 'white', 'children', 'begin', 'got', 'walk', 'example', 'ease', 'paper', 'group', 'always', 'music', 'those', 'both', 'mark', 'often', 'letter', 'until', 'mile', 'river', 'car', 'feet', 'care', 'second', 'book', 'carry', 'took', 'science', 'eat', 'room', 'friend', 'began', 'idea', 'fish', 'mountain', 'stop', 'once', 'base', 'hear', 'horse', 'cut', 'sure', 'watch', 'color', 'face', 'wood', 'main', 'enough', 'plain', 'girl', 'usual', 'young', 'ready', 'above', 'ever', 'red', 'list', 'though', 'feel', 'talk', 'bird', 'soon', 'body', 'dog', 'family', 'direct', 'pose', 'leave', 'song', 'measure', 'door', 'product', 'black', 'short', 'numeral', 'class', 'wind', 'question', 'happen', 'complete', 'ship', 'area', 'half', 'rock', 'order', 'fire', 'south', 'problem', 'piece', 'told', 'knew', 'pass', 'since', 'top', 'whole', 'king', 'space', 'heard', 'best', 'hour', 'better', 'true', 'during', 'hundred', 'five', 'remember', 'step', 'early', 'hold', 'west', 'ground', 'interest', 'reach', 'fast', 'verb', 'sing', 'listen', 'six', 'table', 'travel', 'less', 'morning', 'ten', 'simple', 'several', 'vowel', 'toward', 'war', 'lay', 'against', 'pattern', 'slow', 'center', 'love', 'person', 'money', 'serve', 'appear', 'road', 'map', 'rain', 'rule', 'govern', 'pull', 'cold', 'notice', 'voice', 'unit', 'power', 'town', 'fine', 'certain', 'fly', 'fall', 'lead', 'cry', 'dark', 'machine', 'note', 'wait', 'plan', 'figure', 'star', 'box', 'noun', 'field', 'rest', 'correct', 'able', 'pound', 'done', 'beauty', 'drive', 'stood', 'contain', 'front', 'teach', 'week', 'final', 'gave', 'green', 'oh', 'quick', 'develop', 'ocean', 'warm', 'free', 'minute', 'strong', 'special', 'mind', 'behind', 'clear', 'tail', 'produce', 'fact', 'street', 'inch', 'multiply', 'nothing', 'course', 'stay', 'wheel', 'full', 'force', 'blue', 'object', 'decide', 'surface', 'deep', 'moon', 'island', 'foot', 'system', 'busy', 'test', 'record', 'boat', 'common', 'gold', 'possible', 'plane', 'stead', 'dry', 'wonder', 'laugh', 'thousand', 'ago', 'ran', 'check', 'game', 'shape', 'equate', 'hot', 'miss', 'brought', 'heat', 'snow', 'tire', 'bring', 'yes', 'distant', 'fill', 'east', 'paint', 'language', 'among', 'grand', 'ball', 'yet', 'wave', 'drop', 'heart', 'am', 'present', 'heavy', 'dance', 'engine', 'position', 'arm', 'wide', 'sail', 'material', 'size', 'vary', 'settle', 'speak', 'weight', 'general', 'ice', 'matter', 'circle', 'pair', 'include', 'divide', 'syllable', 'felt', 'perhaps', 'pick', 'sudden', 'count', 'square', 'reason', 'length', 'represent', 'art', 'subject', 'region', 'energy', 'hunt', 'probable', 'bed', 'brother', 'egg', 'ride', 'cell', 'believe', 'fraction', 'forest', 'sit', 'race', 'window', 'store', 'summer', 'train', 'sleep', 'prove', 'lone', 'leg', 'exercise', 'wall', 'catch', 'mount', 'wish', 'sky', 'board', 'joy', 'winter', 'sat', 'written', 'wild', 'instrument', 'kept', 'glass', 'grass', 'cow', 'job', 'edge', 'sign', 'visit', 'past', 'soft', 'fun', 'bright', 'gas', 'weather', 'month', 'million', 'bear', 'finish', 'happy', 'hope', 'flower', 'clothe', 'strange', 'gone', 'jump', 'baby', 'eight', 'village', 'meet', 'root', 'buy', 'raise', 'solve', 'metal', 'whether', 'push', 'seven', 'paragraph', 'third', 'shall', 'held', 'hair', 'describe', 'cook', 'floor', 'either', 'result', 'burn', 'hill', 'safe', 'cat', 'century', 'consider', 'type', 'law', 'bit', 'coast', 'copy', 'phrase', 'silent', 'tall', 'sand', 'soil', 'roll', 'temperature', 'finger', 'industry', 'value', 'fight', 'lie', 'beat', 'excite', 'natural', 'view', 'sense', 'ear', 'else', 'quite', 'broke', 'case', 'middle', 'kill', 'son', 'lake', 'moment', 'scale', 'loud', 'spring', 'observe', 'child', 'straight', 'consonant', 'nation', 'dictionary', 'milk', 'speed', 'method', 'organ', 'pay', 'age', 'section', 'dress', 'cloud', 'surprise', 'quiet', 'stone', 'tiny', 'climb', 'cool', 'design', 'poor', 'lot', 'experiment', 'bottom', 'key', 'iron', 'single', 'stick', 'flat', 'twenty', 'skin', 'smile', 'crease', 'hole', 'trade', 'melody', 'trip', 'office', 'receive', 'row', 'mouth', 'exact', 'symbol', 'die', 'least', 'trouble', 'shout', 'except', 'wrote', 'seed', 'tone', 'join', 'suggest', 'clean', 'break', 'lady', 'yard', 'rise', 'bad', 'blow', 'oil', 'blood', 'touch', 'grew', 'cent', 'mix', 'team', 'wire', 'cost', 'lost', 'brown', 'wear', 'garden', 'equal', 'sent', 'choose', 'fell', 'fit', 'flow', 'fair', 'bank', 'collect', 'save', 'control', 'decimal', 'gentle', 'woman', 'captain', 'practice', 'separate', 'difficult', 'doctor', 'please', 'protect', 'noon', 'whose', 'locate', 'ring', 'character', 'insect', 'caught', 'period', 'indicate', 'radio', 'spoke', 'atom', 'human', 'history', 'effect', 'electric', 'expect', 'crop', 'modern', 'element', 'hit', 'student', 'corner', 'party', 'supply', 'bone', 'rail', 'imagine', 'provide', 'agree', 'thus', 'capital', "won't", 'chair', 'danger', 'fruit', 'rich', 'thick', 'soldier', 'process', 'operate', 'guess', 'necessary', 'sharp', 'wing', 'create', 'neighbor', 'wash', 'bat', 'rather', 'crowd', 'corn', 'compare', 'poem', 'string', 'bell', 'depend', 'meat', 'rub', 'tube', 'famous', 'dollar', 'stream', 'fear', 'sight', 'thin', 'triangle', 'planet', 'hurry', 'chief', 'colony', 'clock', 'mine', 'tie', 'enter', 'major', 'fresh', 'search', 'send', 'yellow', 'gun', 'allow', 'print', 'dead', 'spot', 'desert', 'suit', 'current', 'lift', 'rose', 'continue', 'block', 'chart', 'hat', 'sell', 'success', 'company', 'subtract', 'event', 'particular', 'deal', 'swim', 'term', 'opposite', 'wife', 'shoe', 'shoulder', 'spread', 'arrange', 'camp', 'invent', 'cotton', 'born', 'determine', 'quart', 'nine', 'truck', 'noise', 'level', 'chance', 'gather', 'shop', 'stretch', 'throw', 'shine', 'property', 'column', 'molecule', 'select', 'wrong', 'gray', 'repeat', 'require', 'broad', 'prepare', 'salt', 'nose', 'plural', 'anger', 'claim', 'continent', 'oxygen', 'sugar', 'death', 'pretty', 'skill', 'women', 'season', 'solution', 'magnet', 'silver', 'thank', 'branch', 'match', 'suffix', 'especially', 'fig', 'afraid', 'huge', 'sister', 'steel', 'discuss', 'forward', 'similar', 'guide', 'experience', 'score', 'apple', 'bought', 'led', 'pitch', 'coat', 'mass', 'card', 'band', 'rope', 'slip', 'win', 'dream', 'evening', 'condition', 'feed', 'tool', 'total', 'basic', 'smell', 'valley', 'nor', 'double', 'seat', 'arrive', 'master', 'track', 'parent', 'shore', 'division', 'sheet', 'substance', 'favor', 'connect', 'post', 'spend', 'chord', 'fat', 'glad', 'original', 'share', 'station', 'dad', 'bread', 'charge', 'proper', 'bar', 'offer', 'segment', 'slave', 'duck', 'instant', 'market', 'degree', 'populate', 'chick', 'dear', 'enemy', 'reply', 'drink', 'occur', 'support', 'speech', 'nature', 'range', 'steam', 'motion', 'path', 'liquid', 'log', 'meant', 'quotient', 'teeth', 'shell', 'neck']

def df_scatter(df, title, seperate_y_axis=False, y_axis_label='', scale='linear', initial_hide=False):
   label_arr = list(df)
   series_arr = list(map(lambda col: df[col], label_arr))

   layout = go.Layout(
       title=title,
       paper_bgcolor='rgba(0,0,0,0)',
       #plot_bgcolor='rgba(0,0,0,0)',
       legend=dict(orientation="h"),
       xaxis=dict(type='date'),
       yaxis=dict(
           title=y_axis_label,
           showticklabels=True,
           type=scale
       )
   )

   y_axis_config = dict(
       overlaying='y',
       showticklabels=False,
       type=scale)

   visibility = 'visible'
   if initial_hide:
       visibility = 'legendonly'

   # Form Trace For Each Series
   trace_arr = []
   for index, series in enumerate(series_arr):
       trace = go.Scatter(
           x=series.index,
           y=series,
           name=label_arr[index],
           visible=visibility
       )

       trace_arr.append(trace)

   fig = go.Figure(data=trace_arr, layout=layout)
   return py.plot(fig,auto_open=False, output_type='div')




def say_hello(request):
    # -------------------------- rating -----------------------------------
    current_date = timezone.now()
    current_backdate = current_date - timedelta(days=5)
    topcurr = Value.objects.raw(
        'SELECT 1 as id, currency_name, min(quote) as min_quote, max(quote) as max_quote FROM Value WHERE time>%s and time<%s group by currency_name',
        [current_backdate, current_date]
    )

    rate_list = []
    for line in topcurr:
        rate_value = (line.max_quote - line.min_quote) / line.max_quote
        rate_list.append([line.currency_name, rate_value])
    rate_list.sort(key=lambda x: x[1])
    rate_list = rate_list[:-11:-1]
    #rate_list = rate_list[:10]

    new_rate_list = [str(i[0]) for i in rate_list]
    latest_prices = Value.objects.raw(
        'select distinct f.currency_name, f.time, 1 as id, f.quote from (select currency_name, max(time) as latest_time from CryptoNews.Value group by currency_name) as x inner join CryptoNews.Value as f on f.currency_name = x.currency_name and f.time = x.latest_time where f.currency_name in {}'.format(
            tuple(new_rate_list)))

    for line in latest_prices:
        for i in range(len(rate_list)):
            if (line.currency_name == rate_list[i][0]):
                rate_list[i][1] = line.quote

    # -------------------------- end rating -----------------------------------



    #-------------------------- correlation -----------------------------------
    crypto_list_query = Value.objects.raw('SELECT distinct currency_name, 1 as id FROM Value')
    crypto_list_all = [item.currency_name for item in crypto_list_query]

    currency_pdict = {}
    currency_price_all = Value.objects.raw(
        'SELECT currency_name, quote, 1 as id FROM Value WHERE year(time)>2016 ORDER BY time')

    for record in currency_price_all:
        if record.currency_name in currency_pdict.keys():
            currency_pdict[record.currency_name].append(record.quote)
        else:
            currency_pdict[record.currency_name] = [record.quote]

    bitcoin_baseline = currency_pdict['Bitcoin']

    correlation_list = []

    for crypto_curr in crypto_list_all:
        if crypto_curr in currency_pdict.keys():
            if (len(bitcoin_baseline) <= len(currency_pdict[crypto_curr])):
                correlation_coeff = pearsonr(bitcoin_baseline, currency_pdict[crypto_curr][:len(bitcoin_baseline)])

            if ((not math.isnan(float(correlation_coeff[0]))) & (float(correlation_coeff[0]) > 0.14189)):
                correlation_list.append([crypto_curr, float(correlation_coeff[0])])
    correlation_list = sorted(correlation_list, key=lambda x: x[1], reverse=True)

    top_5 = correlation_list[7:12]
    bot_5 = correlation_list[-6:-1]
    top_list = ['Bitcoin']
    for i in top_5:
        top_list.append(i[0])
    for i in bot_5:
        top_list.append(i[0])

    top_list = [str(i) for i in top_list]

    top_prices = Value.objects.raw(
        'select currency_name, quote, time, 1 as id from Value where year(time)>2016 AND currency_name in {}'.format(
            tuple(top_list)))
    crypto_top_dict = {}
    crypto_top_dict['date'] = []

    for row in top_prices:
        if row.currency_name in crypto_top_dict.keys():
            crypto_top_dict[row.currency_name].append(row.quote)
        else:
            crypto_top_dict[row.currency_name] = [row.quote]
        if (row.currency_name == 'Bitcoin'):
            crypto_top_dict['date'].append(row.time)

    combined_df = pd.DataFrame.from_dict(crypto_top_dict)
    combined_df.set_index('date', inplace=True)

    combined_df = combined_df[top_list]

    div = df_scatter(combined_df, 'Cryptocurrency Prices (USD)', seperate_y_axis=False, y_axis_label='Coin Value (USD)',
                     scale='log')

    # -------------------------- end correlation -----------------------------------




    # -------------------------- hot and new -----------------------------------

    #get name and price of 5 cryptos
    currs_less = Value.objects.raw('SELECT currency_name,1 as id, quote FROM Value LIMIT 5')

    #get the currencies sorted descending based on news article mentions
    news_curr = Value.objects.raw('SELECT currency_name, 1 as id, count(*) as news_article_mentions FROM currency_news GROUP BY currency_name ORDER BY count(*) DESC')

    #cryptos in march
    feb_curr = Value.objects.raw('select distinct currency_name, 1 as id from Value where month(time) = "02" and year(time) = "2018"')

    # cryptos in april
    april_curr = Value.objects.raw('select distinct currency_name, 1 as id from Value where month(time) = "04" and year(time) = "2018"')

    #new -----------------
    march_curr_list = []
    for curr in feb_curr:
        if curr.currency_name.lower() not in stop_word_list:
            march_curr_list.append(curr.currency_name)
    april_curr_list = []
    for curr in april_curr:
        if curr.currency_name.lower() not in stop_word_list:
            april_curr_list.append(curr.currency_name)

    new_list = list(set(april_curr_list) - set(march_curr_list))
    #------------------------


    #hot -------------------
    news_curr_dict = {}
    for curr in news_curr:
        if curr.currency_name.lower() not in stop_word_list:
            news_curr_dict[curr.currency_name] = curr.news_article_mentions

    sorted_news_curr_dict =  sorted(news_curr_dict.items(), key=operator.itemgetter(1), reverse=True)
    sorted_news_curr_list = [i[0] for i in sorted_news_curr_dict]
    hot_list = sorted_news_curr_list
    #----------------------

    hot_new_list = []
    for i1 in hot_list:
        for i2 in new_list:
            if i1 == i2:
                hot_new_list.append(i1)

    hot_new_list = [str(item) for item in hot_new_list]


    hot_new_query = 'select distinct f.currency_name, f.time, f.quote, 1 as id from (select currency_name, max(time) as latest_time, 1 as id from CryptoNews.Value group by currency_name ) as x inner join CryptoNews.Value as f on f.currency_name = x.currency_name and f.time = x.latest_time where f.currency_name in {}'.format(tuple(hot_new_list[:3]))
    hot_new_query_result = Value.objects.raw(hot_new_query)

    for curr in hot_new_query_result:
        print curr.currency_name, curr.quote, curr.time

    # -------------------------- end hot and new -----------------------------------



    return render(request, 'say_hello.html', {
        'count': '1',  'currs_less': currs_less, 'hot_new_currs': hot_new_query_result,  'topcurr': rate_list, 'mygraph': div

    })

def blog(request,mycurr):

    currency = str(mycurr)

    articles = CurrencyNews.objects.raw('SELECT currency_name, 1 as id, link, title FROM currency_news WHERE currency_name = %s LIMIT 10', [currency])

    # -------------------------- graph -----------------------------------
    crypto_prices_result = Value.objects.raw('select currency_name, quote, time, 1 as id from Value where currency_name = %s', [currency])
    crypto_prices_dict_list = {}
    for row in crypto_prices_result:
        if row.currency_name in crypto_prices_dict_list.keys():
            crypto_prices_dict_list[row.currency_name].append((row.time.strftime("%Y-%m-%d"), row.quote))
        else:
            crypto_prices_dict_list[row.currency_name] = [(row.time.strftime("%Y-%m-%d"), row.quote)]
    #print crypto_prices_dict_list[currency]
    #print zip(*crypto_prices_dict_list[currency])

    dataSource = {}
    dataSource['chart'] = {
                                "caption": "Price Variation",
                                "subCaption": "Past few weeks",
                                "xAxisName": "Time",
                                "yAxisName": "Price",
                                "lineThickness": "3",
                                "paletteColors": "#0075c2",
                                "baseFontColor": "#333333",
                                "baseFont": "Helvetica Neue,Arial",
                                "captionFontSize": "14",
                                "subcaptionFontSize": "14",
                                "subcaptionFontBold": "0",
                                "showBorder": "0",
                                "bgColor": "#ffffff",
                                "showShadow": "0",
                                "canvasBgColor": "#ffffff",
                                "canvasBorderAlpha": "0",
                                "divlineAlpha": "100",
                                "divlineColor": "#31B8C2",
                                "divlineThickness": "1",
                                "divLineIsDashed": "1",
                                "divLineDashLen": "1",
                                "divLineGapLen": "1",
                                "showXAxisLine": "1",
                                "xAxisLineThickness": "1",
                                "xAxisLineColor": "#31B8C2",
                                "showAlternateHGridColor": "0",
                                "slantLabels": "1",
                                "showvalues": "0",
                                "drawAnchors": "0"
                            }

    dataSource['data'] = []

    for tup in crypto_prices_dict_list[currency]:
        data = {}
        data['label'] = tup[0]
        data['value'] = tup[1]
        dataSource['data'].append(data)

    # Create an object for the Column 2D chart using the FusionCharts class constructor
    line2d = FusionCharts("line", "ex1", "1200", "350", "chart-1", "json", dataSource)

    # -------------------------- end graph-----------------------------------

    return render(request, 'blog.html', {
        'currency': currency, 'articles': articles, 'graph' : line2d.render()
    })