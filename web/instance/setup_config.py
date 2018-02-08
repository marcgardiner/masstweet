#instance/setup_config.py

import os
import sys

import json
import argparse

import urllib.request


def main():
    parser = argparse.ArgumentParser(description="setting up configuration")
    parser.add_argument('-c', '--consul-server', help='The Consul server address', required=True)
    parser.add_argument('-f', '--file', help='The file that holds the configuration. e.g. dev.json', required=True)
    args = vars(parser.parse_args())
    consul_server = args['consul_server']
    config_data_file = args['file']

    if consul_server == '127.0.0.1':
        print("Cannot use loopback interface as consul server")
        sys.exit()

    try:
        with open(os.path.dirname(os.path.abspath(__file__))+'/../env/'+config_data_file) as data_file:
            data = json.load(data_file)
            consul_url = 'http://'+consul_server+':8500/v1/kv/'
            opener = urllib.request.build_opener(urllib.request.HTTPHandler)

            for key, val in data.items():
                os.environ[key] = str(val)
                request = urllib.request.Request(consul_url+key, data=val)
                request.get_method = lambda: 'PUT'
                try:
                    url = opener.open(request)
                except Exception as ex:
                    print("Cannot write '"+key+"' to consul. Please update it manually")

            print("Settings updated successfully")

    except Exception as ex:
        print(str(ex))
        print("Exiting ...")
        sys.exit(1)


if __name__ == "__main__":
    main()
