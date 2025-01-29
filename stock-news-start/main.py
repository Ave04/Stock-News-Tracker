import requests
import smtplib
import datetime as dt
from dotenv import load_dotenv
import os

load_dotenv(
    r'Enter-Full-Path-Here')
now = dt.datetime.now()
today = now.date() - dt.timedelta(days=2)
yesterday = today - dt.timedelta(days=1)

today = str(today)
yesterday = str(yesterday)

NEWSNEEDED = 3
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
my_email = os.getenv('Email')
my_password = os.getenv('Password')

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stockapi_key = os.getenv('Stock_api_key')
stockparams = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': 'IBM',
    'apikey': stockapi_key
}
stockresponse = requests.get(url='https://www.alphavantage.co/query', params=stockparams)
stockresponse.raise_for_status()
stockdata = stockresponse.json()
dailytimeseriesdata = stockdata['Time Series (Daily)']

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
newsapi_key = os.getenv('News_api_key')
news_url = os.getenv('News_URL')
newsresponse = requests.get(url=news_url)
newsresponse.raise_for_status()
newsdata = newsresponse.json()
articles = newsdata['articles']
percentdiff = float(dailytimeseriesdata[today]['2. high']) - float(dailytimeseriesdata[today]['3. low'])
msg = []
title = ['0']
if percentdiff < 5:
    msg.append(f"The percentage difference is {percentdiff}")
    for i in range(NEWSNEEDED):
        msg.append(articles[i]['description'])
        title.append(articles[i]['title'])

# title[2] = "yes"
# msg[2] = "turkey"
#
# print(title)
## STEP 3: Send to email or messaging app
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

for i in range(1, len(msg)):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        email_msg = f'Subject:{title[i]}\n\nThe percentage difference was {msg[0]}.\n{msg[i]}'
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=email_msg.encode("utf-8"))

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
