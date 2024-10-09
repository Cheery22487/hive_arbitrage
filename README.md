# Overview
This is a small arbitrage bot working on the hive blockchain. It is just a small personal project and is therefore lacking documentation mostly.

!Note: This bot will break when attempting to perform a trade and no hiveaccount with a postingkey and activekey is provided.

# Scope
This is a proof of concept. Initially, the bot was funded with 10 Hive (equivalent to approximately $2 at the time). While the bot does function as intended and has generated a small profit, it requires a relatively significant one-time initial investment to cover ongoing RC costs (the equivalent of gas fees on the Hive blockchain). It is important to note that there is no exponential scaling or increase in profit from providing additional liquidity. The bot already captures all available arbitrage opportunities within the current system.

# Milestones
Start: 10 Hive on 11 August 2024
100 Hive (~20 USD) profit: 22 August 2024
200 Hive (~40 USD) profit: 07 September 2024
250 Hive (~50 USD) profit: 29 September 2024

You can see the current amount of Hive using the following link: https://hive-engine.com/@cursedellie/wallet.
And you can explore the blockchain interactions here: https://hivehub.dev/@cursedellie

# Plot

This is a view of the bots performance since the start.

[Arbitrage Performance](plot/plot.png)

It is interesting to note that the performance has significantly deteriorated since its release on GitHub. Given the number of clones following the published updates and the trading behavior of certain accounts, it can be assumed that several users are currently using this bot or a bot inspired by this release.

These bots are in direct competition with each other, and they can interfere so much that it may even lead to losses.


# Where is the profit coming from?
There are two main ways of trading tokens. You can use the market with buy- and sellorders (https://hive-engine.com/trade/SWAP.BTC) or use a liquidity pool (https://beeswap.dcity.io/swap?input=SWAP.HIVE&output=SWAP.BTC). As both options are in theory independent of eachother in terms of price discovery, there may arise somewhat significant differences in price.

For example: If a person has a lot of Bitcoin and sells them on the market, it will lower the price of bitcoin on the market. The price in the liquidity pool however remains unchanged. If you are the first one to notice such a case, you can buy BTC at a lower price on the open market, swap it back to your starting currency using a liquidity pool and make a profit.

While this example is easy to understand, this is barely ever the case and there are other bots already taking advantage of such simple cases. In reality, the opportunity for profitable trades arises mostly when liquidity pools are slightly tipped in one direction and the algorithm can discover a route of liquidity swaps after which it has increased its amount of tokens.

Real example (28 August 2024): 10 Hive -> 0.00003058 BTC -> 21.856 BEE -> 1.811 USDT -> 10.07 Hive.

Also sometimes liquidity pools are tipped so significantly that there is profit to be made by doing a swaps in a circle even though each individual swap has a fee of 0.25% attached.

Real example (28 August 2024): 21.903 BEE -> 0.0007161 ETH -> 0.00003063 BTC -> 21.980 BEE