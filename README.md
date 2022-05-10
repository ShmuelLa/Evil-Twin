# 💀Evil twin attack💀
Evil Twin attack python implementation
# Created by: 
### Shmuel Lavian
### Ron Kolsky
### Avigael Abitbol
### Afik Peretz


### Explaination:
For this assignement we created hacking tool based on the "evil-twin attack" concept.<br>
An evil twin is a fraudulent Wi-Fi access point that appears to be legitimate for the user but is set up to eavesdrop on wireless communications.
The evil twin is the wireless LAN equivalent of the phising scam cyberattacks. 
This type of attack is used to steal unsuspecting users passwords, or personal information, either by monitoring their logins or through phishing, which consists of creating a fraudulent website and luring people to it.

### Method
The attacker snoops on Internet traffic using a wireless access point.
The "victims" can be any AP around (Wifi access point). Also the mission was besides attack also create a defence against this attack. This tool is mainly target open public wifi networks. Our victim will think he is fine and have full access to interenet but he doesn't he logged in malicious hotspot. From here, you can do alot of things - for example to add bitcoin miner to each request, find a way to make client download malicious script and get full access to his computer and so on..

#The attack following by few steps:

1. Scanning the area, searching for wifi access
2. Selecting which wifi we want to attack
3. Sending probe requests / deauth packets cousing struggles there
4. Raising up fake AP with the same ESSID
5. Clients will connect to our fake AP
6. Phishing site will be installed
7. Personal information will be stolen
When the client is connected to us, we can sniff information and this is what we doing here, in this example we store gmail phishing site and when client attempt to connect gmail he will actually see the fake page and will enter his details.

 ### Visual explication:
  <img src="image_gif/19112020_evil.jpg" width="600" height="350" >

### Hardware:
💻 Laptop <br>
📡 Network Card - TP_Link Archer T4U - Which allows to use moniter mode<br>
⚡Operation system: Kali linux<br>
 
 
