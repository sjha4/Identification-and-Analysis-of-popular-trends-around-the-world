import subprocess

ipAddressList = ('167.33.22.10','google.com', 'twitter.com')
ipUp = dict()
for i in ipAddressList:
    ipUp[i] = False
primaryIP = '167.33.22.10'

ipUp[primaryIP] = True

def pingChecker(ipAddress):
    res = subprocess.call(['ping', '-c', '3', ipAddress])
    if res == 0:
        print True
    elif res == 2:
        print False
    else:
        print False

index = 1
while True:
    if not pingChecker(primaryIP):
        newIPAdd = ipAddressList - set(primaryIP)
        if not pingChecker(newIPAdd[1]):
            