import model
mappings=model.get_transform()
print(mappings)
fp1=open("../addmapp.txt","w")
fp1.write(str(mappings['Address']))
fp2=open("../dowmapp.txt","w")
fp2.write(str(mappings['DayOfWeek']))
fp3=open("../pdmapp.txt","w")
fp3.write(str(mappings['PdDistrict']))