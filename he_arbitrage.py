import requests
import time
from beem import Hive
from beem.account import Account
from beem.nodelist import NodeList

with open("keys.txt","r") as f:
    postingkey, activekey = f.read().split("\n")    #line1: postingkey, line2: activekey
account = ["cursedellie",postingkey,activekey]

NODE = "https://anyx.io"
#NODE = "https://api.deathwing.me"
rpc = "https://herpc.dtools.dev"
pool_rpc = "https://engine.beeswap.tools"

hive = Hive(keys=[account[2],account[1]],node=NODE)

HIVE_TESTAMOUNT = 5                         #amount of hive initially tested in swawps/trades
MAXIMUM_TRADEAMOUNT = 10                    #absolute maximum amount of hive wagered per trade
MAXIMUM_SHARE_TRADED = 0.1                  #maximum share of owned hive wagered per trade

tokenlist = ["DEC","SPS","BEE","SWAP.USDT","SWAP.BTC","VOUCHER","SWAP.DOGE","SWAP.LTC","SWAP.HBD","SWAP.ETH","PART","SHARD","SWAP.BNB","CHAOS","BEE","LEO","LGN","SWAP.BLURT"]

#bannedpools = ["DEC:SUFB","SWAP.HIVE:SWAP.WAX","BEE:SWAP.WAX","SPS:SWAP.WAX","SPS:SWAP.SLP","SWAP.AXS:SWAP.SLP","SPS:SWAP.AXS","SPS:SWAP.GALA","SPS:FSPS","STARBITS:SWAP.HBD","DEC:VOID","SWAP.HIVE:SEED","SWAP.HBD:SEED"]
bannedpools = []

testasfdsg = 1

def get_hive_balances(token,name):
    try:
        url = rpc + "/contracts"
        json_params = {"jsonrpc":"2.0","id":1677854951123,"method":"find","params":{"contract":"tokens","table":"balances","query":{"account":name,"symbol":{"$in":[token]}}}}
        resp = requests.post(url, json=json_params).json()
        if resp["result"] == []:
            return 0
        else:
            return resp["result"][0]["balance"]
    except:
        time.sleep(0.1)
        print(f"Trying API-Request again..: {token}")
        resp1 = get_hive_balances(token,name)
        return resp1

def get_he_buy_orders(token):
    try:
        url = rpc + "/contracts"
        json_params = {"jsonrpc":"2.0","id":42069,"method":"find","params":
                       {"contract":"market","query":{"symbol":token},"indexes":[{"index":"priceDec","descending":True}],"limit":1000,"offset":0,"table":"buyBook"}}
        resp = requests.post(url, json=json_params).json()
        resp = resp["result"]
        return resp 
    except:
        time.sleep(0.1)
        resp = get_he_buy_orders(token)
        return resp

def get_he_sell_orders(token):
    try:
        url = rpc + "/contracts"
        json_params = {"jsonrpc":"2.0","id":42069,"method":"find","params":
                       {"contract":"market","query":{"symbol":token},"indexes":[{"index":"priceDec","descending":False}],"limit":1000,"offset":0,"table":"sellBook"}}
        resp = requests.post(url, json=json_params).json()
        resp = resp["result"]
        return resp 
    except:
        time.sleep(0.1)
        x = get_he_sell_orders(token)
        return x

def get_pools():
    url = pool_rpc + "/contracts"
    json_params = {"id":0,"jsonrpc":"2.0","method":"find","params":{"contract":"marketpools","table":"pools","query":{},"limit":1000,"offset":0}}
    try:
        resp = requests.post(url, json=json_params).json()
        resp = resp["result"]
        return resp
    except:
        return False

def get_precisions():
    url = "https://api.hive-engine.com/rpc/contracts"
    json_params = {"id":0,"jsonrpc":"2.0","method":"find","params":{"contract":"tokens","table":"tokens","query":{},"limit":1000,"offset":0}}
    resp = requests.post(url, json=json_params).json()
    resp = resp["result"]

    json_params = {"id":0,"jsonrpc":"2.0","method":"find","params":{"contract":"tokens","table":"tokens","query":{},"limit":1000,"offset":1000}}
    resp2 = requests.post(url, json=json_params).json()
    #print(resp2)
    resp2 = resp2["result"]

    precisions = {}
    for token in resp:
        precisions[token["symbol"]] = token["precision"]
    for token in resp2:
        precisions[token["symbol"]] = token["precision"]
    #print(precisions)
    return precisions

def round_down(value, decimals):
    factor = 1 / (10 ** decimals)
    return (value // factor) * factor

def get_pool_trade(starttoken,tradetoken,amount,pools,precisions):
    amount = round(float(amount),int(precisions[starttoken]))
    for pool in pools:
        #print(pool)
        if starttoken in pool["tokenPair"].split(":") and tradetoken in pool["tokenPair"].split(":"):
            x = float(pool["baseQuantity"])
            y = float(pool["quoteQuantity"])
            const_prod = float(x) * float(y)
            
            pair = pool["tokenPair"].split(":")

            if starttoken == pair[0]:
                if amount > x/50:
                    return 0
            if starttoken == pair[1]:
                if amount > y/50:
                    return 0

            if starttoken == pair[0]:
                result = (y - (const_prod/(x+amount))) * 0.9975       #   float(pool["basePrice"]) * amount * 0.9975
                return round_down(result, int(precisions[tradetoken]))
            elif starttoken == pair[1]:
                result = (x - (const_prod/(y+amount))) * 0.9975       #   float(pool["quotePrice"]) * amount * 0.9975
                return round_down(result, int(precisions[tradetoken]))
    #print(starttoken)
    #print("Error 1")
    return False
    #exit()

def get_pool_trade_multi(starttoken,tradetoken,amount,pools,precisions,multi):
    amount = round(float(amount),int(precisions[starttoken]))
    for pool in pools:
        #print(pool)
        if starttoken in pool["tokenPair"].split(":") and tradetoken in pool["tokenPair"].split(":"):
            x = float(pool["baseQuantity"])
            y = float(pool["quoteQuantity"])
            const_prod = float(x) * float(y)
            
            pair = pool["tokenPair"].split(":")

            if starttoken == pair[0]:
                if amount > x/50:
                    return 0
            if starttoken == pair[1]:
                if amount > y/50:
                    return 0

            if starttoken == pair[0]:
                x = x + 2*multi*amount
                y = const_prod/x
                result = (y - (const_prod/(x+amount))) * 0.9975       #   float(pool["basePrice"]) * amount * 0.9975
                return round_down(result, int(precisions[tradetoken]))
            elif starttoken == pair[1]:
                y = y + 2*multi*amount
                x = const_prod/y
                result = (x - (const_prod/(y+amount))) * 0.9975       #   float(pool["quotePrice"]) * amount * 0.9975
                return round_down(result, int(precisions[tradetoken]))
    #print(starttoken)
    #print("Error 1")
    return False
    #exit()

def tokens_in_hive(tokenamounts,pools,precisions):
    good_trades = []
    buyorders_dict = {}
    for key,value in tokenamounts.items():
        time.sleep(0.02)
        pool_hive = get_pool_trade(key,"SWAP.HIVE",value[0],pools,precisions)
        buyorders = get_he_buy_orders(key)
        buyorders_dict[key+",SWAP.HIVE"] = buyorders
        if len(buyorders) <= 0:
            continue
        he_hive = value[0]*float(buyorders[0]["price"])
        #he_hive = round_down(he_hive, int(precisions["SWAP.HIVE"]))
        #print(key,pool_hive,he_hive)
        maxamount = min(value[2],float(buyorders[0]["quantity"]) * float(buyorders[0]["price"]))
        
        if (pool_hive != False and (pool_hive >= HIVE_TESTAMOUNT*1.005 or (pool_hive > HIVE_TESTAMOUNT*1.004 and len(tokenamounts[key][1].split("|")) <= 3))) or (he_hive != False and (he_hive >= HIVE_TESTAMOUNT*1.005 or (he_hive > HIVE_TESTAMOUNT*1.004 and len(tokenamounts[key][1].split("|")) <= 3))):
            if (pool_hive != False and he_hive != False and pool_hive > he_hive) or (pool_hive != False and he_hive == False):
                tokenamounts[key][1] = tokenamounts[key][1] + "|" + key + ":" + "SWAP.HIVE"
                tokenamounts[key][0] = pool_hive
            elif (pool_hive != False and he_hive != False and he_hive > pool_hive) or (he_hive != False and pool_hive == False):
                tokenamounts[key][1] = tokenamounts[key][1] + "|" + key + "," + "SWAP.HIVE"
                tokenamounts[key][0] = he_hive
                tokenamounts[key][2] = maxamount
            #preventing the most simple case of buy on market & then sell in pool or the other way around. Other bots seem to be faster and it often ends up a losing venture
            if maxamount >= 0.5 and len(tokenamounts[key][1].split("|")) >= 3:          #minimum 0.5 hive traded to not accrue too much rc costs   
                good_trades.append(tokenamounts[key])
    return good_trades, buyorders_dict
    #print("Nothing found")

    
def all_poolswaps(tokenamounts,pools,precisions):
    for key,value in tokenamounts.items():
        tokenamounts2 = {}
        tokenamounts2[key] = value
        for pool in pools:
            if key in pool["tokenPair"].split(":") and "SWAP.HIVE" not in pool["tokenPair"].split(":") and pool["tokenPair"] not in bannedpools and pool["_id"] <= 235:
                tokenpair = pool["tokenPair"].split(":")
                if key == tokenpair[0]:
                    new_amount = get_pool_trade(key,tokenpair[1],value[0],pools,precisions)
                    #print(tokenpair[1],value[0],new_amount)
                    tokenamounts2[tokenpair[1]] = [new_amount,value[1]+"|"+key+":"+tokenpair[1],value[2]]
                elif key == tokenpair[1]:
                    new_amount = get_pool_trade(key,tokenpair[0],value[0],pools,precisions)
                    #print(tokenpair[0],value[0],new_amount)
                    tokenamounts2[tokenpair[0]] = [new_amount,value[1]+"|"+key+":"+tokenpair[0],value[2]]
    #print(tokenamounts2)
    return tokenamounts2

def all_poolswaps_2(tokenamounts,pools,precisions):
    tokenamounts2 = {}
    for key,value in tokenamounts.items():
        prev_values = value[-1]
        if key not in tokenamounts2.keys():
            tokenamounts2[key] = value
        elif tokenamounts[key][0] > tokenamounts2[key][0]:
            tokenamounts2[key] = value
        for pool in pools:
            if key in pool["tokenPair"].split(":") and "SWAP.HIVE" not in pool["tokenPair"].split(":") and pool["tokenPair"] not in bannedpools and pool["_id"] <= 235:# and pool["tokenPair"] not in tokenamounts[key][1]:
                tokenpair = pool["tokenPair"].split(":")
                tknpair = pool["tokenPair"].split(":")
                tknpair2 = ":".join([tknpair[1],tknpair[0]])
                tknpair = ":".join(tknpair)
                if key == tokenpair[0]:
                    if tknpair in tokenamounts[key][1] or tknpair2 in tokenamounts[key][1]:
                        count = tokenamounts[key][1].count(tknpair) + tokenamounts[key][1].count(tknpair2)
                        new_amount = get_pool_trade_multi(key,tokenpair[1],value[0],pools,precisions,count)
                    else:
                        new_amount = get_pool_trade(key,tokenpair[1],value[0],pools,precisions)
                    token_temp = tokenpair[1]
                    tokenamounts_temp = [new_amount,value[1]+"|"+key+":"+tokenpair[1],value[2]]
                elif key == tokenpair[1]:
                    if tknpair in tokenamounts[key][1] or tknpair2 in tokenamounts[key][1]:
                        count = tokenamounts[key][1].count(tknpair) + tokenamounts[key][1].count(tknpair2)
                        new_amount = get_pool_trade_multi(key,tokenpair[0],value[0],pools,precisions,count)
                    else:
                        new_amount = get_pool_trade(key,tokenpair[0],value[0],pools,precisions)
                    token_temp = tokenpair[0]
                    tokenamounts_temp = [new_amount,value[1]+"|"+key+":"+tokenpair[0],value[2]]
                if token_temp not in tokenamounts2.keys():
                    tokenamounts2[token_temp] = tokenamounts_temp
                    tokenamounts2[token_temp].append(prev_values+","+str(tokenamounts_temp[0]))
                elif new_amount > tokenamounts2[token_temp][0]:
                    tokenamounts2[token_temp] = tokenamounts_temp
                    tokenamounts2[token_temp].append(prev_values+","+str(tokenamounts_temp[0]))
    #print(tokenamounts2)
    return tokenamounts2

def swap_tokens(input_token,output_token,amount,pools,precisions):
    amount = str(round(float(amount),int(precisions[input_token])))
    balance2 = get_hive_balances("SWAP.HIVE","richzuleyka")
    if float(balance2) < 0.000000001:
        data = {"contractName":"tokens","contractAction":"transfer","contractPayload":{"symbol":"SWAP.HIVE","to":"richzuleyka","quantity":"1e-8","memo":""}}
        hive.custom_json("ssc-mainnet-hive", json_data=data, required_auths=[account[0]])
    for pool in pools:
        if input_token in pool["tokenPair"].split(":") and output_token in pool["tokenPair"].split(":"):
            tokenpair = pool["tokenPair"]
    data = {"contractName":"marketpools","contractAction":"swapTokens","contractPayload":{"tokenPair":tokenpair,"tokenSymbol":input_token,"tokenAmount":str(amount),"tradeType":"exactInput"}}
    try:
        hive.custom_json("ssc-mainnet-hive", json_data=data, required_auths=[account[0]])
    except Exception as err:
        print(err)

    time.sleep(3)
    balance = 0
    while float(balance) <= 0.00000002 or balance == "0":
        balance = get_hive_balances(output_token,account[0])
        time.sleep(0.5)
    #print(balance)
    #print(listing_id)
    #print(balance)
    if float(balance) > 0.00000002:
        return balance
    else:
        return 0
    

def buy_token_he(token, price, amount):
    data = {"contractName":"market","contractAction":"buy","contractPayload":{"symbol":token,"quantity":amount,"price":price}}
    hive.custom_json("ssc-mainnet-hive", json_data=data, required_auths=[account[0]])

def sell_token_he(token, price, amount):
    data = {"contractName":"market","contractAction":"sell","contractPayload":{"symbol":token,"quantity":amount,"price":price}}
    hive.custom_json("ssc-mainnet-hive", json_data=data, required_auths=[account[0]])

#sell_token_he(account, "DEC", str(round(he_dec_price_hive-0.00000001,8)), str(round(dec_sellamount,3)))
#check_dec_listings(account)


def check_buy_listings(token):
    try:
        url = rpc + "/contracts"
        json_params = {"jsonrpc":"2.0","id":1677853057215,"method":"find","params":
                       {"contract":"market","query":{"symbol":token},"indexes":[{"index":"priceDec","descending":True}],"limit":1000,"offset":0,"table":"buyBook"}}
        resp = requests.post(url, json=json_params).json()
        resp = resp["result"]
        for listing in resp:
            if listing["account"] == account[0]:
                return listing["txId"]
        return 0
    except:
        time.sleep(1)
        aaa = check_buy_listings(token)
        return aaa

def check_sell_listings(token):
    try:
        url = rpc + "/contracts"
        json_params = {"jsonrpc":"2.0","id":1677853057215,"method":"find","params":
                       {"contract":"market","query":{"symbol":token},"indexes":[{"index":"priceDec","descending":False}],"limit":1000,"offset":0,"table":"sellBook"}}
        resp = requests.post(url, json=json_params).json()
        resp = resp["result"]
        for listing in resp:
            if listing["account"] == account[0]:
                return listing["txId"]
        return 0
    except:
        time.sleep(1)
        aaa = check_sell_listings(token)
        return aaa

def cancel_listing(buy_ids, book):
    try:
        for i in range(len(buy_ids)):
            data = [{"contractName":"market","contractAction":"cancel","contractPayload":{"type":book,"id":str(buy_ids[i])}}]
            hive.custom_json("ssc-mainnet-hive", json_data=data, required_auths=[account[0]])
    except Exception as e:
        print(f"Error cancelling HE_listing: {e}")
        exit()

def buy_from_he(token, amount, sellorders, precisions):
    amount = float(amount) / float(sellorders[0]["price"])
    buy_token_he(token, str(round(float(sellorders[0]["price"])+0.00000001,8)), str(round(amount,int(precisions[token]))))
    time.sleep(7)
    listing_id = 0
    balance = 0
    while listing_id == 0 and (float(balance) < 0.00000001 or balance == "0"):
        listing_id = check_buy_listings(token)
        balance = get_hive_balances(token,account[0])
        time.sleep(0.5)
    #print(balance)
    #print(listing_id)
    listing_id = check_buy_listings(token)
    if listing_id != 0:
        print("Buyorder didnt get filled instantly: cancel buy-listing")
        cancel_listing([listing_id], "buy")
        time.sleep(15)
        balance = get_hive_balances(token,account[0])
    if float(balance) > 0.00000001:
        return balance
    else:
        return 0

def sell_to_he(token, amount, buyorders, precisions):
    hive_start = get_hive_balances("SWAP.HIVE",account[0])
    time.sleep(0.01)
    balance = get_hive_balances(token,account[0])
    prev_balance = balance
    amount = float(balance)
    sell_token_he(token, str(round(float(buyorders[0]["price"])-0.00000001,8)), str(round(amount,int(precisions[token]))))
    for x in range(5,20):
        time.sleep(1)
        hive_now = get_hive_balances("SWAP.HIVE",account[0])
        balance = get_hive_balances(token,account[0])
        #print(balance, type(balance))
        listing_id = check_sell_listings(token)
        if float(hive_now) > float(hive_start) + 0.0000001 and abs(float(prev_balance) - float(balance)) > 0.0000002 and listing_id == 0:
            return balance
    
    while abs(float(prev_balance) - float(balance)) < 0.0000002:
        time.sleep(1)
        balance = get_hive_balances(token,account[0])
    listing_id = check_sell_listings(token)
    while listing_id != 0 or float(balance) > 0.00000002:
        if listing_id != 0:
            cancel_listing([listing_id], "sell")
            time.sleep(20)
            balance = get_hive_balances(token,account[0])
            time_x = time.time()
            while float(balance) <= 0.00000002 and time.time() - time_x < 60:
                time.sleep(1)
                balance = get_hive_balances(token,account[0])
            buyorders = get_he_buy_orders(token)
        else:
            prev_balance = balance
            amount = float(balance)
            sell_token_he(token, str(round(float(buyorders[0]["price"])-0.00000001,8)), str(round(amount,int(precisions[token]))))
            time.sleep(20)
            while abs(float(prev_balance) - float(balance)) < 0.0000002 and float(balance) >= 0.00000001:
                time.sleep(1)
                balance = get_hive_balances(token,account[0])
        listing_id = check_sell_listings(token)
    return balance


def perform_arbitrage(tokendata,precisions,pools):
    print("Starting trades...")
    route = tokendata[1].split("|")
    zieltoken = "SWAP.HIVE"
    for i,trade in enumerate(route):
        starttoken = zieltoken
        if "," in trade:
            zieltoken = route[i].split(",")
        elif ":" in trade:
            zieltoken = route[i].split(":")
        if starttoken == zieltoken[0]:
            zieltoken = zieltoken[1]
        elif starttoken == zieltoken[1]:
            zieltoken = zieltoken[0]
        else:
            print("Error: WTF")
            exit()
        if i == 0:
            if "," in trade:
                sellorders = get_he_sell_orders(zieltoken)
                new_balance = buy_from_he(zieltoken, tokendata[2], sellorders, precisions)
                print(f"-{zieltoken}: {new_balance}")
                if float(new_balance) < 0.00000002:
                    return
            elif ":" in trade:
                new_balance = swap_tokens("SWAP.HIVE",zieltoken,tokendata[2],pools,precisions)
                print(f"-{zieltoken}: {new_balance}")
        elif i == len(route)-1:
            if "," in trade:
                buyorders = get_he_buy_orders(starttoken)
                new_balance = sell_to_he(starttoken, new_balance, buyorders, precisions)
                print(f"-{starttoken} left: {new_balance}")
            elif ":" in trade:
                new_balance = swap_tokens(starttoken,zieltoken,new_balance,pools,precisions)
                time.sleep(20)
                endbalance = get_hive_balances(starttoken,account[0])
                print(f"-{starttoken} left: {endbalance}")
        else:
            new_balance = swap_tokens(starttoken,zieltoken,new_balance,pools,precisions)
            print(f"-{zieltoken}: {new_balance}")

def print_trade(trade):
    print("Chosen Route:")
    print(f"{trade[1]}")
    print(f"Hive being wagered: {trade[2]:.4f}, Expected Hive: {trade[2] * (1+(trade[0]-HIVE_TESTAMOUNT)/HIVE_TESTAMOUNT):.4f} (+{100*(trade[0]-HIVE_TESTAMOUNT)/HIVE_TESTAMOUNT:.3f}%)")

def check_single_route(traderoute,amount,sellorders_dict,pools,buyorders_dict,precisions):
    route = traderoute[1].split("|")
    zieltoken = "SWAP.HIVE"
    amount = round_down(amount, int(precisions["SWAP.HIVE"]))
    for i,trade in enumerate(route):
        starttoken = zieltoken
        if "," in trade:
            zieltoken = route[i].split(",")
        elif ":" in trade:
            zieltoken = route[i].split(":")
        if starttoken == zieltoken[0]:
            zieltoken = zieltoken[1]
        elif starttoken == zieltoken[1]:
            zieltoken = zieltoken[0]
        if i == 0:
            if "," in trade:
                sellorders = sellorders_dict[route[0]]
                new_balance = amount/float(sellorders[0]["price"])
                maxamount = float(sellorders[0]["quantity"]) * float(sellorders[0]["price"])
                if maxamount < amount:
                    return 0
                #print(float(sellorders[0]["quantity"]),float(sellorders[0]["price"]),maxamount)
            elif ":" in trade:
                new_balance = get_pool_trade("SWAP.HIVE",zieltoken,amount,pools,precisions)
        elif i == len(route)-1:
            if "," in trade and route[-1] in buyorders_dict.keys():
                buyorders = buyorders_dict[route[-1]]
                if new_balance > float(buyorders[0]["quantity"]):
                    return 0
                new_balance = new_balance*float(buyorders[0]["price"])
            elif ":" in trade:
                new_balance = get_pool_trade(starttoken,"SWAP.HIVE",new_balance,pools,precisions)
            else:
                print("Error3")
                exit()
        else:
            tknpair = trade.split(":")
            tknpair2 = ":".join([tknpair[1],tknpair[0]])
            tknpair = ":".join(tknpair)
            count = traderoute[1].count(tknpair) + traderoute[1].count(tknpair2) - 1
            if count > 0:
                new_balance = get_pool_trade_multi(starttoken,zieltoken,new_balance,pools,precisions,count)
            else:
                new_balance = get_pool_trade(starttoken,zieltoken,new_balance,pools,precisions)
        new_balance = round_down(new_balance, int(precisions[zieltoken]))
        #print(zieltoken, new_balance)

    return new_balance


def main():
    precisions = get_precisions()
    balance = get_hive_balances("SWAP.HIVE",account[0])
    print(f"SWAP.HIVE: {balance}")
    while True:
        sellorders_dict = {}
        max_trade_hive = min(MAXIMUM_TRADEAMOUNT,MAXIMUM_SHARE_TRADED*float(balance))
        tokenamounts = {}
        for token in tokenlist:
            sellorders_x = get_he_sell_orders(token)
            sellorders_dict["SWAP.HIVE,"+token] = sellorders_x
            time.sleep(0.01)
        pools = get_pools()
        if pools == False:
            continue
        for token in tokenlist:
            #print("---")
            sellorders = sellorders_dict["SWAP.HIVE,"+token]
            if pools == False or sellorders == False:
                time.sleep(5)
                continue
            swapamount = get_pool_trade("SWAP.HIVE",token,HIVE_TESTAMOUNT,pools,precisions)
            tokenamounts[token] = [swapamount,"SWAP.HIVE:"+token,HIVE_TESTAMOUNT,str(swapamount)]
            maxamount = min(float(sellorders[0]["quantity"]) * float(sellorders[0]["price"]),HIVE_TESTAMOUNT)

            he_amount = maxamount/float(sellorders[0]["price"])
            he_amount = round_down(he_amount, int(precisions[token]))
            he_ghostamount = HIVE_TESTAMOUNT/float(sellorders[0]["price"])
            he_ghostamount = round_down(he_ghostamount, int(precisions[token]))
            if he_ghostamount > tokenamounts[token][0]:
                tokenamounts[token] = [he_ghostamount, "SWAP.HIVE,"+token, maxamount,str(he_ghostamount)]

            
        for i in range(10):
            tokenamounts = all_poolswaps_2(tokenamounts,pools,precisions)

            
        good_trades, buyorders_dict = tokens_in_hive(tokenamounts,pools,precisions)

        if len(good_trades) > 0:
            print("--")
            print("Possible trades:")
            for x in good_trades:
                print(x[:-1])
            #print(good_trades)
            #print("--")
            max_hive = 0
            for trade in good_trades:
                if trade[0] > max_hive:
                    max_hive = trade[0]
                    g_trade = trade
            if int(g_trade[2]) == HIVE_TESTAMOUNT and max_trade_hive > HIVE_TESTAMOUNT:
                poss_traded_hive_amounts = [HIVE_TESTAMOUNT + x*(max_trade_hive-HIVE_TESTAMOUNT)/9 for x in range(10)]
                expected_returns = []
                expected_diff = []
                for amount in poss_traded_hive_amounts:
                    expected_return = check_single_route(g_trade,amount,sellorders_dict,pools,buyorders_dict,precisions)
                    expected_returns.append(expected_return)
                    expected_diff.append(expected_return-amount)
                max_value = max(expected_diff)
                max_index = expected_diff.index(max_value)
                best_tradeamount = poss_traded_hive_amounts[max_index]
                g_trade[0] = float(best_tradeamount+max_value)*HIVE_TESTAMOUNT/best_tradeamount
                g_trade[2] = best_tradeamount
            print_trade(g_trade)
            perform_arbitrage(g_trade,precisions,pools)
            balance = get_hive_balances("SWAP.HIVE",account[0])
            print(f"New SWAP.HIVE Balance: {balance}")
        #exit()


if __name__ == '__main__':
    main()