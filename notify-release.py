#!/usr/bin/env python3

import argparse
import json
import os
import sys
import urllib.request

def main(slack_webhook_url: str):
    print("Notifying the release")
    webhook_json = {
            "text": "Notice: A new version has been released",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": ":triangular_flag_on_post: A new version has been released :triangular_flag_on_post:"
                    }
                }
            ]
    }
    json_data = json.dumps(webhook_json).encode("utf-8")
    slack_req = urllib.request.Request(slack_webhook_url)
    slack_req.add_header("Content-Type", "application/json")
    urllib.request.urlopen(slack_req, json_data)

if __name__ == "__main__":
    slack_url = "https://hooks.slack.com/services/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"
    main(slack_url)
