import argparse
import requests
import csv

import os

from gcp_utils import dump_and_upload


def get_otc_tickers():
    l = "http://otcmarkets.com/research/stock-screener/api/downloadCSV"
    r = requests.get(l)
    decoded_content = r.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    tickers = [x[0] for x in list(cr)]
    return tickers

def main(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('--project',
                        dest='project',
                        default = None,
                        help='This is the GCP project you wish to send the data')
    parser.add_argument('--bucket',
                        dest='bucket',
                        default = None,
                        help='This is the sport type (for now)')
    parser.add_argument('--creds',
                        dest='creds',
                        default = None,
                        help='This is the sport type (for now)')

    args, _ = parser.parse_known_args(argv)

    tickers = get_otc_tickers()

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{args.creds}.json"
    dump_and_upload(obj=tickers,
                    filename="tickers",
                    project_id=args.project,
                    bucket_name=args.bucket,
                    destination_file_name="otc/otc_tickers.pkl")

if __name__ == '__main__':
    main()
