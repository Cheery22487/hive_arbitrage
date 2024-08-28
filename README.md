# Overview
This is a small arbitrage bot working on the hive blockchain. Note: This bot will only work when you provide a working account with a postingkey and activekey.
# Scope
This is a proof of concept. This bot was initially given 10 Hive (~2 USD at the time) on 11 August 2024 to start out and reached 110 Hive, which means 100 Hive (~20 USD) in profit, on 22 August 2024. While it does work and there is a small amount of profit, it requires a (in comparison) significant initial one-time investment to cover the ongoing rc-costs (gas fees in hive). Also it needs to be stated that there is no exponential scaling involved or an increase in profit by providing more liquidity. This bot already covers all arbitrage opportunities.
# Current Standings
You can see the current amount of Hive using the following link: https://hive-engine.com/@cursedellie/wallet.
And you can explore the blockchain interactions here: https://hivehub.dev/@cursedellie
# Where is the profit coming from?
There are two main ways of trading tokens. You can use the market with buy- and sellorders (https://hive-engine.com/trade/SWAP.BTC) or use a liquidity pool (https://beeswap.dcity.io/swap?input=SWAP.HIVE&output=SWAP.BTC). As both options are in theory independent of eachother in terms of price discovery, there may arise somewhat significant differences in price.

For example: If a person has a lot of Bitcoin and sells them on the market, it will lower the price of bitcoin on the market. The price in the liquidity pool remains unchanged. If you are the first one to notice such a case, you can buy BTC at a lower price on the open market, swap it back to your starting currency using a liquidity pool and make a profit.

While this example is easy to understand, this is barely ever the case and there are other bots already taking advantage of such simple cases. In reality, the opportunity for profitable trades arise when a liquidity pool is slightly tipped in one direction and the algorithm can discover a route of liquidity swaps after which it has increased its amount of tokens.

Real example (28 August 2024): Using 10 Hive to buy 128.205 Voucher on the Market. Swapping 128.205 Voucher for 260.565 SPS using a liquidity pool. Swapping 260.565 SPS for 21.700 BEE using a liquidity pool. Swapping 21.700 BEE to 1.808 USDT using a liquidity pool. Selling 1.808 USDT on the market for 10.07 Hive.

Also sometimes liquidity pools are tipped so significantly that there is profit to be made by doing a swaps in a circle: Real example (28 August 2024):
21.903 BEE -> 0.0007161 ETH -> 0.00003063 BTC -> 21.980 BEE
