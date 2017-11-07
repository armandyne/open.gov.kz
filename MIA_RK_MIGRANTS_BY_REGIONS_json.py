# -*- coding: utf-8-*-
import requests
from bs4 import BeautifulSoup

wikipage = requests.get("https://kk.wikipedia.org/wiki/ISO_3166-2:KZ").text
soup = BeautifulSoup(wikipage, "html.parser")

iso_codes = {}
table = soup.find("table", {"class":"wikitable sortable"})
for tr in table.find_all("tr"):
    a = tr.find("a")
    tt = tr.find("tt")
    if tt is not None:
        print(tt.text, a.text)
        iso_codes[a.text.lower()] = tt.text

iso_codes["Алматы қаласы".lower()] = iso_codes.get("Алматы".lower())
iso_codes["Астана қаласы".lower()] = iso_codes.get("Астана".lower())
print(iso_codes)

url_meta = "https://data.egov.kz/meta/kazakstan_respublikasynda_uaky/v5"
url_data = "https://data.egov.kz/api/v2/kazakstan_respublikasynda_uaky/v5"
json_meta = requests.get(url_meta, verify=False).json()
json_data = requests.get(url_data, verify=False).json()
 
print(json_meta)
print(json_data)
 
pfRU = "Ru"
pfKZ = "Kk"
dscrFldNm = "description"
dateFldNm = "modifiedDate"
ownerFldNm = "fullname"
result = {dscrFldNm + pfKZ:json_meta[dscrFldNm + pfKZ],
          dscrFldNm + pfRU:json_meta[dscrFldNm + pfRU],
          dateFldNm: json_meta[dateFldNm],
          ownerFldNm + pfKZ:json_meta[ownerFldNm + pfKZ],
          ownerFldNm + pfRU:json_meta[ownerFldNm + pfRU]          
          }
 
tmp_dict = []
labelFldNm = "label"
for r in json_meta["fields"]:
    print(json_meta["fields"][r][labelFldNm + pfRU], json_meta["fields"][r][labelFldNm + pfKZ], json_data[0][r])
    tmp_dict.append({labelFldNm + pfRU:json_meta["fields"][r][labelFldNm + pfRU],
                   labelFldNm + pfKZ:json_meta["fields"][r][labelFldNm + pfKZ],
                   "data":json_data[0][r],
                   "iso_geocode":iso_codes.get(json_meta["fields"][r][labelFldNm + pfKZ].lower())
                  })
 
result["fields"] = tmp_dict
print(result)

f = open("data_migrants.json", "w", encoding="utf-8")
f.write("[{\n")
nn = 0
nn2 = 0
nn3 = 0
for k, v in result.items():
    if k == "fields":
        f.write(',"' + k + '":[\n')
        nn2 = 0
        for k2 in result[k]:     
            nn3 = 0
            if nn2 > 0: f.write(",")
            f.write('{')
            for k3, v3 in k2.items():
                if nn3 > 0: f.write(",")
                f.write('"' + k3 + '":"' + v3 + '"')
                nn3 += 1 
            f.write('}')
            nn2 += 1
        f.write("]\n")
    else:
        if nn > 0: f.write(",")
        f.write('"' + k + '":"' + v + '"\n')
        nn += 1       
f.write("}]")
f.close()
