gcloud builds submit --tag gcr.io/scarlet-labs/otc_ticker_data_collect

docker pull gcr.io/scarlet-labs/otc_ticker_data_collect:latest
docker run gcr.io/scarlet-labs/otc_ticker_data_collect:latest ./otc-py-runner/src/python/otc_main.py --n 10 --project_id scarlet-labs --bucket scarlet-crypto
