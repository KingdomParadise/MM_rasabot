# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet,FollowupAction
from rasa_sdk.executor import CollectingDispatcher
import requests,re
import random, time
import string
from . api_handler import *
t =False
class ActionInitial(Action):
	def name(self):
		return "initial"
	def run(self,dispatcher,tracker,domain):
		print("initialize")
		dispatcher.utter_message(text = "Hello!👋 I am a bot and I'm here to help. What is your zip code")
		return[SlotSet("ResidenceZipCode",None),SlotSet("number",None),SlotSet("pin",None),SlotSet("phonenumber",None),SlotSet("income",None),SlotSet("edit_item",None),SlotSet("phonesetting",None),SlotSet("isemail",None),SlotSet("email",None),SlotSet("isChecked",None),SlotSet("userid",None)]	

class ActionValidateNumber(Action):
	def name(self):
		return "validate_number"

	def run(self, dispatcher,tracker,domain):
		print("validate_number")
		#get the number from the message
		number = tracker.get_slot('number')
		#get the type of the message
		message = tracker.latest_message['text']
		zipstr = ""
		phonestr = ""
		incomestr = ""
		pinstr = ""
		zipstr = re.findall(r'^[Zz][Ii][Pp]', message)
		if len(zipstr)==0:
			zipstr=""
		else:
			zipstr = zipstr[0]	
		phonestr = re.findall(r'^[Pp][Hh][Oo][Nn][Ee]', message)
		if len(phonestr)==0:
			phonestr=""
		else:
			phonestr = phonestr[0]	
		incomestr = re.findall(r'^[Ii][Nn][Cc][Oo][Mm][Ee]', message)
		if len(incomestr)==0:
			incomestr=""
		else:
			incomestr = incomestr[0]	
		pinstr = re.findall(r'^[Pp][Ii][Nn]', message)
		if len(pinstr)==0:
			pinstr=""
		else:
			pinstr = pinstr[0]	
		print(zipstr,phonestr,incomestr,pinstr)
		print(number)
		#get the initial value
		zipcode = tracker.get_slot("ResidenceZipCode")
		pin = tracker.get_slot("pin")
		phonenumber = tracker.get_slot("phonenumber")
		income = tracker.get_slot("income")
		edit_item = tracker.get_slot("edit_item")
		print("zipcode->"+str(zipcode)+"pincode->"+str(pin)+"phonenumber"+str(phonenumber)+"income->"+str(income)+"edit_item"+str(edit_item))
		#if go to the editing interface if I have edit_item
		if edit_item!=None:
			return[FollowupAction("edit_personal_info_modify")]
		#if the email is not correct, go to the email inputing part
		if tracker.get_slot('isemail')==False:
			return []
		#zipcode, income, phonenumber, pincode
		if incomestr!="" or tracker.latest_message['text']=="/affirm_income":
			print("income editing")
			if tracker.get_slot('isChecked')!=True:
				dispatcher.utter_message(text = "Please complete the multiwebform")
				return[FollowupAction("initial")]
			return[SlotSet("income",number),SlotSet("phonenumber",None),SlotSet("pin",None),FollowupAction("provide_income_info")]
		if phonestr!="":
			print("phonenumber editing")
			if tracker.get_slot('isChecked')!=True:
				dispatcher.utter_message(text = "Please complete the multiwebform")
				return[FollowupAction("initial")]
			return[SlotSet("phonenumber",number),SlotSet("phonesetting",True),SlotSet("pin",None),FollowupAction("validate_number_code")]
		if  pinstr!="":
			print("pincode editing")
			if tracker.get_slot('isChecked')!=True:
				dispatcher.utter_message(text = "Please complete the multiwebform")
				return[FollowupAction("initial")]
			return[SlotSet("pin",number),SlotSet("phonesetting",False),FollowupAction("validate_number_code")]  
		if zipcode==None or zipstr!="":
			print("zipcode editing")
			zipcode = number
			if zipcode!=None and len(zipcode) == 5:
				#validate the zipcode
				current = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+zipcode+"&key=AIzaSyAJGToD7umZ-VdfAl95vSnd1AlxVxt9lUI").json()
				if current['status'] == 'OK':
					dispatcher.utter_message( response = "utter_zipcode_sucess")
					return [SlotSet("ResidenceZipCode", zipcode), SlotSet("ResidenceCity", current['results'][0]['address_components'][1]['short_name']), SlotSet("ResidenceState", current['results'][0]['address_components'][2]['short_name']),SlotSet("income",None),SlotSet("phonenumber",None),SlotSet("pin",None),SlotSet("phonesetting",None),SlotSet("isChecked",None),SlotSet("userid",None)]
				else:
					dispatcher.utter_message( response = "utter_zipcode_error")     
					return [SlotSet("income",None),SlotSet("phonenumber",None),SlotSet("pin",None),SlotSet("userid",None),SlotSet("phonesetting",None),SlotSet("ResidenceZipCode",None)] 
			else:
				dispatcher.utter_message( response = "utter_zipcode_error")     
				return [SlotSet("ResidenceZipCode",None),SlotSet("income",None),SlotSet("phonenumber",None),SlotSet("pin",None),SlotSet("phonesetting",None),SlotSet("userid",None)] 

		if tracker.get_slot('isChecked')!=True:
				dispatcher.utter_message(text = "Please complete the multiwebform")
				return[FollowupAction("initial")]
		if  zipcode!=None and income==None:
			return[SlotSet("income",number),SlotSet("phonenumber",None),SlotSet("pin",None),FollowupAction("provide_income_info")]
		if zipcode!=None and income!=None and phonenumber==None :
			return[SlotSet("phonenumber",number),SlotSet("phonesetting",True),SlotSet("pin",None),FollowupAction("validate_number_code")]
		if zipcode!=None and income!=None and phonenumber!=None and pin==None:
			return[SlotSet("pin",number),SlotSet("phonesetting",False),FollowupAction("validate_number_code")]                
		
		  

class ActionValidateEmail(Action):
	def name(self):
		return "validate_email" 

	def run(self, dispatcher, tracker, domain):
		

		email = tracker.get_slot('email')
		response = requests.get("https://isitarealemail.com/api/email/validate", params = {'email': email})
		status = response.json()['status']
		if status=='valid':
			dispatcher.utter_message( response = "utter_email_success")
			return [SlotSet("isemail",True)]
		else:
			dispatcher.utter_message( response = "utter_email_error")   
			return [SlotSet("isemail",False),FollowupAction("validate_number")]

class ActionConfiguration(Action):
	def name(self):
		return "configuration"

	def run(self,dispatcher,tracker,domain):
		print("configuration")
		if tracker.latest_message['text']=='/deny_edit':
			return [FollowupAction('validate_name_address')]

		if tracker.get_slot('userid')!=None:
				tribalEligible = tracker.get_slot('TribalEligible')
				if tribalEligible==True:
					dispatcher.utter_message( response = "utter_tribal_lands")   
					return []       
				else:
					print("edit_personal_info_check-remove")
					return [SlotSet('TribalResident',False),FollowupAction('edit_personal_info_check')]
		token='d3a1b634-90a7-eb11-a963-005056a96ce9'
		check_avaliability_url = 'https://lifeline.cgmllc.net/api/v2/checkavailability'
		user_confituration_url = 'https://lifeline.cgmllc.net/api/v2/userconfiguration'
		state_configuration_url = 'https://lifeline.cgmllc.net/api/v2/stateconfiguration'
		start_order_url = 'https://lifeline.cgmllc.net/api/v2/startorder'  
		email = tracker.get_slot('email')
		zipcode = tracker.get_slot('ResidenceZipCode')
		state = tracker.get_slot('ResidenceState')
		isemail = tracker.get_slot('isemail')
		if isemail==False:
			return [FollowupAction("validate_number")]

		letters = string.ascii_lowercase
		userid = ''.join(random.choice(letters) for i in range(10))


		res = requests.post(check_avaliability_url, data={'Token':token,'ZipCode':zipcode,'Email':email}).json() 
		if res['Status']=='Success':
			print("success->check_avaliability")
			res_user_configuration = requests.post(user_confituration_url,data={'Token':token}).json()
			if res_user_configuration['Status']=='Success':
				print("success->userconfiguration")
				res_state_configuration = requests.post(state_configuration_url,data={'Token':token,'state':state}).json()
				if res_state_configuration['Status']=='Success':
					print("success-state_configuration")
					data = {
						'Token':token,
						'State':state,
						'AppVersion':'89.0.4389.72',
						'Platform':'WebApp',
						'SerialNumber':'www.zapier.com',
						'SaleTypeid':3
						}
					res_start_order = requests.post(start_order_url,data=data).json()
					if res_start_order['Status'] == 'Success':
						print("success->start_order")
			#			dispatcher.utter_message(response = "utter_multi_webform",userid = userid)
						if tracker.get_slot("userid")==None:
							print("new-multi-webform")
							#message1 = {
					        #       "attachment": {
					        #            "type": "template",
					        #            "payload": {
					        #              "template_type": "button",
					        #              "text": "click below to open Multi-page",
					        #              "buttons": [
					        #                {
					        #                   "type":"web_url",
					        #                   "url":"https://f702-5-61-61-227.ngrok.io/submit_info/{})".format(userid),
					        #                   "title": "Multi WebForm",
					        #                   #"messenger_extensions": "true",
					        #                   "webview_height_ratio": "tall"
					        #                }
					        #             ]
					        #            }
					        #        }
							#    }
							# send payload to Facebook Messenger
							#dispatcher.utter_message(json_message =  message1)
							dispatcher.utter_message(text = "Please Complete Multi-page Web Form  (https://f702-5-61-61-227.ngrok.io/submit_info/{})".format(userid))
						
							return [SlotSet("userid",userid),SlotSet("ReservationUserCode",res_user_configuration['ReservationUserCode']),SlotSet("ReservationClientCode",res_user_configuration['ReservationClientCode']),SlotSet("ReservationVendorCode",res_user_configuration['ReservationVendorCode']),SlotSet("OrderNumber",res_start_order['OrderNumber']),SlotSet("PackageId",res_start_order['PackageId']),SlotSet("TribalEligible",res_state_configuration['TribalEligible']),SlotSet("EligibiltyPrograms",res_state_configuration['EligibiltyPrograms'][0]['Code']),SlotSet("FcraDisclosureText",res_state_configuration['FcraDisclosureText']),SlotSet("FcraAdditionalDisclosureText",res_state_configuration['FcraAdditionalDisclosureText']),SlotSet("FcraAcknowledgement",res_state_configuration['FcraAcknowledgement'])]  
						
				dispatcher.utter_message( response = "utter_system_trouble")
				return [SlotSet('ResidenceZipCode',None),SlotSet("email",None)] 	     

		else:
			dispatcher.utter_message( response = "utter_zipcode_service_error", zipcode = zipcode)
			return [SlotSet('ResidenceZipCode',None),SlotSet("email",None)]


class ActionApproveOfferTribal(Action):
	def name(self):
		return "action_approve_offer_tribal"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		if message=="/affirm_tribal":
			return [SlotSet('TribalResident',True),FollowupAction("edit_personal_info_check")] 
		else:
			return [SlotSet('TribalResident',False),FollowupAction("edit_personal_info_check")]    

class ActioSetTribalResident(Action):
	def name(self):
		return "set_tribal_resident"

	def run(self,dispatcher,tracker,domain):
		time.sleep(30)
		while 1:
			confirm = check_multi_webform(tracker.get_slot("userid"))
			if confirm['confirm'] == True:
				print("submit info success")
				break
			time.sleep(2)		
		tribalEligible = tracker.get_slot('TribalEligible')
		if tribalEligible==True:
			dispatcher.utter_message( response = "utter_tribal_lands")   
			return []       
		else:
			print("set_tribal-->personal_info_check")
			return [SlotSet('TribalResident',False),FollowupAction("edit_personal_info_check")]

class ActionEditPersonalInfoCheck(Action):
	def name(self):
		return "edit_personal_info_check"
	def run(self,dispatcher,tracker,domain):
		print("edit_personal_info_check")
		if tracker.get_slot('isChecked')!=True:
			print("isChekced->",tracker.get_slot('isChecked'))
			res = get_info(tracker.get_slot('userid'),"d3a1b634-90a7-eb11-a963-005056a96ce9",tracker.get_slot("PackageId"),tracker.get_slot("ResidenceState"),tracker.get_slot("TribalResident"),tracker.get_slot("EligibiltyPrograms"))

			#dispatcher.utter_message(
			#	response="utter_personal_info",
			#	firstName = res['message']['first_name'],
			#	middleName = res['message']['middle_name'],
			#	lastName = res['message']['last_name'],
			#	suffix = res['message']['suffix'],
			#	dateOfBirth = res['message']['date'],
			#	socialSecurityNo = res['message']['last_four_social'],
			#	residenceAddress = res['message']['residential_address'],
			#	apt_unit1 = res['message']['apt_unit1'],
			#	residenceCity = tracker.get_slot('ResidenceCity'),
			#	residenceState = tracker.get_slot('ResidenceState'),
			#	residenceZipCode = tracker.get_slot('ResidenceZipCode')
			#)

			return[SlotSet("FirstName",res['message']['first_name']),SlotSet("MiddleName",res['message']['middle_name']),SlotSet("LastName",res['message']['last_name']),SlotSet("Suffix",res['message']['suffix']),SlotSet("DateOfBirth",res['message']['date']),SlotSet("SocialSecurityNo",res['message']['last_four_social']),SlotSet("ResidenceAddress",res['message']['residential_address']),SlotSet("Apt_unit1",res['message']['apt_unit1']),SlotSet("Address_nature",res['message']['address_nature']),SlotSet("isChecked",True),SlotSet("Program",res['message']['program'])]  
		elif tracker.get_slot('isChecked')==True:
			print("mmm")
			dispatcher.utter_message(
				response="utter_personal_info",
				firstName = tracker.get_slot("FirstName"),
				middleName = tracker.get_slot("MiddleName"),
				lastName = tracker.get_slot("LastName"),
				suffix = tracker.get_slot("Suffix"),
				dateOfBirth = tracker.get_slot("DateOfBirth"),
				socialSecurityNo = tracker.get_slot("SocialSecurityNo"),
				residenceAddress = tracker.get_slot("ResidenceAddress"),
				apt_unit1 = tracker.get_slot("Apt_unit1"),
				residenceCity = tracker.get_slot('ResidenceCity'),
				residenceState = tracker.get_slot('ResidenceState'),
				residenceZipCode = tracker.get_slot('ResidenceZipCode')
			)
			return[]    

class ActionEditPersonalInfoConfirm(Action):
	def name(self):
		return "edit_personal_info_confirm"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		if message=="/affirm_edit" or message!="/deny_edit":
			dispatcher.utter_message ( response = "utter_ask_edit_item")
			return[]
		elif message == "/deny_edit":
			return [FollowupAction("validate_name_address")]    

class ActionEditPersonalInfoSelect(Action):
	def name(self):
		return "edit_personal_info_select"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		dispatcher.utter_message( response = "utter_edit_item", item = message[1:])
		return [SlotSet("edit_item",message[1:])]

class ActionEditPersonalInfoModify(Action):
	def name(self):
		return "edit_personal_info_modify"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']    
		edit_item = tracker.get_slot('edit_item')
		return[SlotSet(edit_item,message),SlotSet("edit_item",None),FollowupAction("edit_personal_info_check")]

class ActionValidateNameAddress(Action):
	def name(self):
		return "validate_name_address"
	def run(self,dispatcher,tracker,domain):
		first_name = tracker.get_slot('FirstName')
		last_name = tracker.get_slot('LastName')
		dob = tracker.get_slot('DateOfBirth')
		social = tracker.get_slot('SocialSecurityNo')
		eligibiltyprogram = tracker.get_slot('EligibiltyPrograms')
		address = tracker.get_slot('ResidenceAddress')
		city = tracker.get_slot('ResidenceCity')
		state = tracker.get_slot('ResidenceState')
		zipcode = tracker.get_slot('ResidenceZipCode')
		packageid = tracker.get_slot('PackageId')
		vendor = tracker.get_slot('ReservationVendorCode')
		client = tracker.get_slot('ReservationClientCode')
		user = tracker.get_slot('ReservationUserCode')
		FcraDisclosureText = tracker.get_slot("FcraDisclosureText")
		FcraAdditionalDisclosureText = tracker.get_slot("FcraAdditionalDisclosureText")
		FcraAcknowledgement = tracker.get_slot("FcraAcknowledgement")
		#you have to uncommit in the future 
		res = validate_name_address(first_name,last_name,dob,social,eligibiltyprogram,address,city,state,zipcode,packageid,vendor,client,user)
		
		#you have to change status into res['status'] in the future
		status = res['Status']
		####################################
		#status = "Success"
		if status=="Success":
			if state=="CA":
				dispatcher.utter_message (response = "utter_fcra_display",FcraDisclosureText = FcraDisclosureText,FcraAdditionalDisclosureText = FcraAdditionalDisclosureText,FcraAcknowledgement = FcraAcknowledgement)
				return []
			else:
				return [FollowupAction("cgm_check")]
		else:
			if "Invalid" in res['Message']:
				dispatcher.utter_message( response = "utter_cgm_invalid")
				return [FollowupAction("edit_personal_info_confirm")]
			elif "Validation error" in res['Message']:
				dispatcher.utter_message( response = "utter_cgm_validation_error", error = res['ValidationErrors'])
				return [FollowupAction("edit_personal_info_confirm")]   

class ActionCGMCheck(Action):
	def name(self):
		return "cgm_check"      
	def run(self,dispatcher,tracker,domain):
		PackageId = tracker.get_slot('PackageId')
		FirstName = tracker.get_slot('FirstName')
		LastName = tracker.get_slot('LastName')
		DateOfBirth = tracker.get_slot('DateOfBirth')
		Ssn = tracker.get_slot('SocialSecurityNo')
		ResidenceAddress01 = tracker.get_slot('ResidenceAddress')
		ResidenceCity = tracker.get_slot('ResidenceCity')
		ResidenceState = tracker.get_slot('ResidenceState')
		ResidenceZip  = tracker.get_slot('ResidenceZipCode')
		TribalResident = tracker.get_slot('TribalResident')
		SocialSecurityNo = tracker.get_slot('SocialSecurityNo')
		Program = tracker.get_slot('Program')
		#uncommit in the future
		res = check_duplicate_customers(PackageId, FirstName,LastName,DateOfBirth, Ssn, ResidenceAddress01,ResidenceCity, ResidenceState,ResidenceZip)
		cover = coverage_check(PackageId,TribalResident,ResidenceAddress01,ResidenceCity,ResidenceState,ResidenceZip)
		eligibility = confirm_state_eligibility(PackageId,FirstName,LastName,DateOfBirth,SocialSecurityNo,ResidenceAddress01,ResidenceCity,ResidenceState,ResidenceZip,TribalResident,Program)
		reply = ""
		if res['Status']=="Success":
			if cover["Status"]=="Success":
				if cover['Coverage'] == True:
					reply = "Pass"
				else:
					reply = "No-Pass" 
			else:
				reply = "error"     
		else:
			reply = "error"
		eli = eligibility['Status']
		if reply=="error":
			dispatcher.utter_message( response = "utter_trouble_request") 
			return[]
		elif reply == "No-Pass":
			dispatcher.utter_message( response = "utter_offer_coverage")
			return[] 
		else:
			if ResidenceState!="CA" or eli=="Success":
				return[]    
			elif eli != "Success":
				dispatcher.utter_message( response = "utter_trouble_request") 
				return[]
			
class ActionlifeLinePlans(Action):
	def name(self):
		return "life_line_plans"

	def run(self,dispatcher,tracker,domain):
		print("life_line_plans-making buttons")
		global t
		PackageId = tracker.get_slot('PackageId')
		ResidenceState = tracker.get_slot('ResidenceState')
		ResidenceZip = tracker.get_slot('ResidenceZipCode')
		TribalResident = tracker.get_slot('TribalResident')
		#uncommit in the future
		res = lifeline_plan(PackageId,ResidenceState,ResidenceZip,TribalResident)
		if t==False:
			t=True
			return[]
		if res!=None:
			buttons = []
			for i in range(len(res)):
				buttons.append({"payload":"/plan"+str(i+1),"title": str(res[i])})
			dispatcher.utter_message( text = "You quality for ",buttons = buttons)
			return[SlotSet("plans",res)]
		else:
			dispatcher.utter_message( response = "utter_lifeline_plan_error")
			return []    

class ActionlifeLinePlansSelect(Action):
	def name(self):
		return "life_line_plans_select"
	def run(self,dispatcher,tracker,domain):
		print("life_line_select")
		ResidenceState = tracker.get_slot('ResidenceState')
		message = tracker.latest_message['text']
		plans = tracker.get_slot("plans")
		if ResidenceState=="CA":
			dispatcher.utter_message( response = "utter_language_es")
			return [SlotSet("lifeline",plans[int(message[5:])-1])]
		else:
			return [SlotSet("lifeline",plans[int(message[5:])-1]),FollowupAction("check_application_status")]

class ActionSelectLanguages(Action):
	def name(self):
		return "select_language_es"
	def run(self,dispatcher,tracker,domain):
			message = tracker.latest_message['text']
			if message == "/English":
				return[SlotSet("language","English"),FollowupAction("check_application_status")]
			elif message=="/Spanish":
				return[SlotSet("language","Spanish"),FollowupAction("check_application_status")]
			else:
				dispatcher.utter_message( response = "utter_language_ck")
				return []

class ActionSelectLanguages(Action):
	def name(self):
		return "select_language_ck"
	def run(self,dispatcher,tracker,domain):
			message = tracker.latest_message['text']
			if message == "/Chinese":
				return[SlotSet("language","Chinese"),FollowupAction("check_application_status")]
			elif message=="/Korean":
				return[SlotSet("language","Korean"),FollowupAction("check_application_status")]
			else:

				dispatcher.utter_message( response = "utter_language_jv")
				return []

class ActionSelectLanguages(Action):
	def name(self):
		return "select_language_jv"
	def run(self,dispatcher,tracker,domain):
			message = tracker.latest_message['text']
			if message == "/Japanese":
				return[SlotSet("language","Japanese")]
			elif message=="/Vietnamese":
				return[SlotSet("language","Vietnamese")]

class ActionCheckApplicationStatus(Action):
	def name(self):
		return "check_application_status"                       
	def run(self,dispatcher,tracker,domain):
		dispatcher.utter_message( response = "utter_notification")         
		ResidenceState = tracker.get_slot('ResidenceState')
		PackageId = tracker.get_slot("PackageId")
		last_four_social = tracker.get_slot("SocialSecurityNo")
		first_name = tracker.get_slot("FirstName")
		last_name = tracker.get_slot("LastName")
		date = tracker.get_slot("DateOfBirth")
		residence_address = tracker.get_slot("ResidenceAddress")
		ResidenceCity = tracker.get_slot("ResidenceCity")
		ResidenceZip = tracker.get_slot("ResidenceZipCode")
		TribalResident = tracker.get_slot("TribalResident")
		
		if ResidenceState=="CA":
			res = check_NladEbb_application_status(PackageId,last_four_social,first_name,last_name,date,residence_address,ResidenceCity,ResidenceState,ResidenceZip,TribalResident)
		else:
			res = check_nv_application_status(PackageId,last_four_social,first_name,last_name,date,residence_address,ResidenceCity,ResidenceState,ResidenceZip,TribalResident)

		#uncommit in the future
		if "ApplicationStatus" in res.keys():
			if res['ApplicationStatus'] == "ApplicationPending":
				dispatcher.utter_message( response = "utter_national_verifier")
				return[]

			elif res['ApplicationStatus'] == "ApplicationNotComplete" or res['ApplicationStatus'] == "ApplicationNotFound":
				return[FollowupAction("dis_closure_configuration")]   
			else:
				dispatcher.utter_message( response = "utter_wireless")
				return[FollowupAction("dis_closure_configuration")]
		else: 
				return[FollowupAction("dis_closure_configuration")]

class ActionApplicationStatus_Select(Action):
	def name(self):
		return "application_status_select"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		if message=="/check_status":
			return [FollowupAction("check_application_status")] 
		elif message == "/affirm_application_status":
			return[FollowupAction("dis_closure_configuration")]             
		elif message == "/deny_application_status":
			dispatcher.utter_message(response = "utter_sad")
			return[FollowupAction("end_chat")]  

class ActionDisClosureConfiguration(Action):
	def name(self):
		return "dis_closure_configuration"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		if message=="/affirm_application_status":
			dispatcher.utter_message( response = "utter_happy")
		#dispatcher.utter_message (response = "utter_disclosure_webapp",userid = tracker.get_slot("userid"))
		#message1 = {
        #       "attachment": {
         #           "type": "template",
          #          "payload": {
           #           "template_type": "button",
            #          "text": "click below to open Disclosure Web App",
             #         "buttons": [
              #          {
               #            "type":"web_url",
                #           "url":"https://f702-5-61-61-227.ngrok.io/start/{})".format(tracker.get_slot("userid")),
                 #          "title": "",
                  #         "messenger_extensions": "true",
                   #        "webview_height_ratio": "tall"
                    #    }
                     #]
                 # }
              # }
		#}
		# send payload to Facebook Messenger
		#dispatcher.utter_message(json_message =  message1)
		dispatcher.utter_message(text = "Disclosure Web App (https://f702-5-61-61-227.ngrok.io/start/{})".format(tracker.get_slot("userid")))
		return[FollowupAction("ieh_select")]      

class ActionIehSelect(Action):
	def name(self):
		return "ieh_select"
	def run(self,dispatcher,tracker,domain):
		time.sleep(10)
		iehBool = ""
		while 1:
			iehBool = get_ieh(tracker.get_slot("userid"))['ieh']
			if iehBool!="":
				break;
			time.sleep(1)		

		if iehBool==True:
			print("ieh-->",iehBool)
			dispatcher.utter_message( response = "utter_ieh_select")
			return [SlotSet("ieh",iehBool)]
		else:
			print("Go submitordere")
			return[SlotSet("ieh",iehBool),FollowupAction("submit_order")]           

class ActionLifelineService(Action):
	def name(self):
		return "life_line_service"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		if message=="/affirm_disclosure":
			dispatcher.utter_message( response = "utter_affirm_disclosure")
			return [FollowupAction("end_chat")]
		else:
			
			dispatcher.utter_message(response = "utter_select_adult")
			return []
class ActionShareLivingExpenses(Action):
	def name(self):
		return "share_living_expenses"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		if message=="/parent" or message =="/child" or message=="/otheradultrelative" or message=="/adultroommate":
			dispatcher.utter_message( response = "utter_share_live")
			return [SlotSet("adultrelative",message)]
		#insert in the future about the this function now hate it 
		elif message=="/otheradult":
			dispatcher.utter_message( response = "utter_relationship")
			return [SlotSet("otheradult",message)]

		else:
			dispatcher.utter_message( response = "utter_apply_lifeline")
			return [SlotSet("adultrelative",message),FollowupAction("submit_order")]        
class ActionShareExpensesConfirm(Action):
	def name(self):
		return "share_living_expenses_confirm"
	def run(self, dispatcher, tracker,domain):
		message = tracker.latest_message['text']
		if message=="/affirm_share_expenses":
			dispatcher.utter_message( response = "utter_deny_lifeline")  
			return [FollowupAction("end_chat")]
		else:
			dispatcher.utter_message( response = "utter_apply_lifeline")
			return [FollowupAction("submit_order")]

class ActionSubmitOrder(Action):
	def name(self):
		return "submit_order"
	def run(self, dispatcher, tracker, domain):
		print("submit_order")
		Program = tracker.get_slot("Program")


		if Program=="135p" or Program== "150p":
			dispatcher.utter_message(response = "utter_income")
			return[]
		else:
			dispatcher.utter_message(response = "utter_best_way")
			return[SlotSet("income","1000")]
class ActionProvideIncomeInfo(Action):
	def name(self):
		return "provide_income_info"
	def run(self,dispatcher,tracker,domain):
		print("provide_income_info")
		dispatcher.utter_message( response = "utter_more_income")
		return[]

class ActionProvideIncomeSelect(Action):
	def name(self):
		return "provide_income_select"
	def run(self,dispatcher,tracker,domain):
		print("provide_income_select")
		message = tracker.latest_message['text']
		if message == "/affirm_income":
			return [FollowupAction("submit_order")]         
		else:
			dispatcher.utter_message(response = "utter_best_way")
			return[]
class ActionSelectBestWay(Action):
	def name(self):
		return "select_best_way"
	def run(self,dispatcher,tracker,domain):
		print("select_best_way")
		message = tracker.latest_message['text']
		if message=="/Phone":
			dispatcher.utter_message(response = "utter_phone_number")
			return[SlotSet("BestWayToReachYou","phone"),SlotSet("phonesetting",True)]
		elif message=="/Mail" or message=="/Email":
			dispatcher.utter_message(response = "utter_pin_code" )
			return[SlotSet("phonenumber","0000000000"),SlotSet("BestWayToReachYou",message[1:].lower()),SlotSet("phonesetting",False)]  

class ActionEnterCode(Action):
	def name(self):
		return "validate_number_code"
	def run(self,dispatcher,tracker,domain):


		phonenumber = tracker.get_slot("phonenumber")
		pin = tracker.get_slot("pin")

		setting = tracker.get_slot("phonesetting")
		if setting == True:
			if len(phonenumber)==10:
				dispatcher.utter_message(response = "utter_pin_code" )

				return [SlotSet("phonenumber",phonenumber),SlotSet("phonesetting",False)]
			else:
				dispatcher.utter_message(response = "utter_wrong_phone_number") 
				return[SlotSet("phonenumber",None)]
		if setting == False:
			if len(pin)==4:
				return [SlotSet("pin",pin),FollowupAction("submit_order_call")]
			else:
				dispatcher.utter_message( response = "utter_wrong_pin_code")
				return [SlotSet("pin",None)]    


class ActionSubmitOrederCall(Action):
	def name(self):
		return "submit_order_call"
	def run(self,dispatcher,tracker,domain):
		print("submit_order_call")
		PackageId = tracker.get_slot("PackageId")
		EligibiltyPrograms = tracker.get_slot("EligibiltyPrograms")
		first_name = tracker.get_slot("FirstName")
		last_name = tracker.get_slot("LastName")
		suffix = tracker.get_slot("Suffix")
		date = tracker.get_slot("DateOfBirth")
		last_four_social = tracker.get_slot("SocialSecurityNo")
		residential_address = tracker.get_slot("ResidenceAddress")
		ResidenceCity = tracker.get_slot("ResidenceCity")
		ResidenceState = tracker.get_slot("ResidenceState")
		ResidenceZip = tracker.get_slot("ResidenceZipCode")
		BestWayToReachYou = tracker.get_slot("BestWayToReachYou")
		PhoneNumber = tracker.get_slot("phonenumber")
		email = tracker.get_slot("email")

		res = submit_order_call(PackageId,EligibiltyPrograms,first_name,last_name,suffix,date,last_four_social,residential_address,ResidenceCity,ResidenceState,ResidenceZip,BestWayToReachYou,PhoneNumber,email)

		if res['Status']=="Success":
			print("check_nv_eligibility complete")
			return [FollowupAction("check_nv_eligibility")]
		else:
			#buttons = [{"payload":"/customer_help","title":"Do yo u need help"},{"payload":"/customer_restart","title":"Do you restart?"},{"payload":"/National","title":"National Questions"}]
			print("submit_order_call_failed")
			dispatcher.utter_message(response = "utter_offer_faild")
			return []

class ActionCheckNvEligibility(Action):
	def name(self):
		return "check_nv_eligibility"   
	def run(self,dispatcher,tracker,domain):
		print("check_nv_eligibility")
		PackageId = tracker.get_slot("PackageId")
		response = check_nv_eligibilty(PackageId)       
		redirect_url = response['Action']['RedirectUrl']
		status = response['ApplicationStatus']
		if  tracker.get_slot("EligibiltyUrl")!=None:
			status= "Complete"
		#uncommit in the future ##########
		if response['Status']=="Success":
			######remove in the future but not now#########################
			
			if status in  ["PendingCertification","PendingResolution","PendingEligibility"]:
				dispatcher.utter_message( response = "utter_pending_offer")
				dispatcher.utter_message(response = "utter_generate_new_link", url = redirect_url)
				return [SlotSet("EligibiltyUrl",redirect_url)]

			elif status == "Complete":
				return [FollowupAction("get_lifeline_Form")]

			elif status in ["PendingReview","InProgress"]:

				dispatcher.utter_message( response = "utter_pending_national" )
				return[]
		else:
			dispatcher.utter_message( response = "utter_reject_national")
			return[]

class ActionCheckNVSelect(Action):
	def name(self):
		return "check_nv_select"
	def run(self,dispatcher,tracker,domain):
		print("check_nv_select")
		message = tracker.latest_message['text']
		if message == "/generate_new_link" or message=="continue_pending":
			return [FollowupAction("check_nv_eligibility")]

class ActionGetLifeLineForm(Action):
	def name(self):
		return "get_lifeline_Form"
	def run(self,dispatcher,tracker,domain):
		print("get_lifeline_Form")
		PackageId = tracker.get_slot('PackageId')
		res = get_lifeline_form(PackageId)  
		print(res)
		if res == "Success":
			dispatcher.utter_message( response = "utter_get_lifeline_success")
			return[]
		else:
			return[]    

class ActionsubmitService(Action):          
	def name(self):
		return "submit_service"
	def run(self,dispatcher,tracker,domain):
		PackageId = tracker.get_slot('PackageId')
		ServicePlan = tracker.get_slot('lifeline')
		res = submit_service_type(PackageId,ServicePlan)
		if res['Status'] == "Success":
			res = submit_service_status(PackageId)
			if res['Status'] == "Success":
				print("submit_service success")
				return[]        
		dispatcher.utter_message(response = "utter_trouble_application")
		return []


class ActionVerifyEligibility(Action):
	def name(self):
		return "verify_check_nv_eligibility"
	def run(self,dispatcher,tracker,domain):
		PackageId = tracker.get_slot("PackageId")
		
		print("verify_check_nv_eligibility")
		res = check_nv_eligibilty(PackageId) 
		status = res['ApplicationStatus']
		#############remove in the future###############
		status = "ApplicationComplete"
		########################
		if res['Status']=="Success":
			if status == "ApplicationComplete":
				return[]
			else:     
				dispatcher.utter_message(response = "utter_national_verifier_error")
				return []   
		else:   
			dispatcher.utter_message(response = "utter_reject_national" )
			return []

class ApplicationEndSuccess(Action):
	def name(self):
		return "end_success"
	def run(self,dispatcher,tracker,domain):
		ordernum = tracker.get_slot("OrderNumber")
		dispatcher.utter_message(response = "utter_success",ordernum = ordernum)
		return[]

class ActionEndChat(Action):
	def name(self):
		return "end_chat"
	def run(self,dispatcher,tracker,domain):
		dispatcher.utter_message(text = "The End")
		return[]


