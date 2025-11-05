"""
  ___________________    _   __   _____ __________ _    __________________
 /_  __/  _/_  __/   |  / | / /  / ___// ____/ __ \ |  / /  _/ ____/ ____/
  / /  / /  / / / /| | /  |/ /   \__ \/ __/ / /_/ / | / // // /   / __/   
 / / _/ /  / / / ___ |/ /|  /   ___/ / /___/ _, _/| |/ // // /___/ /___   
/_/ /___/ /_/ /_/  |_/_/ |_/   /____/_____/_/ |_| |___/___/\____/_____/   
                                                                          gh: titanleg1t ds: t1tanleg1t
                                                                          """

import discord
import asyncio
import os
import time
from pystyle import Colors, Colorate, Write, Center
from discord import Intents

class ShadowControl:
    def __init__(self):
        self.tokens = []
        self.botcount = 0
        self.success = 0
        self.failed = 0
        self.starttime = 0
        self.times = 1
    
    def clearscr(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def showBanner(self):
        banner = """
 ███▄ ▄███▓ ▄▄▄        ██████   ██████    ▓█████▄  ███▄ ▄███▓
▓██▒▀█▀ ██▒▒████▄    ▒██    ▒ ▒██    ▒    ▒██▀ ██▌▓██▒▀█▀ ██▒
▓██    ▓██░▒██  ▀█▄  ░ ▓██▄   ░ ▓██▄      ░██   █▌▓██    ▓██░
▒██    ▒██ ░██▄▄▄▄██   ▒   ██▒  ▒   ██▒   ░▓█▄   ▌▒██    ▒██ 
▒██▒   ░██▒ ▓█   ▓██▒▒██████▒▒▒██████▒▒   ░▒████▓ ▒██▒   ░██▒
░ ▒░   ░  ░ ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░    ▒▒▓  ▒ ░ ▒░   ░  ░
░  ░      ░  ▒   ▒▒ ░░ ░▒  ░ ░░ ░▒  ░ ░    ░ ▒  ▒ ░  ░      ░
░      ░     ░   ▒   ░  ░  ░  ░  ░  ░      ░ ░  ░ ░      ░   
       ░         ░  ░      ░        ░        ░           ░   
                                           ░                 
        """
        centered = Center.XCenter(banner)
        print(Colorate.Vertical(Colors.purple_to_blue, centered))
    
    def showSettings(self, target="", msg="", status="", times=""):
        loaded = f"Loaded: {self.botcount} Token/s"
        settings = f"""
{loaded}
────────────────────────────────
SETTINGS
────────────────────────────────
TARGET: {target or 'Not set'}
MESSAGE: {msg or 'Not set'}
TIMES: {times or 'Not set'}
BOT STATUS: {status or 'Not set'}
────────────────────────────────
        """
        print(Colorate.Vertical(Colors.purple_to_blue, settings))
    
    def loadTokens(self):
        try:
            with open('token.txt', 'r') as f:
                self.tokens = [line.strip() for line in f.readlines() if line.strip()]
            self.botcount = len(self.tokens)
            return True
        except:
            return False
    
    def currentTime(self):
        return time.strftime("%H:%M:%S")
    
    async def sendDM(self, token, userid, message, botnum):
        intents = Intents.all()

        class BotClient(discord.Client):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            async def on_ready(self):
                user = await self.fetch_user(userid)
                for i in range(self.control.times):
                    try:
                        await user.send(message)
                        timenow = self.control.currentTime()
                        timecolor = Colorate.Vertical(Colors.purple_to_blue, f"[{timenow}]")
                        successcolor = Colorate.Vertical(Colors.green, f" Bot #{botnum:02d} → Message {i+1}/{self.control.times} sent successfully!")
                        print(f"{timecolor}{successcolor}")
                        self.control.success += 1
                    except:
                        timenow = self.control.currentTime()
                        timecolor = Colorate.Vertical(Colors.purple_to_blue, f"[{timenow}]")
                        errorcolor = Colorate.Vertical(Colors.red, f" Bot #{botnum:02d} → Message {i+1}/{self.control.times} failed to send!")
                        print(f"{timecolor}{errorcolor}")
                        self.control.failed += 1
                await self.close()

        client = BotClient(intents=intents, max_messages=None)
        client.control = self

        try:
            await client.start(token)
        except:
            timenow = self.currentTime()
            timecolor = Colorate.Vertical(Colors.purple_to_blue, f"[{timenow}]")
            errorcolor = Colorate.Vertical(Colors.red, f" Bot #{botnum:02d} → Connection failed")
            print(f"{timecolor}{errorcolor}")
            self.failed += self.times  
    
    async def deployAll(self, userid, message):
        self.starttime = time.time()
        self.success = 0
        self.failed = 0
        
        print(Colorate.Vertical(Colors.purple_to_blue, "\n" + "─" * 50))
        print(Colorate.Vertical(Colors.purple_to_blue, "STARTING MASS DM..."))
        print(Colorate.Vertical(Colors.purple_to_blue, "─" * 50))
        
        tasks = []
        for i, token in enumerate(self.tokens):
            task = self.sendDM(token, userid, message, i+1)
            tasks.append(task)
        
        semaphore = asyncio.Semaphore(5)
        
        async def limitedTask(task):
            async with semaphore:
                return await task
        
        limitedtasks = [limitedTask(task) for task in tasks]
        await asyncio.gather(*limitedtasks, return_exceptions=True)
        
        self.showResults()
    
    def showResults(self):
        endtime = time.time()
        totaltime = endtime - self.starttime

        print(Colorate.Vertical(Colors.purple_to_blue, "\n" + "─" * 50))
        print(Colorate.Vertical(Colors.purple_to_blue, "COMPLETE"))
        print(Colorate.Vertical(Colors.purple_to_blue, "─" * 50))

        total_messages = self.botcount * self.times
        success_rate = (self.success / total_messages) * 100 if total_messages > 0 else 0
        results = f"""
TOTAL BOTS: {self.botcount}
TOTAL MESSAGES: {total_messages}
SUCCESSFUL: {self.success}
FAILED: {self.failed}
SUCCESS RATE: {success_rate:.1f}%
TIME ELAPSED: {totaltime:.2f}s
────────────────────────────────
        """
        print(Colorate.Vertical(Colors.purple_to_blue, results))

async def main():
    control = ShadowControl()
    
    control.clearscr()
    control.showBanner()
    
    if not control.loadTokens():
        print(Colorate.Vertical(Colors.purple_to_blue, "cant find token file"))
        return
    
    control.showSettings()
    
    print(Colorate.Vertical(Colors.purple_to_blue, "\n" + "─" * 50))
    print(Colorate.Vertical(Colors.purple_to_blue, " CONFIG"))
    print(Colorate.Vertical(Colors.purple_to_blue, "─" * 50))
    
    targetid = Write.Input("\n[*] Enter User ID: ", Colors.purple_to_blue, interval=0.005)
    control.clearscr()
    control.showBanner()
    control.showSettings(target=targetid)
    
    usermsg = Write.Input("\n[*] Enter Message: ", Colors.purple_to_blue, interval=0.005)
    control.clearscr()
    control.showBanner()
    control.showSettings(target=targetid, msg=usermsg)

    times_input = Write.Input("\n[*] amount of messages per bot: ", Colors.purple_to_blue, interval=0.005)
    control.times = int(times_input)
    control.clearscr()
    control.showBanner()
    control.showSettings(target=targetid, msg=usermsg, times=control.times)
    
    print(Colorate.Vertical(Colors.purple_to_blue, "\n[*] Select Bot Status:"))
    print(Colorate.Vertical(Colors.purple_to_blue, "1. Online 🟢"))
    print(Colorate.Vertical(Colors.purple_to_blue, "2. Offline ⚫"))
    statuspick = Write.Input("\n[*] Choice (1/2): ", Colors.purple_to_blue, interval=0.005)
    botstatus = "ONLINE" if statuspick == "1" else "OFFLINE"
    
    control.clearscr()
    control.showBanner()
    control.showSettings(target=targetid, msg=usermsg, status=botstatus)
    
    confirm = Write.Input(f"\n[*] Start with {control.botcount * control.times} messages? (y/n): ", Colors.purple_to_blue, interval=0.005)
    
    if confirm.lower() == 'y':
        control.clearscr()
        control.showBanner()
        await control.deployAll(int(targetid), usermsg)
        input(Colorate.Vertical(Colors.purple_to_blue, "\n[?] Press Enter to exit..."))
    else:
        print(Colorate.Vertical(Colors.purple_to_blue, "\ncancelled!"))

if __name__ == "__main__":
    asyncio.run(main())
