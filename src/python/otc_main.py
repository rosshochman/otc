import argparse
import time
from random import randint

from otc_dependencies.ticker_parse import parseTicker
from otc_dependencies.ticker_request import get_otc_tickers, get_ticker_json

import pandas as pd


def main(argv=None):

    parser = argparse.ArgumentParser()

    parser.add_argument('--n',
                        dest='n',
                        default = None,
                        help='how many tickers do you want to pull? (alphabetical)')

    args, _ = parser.parse_known_args(argv)

    ticker_list = get_otc_tickers()

    if args.n is None:
        n = len(ticker_list)
    elif int(args.n) > len(ticker_list):
        n = len(ticker_list)
    else:
        n = int(args.n)

    ticker_df = pd.DataFrame()
    failed_list = []
    for ticker in ticker_list[0:n]:
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
    return ticker_df, failed_df


if __name__ == '__main__':
    tdf = main()
    tdf[0].to_csv("data/ticker_data.csv", index = False)
    tdf[1].to_csv("data/failed_tickers.csv", index = False)
