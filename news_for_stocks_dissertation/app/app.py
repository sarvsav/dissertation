#  Copyright (c) 2023.
#  BITS Pilani, Dissertation
#  Student Name: Sarvsav Sharma
#  Student Id: 2020sc04239
import pickle
import sklearn
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

def predict_purchase(predicted_close_price, amount, loss_margin, platform_fees, stock_stats_today):
    #print(f"Current price: {round(predicted_close_price[0],2)}")
    quantity_to_buy = int(amount / stock_stats_today['max_buy_price'])
    quantity_to_sell = int(amount / stock_stats_today['max_sell_price'])
    print(f"Max buy price: {stock_stats_today['max_buy_price']}, Max sell price: {stock_stats_today['max_sell_price']}")
    #print(f"Buy quantity: {quantity_to_buy}, Sell quantity: {quantity_to_sell}")
    sum_buy_price = quantity_to_buy * stock_stats_today['max_buy_price']
    sum_sell_price = quantity_to_sell * stock_stats_today['max_sell_price']

    sum_closed_buy_price = quantity_to_buy * predicted_close_price[0]
    sum_closed_sell_price = quantity_to_sell * predicted_close_price[0]

    profit_in_buying = sum_buy_price - sum_closed_buy_price
    profit_in_selling = sum_closed_sell_price - sum_sell_price

    if profit_in_buying > profit_in_selling:
        if profit_in_buying > loss_margin + platform_fees:
            return f"Buy the shares for amount: {round(sum_closed_buy_price,2)} of quantity: {quantity_to_buy}, to profit: {round(profit_in_buying - platform_fees, 2)}"
        else:
            return "Do not buy or sell because of volatility in market"
    else:
        if profit_in_selling > loss_margin + platform_fees:
            return f"Sell the shares for amount: {round(sum_closed_sell_price,2)} of quantity: {quantity_to_sell}, to profit: {round(profit_in_selling - platform_fees, 2)}"
        else:
            return "Do not buy or sell because of volatility in market"

def read_news():
    with open('out/data.csv', encoding="utf8") as fh:
        news_data = fh.readline()

    date_info = news_data.split(",")[0]
    joined_news = " ".join(news_data.split(",")[1:])
    clean_news = re.sub('\W+', ' ', joined_news)
    return (date_info, clean_news)

def calculate_sentiment_data(news_data):
    sentiment_id = SentimentIntensityAnalyzer()
    sentiment_result = sentiment_id.polarity_scores(news_data[1])
    return sentiment_result


def run(stock_stats_today):
    stock_name = input('Enter stock name: ')
    amount = float(input('Enter money to invest in Rupees: '))
    loss_margin = float(input('Enter how much loss can be acceptable in rupees?: '))
    risk_level = float(input('Enter risk level (1 would be minimum and 5 would be maximum): '))
    platform_fees = float(input('Enter the platform fees?: '))
    print(f"Open: {stock_stats_today['open']}, Previous Close: {stock_stats_today['prev close']}")
    ## Fetch the last evening news to calculate sentiment score
    news_data = read_news()
    print('News data: ', news_data[0], news_data[1][0:100])

    ## Convert the news headlines into sentiment score using vader
    sentiment_data_numerical = calculate_sentiment_data(news_data)
    print(f"Positive news: {sentiment_data_numerical['pos']}, and negative news: {sentiment_data_numerical['neg']}")
    ## load the model
    stock_prediction_model = pickle.load(open('./models/svr_poly.pkl', 'rb'))
    print(stock_prediction_model)
    data = [
        {
            'prev close': stock_stats_today['prev close'],
            'open': stock_stats_today['open'],
            'high': stock_stats_today['high'],
            'low': stock_stats_today['low'],
            'last': stock_stats_today['last'],
            'compound': sentiment_data_numerical['compound'],
            'negative': sentiment_data_numerical['neg'],
            'neutral': sentiment_data_numerical['neu'],
            'positive': sentiment_data_numerical['pos'],
        }
    ]
    input_data = pd.DataFrame(data, index=['2023-03-22'])
    if sentiment_data_numerical['pos'] > sentiment_data_numerical['neg']:
        print("Based on news polarity, its good to buy stocks today")
    else:
        print("Based on news polarity, its good to sell stocks today")

    ## Predict the close value for the model by feeding all the inputs
    #predicted_close_price = stock_prediction_model.predict(sentiment_data_numerical, input_data)
    predicted_close_price = stock_prediction_model.predict(input_data)
    print(f"Predicted close price: {predicted_close_price}")

    ## Check for buy or sell
    print(predict_purchase(predicted_close_price, amount, loss_margin, platform_fees, stock_stats_today))

