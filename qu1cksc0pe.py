#!/usr/bin/env python3

import os,sys,argparse
# Colors
red = '\u001b[91m'
cyan = '\u001b[96m'
white = '\u001b[0m'
green = '\u001b[92m'

banner='''
  ██████╗ ██╗   ██╗ ██╗ ██████╗██╗  ██╗███████╗ ██████╗ ██████╗ ██████╗ ███████╗
 ██╔═══██╗██║   ██║███║██╔════╝██║ ██╔╝██╔════╝██╔════╝██╔═████╗██╔══██╗██╔════╝
 ██║   ██║██║   ██║╚██║██║     █████╔╝ ███████╗██║     ██║██╔██║██████╔╝█████╗  
 ██║▄▄ ██║██║   ██║ ██║██║     ██╔═██╗ ╚════██║██║     ████╔╝██║██╔═══╝ ██╔══╝  
 ╚██████╔╝╚██████╔╝ ██║╚██████╗██║  ██╗███████║╚██████╗╚██████╔╝██║     ███████╗
  ╚══▀▀═╝  ╚═════╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚══════╝
                                                                               
  >>> Quick suspicious file analysis tool.
  ----------------------------------------
  >>> By CYB3RMX_   | Version: 1.4
  ----------------------------------------

'''
args = []
def scope():
   # Category arrays 
   regs = []
   fils = []
   netw = []
   web = [] 
   keys = []
   proc = []
   dll = []
   debg = []
   sysp = []
   como = []
   leak = []
   othe = []

   # Argument crating and parsing
   parser = argparse.ArgumentParser()
   parser.add_argument("-f", "--file",required=False,help="Select a suspicious file.")
   parser.add_argument("-c", "--category",required=False,help="Scan for specified category.")
   parser.add_argument("--install",required=False,help="Install Qu1cksc0pe.",action="store_true")
   parser.add_argument("--metadata",required=False,help="Get exif information.",action="store_true")
   parser.add_argument("--vtscan",required=False,help="Scan with VirusTotal api.",action="store_true")
   parser.add_argument("--dll",required=False,help="Look for used DLL files.",action="store_true")
   parser.add_argument("--key_init",required=False,help="Enter your VirusTotal api key.",action="store_true")
   args = parser.parse_args()

   # Getting all strings from the file
   if args.file:
       command = "strings {} > temp.txt".format(args.file)
       os.system(command)
       allStrings = open("temp.txt", "r").read().split('\n')

   # Configuring the arguments
   if args.install:
       command = "cp qu1cksc0pe.py qu1cksc0pe; chmod +x qu1cksc0pe; sudo mv qu1cksc0pe /usr/bin/"
       os.system(command)
       print("[+] Installed.")
       sys.exit(0)
   if args.metadata:
       print("{}[{}+{}]{} Exif/Metadata information".format(cyan,red,cyan,white))
       command = "exiftool {}".format(args.file)
       print("+","-"*50,"+")
       os.system(command)
       print("+","-"*50,"+")
   if args.vtscan:
       try:
           apik = open(".apikey.txt", "r").read().split("\n")
       except:
           print("{}[{}!{}]{} Use --key_init to enter your key.".format(cyan,red,cyan,white))
           sys.exit(1)
       if apik[0] == '' or apik[0] == None or len(apik[0]) != 64:
           print("{}[{}!{}]{} Please get your api key from -> {}https://www.virustotal.com/{}".format(cyan,red,cyan,white,green,white))
           sys.exit(1)
       else: 
           print("\n{}[{}+{}]{} VirusTotal Scan".format(cyan,red,cyan,white))
           print("+","-"*50,"+")
           command = "python3 VTwrapper.py {} {}".format(apik[0], args.file)
           os.system(command)
           print("+","-"*50,"+")
   if args.key_init:
       apikey = str(input("{}[{}+{}]{} Enter your VirusTotal api key: ".format(cyan,red,cyan,white)))
       command = "echo '{}' > .apikey.txt".format(apikey)
       os.system(command)
       print("{}[{}+{}]{} Your VirusTotal api key saved.".format(cyan,red,cyan,white))
   if args.dll:
       dllArray = ["KERNEL32.DLL","ADVAPI32.dll","WSOCK32.dll","WS2_32.dll",
                   "MSVCRT.dll","ntdll.dll","Advapi32.dll","shell32.dll",
                   "msimsg.dll","ole32.dll","SHELL32.dll","WININET.dll",
                   "USER32.dll","COMCTL32.dll","VERSION.dll","KERNEL32.dll",
                   "OLEAUT32.dll","SHLWAPI.dll","GDI32.dll","WINTRUST.dll",
                   "CRYPT32.dll","msi.dll","user32.dll","MSVBVM60.DLL","msvbvm60.dll",
                   "VBA6.DLL", "vba6.dll"]
       print("{}[{}+{}]{} Used DLL files".format(cyan,red,cyan,white))
       print("+","-"*20,"+")
       for dl in allStrings:
           if dl in dllArray:
               print("{}=> {}{}".format(red,white,dl))
       print("+","-"*20,"+\n")

   # Keywords for categorized scanning    
   regdict={
      "Registry": ["RegKeyOpen","RegOpenKeyExA","RegQueryValueExA","RegSetValue","RegGetValue","RtlWriteRegistryValue","RtlCreateRegistryKey","RegQueryValueExW","RegCloseKey","RegCreateKeyExW","RegSetValueExW"],
      "File": ["CreateFile","ReadFile","WriteFile","FindResource","FindResourceW","LoadResource","FindFirstFile","FindNextFile","NtQueryDirectoryFile","CreateFileMapping","MapViewOfFile","GetTempPath","SetFileTime","SfcTerminateWatcherThread"],
      "Network": ["WSAStartup","WSAGetLastError","socket","recv","connect","getaddrinfo","accept","send","listen"],
      "Web": ["InternetOpen","InternetOpenURL","InternetConnect","InternetReadFile","InternetWriteFile","HTTPOpenRequest","HTTPSendRequest","HTTPQueryInfo","URLDownloadToFile"],
      "Keyboard/Keylogger": ["GetKeyboardType","SetWindowsHook","CallNextHook","MapVirtualKey","GetKeyState","GetAsyncKeyState","GetForegroundWindow","AttachThreadInput","RegisterHotKey"],
      "Process": ["CreateProcess","VirtualAlloc","VirtualProtect","OpenProcess","EnumProcesses","EnumProcessModules","CreateRemoteThread","WriteProcessMemory","AdjustTokenPrivileges","IsWow64Process","QueueUserAPC","NtSetInformationProcess","GetProcAddress","ExitProcess"],
      "Dll": ["LoadLibrary","LoadLibraryExA","LoadLibraryA", "LdrLoadDll","DllFunctionCall"],
      "DebuggerIdentifying": ["IsDebuggerPresent","CheckRemoteDebuggerPresent","FindWindow","GetTickCount","NtQueryInformationProcess","OutputDebugString","OutputDebugStringA"],
      "SystemPersistence": ["CreateService","ControlService"],
      "COMObject": ["OleInitialize","CoInitialize"],
      "DataLeakage": ["LsaEnumerateLogonSessions","SamIConnect","SamIGetPrivateData","SamQueryInformationUse","NetShareEnum","ReadProcessMemory","Toolhelp32ReadProcessMemory"],
      "Other": ["CreateMutex","ShellExecute","WinExec","System","CryptAcquireContext","EnableExecuteProtectionSupport","GetSystemDefaultLangId","StartServiceCtrlDispatcher","IsNTAdmin","IsUserAnAdmin"]
   }
   if args.category.lower() == 'registry':
       for categ in regdict['Registry']:
           if categ in allStrings:
               regs.append(categ)
       if regs != []:
           print("{}[{}+{}]{} Registry operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in regs:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       else:
           print("{}[{}!{}]{} Nothing found.".format(cyan,red,cyan,white))
   elif args.category.lower() == 'file':
       for categ in regdict['File']:
           if categ in allStrings:
               fils.append(categ)
       if fils != []:
           print("{}[{}+{}]{} File operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in fils:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       else:
           print("{}[{}!{}]{} Nothing found.".format(cyan,red,cyan,white))
   elif args.category.lower() == 'network':
       for categ in regdict['Network']:
           if categ in allStrings:
               netw.append(categ)
       if netw != []:
           print("{}[{}+{}]{} Network operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in netw:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       else:
           print("{}[{}!{}]{} Nothing found.".format(cyan,red,cyan,white))
   elif args.category.lower() == 'web':
       for categ in regdict['Web']:
           if categ in allStrings:
               web.append(categ)
       if web != []:
           print("{}[{}+{}]{} Web operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in web:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       else:
           print("{}[{}!{}]{} Nothing found.".format(cyan,red,cyan,white))
   elif args.category.lower() == 'keylogger':
       for categ in regdict['Keyboard/Keylogger']:
           if categ in allStrings:
               keys.append(categ)
       if keys != []:
           print("{}[{}+{}]{} Keyboard/Keylogger operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in keys:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       else:
           print("{}[{}!{}]{} Nothing found.".format(cyan,red,cyan,white))
   elif args.category.lower() == 'process':
       for categ in regdict['Process']:
           if categ in allStrings:
               proc.append(categ)
       if proc != []:
           print("{}[{}+{}]{} Process operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in proc:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       else:
           print("{}[{}!{}]{} Nothing found.".format(cyan,red,cyan,white))
   elif args.category.lower() == 'dll':
       for categ in regdict['Dll']:
           if categ in allStrings:
               dll.append(categ)
       if dll != []:
           print("{}[{}+{}]{} DLL operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in dll:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       else:
           print("{}[{}!{}]{} Nothing found.".format(cyan,red,cyan,white))
   elif args.category.lower() == 'debugger':
       for categ in regdict['DebuggerIdentifying']:
           if categ in allStrings:
               debg.append(categ)
       if debg != []:
           print("{}[{}+{}]{} Debugger Identifying operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in debg:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       else:
           print("{}[{}!{}]{} Nothing found.".format(cyan,red,cyan,white))
   elif args.category.lower() == 'persistence':
       for categ in regdict['SystemPersistence']:
           if categ in allStrings:
               sysp.append(categ)
       if sysp != []:
           print("{}[{}+{}]{} System Persistence operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in regs:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       else:
           print("{}[{}!{}]{} Nothing found.".format(cyan,red,cyan,white))
   elif args.category.lower() == 'comobject':
       for categ in regdict['COMObject']:
           if categ in allStrings:
               como.append(categ)
       if como != []:
           print("{}[{}+{}]{} COM Object operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in como:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       else:
           print("{}[{}!{}]{} Nothing found.".format(cyan,red,cyan,white))
   elif args.category.lower() == 'dataleak':
       for categ in regdict['DataLeakage']:
           if categ in allStrings:
               leak.append(categ)
       if leak != []:
           print("{}[{}+{}]{} Data Leakage operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in leak:
              print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       else:
           print("{}[{}!{}]{} Nothing found.".format(cyan,red,cyan,white))
   elif args.category.lower() == 'other':
       for categ in regdict['Other']:
           if categ in allStrings:
               othe.append(categ)
       if othe != []:
           print("{}[{}+{}]{} Other operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in othe:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       else:
           print("{}[{}!{}]{} Nothing found.".format(cyan,red,cyan,white))
   
   elif args.category.lower() == 'all':
       for categ in regdict['Registry']:
           if categ in allStrings:
               regs.append(categ)
       if regs != []:
           print("\n{}[{}+{}]{} Registry operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in regs:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       for categ in regdict['File']:
           if categ in allStrings:
               fils.append(categ)
       if fils != []:
           print("\n{}[{}+{}]{} File operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in fils:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       for categ in regdict['Network']:
           if categ in allStrings:
               netw.append(categ)
       if netw != []:
           print("\n{}[{}+{}]{} Network operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in netw:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       for categ in regdict['Web']:
           if categ in allStrings:
               web.append(categ)
       if web != []:
           print("\n{}[{}+{}]{} Web operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in web:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       for categ in regdict['Keyboard/Keylogger']:
           if categ in allStrings:
               keys.append(categ)
       if keys != []:
           print("\n{}[{}+{}]{} Keyboard/Keylogger operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in keys:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       for categ in regdict['Process']:
           if categ in allStrings:
               proc.append(categ)
       if proc != []:
           print("\n{}[{}+{}]{} Process operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in proc:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       for categ in regdict['Dll']:
           if categ in allStrings:
               dll.append(categ)
       if dll != []:
           print("\n{}[{}+{}]{} DLL operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in dll:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       for categ in regdict['DebuggerIdentifying']:
           if categ in allStrings:
               debg.append(categ)
       if debg != []:
           print("\n{}[{}+{}]{} Debugger Identifying operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in debg:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       for categ in regdict['SystemPersistence']:
           if categ in allStrings:
               sysp.append(categ)
       if sysp != []:
           print("\n{}[{}+{}]{} System Persistence operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in regs:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       for categ in regdict['COMObject']:
           if categ in allStrings:
               como.append(categ)
       if como != []:
           print("\n{}[{}+{}]{} COM Object operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in como:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       for categ in regdict['DataLeakage']:
           if categ in allStrings:
               leak.append(categ)
       if leak != []:
           print("\n{}[{}+{}]{} Data Leakage operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in leak:
              print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
       for categ in regdict['Other']:
           if categ in allStrings:
               othe.append(categ)
       if othe != []:
           print("\n{}[{}+{}]{} Other operations".format(cyan,red,cyan,white))
           print("+","-"*20,"+")
           for i in othe:
               print("{}=> {}{}".format(red,white,i))
           print("+","-"*20,"+")
   else:
       print("{}[{}!{}]{} Try -h to see available arguments.".format(cyan,red,cyan,white))
       sys.exit(1)

# Exectuion area
if __name__ == '__main__':
    print(banner)
    try:
        scope()
        os.system("rm -rf temp.txt")
    except:
        os.system("rm -rf temp.txt")