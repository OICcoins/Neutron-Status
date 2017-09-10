How to get a Neutron Masternode running on a $5 VPS and keep your coins on your desktop wallet.

###Word of Warning:###

Always test you can use a linux wallet before committing all your 25000 coins to it, if you have 
never used a CLI/Non GUI wallet it is YOUR responsibility to learn what you need to know.

###Assumptions:###  

Ubuntu 16.04 installed on your VPS and can SSH into it and you are accessing via SSH with a 
username and password.

###VPS Security is your responsibility:###

if you do not setup access to your VPS using ssh keys and a firewall then i suggest that you make 
sure you have at least enabled the firewall on your VPS and only allow the required TCP ports 
incoming for the Neutron Masternode and SSH, you should also define only a single IP as the 
source address for TCP Port 22/SSH access be it your work or home IP. When you are not accessing 
the server for maintenance you should block port 22/SSH in your firewall at the VPS console so 
it is only open for the time required. Also enable 2FA at your VPS if available.

##VPS Setup##

If you need a VPS provider thats only ~$5/month then signup at Digital Ocean and get $10 free 
credit here when you join (approx 2 months free with a basic VPS).

Create a new droplet, ideally you will use the $10 option as it will allow for longer lifespan 
but the $5 should be sufficient for some time. https://m.do.co/c/9382837482e2
Take a note of your VPS IP address for later.


##Lets roll.....##

Install the wallet on your Windows, Mac, Linux Desktop. This will be the wallet you use to store 
your coins.
Download the precompiled binary from https://www.neutroncoin.com
Run and wait for the wallet to sync before transferring your coins here from the exchange.

##Create your Masternode Config and Collateral Address##

Note: A Collateral Address is just the public key or NTRN address where you will send your coins.

Now your wallet is ready to go we are going to create a masternode
You can also outsouce management of your masternode hosting here http://nodeshare.in/coins/neutron
They have a great guide showing some of the steps here keep in mind we do it a bit different. 
http://nodeshare.in/coins/neutron/installguide/

1. Open your wallet and Click on the "Nucleus" tab
1. Then "My Nucleus Nodes"
1. Click "Create"
1. Give the node a name like "Masternode01"
1. Insert in the Address your IP address of your VPS followed by :32001 eg. "1.2.3.4:32001"
1. You now have your Collateral Address, copy that and store it for later
1. Click "Get Config" and copy the contents to a text file on your pc.


Backup your wallet now so it contains the keys for your new masternode address!!!

##Configure the VPS##

Here we will get the wallet running on the VPS and setup the config ready for masternoding!

##Setup Swap Space##

This is needed to compile neutrond if you skip this it will fail if you have low RAM on the VPS.

```
lssudo dd if=/dev/zero of=/var/swap.img bs=1024k count=1000
sudo mkswap /var/swap.img
sudo swapon /var/swap.img
```

##Install Dependencies##

```
sudo apt-get update && sudo apt-get install automake libdb++-dev build-essential libtool autotools-dev autoconf pkg-config libssl-dev libboost-all-dev libminiupnpc-dev git software-properties-common python-software-properties g++ qt5-default
```


##Download source from the git repo and compile##
You may need to manually update the branch if a new release becomes available

##Compile##

```
cd ~/
git clone --branch v1.1.2 https://github.com/neutroncoin/neutron.git
cd ./neutron
cd ./src
sudo make -f makefile.unix
cp ./neutrond ~/
mkdir ~/.neutron
touch ~/.neutron/neutron.conf
cd ~/
```


##Run neutrond and create the config##

Run neutrond and let it generate an RPC user and password for you to use below in the 
neutron.conf
```
./neutrond
```

setup the neutron.conf
```
nano ~/.neutron/neutron.conf
```

copy in the following lines to the neutron.conf file that you got above when you made the 
masternode on your PC wallet and add in staking=0.

```
daemon=1
rpcallowip=127.0.0.1
rpcuser=Neutronrpc
rpcpassword=[RANDOM Password from the above step]
server=1
listen=1
port=32001
masternode=1
masternodeaddr=[You masternode IP]:32001
masternodeprivkey=[Your one generated earlier]
staking=0
```

run neutrond again and wait for blockchain to sync
```
./neutrond
```

you can basically check on the status of the sync by checking the size of blk0001.dat it is 
approx 630MB at the time of writing this. So check the filesize with the below command until 
you are convinced that the file size hasn't changed for a few minutes and this will indicate 
when you have caught up to the blockchain. Allow a few minutes between checks of the file as 
sometimes sync can stop for a while.

```
ls -la ~/.neutron/neutron.conf
```

You can always hurry along the process by downloading a recent blockchain from the following 
source, this will save you at least a day. All we do is download a file unzip it into the ~/.neutron/ 
folder overwriting the files in there then we start neutrond to catchup on the last bit of the 
blockchain it's missing.
```
./neutrond stop
cd ~/.neutron
wget http://108.61.216.160/cryptochainer.chains/chains/Neutron_blockchain.zip
mv Neutron_blockchain.zip ./.neutron/
sudo apt-get install unzip
unzip Neutron_blockchain.zip
rm Neutron_blockchain.zip
cd ~\
./neutrond
```

Did the blockchain sync fully? Lets move on.


##Send your 25000 coins to the collateral address##

This MUST be in one transaction, if you store your funds on a desktop wallet it 
should add the fee on top of the amount you send, from an exchange you may need 
to test with a small amount like 1 NTRN to another address just to confirm how 
their fees work but more than likely from an exchange you need to add 0.01 to the 
total amount you want to send. Sending from a desktop wallet will require only 
25000 NTRN and it will give a warning about the transaction being oversize and 
need a fee to be paid, this fee will be added so you do not need to compensate 
for that.

Using your collateral Address obtained earlier send 25000 coins there.

After you send your coins you need to wait for 13 confirmations before continuing
(or when a green tick is next to the transaction in your PC wallet):


##Startup the Masternode##

Stop the daemon
```
./neutrond stop
```

Restart the daemon
```
./neutrond
```

Check your node is running by running this and see if it's in the list:
```
./neutrond masternode list
```

if you want to search easier then search this way:
```
./neutrond masternode list | grep [YOUR IP]
```

eg `./neutrond masternode list | grep 1.2.3.4`

On the PC Wallet make sure you unlock your wallet and select for staking only, you can now go 
to the Nucleus tab and select your masternode and click start.
You should see "Adrenaline node at [YOUR IP] started."

And you are done. 

You can keep an eye on your masternode at http://www.presstab.pw/phpexplorer/NTRN/address.php
NTRN Donations Welcome: 9rHiPWcdyAkF2WvNfzrCdovgdgsn5fjS6v
