#!/usr/bin/env python3

import argparse
import json
from operator import contains
import os
import sys
import urllib.request
from re import search


def main(ci_commit_tag, slack_webhook_url_automation_tag, slack_webhook_url_release_tag, ci_pipeline_tag):
   
#    print("Notifying the release")
    

    if search("release",ci_commit_tag):
        
            print("release string found")
            slack_webhook_url = slack_webhook_url_release_tag

        
    elif search("automation",ci_commit_tag):
        
            print("automation string found")
            slack_webhook_url = slack_webhook_url_automation_tag
 
    webhook_json = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": ":robot_face: A new release was triggered, Below are the details"
                    }
            },

            {
                "type": "divider"
            },

            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Current Release Is : *`{ci_commit_tag}`*"
                }
            },

            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Pipeline URL Is : <{ci_pipeline_tag}>"
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
    parser.add_argument('--slack-url-release-tag', default=os.environ.get('SLACK_WEBHOOK_URL_CI_AUTOMATION_TEST_TAG'), help="Can also be set as env var SLACK_WEBHOOK_URL_CI_AUTOMATION_TEST_TAG.")
    parser.add_argument('--slack-url-automation-tag', default=os.environ.get('SLACK_WEBHOOK_URL_RELEASE_TAG'), help="Can also be set as env var SLACK_WEBHOOK_URL_RELEASE_TAG.")
    parser.add_argument('--CI_COMMIT_TAG', default=os.environ.get('CI_COMMIT_TAG'), help="Can also be set as env var SLACK_WEBHOOK_URL.")
    parser.add_argument('--CI_PIPELINE_TAG', default=os.environ.get('CI_PIPELINE_TAG'), help="Can also be set as env var SLACK_WEBHOOK_URL.")

    args = parser.parse_args()
    main(args.CI_COMMIT_TAG, args.slack_url_release_tag, args.slack_url_automation_tag, args.CI_PIPELINE_TAG)


