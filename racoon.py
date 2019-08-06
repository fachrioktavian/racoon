import re, sys, requests, threading
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
    '''print(a.method)
    print(a.param)
    print(a.headers)
    print(a.data)
    print(a.url)'''

def sendPost(i, u, x, y, z):
    r = requests.post(u, headers=x, params=y, data=z, verify=False)
    print('thread-'+ str(i) + '> ' + str(r.content))

def sendPut(i, u, x, y, z):
    r = requests.put(u, headers=x, params=y, data=z, verify=False)
    print('thread-'+ str(i) + '> ' + str(r.content))

def sendReq(a, n, h):
    u = h + '://' + a.url
    param = a.param
    data = a.data
    headers = a.headers
    if (a.method == 'POST'):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            for i in range (0, n):
                executor.submit(sendPost, i, u, headers, param, data)
                #threading.Thread(target=sendPost(i, u, headers, param, data)).start()
    elif (a.method == 'PUT'):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for i in range (0, n):
                executor.submit(sendPut, i, u, headers, param, data)


if __name__ == '__main__':
    inp = sys.argv[1]
    a = Agent()
    getInfo(inp, a)
    sendReq(a, 20, 'https')

    '''fr = open(inp, 'r')
    for line in fr:
        if (line == '\n'):
            print('newline')
            continue
        print(line)'''