# using gcloud build to build the docker image from cli
gcloud builds submit --tag gcr.io/scarlet-labs/otc_ticker_data_collect

# pulling docker image and running
docker pull gcr.io/scarlet-labs/otc_ticker_data_collect:latest
docker run gcr.io/scarlet-labs/otc:latest ./otc-py-runner/src/python/otc_main.py --n 10 --project_id scarlet-labs --bucket scarlet-crypto --ticker_price 0.5

# copy local files to vm
gcloud compute scp --recurse gce otc:~/ --zone=us-central1-a

# creating a pubsub topic
gcloud pubsub topics create otc

# scheduling the pubsub topic to send a message on cron cadence
gcloud scheduler jobs create pubsub otc --schedule="0 */6 * * *" \
  --topic=otc --message-body="otc"


# ssh into vm and run command
gcloud compute ssh otc --zone=us-central1-a	--command="docker run gcr.io/scarlet-labs/otc:latest ./otc-py-runner/src/python/otc_main.py --project_id scarlet-labs --bucket scarlet-crypto --ticker_price 0.5 --n 10"
