class Agent(object):
    method: str = ''
    url: str = ''
    param: tuple = ()
    headers: dict = {}
    data: str = ''

    def setMethod(self, x):
        a = x.split(' ')
        self.method = a[0]
    
    def setUrl(self, x):
        a = x.split(' ')
        b = a[1].split('?')
        self.url = b[0]

    def setParam(self, x):
        a = x.split(' ')
        b = a[1].split('?')
        if (len(b) == 1):
            self.param = ()
            return
        c = b[1].split('&')
        tup = ()
        for d in c:
            e = d.split('=')
            tup = (*tup, (e[0],e[1]))
        self.param = tup
    
    def setHeaders(self, x):
        a = x.split(': ')
        if (a[0] == 'Host'):
            self.url = a[1][:-1:] + self.url
        #print(self.head)
        self.headers.update({a[0]:a[1][:-1:]})
    
    def setData(self,x):
        self.data = x

'''a = Agent()
a.setUrl('POST /_exclusive/gundala-games/sessions/finishes?access_token=7e67f8879fb3623357d70c8839faa45f4598a696df8c8a50b5358b4d73305cef HTTP/1.1')
a.setHeaders('Host: api.bukalapak.com')
print(a.url)'''