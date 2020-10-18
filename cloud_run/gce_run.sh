#!/bin/bash

gcloud compute ssh otc --zone=us-central-a --command="docker run gcr.io/scarlet-labs/otc:latest ./otc-py-runner/src/python/otc_main.py --project_id scarlet-labs --bucket scarlet-crypto --ticker_price 0.5"
