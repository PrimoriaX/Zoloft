import os
from colorama import Fore, Back, Style
from zoloft import Zoloft

def run():
    startup()
    prints()
    Zoloft().start()

def startup():
    os.system("color")
    os.system(f"title Zoloft")

def prints():
    ascii_art = """
                                           @@@@@@
                                       @@@@@@@@@@@@
                                     @@@@@@@@@@@@@@@@
                                    @@@@@@@@@@@@@@@@@@
                                   @@@@@@@@@@@@@@@@@@@@@
                                    @@@@@@@@@@@@@@@@@@@@@@@
                                     @@@@@@@@@@@@@@@@@@@######
                                     @@@@@@@@@@@@@@@@##########
                                       @@@@@@@@@@@@##############
                                         @@@@@@@@@#################
                                           @@@@@@####################
                                             @@@#######################
                                                 ########################
                                                  ######################
                                                    ###################
                                                      ###############
                                                        ###########
                                                          #######
                                            ·▄▄▄▄•      ▄▄▌        ·▄▄▄▄▄▄▄▄
                                            ▪▀·.█▌▪     ██•  ▪     ▐▄▄·•██  
                                            ▄█▀▀▀• ▄█▀▄ ██▪   ▄█▀▄ ██▪  ▐█.▪
                                            █▌▪▄█▀▐█▌.▐▌▐█▌▐▌▐█▌.▐▌██▌. ▐█▌·
                                            ·▀▀▀ • ▀█▄▀▪.▀▀▀  ▀█▄▀▪▀▀▀  ▀▀▀ 
    """
    ascii_art = ascii_art.replace("@", f"{Fore.CYAN}@{Style.RESET_ALL}").replace(".", f"{Fore.WHITE}.{Style.RESET_ALL}")
    support_discord = f"{Fore.LIGHTBLACK_EX}\t\t\t  [{Fore.CYAN}x{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL} Join our support discord server: {Fore.CYAN}discord.gg/hPwRBpAZcr   {Style.RESET_ALL}"
    
    print(ascii_art)
    print(support_discord)
    
run()
