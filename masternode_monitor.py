###################################
# Neutron Masternode Monitor Tool #
# 14 SEP 2017 @djmeekee           #
###################################
#
# JSON Parser for neutrond RPC Server results with slack webhooks integration.
# Monitor your masternode from slack!
# Sign up for your own private slack team for free then you can setup webhooks integration.
# Details on setting up slack webhooks are here: https://api.slack.com/incoming-webhooks
# NTRN goes here :)  9rHiPWcdyAkF2WvNfzrCdovgdgsn5fjS6v
#
################
# Installation #
################
#
# [SSH into your VPS]
# cd ~/
# nano masternode_monitor.py
# Replace the rpcuser and rpcpassword with your ones
# Replace the slack webhooks URL with your one.
# [paste the contents of this script in and ctrl+x to save]
# [Install pip and the requests library]
# sudo apt-get install python-pip
# pip install requests
# [Now setup a cron schedule]
# crontab -e
# select 2 for nano
# [Add the next line to the bottom of the file and ctrl+x to save]
# */30 * * * * /usr/bin/python /root/masternode_monitor.py
#
#################################################

import json
import requests

# You will need to update rpcuser and rpc password to your ones you can find in ~/.neutron/neutron.conf

daemon_url = 'http://rpcuser:rpcpassword@127.0.0.1:32000'
mydata = ""

# This posts to slack

def post_to_slack(mn_status, mn_ip):
    webhook_url = 'https://hooks.slack.com/services/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    slack_data = {'text': "Your Masternode at "+str(mn_ip)+" is "+str(mn_status)}

    response = requests.post(
    webhook_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
    )

# This connects and sends your requests to the RPC service
# You can send one or 2 parameters to the function, If you only need to send 1
# the 2nd parameter is set by default as empty.
# This is easily extended to have 3,4,5+ parameters depending on the request you need to send

def connect_daemon(my_method,my_params=""):
    if len(my_params) < 1:
        daemon_data = {"jsonrpc":"1.0","id":"curltext","method":str(my_method),"params":[]}
    else:
        daemon_data = {"jsonrpc":"1.0","id":"curltext","method":str(my_method),"params":[str(my_params)]}

    response = requests.post(
        daemon_url, data=json.dumps(daemon_data),
        headers={'Content-Type': 'text/plain'}
        )
    mydata = response.json()
    return(mydata)

# This parses getinfo data and prints to the screen

def funct_getinfo(json_data):

    if json_data['result']['connections'] == 0:
        print "   Node has "+ str(json_data['result']['connections'])+ " to the network"
    else:
        print "   Node IP is: " + json_data['result']['ip']
        mn_ip = str(json_data['result']['ip'])
        print "   Node has "+ str(json_data['result']['connections'])+ " connections to the network"
        print "   You are at block: " + str(json_data['result']['blocks'])

    print "   Wallet Version: "+ str(mydata['result']['version'])
    return(mn_ip)

# This checks your Masternode IP against connected node list and posts result to slack

def funct_list_mn(mn_ip):
    mn_data = connect_daemon("masternode","list")
    #needs full field with port
    if mn_ip in mn_data['result']:
        print "   Yay Masternode is still running!\n"
        post_to_slack("Online", mn_ip) #Masternode offline? Seld Slack Alert
    else:
        print "   Boo Masternode is not running!\n"
        post_to_slack("Offline", mn_ip) #Masternode offline? Seld Slack Alert


print "\n\n[+]---------------Node Stats---------------[+]\n"

mydata = connect_daemon("getinfo")
mn_ip = funct_getinfo(mydata)
mn_ip = mn_ip+":32001"
funct_list_mn(mn_ip)

print "[+]----------------------------------------[+]\n\n\n"
