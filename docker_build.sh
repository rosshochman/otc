gcloud builds submit --tag gcr.io/scarlet-labs/otc_ticker_data_collect

docker pull gcr.io/scarlet-labs/otc_ticker_data_collect:latest
docker run gcr.io/scarlet-labs/otc:latest ./otc-py-runner/src/python/otc_main.py --n 10 --project_id scarlet-labs --bucket scarlet-crypto --ticker_price 0.5




gcloud compute scp --recurse gce otc:~/ --zone=us-central1-a

gcloud pubsub topics create otc

gcloud scheduler jobs create pubsub otc --schedule="0 */6 * * *" \
  --topic=otc --message-body="otc"
