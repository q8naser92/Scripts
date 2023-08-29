import datetime
import ipaddress
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

subnet = ipaddress.ip_network('192.168.0.0/16')
ip_list = list(subnet.hosts())

baseurl = "Beyond Trust Server Url" + "/BeyondTrust/api/public/v3"
apikey = "Beyond Trust API Key"
apiuser = r"Domain\User"
workgroup = "Beyondtrust Workgroup"

header = {'Authorization':'PS-Auth key=' +apikey+"; runas="+apiuser+";"}
session = requests.Session()
session.headers.update(header)

logfile = 'log.txt'

with open(logfile, 'a' , newline="") as file:
  response = session.post(baseurl + "/Auth/SignAppin", verify=False)
  file.write(str(datetime.datetime.now())+"\nAuth Code: " + str(response.status_code)+"\n")
  for ip in ip_list:
    asset_data = {
      "name" : str(ip),
      "description" : "Added via script",
      "IPAddress": str(ip),
    }
    response = session.post(baseurl+"/Workgroups/"+workgroup+"/Assets",json=asset_data, verify=False)
    if(response.status_code >=300):
      file.write(str(ip)+" - " + str(response.status_code) + " - " + str(response.content) + "\n")
  file.write("\n")
  file.close()

