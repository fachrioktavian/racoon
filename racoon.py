import re, sys, requests, threading, argparse
import concurrent.futures
from agent import Agent

requests.packages.urllib3.disable_warnings()

def getInfo(inp, a):
    fr = open(inp, 'r')
    it = 0
    nowdata = False
    for line in fr:
        if (it == 0):
            a.setMethod(line)
            a.setUrl(line)
            a.setParam(line)
        elif (line != '\n' and (not nowdata)):
            a.setHeaders(line)
        elif (line == '\n'):
            nowdata = True
        elif (nowdata):
            a.setData(line)
        it+=1

def sendPost(i, u, x, y, z):
    r = requests.post(u, headers=x, params=y, data=z, verify=False)
    print('thread-'+ str(i) + '> ' + str(r.content))

def sendPut(i, u, x, y, z):
    r = requests.put(u, headers=x, params=y, data=z, verify=False)
    print('thread-'+ str(i) + '> ' + str(r.content))

def sendGet(i, u, x, y, z):
    r = requests.get(u, headers=x, params=y, data=z, verify=False)
    print('thread-'+ str(i) + '> ' + str(r.content))

def sendPatch(i, u, x, y, z):
    r = requests.patch(u, headers=x, params=y, data=z, verify=False)
    print('thread-'+ str(i) + '> ' + str(r.content))

def sendReq(a, w, h):
    u = h + '://' + a.url
    param = a.param
    data = a.data
    headers = a.headers
    if (a.method == 'POST'):
        with concurrent.futures.ThreadPoolExecutor(max_workers=w) as executor:
            for i in range (0, w):
                executor.submit(sendPost, i, u, headers, param, data)
    elif (a.method == 'PUT'):
        with concurrent.futures.ThreadPoolExecutor(max_workers=w) as executor:
            for i in range (0, w):
                executor.submit(sendPut, i, u, headers, param, data)
    elif (a.method == 'GET'):
        with concurrent.futures.ThreadPoolExecutor(max_workers=w) as executor:
            for i in range (0, w):
                executor.submit(sendGet, i, u, headers, param, data)
    elif (a.method == 'PATCH'):
        with concurrent.futures.ThreadPoolExecutor(max_workers=w) as executor:
            for i in range (0, w):
                executor.submit(sendPatch, i, u, headers, param, data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='racoon - race condition automation')
    parser.add_argument('-t', '--target', type=str, help='target file config')
    parser.add_argument('--https', help='use https. default: no', action='store_true')
    parser.add_argument('-w', '--worker', type=int, help='how many workers run in a time')
    args = parser.parse_args()

    if(not args.target or not args.worker):
        parser.print_help()
        sys.exit(1)

    print('Starting '+str(args.worker)+' threads to test '+args.target+'...')
    a = Agent()
    getInfo(args.target, a)
    sendReq(a, args.worker, 'https') if args.https else sendReq(a, args.worker, 'http')