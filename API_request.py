import requests

class geneacity_API_request():
    json:object=None
    url:str=None
    status:int=0
    error:str=None
    def __init__(self,url:str):
        self.url=url
        response=requests.get(url)
        if response.status_code == 200:
            self.json = response.json()
        else:
            self.error=response.status_code
        
        self.status=self.json['status']

x=250
y=250


