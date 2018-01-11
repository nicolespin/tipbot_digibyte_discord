import discord
from tipper.tipper import *

client = discord.Client()

@client.event
async def on_message(message):
    #make sure bot doesnt reply to himself
    if message.author == client.user:
        return
    
    if message.content.startswith('!price'):
        price = getPrice(full=1,refresh=1)
        price_btc = getPrice(satoshi=1,refresh=1)
        msg = "The current price of AMMO is $%f or %.8f BTC."%(price,price_btc)
        return await client.send_message(message.channel,msg)
    
    if message.content.startswith('!help'):
        helpmsg = "**!price** - shows the current price of AMMO.\n**!deposit** or **!addr** - shows your deposit address.\n**!balance [0conf=false]** - shows your balance\n**!tip [user] [amount]** - tips another user coins.\n**!withdraw [amount] [address]** - withdraws funds to an external address.\n**!rain [amount]** - tips everyone on the server."
        return await client.send_message(message.channel,helpmsg)

    if message.content.startswith('!deposit') or message.content.startswith('!addr'):
        account = message.author.id
        address = getAddress(account)
        msg = '{0.author.mention}, your address is %s.'.format(message)%address
        return await client.send_message(message.channel,msg)

    if message.content.startswith('!balance 0conf'): #0conf balance
        account = message.author.id
        balance = getBalance(account,0)
        msg = '{0.author.mention}, you have %f ammo, including 0-confs.'.format(message)%balance
        return await client.send_message(message.channel,msg)

    if message.content.startswith('!balance'):
        account = message.author.id
        balance = getBalance(account)
        price = getPrice(float(balance))
        msg = '{0.author.mention}, you have %f ammo ($%.2f).'.format(message)%(balance,price)
        return await client.send_message(message.channel,msg)

    if message.content.startswith('!tip '):
        tipper = message.author.id
        content = message.content.split()[1:]
        toTipMention = content[0]
        toTip = toTipMention.replace('<@','').replace('>','') #remove <@> from ID
        amount = content[1]

        #catching errors
        if not toTipMention[:2]=='<@':
            return await client.send_message(message.channel,"{0.author.mention}, invalid account.".format(message))
        try:
            amount = float(amount)
        except ValueError:
            return await client.send_message(message.channel,"{0.author.mention}, invalid amount.".format(message))

        try:
            tip(tipper,toTip,amount)
            price = getPrice(float(amount))
            return await client.send_message(message.channel,"{0.author.mention} has tipped %s %f ammo ($%.2f).".format(message)%(toTipMention,amount,price))
        except ValueError:
            return await client.send_message(message.channel,"{0.author.mention}, insufficient balance.".format(message))

    if message.content.startswith('!withdraw '):
        account = message.author.id
        amount = message.content.split()[1]
        address = message.content.split()[2]
        

        #catching errors again
        if not validateAddress(address):
            return await client.send_message(message.channel,"{0.author.mention}, invalid address.".format(message))
        
        try:
            amount = float(amount)
        except ValueError:
            return await client.send_message(message.channel,"{0.author.mention}, invalid amount.".format(message))

        try:
            txid = withdraw(account,address,amount)
            return await client.send_message(message.channel,"{0.author.mention}, withdrawal complete, TXID %s".format(message)%txid)
        except ValueError:
            return await client.send_message(message.channel,"{0.author.mention}, insufficient balance.".format(message))

    if message.content.startswith('!rain '):
        account = message.author.id
        amount = float(message.content.split()[1])

        if amount < 0.01:
            return await client.send_message(message.channel,"{0.author.mention}, the amount must be bigger than 0.01 ammo.".format(message))
        #catching errors again
        try:
            amount = float(amount)
        except ValueError:
            return await client.send_message(message.channel,"{0.author.mention}, invalid amount.".format(message))

        try:
            eachtip = rain(account,amount) #the function returns each individual tip amount so this just makes it easier
            return await client.send_message(message.channel,"{0.author.mention} has tipped %f ammo to everyone on this server!".format(message)%eachtip)
        except ValueError:
            return await client.send_message(message.channel,"{0.author.mention}, insufficient balance.".format(message))
    
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run('yourtoken')

