from django.shortcuts import render
from Crypto.models import Value
from Crypto.models import CurrencyNews
from django.db import connection
from django.utils import timezone
from datetime import timedelta
from scipy.stats.stats import pearsonr
import math
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go



def say_hello(request):


    current_date = timezone.now()
    current_backdate = current_date - timedelta(days=5)

    topcurr = Value.objects.raw(
        'SELECT 1 as id, currency_name, min(quote) as min_quote, max(quote) as max_quote FROM Value WHERE time>%s and time<%s group by currency_name',[current_backdate, current_date]
    )

    rate_list = []
    for line in topcurr:
        rate_value = (line.max_quote-line.min_quote)/line.max_quote
        rate_list.append([line.currency_name,rate_value])
    rate_list.sort(key=lambda x:x[1])
    rate_list = rate_list[:-11:-1]

    new_rate_list = [i[0] for i in rate_list]
    latest_prices = Value.objects.raw('select distinct f.currency_name, f.time, 1 as id, f.quote from (select currency_name, max(time) as latest_time from CryptoNews.Value group by currency_name) as x inner join CryptoNews.Value as f on f.currency_name = x.currency_name and f.time = x.latest_time where f.currency_name in {}'.format(tuple(new_rate_list)))

    for line in latest_prices:
        for i in range(len(rate_list)):
            if(line.currency_name==rate_list[i][0]):
                rate_list[i][1]=line.quote

    newcurr = CurrencyNews.objects.raw(
        'SELECT currency_name, 1 as id, count(*d) as ct FROM currency_news GROUP BY currency_name ORDER BY count(*) LIMIT 5')


    #********************** Correlation Start********************************************

    crypto_list_query = Value.objects.raw('SELECT distinct currency_name, 1 as id FROM Value')
    crypto_list_all = [item.currency_name for item in crypto_list_query]

    currency_pdict = {}
    currency_price_all = Value.objects.raw('SELECT currency_name, quote, 1 as id FROM Value WHERE year(time)>2016 ORDER BY time')

    for record in currency_price_all:
        if record.currency_name in currency_pdict.keys():
            currency_pdict[record.currency_name].append(record.quote)
        else:
            currency_pdict[record.currency_name] = [record.quote]

    bitcoin_baseline = currency_pdict['Bitcoin']

    correlation_list = []

    for crypto_curr in crypto_list_all:
        if crypto_curr in currency_pdict.keys():
            if(len(bitcoin_baseline)<= len(currency_pdict[crypto_curr])):
                correlation_coeff = pearsonr(bitcoin_baseline,currency_pdict[crypto_curr][:len(bitcoin_baseline)])

            if((not math.isnan(float(correlation_coeff[0])))&(float(correlation_coeff[0])>0.14189)):
                correlation_list.append([crypto_curr, float(correlation_coeff[0])])
    correlation_list = sorted(correlation_list, key=lambda x: x[1], reverse=True)


    top_5 = correlation_list[7:12]
    bot_5 = correlation_list[-6:-1]
    top_list = ['Bitcoin']
    for i in top_5:
        top_list.append(i[0])
    for i in bot_5:
        top_list.append(i[0])

    top_prices = Value.objects.raw(
        'select currency_name, quote, time, 1 as id from Value where year(time)>2016 AND currency_name in {}'.format(tuple(top_list)))
    crypto_top_dict = {}
    crypto_top_dict['date']=[]

    for row in top_prices:
        if row.currency_name in crypto_top_dict.keys():
            crypto_top_dict[row.currency_name].append(row.quote)
        else:
            crypto_top_dict[row.currency_name] = [row.quote]
        if (row.currency_name=='Bitcoin'):
            crypto_top_dict['date'].append(row.time)

    combined_df = pd.DataFrame.from_dict(crypto_top_dict)
    combined_df.set_index('date', inplace=True)
    combined_df = combined_df[top_list]





    div = df_scatter(combined_df, 'Cryptocurrency Prices (USD)', seperate_y_axis=False, y_axis_label='Coin Value (USD)', scale='log')


    # ********************** Correlation End********************************************

    return render(request, 'say_hello.html', {
        'count': '1', 'newcurr': newcurr, 'topcurr': rate_list, 'btcgraph': div
    })


def df_scatter(df, title, seperate_y_axis=False, y_axis_label='', scale='linear', initial_hide=False):
    label_arr = list(df)
    series_arr = list(map(lambda col: df[col], label_arr))

    layout = go.Layout(
        title=title,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
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


def blog(request,mycurr):

    currency = mycurr

    articles = CurrencyNews.objects.raw('SELECT currency_name, 1 as id, link, title FROM currency_news WHERE currency_name = %s LIMIT 10', [currency])

    return render(request, 'blog.html', {
        'currency': currency, 'articles': articles

    })