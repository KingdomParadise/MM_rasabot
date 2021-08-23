import requests
def get_info(userid):
	print('http://127.0.0.1:8000/get_info/{}'.format(userid))
	url = 'http://127.0.0.1:8000/get_info/{}'.format(userid)
	res = requests.get(url).json()
	print(res)
	return res

def get_ieh(userid):
	url = 'http://127.0.0.1:8000/get_ieh/{}'.format(userid)
	res = requests.get(url).json()
	print(res)
	return res

def validate_name_address(first_name,last_name,date,social,EligibiltyPrograms,Address,ResidenceCity,ResidenceState,ResidenceZip,PackageId,ReservationVendorCode,ReservationClientCode,ReservationUserCode):
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
		"ResidenceAddress01": ResidenceAddress01,
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
		"ResidenceAddress01": ResidenceAddress01,
		"ResidenceCity": ResidenceCity,
		"ResidenceState": ResidenceState,
		"ResidenceZip": ResidenceZip
		}
	res = requests.post(coverage_check_url,data=data).json() 
	return res   

def confirm_state_eligibility(PackageId,FirstName,LastName,DateOfBirth,Social,ResidenceAddress01,ResidenceCity,ResidenceState,ResidenceZip,TribalResident,Program):
	confirm_state_url = 'https://lifeline.cgmllc.net/api/v2/confirmstateeligibility'  
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
	plan = []
	res = requests.post(life_line_url,data=data).json()
	if res['Status'] == "Success":
		count = 0
		if len(res['LifelinePlans'])>3:
			count = 3
		else:
			count = len(res['LifelinePlans'])	
		for i in range(count):
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
	res = requests.post(check_nladebb_application_status_url,data = data).json()
	return res

def check_nv_application_status(PackageId,last_four_social,first_name,last_name,date,residential_address,ResidenceCity,ResidenceState,ResidenceZip,TribalResident):
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
	res = requests.post(check_nv_application_status_url,data = data).json()
	print(res)
	return res    

def submit_order_call(PackageId,EligibiltyPrograms,first_name,last_name,suffix,date,last_four_social,residential_address,ResidenceCity,ResidenceState,ResidenceZip,BestWayToReachYou,PhoneNumber,email):
	submit_order_url = "https://lifeline.cgmllc.net/api/v2/submitorder"
	data = {
		"Token":"d3a1b634-90a7-eb11-a963-005056a96ce9",
		"PackageID": PackageId,
		"EligibilityProgram": EligibiltyPrograms,
		"FirstName": first_name,
		"LastName": last_name,
		"NameSuffix": suffix,
		"DateOfBirth": date,
		"Ssn": last_four_social,
		"ResidenceAddress01": residential_address,
		"ResidenceCity": ResidenceCity,
		"ResidenceState": ResidenceState,
		"ResidenceZip": ResidenceZip,
		"BestWayToReachYou": BestWayToReachYou,
		"PhoneNumber": PhoneNumber,
		"Email": email,
	}
	res = requests.post(submit_order_url,data = data).json()
	return res	

def check_nv_eligibilty(PackageId):
	check_nv_eligibility_url  = "https://lifeline.cgmllc.net/api/v2/checknveligibility"    
	data = {
		"Token":"d3a1b634-90a7-eb11-a963-005056a96ce9",
		"PackageID" : PackageId,
	}
	res = requests.post(check_nv_eligibility_url,data = data).json()
	return res

def get_lifeline_form(PackageId):
	get_lifeline_url = "http://lifeline.cgmllc.net/api/v2/getlifelineform"    
	data = {
		'Token':"d3a1b634-90a7-eb11-a963-005056a96ce9",
		'PackageID': PackageId,
	}
	#res = requests.post(get_lifeline_url,data = data).json()
	return "Failure"

def submit_service_type(PackageId,ServicePlan):
	data = {
	'Token' : "d3a1b634-90a7-eb11-a963-005056a96ce9",
	'PackageID' : PackageId,
	'ServicePlan' : ServicePlan
	}
	res = requests.post(submit_service_type_url,data = data).json()
	return res

def submit_service_status(PackageId):
	data = {
	'Token' : "d3a1b634-90a7-eb11-a963-005056a96ce9",
	'PackageID' : PackageId,
	}
	res = requests.post(submit_service_status_url,data = data).json()
	return res    