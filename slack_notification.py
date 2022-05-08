#!/usr/bin/env python3

import argparse
import json
import os
import sys
import urllib.request


def main(CI_COMMIT_TAG, slack_webhook_url):
   
#    print("Notifying the release")

    webhook_json = {
            
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": f"Current release : {CI_COMMIT_TAG}"
                    }
                }
            ]
    }
    json_data = json.dumps(webhook_json).encode("utf-8")
    slack_req = urllib.request.Request(slack_webhook_url)
    slack_req.add_header("Content-Type", "application/json")
    urllib.request.urlopen(slack_req, json_data)
    


  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('CI_COMMIT_TAG')
    parser.add_argument('--slack-url', default=os.environ.get('SLACK_WEBHOOK_URL'), help="Can also be set as env var SLACK_WEBHOOK_URL.")

    args = parser.parse_args()
    main(args.CI_COMMIT_TAG, args.slack_url)
