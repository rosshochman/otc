import argparse
import time
from random import randint
from datetime import datetime

from otc_dependencies.ticker_parse import parseTicker
from otc_dependencies.ticker_request import get_otc_tickers, get_ticker_json

from gcloud_dependencies.storage_dependencies import upload_blob

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

    ticker_list = get_otc_tickers(ticker_price=float(args.ticker_price))

    if args.n is None:
        n = len(ticker_list)
    elif int(args.n) > len(ticker_list):
        n = len(ticker_list)
    else:
        n = int(args.n)

    ticker_df = pd.DataFrame()
    failed_list = []
    print(len(ticker_list[0:n]))
    for ticker in ticker_list[0:n]:
        print(f"{ticker} - {datetime.now()}")
        time.sleep(randint(1,5))
        try:
            ticker_json = get_ticker_json(ticker)
            pt = parseTicker(ticker_json)
            df = pt.run()
            ticker_df = pd.concat([ticker_df, df], axis=0)
        except:
            print(f"{ticker} failed")
            failed_list.append(ticker)
            next

    failed_df = pd.DataFrame(failed_list, columns = ["failed_tickers"])


    import os
    if not os.path.exists('data'):
        os.makedirs('data')

    ticker_df.to_csv("data/ticker_data.csv", index = False)
    failed_df.to_csv("data/failed_tickers.csv", index = False)

    upload_blob(project_id=args.project_id,
                bucket_name=args.bucket_name,
                source_file_name="data/ticker_data.csv",
                destination_blob_name="otc/ticker_data.csv")

    upload_blob(project_id=args.project_id,
                bucket_name=args.bucket_name,
                source_file_name="data/failed_tickers.csv",
                destination_blob_name="otc/failed_tickers.csv")


    return "complete"


if __name__ == '__main__':
    main()