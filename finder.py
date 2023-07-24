import requests
nick = str(input('nick: '))

def getId(nick):
    headers = {
        'authority': 'api.twitch.tv',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': 'Bearer 9fz8oqqxny9ii98mi0v6tyrgye8ywq',
        'client-id': 'rnqe5fseibqp7ub2017x2fd8jfrk5s',
        'dnt': '1',
        'origin': 'https://twitch-tools.rootonline.de',
        'referer': 'https://twitch-tools.rootonline.de/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        'login': f'{nick}',
        '_': '1690167767667',
    }

    r = requests.get('https://api.twitch.tv/helix/users', params=params, headers=headers).json()
    id = r['data'][0]['id']
    return id

def getFollowers(nick):
    id = getId(nick)

    headers = {
        'authority': 'twitch-tools.rootonline.de',
        'accept': 'application/json',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': 'Bearer 9fz8oqqxny9ii98mi0v6tyrgye8ywq',
        'client-id': 'rnqe5fseibqp7ub2017x2fd8jfrk5s',
        'dnt': '1',
        'referer': 'https://twitch-tools.rootonline.de/followinglist_viewer.php?username=nacarama',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'first': '100',
        'from_id': f'{id}',
        '_': '1690167767669',
    }

    response = requests.get('https://twitch-tools.rootonline.de/twitch-api/helix/users/follows', params=params, headers=headers).json()
    return response

def search(nick=nick):
    a = getFollowers(nick=nick)
    count = 0
    assistindo = 0
    for i in a["data"]:
        count += 1
        channel = i["to_name"]
        headers = {'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko'}
        url = 'https://gql.twitch.tv/gql'
        data = [{"operationName":"ChatViewers","variables":{"channelLogin":str(channel)},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"e0761ef5444ee3acccee5cfc5b834cbfd7dc220133aa5fbefe1b66120f506250"}}}]
        
        
        try:
            users = [] 
            r = requests.post(url=url, json=data, headers=headers).json()
            viewers = r[0]["data"]["channel"]["chatters"]["viewers"]
            if len(viewers) >= 1:
                for i in viewers:
                    users.append(i["login"])
                if nick in users:
                    encontrado = (f"Encontrado. Usuário {nick} está na live {channel}.") 
                    assistindo = 1
        except:
            pass
    if assistindo == 1:
        print(encontrado)
    else:
        print("Usuário não encontrado.")
search(nick)