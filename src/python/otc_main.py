import argparse
import time
from random import randint
from datetime import datetime

from otc_dependencies.ticker_parse import parseTicker
from otc_dependencies.ticker_request import get_otc_tickers, get_ticker_json
from otc_dependencies.client_requests import client_data_column_filter, client_data_columns_cleaned

from gcloud_dependencies.storage_dependencies import upload_blob

from telegram_notifications.send_notification import send_notification

import pandas as pd


def main(argv=None):

    parser = argparse.ArgumentParser()

    parser.add_argument('--n',
                        dest='n',
                        default = None,
                        help='how many tickers do you want to pull? (alphabetical)')

    parser.add_argument('--project_id',
                        dest='project_id',
                        default = None,
                        help='please specify a gcp project id')

    parser.add_argument('--bucket',
                        dest='bucket_name',
                        default = None,
                        help='please specify a bucket you wish to write to')

    parser.add_argument('--ticker_price',
                        dest='ticker_price',
                        default = 5,
                        help='specificy ticker max price filter')



    args, _ = parser.parse_known_args(argv)

    ticker_list, prices = get_otc_tickers(ticker_price=float(args.ticker_price))

    if args.n is None:
        n = len(ticker_list)
    elif int(args.n) > len(ticker_list):
        n = len(ticker_list)
    else:
        n = int(args.n)

    ticker_df = pd.DataFrame()
    failed_list = []
    print(len(ticker_list[0:n]))

    ct = 0
    for ticker, price in zip(ticker_list[0:n], prices[0:n]):
        # print(f"{ticker} - {datetime.now()}")
        if ct%100==0:
            print(f"{ticker} - {datetime.now()}")
        time.sleep(randint(1,5))
        try:
            ticker_json = get_ticker_json(ticker)
            pt = parseTicker(ticker_json)
            df = pt.run()
            df["price"] = price
            ticker_df = pd.concat([ticker_df, df], axis=0)
        except:
            print(f"{ticker} failed")
            failed_list.append(ticker)
            next
        ct+=1

    failed_df = pd.DataFrame(failed_list, columns = ["failed_tickers"])


    import os
    if not os.path.exists('data'):
        os.makedirs('data')

    ticker_df.to_csv("data/ticker_data.csv", index = False)
    failed_df.to_csv("data/failed_tickers.csv", index = False)

    now = datetime.now()

    upload_blob(project_id=args.project_id,
                bucket_name=args.bucket_name,
                source_file_name="data/ticker_data.csv",
                destination_blob_name=f"otc/ticker_data_{now.strftime("%Y%m%d%H")}.csv")

    upload_blob(project_id=args.project_id,
                bucket_name=args.bucket_name,
                source_file_name="data/failed_tickers.csv",
                destination_blob_name="otc/failed_tickers.csv")

    try:
        client_df = ticker_df[client_data_column_filter]
        client_df.columns = client_data_columns_cleaned
        client_df.to_csv("data/client_data.csv", index = False)

        upload_blob(project_id=args.project_id,
                    bucket_name=args.bucket_name,
                    source_file_name="data/client_data.csv",
                    destination_blob_name="otc/client_data.csv")
    except:
        return "client data filter error"

    try:
        os.remove('data/ticker_data.csv')
        os.remove('data/failed_tickers.csv')
        os.remove('data/client_data.csv')
    except OSError:
        pass

    send_notification("otc ticker run completed")


    return "complete"


if __name__ == '__main__':
    main()
