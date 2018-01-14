import telnetlib
import sys, getopt
import os
#import httplib

def getFileContent():
	tn=telnetlib.Telnet("192.168.2.1")
	tn.read_until("Login: ")
	tn.write("root\n")
	tn.read_until("Password: ")
	tn.write("Zte521\n")
	tn.read_until("/ # ")
	tn.write("cat /temp/ppp/options.oe0\n")
	tn.read_until("cat /temp/ppp/options.oe0")
	tn.write("exit\n")
	content=tn.read_until("usepeerdns")
	tn.close()
	return content

def simpanTemporary():
	print("Mengunduh Konfigurasi SSID")
	c=getFileContent()
	f=open("tempIndy","w")
	f.write(c)
	f.close()

def muatNoInternet():
	f=open("tempIndy","r")
	s1=f.readlines()
	f.close()
	s2=""
	for s in s1:
		if "user" in(s):
			s2=s
			break
	os.remove("tempIndy")
	return s2[5:17]

def daftarLangsung(email,defais,sandi,hp):
	print("Mendaftarkan Wifi.id")
	c=httplib.HTTPSConnection("my.telkom.co.id/")
	c.request("POST","registrasi-seamless.php")

def prosesLanjut(email,defais,sandi,hp):
	simpanTemporary()
	daftarLangsung(email,defais,sandi,hp)

def main(argv):
	email=""
	defais=""
	sandi=""
	hp=""
	try:
		opts,args=getopt.getopt(argv,"he:n:p:s:",["email=","nama=","password=","smartphone="])
	except getopt.getoptError:
		print("indi.py -e <email> -n <nama> -p <sandi> -s <no-hp>")
		sys.exit()
	for opt,arg in opts:
		if opt=="-h":
			print("indi.py -e <email> -n <nama> -p <sandi> -s <no-hp>")
			sys.exit()
		elif opt in("-e","--email"):
			email=arg
		elif opt in("-n","--nama"):
			defais=arg
		elif opt in("-p","--password"):
			sandi=arg
		elif opt in("-p","--smartphone"):
			hp=arg
	prosesLanjut(email,defais,sandi,hp)

if __name__ == "__main__":
	simpanTemporary()
	print(muatNoInternet())
	#main(sys.argv[1:])
