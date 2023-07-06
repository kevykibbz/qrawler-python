from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeType, ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException, NoSuchWindowException
import requests
import getpass
import os
import colorama
from datetime import datetime,timedelta, date
from colorama import Fore, Back
import time
import threading
import platform
import random
from art import *
import requests
from packaging import version
import firebase_admin
from firebase_admin import credentials
import time
from firebase_admin import firestore
import calendar
from google.cloud.firestore_v1.base_query import FieldFilter


#init colorama
colorama.init(autoreset=True)

play_sound_script='''
var audio=new Audio("https://firebasestorage.googleapis.com/v0/b/qrawler-10df1.appspot.com/o/sounds%2Fsound.mp3?alt=media&token=00251550-3c24-4668-b3cc-3409d352810a&_gl=1*137jxk9*_ga*MTg2MzkyMjczNS4xNjg1NTE4NjEz*_ga_CW55HF8NVT*MTY4NTUxODYxNS4xLjEuMTY4NTUxOTE5Ny4wLjAuMA..");
audio.play();
'''





#define paramaters
#softwareId = "_softwareId_"
softwareId="PPtn6gcmo0ZA"
server_url=f" https://qrawler.herokuapp.com/process/v1/users/data/{softwareId}"
#server_url=f" https://qrawler.herokuapp.com/process/v1/users/data/PPtn6gcmo0ZA"
software_data_url="https://qrawler.herokuapp.com/process/v1/software/data"
payment_url="https://qrawler.herokuapp.com"
url="https://users.verbit.co/"
#url="https://qrawler.herokuapp.com/dummy"
#softwareVersion = "_softwareVersion_"
softwareVersion = "v1.1.0"

service_account={
    "type": "service_account",
    "project_id": "qrawler-10df1",
    "private_key_id": "69bd324bc8416e6ba266356f4b72545fd637a09b",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDR4HcAmVAR5A5y\n6ujz4gUJa2W8uBXtbNvL1nhhxany4iOlcnPTq+oOrWFn5eQXqRwzJGygtnOeGQ72\nQF6wQObDoTEWnZcH9S2TnFM8DaH9GdjtCDwgEEjel9k4B//we19epdxGwcE2X4hN\n4tXLQ+9OCIZzNj0Ii1WyLfi55TZn5oKDcjOROK5NeprQOIZULah65npWNSsJ88WY\nFzqgNBeO5wVWavit3LnOu9MSRhWProQ6Pglun/+4CKgp7h8AITBNF7AyJU0cnAjh\n2WQH34zmHIT2V7Vg1E/0gqDBaOgaa1gzM4ek1I+9HwBYzV2SV0ixNFTohErJ/QFV\n0Klp4aFPAgMBAAECggEAX/eCkryH11ZvoO53TKVJ5k+8enm2VRVUv7U24IYwusXa\nxNk7y0stwD5Zbte433TNVzlNjoM/BMiyhblTUsaqfkOjnZK7r8DVcUym5qvZKVF7\nVo9QZtzrZRUMF0nZJw5SwoWW3qfUAFfYjLyvQ72xm/3b9KyVZeXIbqwEsoPzx7fU\nTAbM2fs4gOeEZrINbGFUfs5iBCm+w8w4HV/dn4BeNaTZQ/Y6ZoaO+cC0VB63n3Tt\nxNC9sj5ciWIZvk5MmPCxdOCODxJiGa9OxftLTiEYUEfyqUZ9H148tyNpW+HtlrNB\nbDIBaFzj6Nca17x5q8vNGjzMXeXiiu6WQxKY2tjmwQKBgQDw+F6BKXQm/QW7ULRc\nim+N+/QnWPb/m96QxcGcgYdECkIlsbCCxmdtpvNfmCJDNsuI15u6XW6DlewAtihQ\n9a6mlMA0bL5iPtRquVrRezlmqE9rw9zA/5q+9skjZgG/1hHdlUGBgdZvmIOOsR9P\n3Hb/82giWWFtJFaCBIqFTqjJrwKBgQDe9567GoyhHL0ZZh+WshTSYrJiI6260tpf\nkHqMQyty9aWTK6pE3Me2pXvFVcXsE5Dz529Y23WDNXStZP5OqqnxVqn/jfBXxup6\nDduMkN2fQSf+WqE9Xr6RQuKrgJqmGsX82NgIJk4BnROgNKhpcKIca9+rdVxSCOhB\n8wyDLLGqYQKBgQDpG+wYWSjDOsxbq7P/PfCy0wUbN2YiWgAR3yzwISHgwWfCHUYb\nDKIronEXjg2/Jff51lIRFKd/Zf4bphwUTcd54LabQINgeVV2NP9VXTZnR/Uk1CHv\nFpX1nLlxpBGXKhi4WdY32Ym/BTRnSpN251i7PBYF/J9SPO/u8UOruC9ygwKBgA1K\nz9CxtX6JWxCfkPSH60vbjGzjWaEQnuohj9y6yGVTFarfaIgwbUuLNATAp0r6o6KW\nwoGWm7vVvP31Tl/cNsNnejz89j4VYrciClun6z5qQPsd5gzlkBDS3vaAdTe/0tvP\nBZn+xpm8BoZ/fSbECzYMjEoJdhaB526/EZjkWjchAoGBAIUo+LdFqqo1mGgWcWm7\nkYVuY+YQsNxvWtkGzahr/oahM2zJzl97dGWxlv70RyqjxcYs1wMMdB5/kvXM61mj\nkNC0pTleqqk35ePeRDp3YLZHl9d9+uYkCae6aZa/KbTqzjT9xYlwCN0yNN/HAzHb\n9S8Tmt1d36/ewWK92v5CDQEN\n-----END PRIVATE KEY-----\n",
    "client_email": "qrawler-10df1@appspot.gserviceaccount.com",
    "client_id": "108122578014145372021",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/qrawler-10df1%40appspot.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

#Initialize Firebase Admin SDK
cred = credentials.Certificate(service_account)  
firebase_admin.initialize_app(cred, {'storageBucket': 'qrawler-10df1.appspot.com'})
    
class Qrawler:
    def __init__(self):
        self.retry_attempts=10
        self.attempt=1
        self.delay=1
        self.retry_delay = 2
        self.retry_count = 2
        self.has_internet_connection=False
        self.should_quit=False
        self.driver = None
        self.name=""
        self.terminate=False
        self.email=None
        self.password=None
        self.package=None
        self.userId=None
        self.start_time = time.time()
        self.db = firestore.client()
        self.latest_version=None
        self.downloads=None
        self.softwareVersion=softwareVersion.split("v")[1]
        self.has_chrome_opened=False
        self.refresh_interval=3
        self.min_refresh_speed=3
        self.max_refresh_speed=5
        self.min_delay=4
        self.max_delay=6
        #get os name
        self.os_name=platform.system()
        
        # Clear the CMD screen
        os.system('cls' if os.name == 'nt' else 'clear')
        print()
        text = text2art(" QRAWLER")
        print(text)
        print(f" DEVELOPED BY {Back.GREEN} DEVME TECHNOLOGIES {Fore.RESET}")
        print(f" EMAIL:{Fore.CYAN}KIBEBEKEVIN@GMAIL.COM{Fore.RESET}{Fore.BLUE}")
        print(f" PHONE:{Fore.CYAN}0796268817{Fore.RESET}")
        print("\n")
        print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Initializing qrawler...{Fore.RESET}\n",end="")
        print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Checking internet connectivity...\n",end="")
      
    
   
    
   
    def get_timestamp(self):
        return datetime.now().strftime('%H:%M:%S')
    
          
    #start keyboard listener
    def start_keyboard_listener(self):
        keyboard_thread = threading.Thread(target=self.keyboard_listener)
        keyboard_thread.daemon = True
        keyboard_thread.start()
        
        
    
    def keyboard_listener(self):
        while True:
            key = input(" Press Q/q to quit the script.\n")
            if key.lower() == 'q':
                self.should_quit = True
                self.quit_driver()
                break
    
    
    def check_internet_connection(self):
        try:
            response = requests.get("https://www.google.com", timeout=5)
            return True
        except (requests.exceptions.RequestException, requests.exceptions.Timeout):
            return False 
        
    
    def quit_driver(self, close_chrome=True):
        print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Shutting down...{Fore.RESET}\n", end="")
        elapsed_time = time.time() - self.start_time
        elapsed_hours = elapsed_time / 3600  # Convert to hours
    
        if close_chrome and self.driver:
            try:
                # Set the users collection with document ID of 1234
                users_ref = self.db.collection('users').document(self.userId)
                users_data = users_ref.get().to_dict()
                users_total_time = users_data.get('total_time', 0) + elapsed_hours
                users_ref.set({'ElapsedTime': users_total_time}, merge=True)
                if self.userId:
                    self.update_user_status("stopped") 
                    print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Status updated [Stpped]...{Fore.RESET}\n",end="")
                self.should_quit = True
                self.driver.quit()
                print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.GREEN} Qrawler ran for {elapsed_hours:.2f} hours.{Fore.RESET}\n", end="")
                print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.GREEN} Qrawler shutdown successfully. Goodbye {self.name }{Fore.RESET}\n", end="")
            except Exception as e:
                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.RED} Error shutting Qrawler down.{Fore.RESET}\n", end="")
        else:
            self.should_quit = True
            print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.GREEN} Qrawler ran for {elapsed_hours:.2f} hours.{Fore.RESET}\n", end="")
            print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.GREEN} Qrawler shutdown successfully. Goodbye {self.name}{Fore.RESET}\n", end="")
    
    
    
    def get_greeting(self):
        currentTime = datetime.now()
        currentTime.hour
        if currentTime.hour < 12:
            return 'Good morning'
        elif 12 <= currentTime.hour < 18:
            return 'Good afternoon'
        else:
            return 'Good evening'
       
       
    def get_credentials(self,url):
        response=requests.get(url)
        response.raise_for_status()
        data=response.json()
        userId=data["UserId"]
        package=data["Package"]
        name=data["FirstName"]
        transactionDate=data["TransactionDate"]
        email=data["VerbitEmail"]
        terminate=data["TerminateProcess"]
        password=data['VerbitPassord']
        status=data["IsAccountActive"]
        expiry_days=data["ExpiryDays"]
        refresh_interval=data["RefreshSpeed"]
        dateJoined=data["DateJoined"]
        seconds = dateJoined['_seconds']
        nanoseconds = dateJoined['_nanoseconds']

        # Create a datetime object by adding seconds and nanoseconds to the epoch time
        epoch = datetime(1970, 1, 1)
        delta = timedelta(seconds=seconds, microseconds=nanoseconds // 1000)
        date = epoch + delta
        
        
        if refresh_interval <=1:
            self.min_refresh_speed=1
            self.max_refresh_speed=3
        else:
            self.min_refresh_speed=refresh_interval
            self.max_refresh_speed=refresh_interval +2
        refresh_interval=random.randint(self.min_refresh_speed,self.max_refresh_speed)
        return userId,name,email,password,status,refresh_interval,date,expiry_days,terminate,package,transactionDate
     
    
    def get_todays_date(self):
        return date.today()
    
    def init_user(self):
        if self.check_internet_connection():
            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Acquaring user credentials...{Fore.RESET}\n",end="")
            try:
                userId,name,email, password, status, refresh_interval,date,expiry_days,terminate,package,transactionDate = self.get_credentials(server_url)
                self.name=name.capitalize()
                self.email=email
                self.terminate=terminate
                self.password=password
                self.userId=userId
                self.package=package
                print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.GREEN} User credentials found.{Fore.RESET}\n",end="")
                print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.GREEN} {self.get_greeting()} {self.name}.{Fore.RESET}\n",end="")
                if self.userId:
                    self.update_user_status("running") 
                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Status updated [Running]...{Fore.RESET}\n",end="")
                print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.CYAN} Package type [{self.package}].{Fore.RESET}\n",end="")   
                 
                if not self.can_terminate():
                    # Convert to datetime
                    start_datetime = datetime.utcfromtimestamp(0)
                    duration_datetime = start_datetime + timedelta(seconds=transactionDate["_seconds"], microseconds=transactionDate["_nanoseconds"] / 1000)

                    # Get current datetime
                    current_datetime = datetime.utcnow()

                    # Calculate duration in days
                    days = (current_datetime - duration_datetime).days
                    # Extract the current month and year
                    current_month = current_datetime.month
                    current_year = current_datetime.year

                    # Get the number of days in the current month
                    num_days = calendar.monthrange(current_year, current_month)[1]
                
                
                    if not status:
                        print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Account status [inactive].{Fore.RESET}\n",end="")
                        if "Free Version" in self.package:
                            #free version
                            #Calculate the difference in days
                            specific_date = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S.%f').date()
                            days_passed = (self.get_todays_date() - specific_date).days
                            if days_passed > expiry_days:
                                users_ref = self.db.collection('users').document(self.userId)
                                users_data = users_ref.get().to_dict()
                                users_ref.set({'FreeTrialExpired': True,}, merge=True)
                                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.CYAN} Your free trial of {expiry_days} days has expired.{Fore.RESET}\n",end="") 
                                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Redirecting to payment page ...{Fore.RESET}\n",end="")
                                self.redirect_to_payments()
                                self.quit_driver(close_chrome=False)
                                return
                            else:
                                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.CYAN} Your are in free trial of {expiry_days} days will expire after {expiry_days-days_passed} days.{Fore.RESET}\n",end="")
                                self.init_software_data()  
                        else:
                        #not free version
                            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Package[{self.package}] has expired.Kindly renew.{Fore.RESET}\n",end="")
                            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Redirecting to payment page ...{Fore.RESET}\n",end="")
                            self.redirect_to_payments()
                            self.quit_driver(close_chrome=False)
                            return
                    else:   
                        #account is active  
                        print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Account status [active].{Fore.RESET}\n",end="")   
                        if days > num_days:
                            users_ref = self.db.collection('users').document(self.userId)
                            users_data = users_ref.get().to_dict()
                            users_ref.set({'IsAccountActive': False,'HasPaid':False}, merge=True)
                            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Package[{self.package}] has expired.Kindly renew.{Fore.RESET}\n",end="")
                            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Redirecting to payment page ...{Fore.RESET}\n",end="")
                            self.redirect_to_payments()
                            self.quit_driver(close_chrome=False)
                            return
                        else:
                            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Your package[{self.package}] will expire after {num_days-days} days.{Fore.RESET}\n",end="")
                            self.init_software_data()  
                else:
                    print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Process terminated...{Fore.RESET}\n",end="")
                    self.quit_driver() 
            except Exception as e:
                print("error:",e)
                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.RED} Error acquiring credentials.{Fore.RESET}\n", end="")
                self.quit_driver()
                return
        else:
            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} No internet connection.Retrying to connect...{Fore.RESET}\n",end="")
            time.sleep(self.delay)  
            self.attempt +=1
            self.delay *=2 
            if self.should_quit:
                return
                
          
    
              
    def can_terminate(self):
        # Select the "users" collection and query for the document with ID 1234
        users_ref = self.db.collection('users')
        query = users_ref.where(filter=FieldFilter('UserId', '==', self.userId))
        results = query.get()

        # Retrieve the email if the document exists
        for doc in results:
            self.terminate = doc.get('TerminateProcess')
            break 
        else:
            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.RED} Something went wrong.{Fore.RESET}\n",end="")
            self.quite_driver()
        return  self.terminate
        
    
    
    def get_software_data(self,url):
        response=requests.get(url)
        response.raise_for_status()
        data=response.json()
        version=data["Version"]
        year_created=data["DateCreated"]
        downloads=data["Downloads"]
        return version,downloads,year_created
    
    
    def compare_versions(self,v1, v2):
        version1 = version.parse(v1)
        version2 = version.parse(v2)

        return version1 == version2
    
    
    
    def redirect_to_payments(self):
        if self.check_internet_connection():
            if not self.can_terminate():
                for retry_count in range(1, self.retry_attempts+1): 
                    if self.should_quit and self.driver and self.has_chrome_opened:
                        self.quit_driver()
                        break
                    
                    try:
                        # Set up the ChromeDriver service
                        service = Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())
                        options=self.setup_option()
                        if not self.has_chrome_opened:
                            self.driver = webdriver.Chrome(service=service, options=options) 
                            current_version = self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
                            latest_version = self.driver.capabilities['browserVersion']
                            if current_version.split('.')[0] != latest_version.split('.')[0]:
                                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Current driver version {current_version}.Latest driver version {latest_version}.{Fore.RESET}\n", end="")
                                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Downloading latest version...{Fore.RESET}\n", end="")
                            else:
                                self.has_chrome_opened=True
                                print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.GREEN} Chrome browser opened successfully.{Fore.RESET}\n",end="")
                                self.driver.get(payment_url)
                        break
                    
                    
                    except WebDriverException:
                        print(Fore.MAGENTA + f" [+] {self.get_timestamp()}-> {Fore.RESET}{Fore.YELLOW}Failed to open Chrome.Retrying ({self.attempt}/{self.retry_attempts})...{Fore.RESET}\n", end="")
                        self.has_chrome_opened=False
                        if self.retry_count < self.retry_attempts:
                            time.sleep(self.retry_delay)
                            self.retry_delay *= 2  # Increase the retry delay exponentially
                            if self.should_quit:
                                break
                        else:
                            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Maximum number of retries reached.{Fore.RESET}\n", end="")
                            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Unable to open Chrome.{Fore.RESET}\n", end="")
                            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Shutting down...{Fore.RESET}\n", end="")
                            break 
            else:
                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Process terminated...{Fore.RESET}\n",end="")
                self.quit_driver() 
        else:
            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} No internet connection.Retrying to connect...{Fore.RESET}\n",end="")
            time.sleep(self.delay)  
            self.attempt +=1
            self.delay *=2 
            if self.should_quit:
                return
            
       
       
            
    def init_software_data(self):
        if self.check_internet_connection():
            if not self.can_terminate():
                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Checking software version...{Fore.RESET}\n", end="") 
                try:
                    version,downloads,duration=self.get_software_data(software_data_url)
                    self.latest_version=version.split("v")[1]
                    self.downloads=downloads
                    # Convert to datetime
                    start_datetime = datetime.utcfromtimestamp(0)
                    duration_datetime = start_datetime + timedelta(seconds=duration["_seconds"], microseconds=duration["_nanoseconds"] / 1000)

                    # Get current datetime
                    current_datetime = datetime.utcnow()

                    # Calculate duration in years
                    years = (current_datetime - duration_datetime).days / 365.25

                    print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.GREEN} Software data acquired.{Fore.RESET}\n",end="")
                    if years > 1:
                        print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Celebrating {years} years of service with over {self.downloads}+ downloads.{Fore.RESET}\n",end="")
                    
                    
                    if self.compare_versions(self.softwareVersion,self.latest_version):
                        print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Software version {self.softwareVersion}[Latest version].{Fore.RESET}\n", end="") 
                        print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Attempting to open chrome browser...{Fore.RESET}\n", end="") 
                        self.open_chrome()
                    else:
                        print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Software version v{self.softwareVersion}[Old version].{Fore.RESET}\n", end="")        
                        print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.CYAN} Kindly update to latest software version.Latest version is v{self.latest_version}.{Fore.RESET}\n", end="")        
                        self.quit_driver() 

                except Exception as e:
                    print("error:",e)
                    print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.RED} Error acquiring software data.{Fore.RESET}\n", end="")
                    self.quit_driver()
                    return
            else:
                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Process terminated...{Fore.RESET}\n",end="")
                self.quit_driver() 
        else:
            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} No internet connection.Retrying to connect...{Fore.RESET}\n",end="")
            time.sleep(self.delay)  
            self.attempt +=1
            self.delay *=2 
            if self.should_quit:
                return
    
    
    def setup_option(self):
        # Create ChromeOptions object
        options = Options()
        options.add_argument("--disable-infobars")
        options.add_argument("--profile-directory=Default") 
        options.add_argument("--start-maximized") 
        options.add_argument("--user-data=dir=C:\\Users\\San\\AppData\\Local\\Google\\Chrome\\User Data\\")
        options.add_experimental_option("detach",True)  
        return options
    
    
    def open_chrome(self):
        if self.check_internet_connection():
            if not self.can_terminate():
                for retry_count in range(1, self.retry_attempts+1): 
                    if self.should_quit and self.driver and self.has_chrome_opened:
                        self.quit_driver()
                        break
                    
                    try:
                        # Set up the ChromeDriver service
                        service = Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())
                        options=self.setup_option()
                        if not self.has_chrome_opened:
                            self.driver = webdriver.Chrome(service=service, options=options) 
                            current_version = self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
                            latest_version = self.driver.capabilities['browserVersion']
                            if current_version.split('.')[0] != latest_version.split('.')[0]:
                                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Current driver version {current_version}.Latest driver version {latest_version}.{Fore.RESET}\n", end="")
                                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Downloading latest version...{Fore.RESET}\n", end="")
                            else:
                                self.has_chrome_opened=True
                                print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.GREEN} Chrome browser opened successfully.{Fore.RESET}\n",end="")
                                self.login()
                        break
                    
                    
                    except WebDriverException:
                        print(Fore.MAGENTA + f" [+] {self.get_timestamp()}-> {Fore.RESET}{Fore.YELLOW}Failed to open Chrome.Retrying ({self.attempt}/{self.retry_attempts})...{Fore.RESET}\n", end="")
                        self.has_chrome_opened=False
                        if self.retry_count < self.retry_attempts:
                            time.sleep(self.retry_delay)
                            self.retry_delay *= 2  # Increase the retry delay exponentially
                            if self.should_quit:
                                break
                        else:
                            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Maximum number of retries reached.{Fore.RESET}\n", end="")
                            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Unable to open Chrome.{Fore.RESET}\n", end="")
                            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Shutting down...{Fore.RESET}\n", end="")
                            break 
            else:
                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Process terminated...{Fore.RESET}\n",end="")
                self.quit_driver() 
        else:
            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} No internet connection.Retrying to connect...{Fore.RESET}\n",end="")
            time.sleep(self.delay)  
            self.attempt +=1
            self.delay *=2 
            if self.should_quit:
                return
      
      
      
      
      
    def login(self):
        if self.check_internet_connection():
            if not self.can_terminate():
                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Redirecting to verbit.co...{Fore.RESET}\n",end="")
                self.driver.get(url)
                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Attempting to login...{Fore.RESET}\n",end="")
                #locate and fill the login form
                try:
                    #explicit wait
                    wait=WebDriverWait(self.driver,10)
                    print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Inputting email...{Fore.RESET}\n",end="")
                    email_field = self.driver.find_element(By.XPATH, "//input[@name='email']")
                    email_field.send_keys(self.email)
                    print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.GREEN} Done.{Fore.RESET}\n",end="")
                    # Locate the button by its text using XPath
                    next_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Next')]")

                    # Click on the button
                    next_button.click()

                
                    password_field=wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@type='password']")))
                    print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Inputting password...{Fore.RESET}\n",end="")
                    password_field.send_keys( self.password)
                    print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.GREEN} Done.{Fore.RESET}\n",end="")
                    print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Authenticating...{Fore.RESET}\n",end="")
                    #Locate the button by its text using XPath
                    login_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Login')]")
                    #Click on the button
                    login_button.click()
                    
                    #error = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "p")))
                    try:
                        login = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[@class='title' and contains(text(), 'My files')]")))
                        if login:
                            print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.GREEN} Logged in successfully.{Fore.RESET}\n",end="")
                            self.claim_job()
                    except NoSuchElementException as e:
                        pass

                except Exception as e:
                    page_source=self.driver.page_source
                    verification_text="Enter verification code"
                    error_text="Incorrect username or password"
                    #verification_text = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[@class='fWwCIu' and contains(text(), 'Enter verification code')]")))
                    #error = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "p")))
                    if verification_text in page_source:
                        print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Kindly login in some other tab before using this script...{Fore.RESET}\n",end="")
                    elif error_text in page_source:
                        print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.RED} Authentication failed.Either email address provided or password is incorrect.{Fore.RESET}\n",end="")
                    else:
                        print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Cant load webpage correctly...{Fore.RESET}\n",end="")
                    self.quit_driver()
            else:
                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Process terminated...{Fore.RESET}\n",end="")
                self.quit_driver() 
        else:
            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} No internet connection.Retrying to connect...{Fore.RESET}\n",end="")
            time.sleep(self.delay)  
            self.attempt +=1
            self.delay *=2 
            if self.should_quit:
                return
            
         
         
    def claim_job(self):
        if self.check_internet_connection():
            if not self.can_terminate():
                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Fetching jobs...{Fore.RESET}\n",end="")
                while True:
                    time.sleep(self.refresh_interval)
                    self.driver.refresh()
                

                    if self.should_quit:
                        break
            
                    try:
                        #wait for links
                        wait=WebDriverWait(self.driver,self.refresh_interval)
                        link_elements=wait.until(EC.presence_of_all_elements_located((By.XPATH,"//a[@class='link-class']")))

                        #randomize the links
                        random.shuffle(link_elements)
                        for link in link_elements:
                            if self.os_name == "Windows" or self.os_name == "Linux":
                                # Add target="_blank" attribute to open the link in a new tab
                                self.driver.execute_script('arguments[0].setAttribute("target", "_blank");', link)
                                link.send_keys(Keys.CONTROL + Keys.RETURN)
                            else:
                                # For macOS, use the "Command" key while clicking the link to open it in a new tab
                                actions = ActionChains(self.driver)
                                actions.key_down(Keys.COMMAND).click(link).key_up(Keys.COMMAND).perform()

                            self.driver.execute_script(play_sound_script)  
                            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.GREEN} Job claimed!{Fore.RESET}\n")
                            
                            time.sleep(random.randint(self.min_delay, self.max_delay))
                        
                        time.sleep(random.randint(self.min_delay, self.max_delay))
                                        
                            
                    except (NoSuchElementException, NoSuchWindowException):
                        print(
                            f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.RED} Element not found!{Fore.RESET}\n",
                            end="")
                        continue
                    #wait  for specified refresh interval
                    self.driver.implicitly_wait(self.refresh_interval)
            else:
                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} Process terminated...{Fore.RESET}\n",end="")
                self.quit_driver() 
        else:
            print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} No internet connection.Retrying to connect...{Fore.RESET}\n",end="")
            time.sleep(self.delay)  
            self.attempt +=1
            self.delay *=2 
            if self.should_quit:
                return
            
    def update_user_status(self, status):
        # Assuming you have a reference to the users collection
        user_ref = self.db.collection('users').document(self.userId)

        # Update the status field with the provided status
        user_ref.update({'SoftwareStatus': status})
        
        
                    
    def run_operations(self):
        self.start_keyboard_listener()
        while not self.should_quit:     
            if not self.has_internet_connection and self.check_internet_connection():
                print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.GREEN} Connected.{Fore.RESET}\n",end="")
                self.init_user()
                self.has_internet_connection = True
                continue
            
            
            if self.should_quit:
                break
            
            if not self.check_internet_connection():
                self.has_internet_connection = False
                print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.YELLOW} No internet connection.{Fore.RESET}\n",end="")
                for retry_count in range(1, self.retry_attempts+1):
                    if self.check_internet_connection():
                        print(f" {Fore.GREEN}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.GREEN} Connected.{Fore.RESET}\n",end="")
                        self.init_user()
                        self.has_internet_connection = True
                        break
                    else:
                        print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Retrying in {self.retry_delay} seconds.Attempts ({retry_count}/{self.retry_attempts})...{Fore.RESET}\n",end="")
                        time.sleep(self.retry_delay)
                        self.retry_delay *= 2  # Increase the retry delay exponentially
                        if self.should_quit:
                            break
                else:
                    print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Maximum number of retries reached.{Fore.RESET}\n",end="")
                    print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} No Internet connection.{Fore.RESET}\n",end="")
                    print(f" {Fore.MAGENTA}[+]{self.get_timestamp()}->{Fore.RESET}{Fore.BLUE} Shutting down...{Fore.RESET}\n",end="")
                    self.should_quit=True
                    break
           


qrawler=Qrawler()
qrawler.run_operations()