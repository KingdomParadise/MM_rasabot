import requests

def validate_name_address(first_name,last_name,data,social,EligibiltyPrograms,Address,ResidenceCity,ResidenceState,ResidenceZip,PackageId,ReservationVendorCode,ReservationClientCode,ReservationUserCode):
	validate_name_address_url = ' https://lifeline.cgmllc.net/api/v2/validatenameaddress'
	data = {
		'FirstName': first_name,
		'LastName': last_name,
		'DateOfBirth': date,
		'SocialSecurityNo': social,
		'StateEligibilityCode': EligibiltyPrograms,
		'ResidenceAddress01': Address,
		'ResidenceCity': ResidenceCity,
		'ResidenceState': ResidenceState,
		'ResidenceZip': ResidenceZip,
		'PackageID': PackageId,
		'Token': 'd3a1b634-90a7-eb11-a963-005056a96ce9',
		'VendorCode' : ReservationVendorCode,
		'ClientCode' : ReservationClientCode,
		'UserCode' : ReservationUserCode,
		}
	res = requests.post(validate_name_address_url,data=data).json()
	return res 

def check_duplicate_customers(PackageId,FirstName,LastName,DateOfBirth,Ssn,ResidenceAddress01,ResidenceCity,ResidenceState,ResidenceZip):
	check_duplicate_customer_url = check_duplicate_customer ='https://lifeline.cgmllc.net/api/v2/checkduplicatecustomer'
	data = {   
		"Token": "d3a1b634-90a7-eb11-a963-005056a96ce9",
		"PackageID": PackageId,
		"FirstName": FirstName,
		"LastName": LastName,
		"DateOfBirth": DateOfBirth,
		"Ssn": Ssn,
		"ResidenceAddress01": ResidenceAddress01ce,
		"ResidenceCity": ResidenceCity,
		"ResidenceState": ResidenceState,
		"ResidenceZip": ResidenceZip
	}   
	res = requests.post(check_duplicate_customer_url,data=data).json()	
	return res

def coverage_check(PackageId,TribalResident,ResidenceAddress01,ResidenceCity,ResidenceState,ResidenceZip):
	coverage_check_url = 'https://lifeline.cgmllc.net/api/v2/coveragecheck'
	data = {
		"Token": "d3a1b634-90a7-eb11-a963-005056a96ce9",
		"PackageID": PackageId,
		"Tribal": TribalResident,
		"ResidenceAddress01": residential_address,
		"ResidenceCity": ResidenceCity,
		"ResidenceState": ResidenceState,
		"ResidenceZip": ResidenceZip
		}
	res = requests.post(coverage_check_url,data=data).json() 
	return res   

def conform_state_eligibilty(PackageId,FirstName,LastName,DateOfBirth,Social,ResidenceAddress01,ResidenceCity,ResidenceState,ResidenceZip,TribalResident,Program):
	confirm_sate_url = 'https://lifeline.cgmllc.net/api/v2/confirmstateeligibility'  
	data = {
		"Token": "d3a1b634-90a7-eb11-a963-005056a96ce9",
		"PackageID": PackageId,
		"FirstName": FirstName,
		"LastName":LastName,
		"DateOfBirth":DateOfBirth,
		"SocialsecurityNo":Social,
		"ResidenceAddress01": ResidenceAddress01,
		"ResidenceCity": ResidenceCity,
		"ResidenceState": ResidenceState,
		"ResidenceZip": ResidenceZip,
		"TribalResident":TribalResident,
		"Program":Program
	}  
	res = requests.post(confirm_state_url,data=data).json()
	return res

def lifeline_plan(PackageId,ResidenceState,ResidenceZip,TribalResident):
	life_line_url = "https://lifeline.cgmllc.net/api/v2/lifelineplans"
	data = {
		"Token":"d3a1b634-90a7-eb11-a963-005056a96ce9",
		"PackageID" : PackageId,
		"State" : ResidenceState,
		"Zip" : ResidenceZip,
		"Tribal" : TribalResident
	}
	res = requests.post(life_line_url,data=data).json()
	if res['Status'] == "Success":
		for i in range(0,len(res['LifelinePlans'])):
			mid=(str(res['LifelinePlans'][i]["Name"]))
			plan.append(mid)
			
			return plan
	else:
			return None

def check_NladEbb_application_status(PackageId,last_four_social,first_name,last_name,date,residential_address,ResidenceCity,ResidenceState,ResidenceZip,TribalResident):
	check_nladebb_application_status_url = "https://lifeline.cgmllc.net/api/v2/CheckNladEbbApplicationstatus"
	data = {
		"Token":"d3a1b634-90a7-eb11-a963-005056a96ce9",
		"PackageID" : PackageId,
		"SSN" : last_four_social,
		"FirstName" : first_name,
		"LastName" : last_name,
		"DOB" : date,
		"PrimaryAddress1" :residential_address,
		"PrimaryCity" : ResidenceCity,
		"PrimaryState": ResidenceState,
		"PrimaryZip" : ResidenceZip,
		"Tribal" : TribalResident,
	}
	res = requests.post(Check_NladEbbApplication_Status_url,data = data).json()
	return res

def check_NladEbb_application_status(PackageId,last_four_social,first_name,last_name,date,residential_address,ResidenceCity,ResidenceState,ResidenceZip,TribalResident):
	check_nv_application_status_url = "https://lifeline.cgmllc.net/api/v2/CheckNVApplicationstatus"
	data = {
		"Token":"d3a1b634-90a7-eb11-a963-005056a96ce9",
		"PackageID" : PackageId,
		"SSN" : last_four_social,
		"FirstName" : first_name,
		"LastName" : last_name,
		"DOB" : date,
		"PrimaryAddress1" :residential_address,
		"PrimaryCity" : ResidenceCity,
		"PrimaryState": ResidenceState,
		"PrimaryZip" : ResidenceZip,
		"Tribal" : TribalResident,
	}
	res = requests.post(Check_nv_application_Status_url,data = data).json()
	return res    