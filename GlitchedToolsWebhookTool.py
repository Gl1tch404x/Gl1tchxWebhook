#Made by Gl1tch : https://github.com/Gl1tch404x

import os
import sys
import json
import time
import requests
import threading
from colorama import Fore, Style, init
init(autoreset=True)
def clear_screen():os.system('cls' if os.name=='nt'else'clear')
def print_logo():
    logo=f"""{Fore.MAGENTA}
 ██████╗ ██╗     ██╗████████╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔════╝ ██║     ██║╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔══██╗
██║  ███╗██║     ██║   ██║   ██║     ███████║█████╗  ██║  ██║
██║   ██║██║     ██║   ██║   ██║     ██╔══██║██╔══╝  ██║  ██║
╚██████╔╝███████╗██║   ██║   ╚██████╗██║  ██║███████╗██████╔╝
 ╚═════╝ ╚══════╝╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝ 
                                                             
████████╗ ██████╗  ██████╗ ██╗     ███████╗                  
╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝                  
   ██║   ██║   ██║██║   ██║██║     ███████╗                  
   ██║   ██║   ██║██║   ██║██║     ╚════██║                  
   ██║   ╚██████╔╝╚██████╔╝███████╗███████║                  
   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝{Style.RESET_ALL}
    {Fore.MAGENTA}Webhook Tool | Made by: Glitched Tools{Style.RESET_ALL}"""
    print(logo)
def validate_webhook(webhook_url):
    if not webhook_url.startswith("https://discord.com/api/webhooks/"):return False
    try:response=requests.get(webhook_url);return response.status_code==200
    except:return False
def get_webhook_info(webhook_url):
    try:
        response=requests.get(webhook_url)
        if response.status_code==200:return response.json()
        else:print(f"{Fore.MAGENTA}Failed to get webhook info. Status code: {response.status_code}{Style.RESET_ALL}");return None
    except Exception as e:print(f"{Fore.MAGENTA}Error: {str(e)}{Style.RESET_ALL}");return None
def display_webhook_info(webhook_url):
    print(f"\n{Fore.MAGENTA}Webhook: {webhook_url}{Style.RESET_ALL}")
    info=get_webhook_info(webhook_url)
    if info:
        print(f"{Fore.MAGENTA}ID:{Style.RESET_ALL} {info.get('id','N/A')}")
        print(f"{Fore.MAGENTA}Name:{Style.RESET_ALL} {info.get('name','N/A')}")
        print(f"{Fore.MAGENTA}Channel ID:{Style.RESET_ALL} {info.get('channel_id','N/A')}")
        print(f"{Fore.MAGENTA}Guild ID:{Style.RESET_ALL} {info.get('guild_id','N/A')}")
        print(f"{Fore.MAGENTA}Token:{Style.RESET_ALL} {info.get('token','N/A')}")
        print(f"{Fore.MAGENTA}URL:{Style.RESET_ALL} {webhook_url}")
def send_webhook_message(webhook_url,content,username=None,avatar_url=None):
    payload={"content":content}
    if username:payload["username"]=username
    if avatar_url:payload["avatar_url"]=avatar_url
    try:response=requests.post(webhook_url,json=payload);return response
    except Exception as e:print(f"{Fore.RED}Error sending message: {str(e)}{Style.RESET_ALL}");return None
def spam_webhook_thread(webhook_url,message,count,username=None,avatar_url=None,thread_id=0):
    sent_count=0;start_time=time.time()
    try:
        while sent_count<count:
            response=send_webhook_message(webhook_url,message,username,avatar_url)
            if response and response.status_code==204:sent_count+=1;print(f"{Fore.GREEN}Message Sent{Style.RESET_ALL}")
            elif response and response.status_code==429:print(f"{Fore.YELLOW}Rate Limited - Not Sent{Style.RESET_ALL}");time.sleep(0.01)
            else:print(f"{Fore.YELLOW}Rate Limited - Not Sent{Style.RESET_ALL}");time.sleep(0.01)
    except KeyboardInterrupt:pass
    except Exception as e:print(f"\n{Fore.MAGENTA}Thread {thread_id} - Error: {str(e)}{Style.RESET_ALL}")
    return sent_count
def spam_multiple_webhooks(webhook_urls):
    clear_screen();print_logo()
    message=input(f"{Fore.MAGENTA}Enter the message to spam: {Style.RESET_ALL}")
    count_input=input(f"{Fore.MAGENTA}Enter the number of messages to send (or 'inf' for infinite): {Style.RESET_ALL}")
    username=input(f"{Fore.MAGENTA}Enter a custom username (or press Enter to skip): {Style.RESET_ALL}")
    avatar_url=input(f"{Fore.MAGENTA}Enter a custom avatar URL (or press Enter to skip): {Style.RESET_ALL}")
    threads_per_webhook=input(f"{Fore.MAGENTA}Enter threads per webhook (default 1): {Style.RESET_ALL}")
    if not message:message="@everyone"
    if count_input.lower()=='inf':count=float('inf')
    else:
        try:count=int(count_input)
        except:count=100
    try:threads_per_webhook=int(threads_per_webhook) if threads_per_webhook else 1
    except:threads_per_webhook=1
    username=username if username else None;avatar_url=avatar_url if avatar_url else None
    print(f"\n{Fore.MAGENTA}Starting spam with {len(webhook_urls)} webhook(s) and {threads_per_webhook} thread(s) per webhook...{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Press Ctrl+C to stop{Style.RESET_ALL}")
    all_threads=[];thread_id=0
    try:
        for webhook_url in webhook_urls:
            for _ in range(threads_per_webhook):
                thread=threading.Thread(target=spam_webhook_thread,args=(webhook_url,message,count,username,avatar_url,thread_id))
                thread.daemon=True;all_threads.append(thread);thread.start();thread_id+=1
        while True:time.sleep(0.01)
    except KeyboardInterrupt:print(f"\n{Fore.MAGENTA}Spam stopped by user. Waiting for threads to finish...{Style.RESET_ALL}")
    print(f"\n{Fore.MAGENTA}Spam completed.{Style.RESET_ALL}")
    input(f"\n{Fore.MAGENTA}Press Enter to return to the main menu...{Style.RESET_ALL}")
def delete_webhook(webhook_url):
    try:
        response=requests.delete(webhook_url)
        if response.status_code==204:print(f"{Fore.MAGENTA}Webhook deleted: {webhook_url}{Style.RESET_ALL}")
        else:print(f"{Fore.MAGENTA}Failed to delete webhook: {webhook_url} - Status code: {response.status_code}{Style.RESET_ALL}")
    except Exception as e:print(f"{Fore.MAGENTA}Error deleting webhook: {webhook_url} - {str(e)}{Style.RESET_ALL}")
def delete_messages(webhook_url):
    clear_screen();print_logo()
    print(f"\n{Fore.MAGENTA}Note: Discord does not provide a direct API to delete multiple webhook messages.{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}You need to know the message ID to delete individual messages.{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}To delete a specific message, you need its ID.{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}You can get message IDs by enabling Developer Mode in Discord and right-clicking on messages.{Style.RESET_ALL}")
    message_id=input(f"\n{Fore.MAGENTA}Enter the message ID to delete (or press Enter to cancel): {Style.RESET_ALL}")
    if not message_id:print(f"\n{Fore.MAGENTA}Message deletion cancelled.{Style.RESET_ALL}");time.sleep(1);return
    try:
        delete_url=f"{webhook_url}/messages/{message_id}";response=requests.delete(delete_url)
        if response.status_code==204:print(f"\n{Fore.MAGENTA}Message deleted successfully!{Style.RESET_ALL}")
        else:print(f"\n{Fore.MAGENTA}Failed to delete message. Status code: {response.status_code}{Style.RESET_ALL}");print(f"{Fore.MAGENTA}Response: {response.text}{Style.RESET_ALL}")
    except Exception as e:print(f"\n{Fore.MAGENTA}Error: {str(e)}{Style.RESET_ALL}")
    input(f"\n{Fore.MAGENTA}Press Enter to return to the main menu...{Style.RESET_ALL}")
def main():
    while True:
        clear_screen();print_logo()
        print(f"\n{Fore.MAGENTA}[1] {Fore.MAGENTA}Spam Webhook{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}[2] {Fore.MAGENTA}Delete Webhook{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}[3] {Fore.MAGENTA}Webhook Info{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}[4] {Fore.MAGENTA}Exit{Style.RESET_ALL}")
        choice=input(f"\n{Fore.MAGENTA}Enter your choice (1-4): {Style.RESET_ALL}")
        if choice=="4":clear_screen();print(f"{Fore.MAGENTA}Thank you for using Adzz Tools! Goodbye!{Style.RESET_ALL}");break
        if choice not in["1","2","3"]:print(f"{Fore.MAGENTA}Invalid choice!{Style.RESET_ALL}");time.sleep(1);continue
        webhooks_input=input(f"\n{Fore.MAGENTA}Enter webhook URL(s) (separate multiple URLs with commas): {Style.RESET_ALL}")
        webhook_urls=[url.strip() for url in webhooks_input.split(',')];valid_webhooks=[]
        for webhook_url in webhook_urls:
            if validate_webhook(webhook_url):valid_webhooks.append(webhook_url)
            else:print(f"{Fore.MAGENTA}Invalid webhook URL skipped: {webhook_url}{Style.RESET_ALL}")
        if not valid_webhooks:print(f"{Fore.MAGENTA}No valid webhook URLs provided!{Style.RESET_ALL}");time.sleep(2);continue
        if choice=="1":spam_multiple_webhooks(valid_webhooks)
        elif choice=="2":
            for webhook_url in valid_webhooks:delete_webhook(webhook_url)
            input(f"\n{Fore.MAGENTA}Press Enter to return to the main menu...{Style.RESET_ALL}")
        elif choice=="3":
            clear_screen();print_logo()
            for webhook_url in valid_webhooks:display_webhook_info(webhook_url)
            input(f"\n{Fore.MAGENTA}Press Enter to return to the main menu...{Style.RESET_ALL}")
if __name__=="__main__":
    try:main()
    except KeyboardInterrupt:clear_screen();print(f"{Fore.GREEN}Program terminated by user. Goodbye!{Style.RESET_ALL}");sys.exit(0)
