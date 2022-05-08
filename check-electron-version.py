#!/usr/bin/env python3

import argparse
import json
import os
import sys
import urllib.request

def main(js_dir: str, slack_webhook_url: str, github_token: str):
    print("getting current Electron version in use")

    with open(f"{js_dir}/package.json", "r") as package_json:
        package_json = json.load(package_json)
        
        electron_specifier = package_json["devDependencies"]["electron"]

    if electron_specifier == None:
        print("no Electron version found in package, aborting!")
        sys.exit(1)

    electron_version = str(electron_specifier).replace("^", "")

    print(f"detected version {electron_version} of Electron")

    releases_url = "https://api.github.com/repos/electron/electron/releases"

    req = urllib.request.Request(releases_url)

    req.add_header("Authorization", github_token)

    with urllib.request.urlopen(req) as response:
        if response.status != 200:
            print("failed to get Electron releases: :", response)

        releases_json = json.load(response)

    (current_major, current_minor, current_patch) = (int(part) for part in electron_version.split("."))

    # Get the latest release
    latest_release = None
    for release in releases_json:
        tag = str(release["tag_name"]).replace("v", "")

        # We want to ignore non-stable versions
        if "nightly" in tag or "beta" in tag or "alpha" in tag:
            continue

        (release_major, release_minor, release_patch) = (int(part) for part in tag.split("."))

        # Check if a new major version has come out
        if release_major > current_major:
            latest_release = release
            break

        if release_minor > current_minor and release_major == current_major:
            latest_release = release
            break

        if release_patch > current_patch and release_major == current_major and release_minor == current_minor:
            latest_release = release
            break


    if latest_release != None:
        new_release = latest_release
        version = new_release["tag_name"]
        release_notes = new_release["html_url"]

        print(f"newer release found: {version}")

        webhook_json = {
            "text": "Notice: A newer version of Electron was found",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": ":triangular_flag_on_post: A newer Electron version was released :triangular_flag_on_post:"
                    }
                },

                {
                    "type": "divider"
                },

                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Current version used: `v{electron_version}`"
                    }
                },

                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"New release's version: `{version}`. Here are the <{release_notes}|release notes>."
                    }
                }
            ]
        }

        # Electron patch and minor versions are usually pretty easy updates given 
        # the amount of functionality we use from its API.
        if release_major == current_major:
            webhook_json["blocks"].append({
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "This looks like a small update. If it is, please open an MR to update OPH :ty:"
                }
            })

        json_data = json.dumps(webhook_json).encode("utf-8")
        slack_req = urllib.request.Request(slack_webhook_url)
        slack_req.add_header("Content-Type", "application/json")
        urllib.request.urlopen(slack_req, json_data)
    else:
        print("Electron is up to date")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('js_dir')
    parser.add_argument('--github-token', default=os.environ.get('COREBOT_GITHUB_TOKEN'), help="Can also be set as env var COREBOT_GITHUB_TOKEN.")
    parser.add_argument('--slack-url', default=os.environ.get('SLACK_WEBHOOK_URL'), help="Can also be set as env var SLACK_WEBHOOK_URL.")

    args = parser.parse_args()
    main(args.js_dir, args.slack_url, args.github_token)
