#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import time
import os
import subprocess
import sys
from urllib.parse import urljoin
from dotenv import load_dotenv
import json

import logging
import http.client as http_client
http_client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

def email():
    # This function is not used in this version of the script
    # Load environment variables from ~/.env
    load_dotenv(verbose=True)
    dotenv_path = os.path.expanduser('~/.env')
    load_dotenv(dotenv_path)
    # WIFI_EMAIL = os.environ.get("WIFI_EMAIL")

def check_captive_portal_status():
    """
    Exits if an active captive portal is detected, based on system command.
    """
    command = ["defaults", "read", "/Library/Preferences/SystemConfiguration/com.apple.captive.control", "Active"]
    # A return code of 0 indicates that the 'Active' key exists, meaning a captive portal is detected.
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 1:
        print("\n[ERROR] Active captive portal detected. You need to run the following command and REBOOT Mac.")
        print("  sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.captive.control Active -boolean false")
        sys.exit(1)

def handle_wi2(session, response, current_url):
    """
    Handles the Wi2 free Wi-Fi specific login steps by finding and submitting
    the necessary forms. This function combines the original steps 3 and 4.
    """
    # --- Step 3 logic: 'Next Page' button ---
    soup = BeautifulSoup(response.text, 'html.parser')
    form = soup.find('form')
    # print(form)
    if form:
        # Starbucks needs to accept the agreement
        next_button = soup.find(id='button_next_page')
        if next_button:
            next_url = urljoin(current_url, form['action'])
            print(f"      -> Found a link. Following to {next_url}")
            response = session.get(next_url, timeout=10)
            response.raise_for_status()
            current_url = response.url
        else:
            print("Could not find a form or link for 'button_next_page'. Move to next step")
            pass

    print(f"      -> Now at: {current_url}")

    # --- Step 4 logic: 'Accept' button ---
    soup = BeautifulSoup(response.text, 'html.parser')
    form = soup.find('form')
    print(form)
    if form:
        accept_button = soup.find(id='button_accept')
        if accept_button:
            accept_url = 'https://service.wi2.ne.jp/wi2auth/xhr/login'
            print(f"      -> Found 'accept' action. Posting to {accept_url}")
            data = {"login_method": "onetap", "login_params": {"agree": "1"}}
            json_data = json.dumps(data)
            print(f"      -> with data: {data}")
            headers = {'Content-Type': 'application/json'}
            response = session.post(accept_url, data=json_data, headers=headers, timeout=10)
        else:
            raise RuntimeError("Could not find 'button_accept' on the second page.")

    return response, current_url

def main():
    """
    Runs the main captive portal login procedure.
    """

    print("--- Captive Portal Login using Requests ---")
    check_captive_portal_status()

    # Use a session to persist cookies across requests
    session = requests.Session()

    portal_url = 'http://captive.apple.com/'
    current_url = portal_url
    response = None

    try:
        # 1. Access the trigger URL to get redirected to the captive portal
        print(f"[1/3] Accessing '{portal_url}' to find portal...")
        response = session.get(portal_url, timeout=10)
        response.raise_for_status()
        current_url = response.url
        if current_url != portal_url:
            print(f"      -> Redirected to: {current_url}")
        else:
            print(f"      -> No redirect. Current URL: {current_url}")

        # 2. Check for immediate success
        if 'Success' in response.text:
            print("\n[SUCCESS] Login status is already 'Success'. No action needed.")
            exit(0)

        # 3. Handle Wi-Fi specific login flow
        print("[2/3] Analyzing page and handling Wi-Fi login flow...")
        response, current_url = handle_wi2(session, response, current_url)
        # response, current_url = handle_starbucks(session, response, current_url)

        print("[3/3] Checking final status...")
        print(response)
        if response.ok:
            # A simple 'Success' check might be too naive. Some portals redirect
            # to the original site, or show a success page. We check both.
            if 'Success' in response.text:
                print("\n[SUCCESS] Login successful. 'Success' message found.")
            else:
                print("\n[COMPLETED] Final step submitted. Please verify connectivity.")
        else:
            print(f"\n[FAILURE] Final step failed with status: {response.status_code}")
            exit(1)

    except (requests.exceptions.RequestException, RuntimeError) as e:
        print(f"\n[ERROR] An error occurred: {e}")
        if response:
            print("      -> Last known URL:", current_url)
            print("      -> Response status:", response.status_code)
        exit(1)

if __name__ == "__main__":
    main()
