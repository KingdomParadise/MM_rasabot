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
import requests
import random
import string
from . api_handler import *

class ActionValidateNumber(Action):
	def name(self):
		return "validate_number"

	def run(self, dispatcher,tracker,domain):
		number = tracker.get_slot('number')
		zipcode = tracker.get_slot("ResidenceZipCode")
		pin = tracker.get_slot("pin")
		phonenumber = tracker.get_slot("phonenumber")
		income = tracker.get_slot("income")
		edit_item = tracker.get_slot("edit_item")
		if edit_item!=None:
			return[FollowupAction("edit_personal_info_modify")]
		if tracker.get_slot('isemail')==False:
			return []

		if zipcode==None:
			zipcode = number
		elif  income==None:
			return[SlotSet("income",number),FollowupAction("provide_income_info")]
		elif phonenumber==None:
			return[SlotSet("phonenumber",number),FollowupAction("validate_number_code")]
		elif pin==None:
			return[SlotSet("pin",number),FollowupAction("validate_number_code")]				

		
		if zipcode!=None and len(zipcode) == 5:
			current = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+zipcode+"&key=AIzaSyAJGToD7umZ-VdfAl95vSnd1AlxVxt9lUI").json()
			if current['status'] == 'OK':
				dispatcher.utter_message( text = "Great! That was a valid zip code! 🎉.")
				dispatcher.utter_message( text = "Please enter your email address? (Ex: example@mail.com) 💬")
				return [SlotSet("ResidenceZipCode", zipcode), SlotSet("ResidenceCity", current['results'][0]['address_components'][1]['short_name']), SlotSet("ResidenceState", current['results'][0]['address_components'][2]['short_name'])]
			else:
				dispatcher.utter_message( text = "That Zip Code was not valid.")     
				return [SlotSet("ResidenceZipCode",None)] 
		else:
			dispatcher.utter_message( text = "That Zip Code was not valid. Please enter a valid zip code.")     
			return [SlotSet("ResidenceZipCode",None)]	

class ActionValidateEmail(Action):
	def name(self):
		return "validate_email" 

	def run(self, dispatcher, tracker, domain):
		email = tracker.get_slot('email')
		response = requests.get("https://isitarealemail.com/api/email/validate", params = {'email': email})
		status = response.json()['status']
		if status=='valid':
			dispatcher.utter_message( text = "Thank You! This will just take a few seconds You are on your way to a FREE phone!📱")
			return [SlotSet("isemail",True)]
		else:
			dispatcher.utter_message( text = "That email address was not valid. Please enter a working email address. (Ex: example@mail.com)")   
			return [SlotSet("isemail",False)]

class ActionConfiguration(Action):
	def name(self):
		return "configuration"

	def run(self,dispatcher,tracker,domain):
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
			return [FollowupAction("validate_zipcode")]
		letters = string.ascii_lowercase
		userid = ''.join(random.choice(letters) for i in range(10))

		res = requests.post(check_avaliability_url, data={'Token':token,'ZipCode':zipcode,'Email':email}).json() 

		if res['Status']=='Success':
			res_user_configuration = requests.post(user_confituration_url,data={'Token':token}).json()
			if res_user_configuration['Status']=='Success':
				res_state_configuration = requests.post(state_configuration_url,data={'Token':token,'state':state}).json()
				if res_state_configuration['Status']=='Success':
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
						

						buttons = [
								{"payload": "/approve_continue", "title": "continue"},
							] 
						dispatcher.utter_message(text = "Multi-page Web Form [www.multiwebform.com] (http://35.153.52.119:8000/submit_info/{})".format(userid),buttons=buttons)
						
						
						return [SlotSet("userid",userid),SlotSet("ReservationUserCode",res_user_configuration['ReservationUserCode']),SlotSet("ReservationClientCode",res_user_configuration['ReservationClientCode']),SlotSet("ReservationVendorCode",res_user_configuration['ReservationVendorCode']),SlotSet("OrderNumber",res_start_order['OrderNumber']),SlotSet("PackageId",res_start_order['PackageId']),SlotSet("TribalEligible",res_state_configuration['TribalEligible']),SlotSet("EligibiltyPrograms",res_state_configuration['EligibiltyPrograms'][0]['Code']),SlotSet("FcraDisclosureText",res_state_configuration['FcraDisclosureText']),SlotSet("FcraAdditionalDisclosureText",res_state_configuration['FcraAdditionalDisclosureText']),SlotSet("FcraAcknowledgement",res_state_configuration['FcraAcknowledgement'])]
					buttons = [
							{"payload": "/customer_help", "title": "Do you need help?"},
							{"payload": "/customer_restart", "title": "Do you restart?"},
						] 
					dispatcher.utter_message( text = "Oh no! Our system is having trouble with your application",buttons = buttons)
					return [SlotSet('ResidenceZipCode',None)]        

		else:  
			buttons = [
					{"payload": "/customer_restart", "title": "Do you restart?"},
				] 
			dispatcher.utter_message( text = "Sorry! We currently do not offer any service plans for the"+zipcode+"area.",buttons = buttons)
			return [SlotSet('ResidenceZipCode',None)]

#######################flowchart4###########################
class ActionApproveOfferTribal(Action):
	def name(self):
		return "action_approve_offer_tribal"
	def	run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		if message=="/affirm_tribal":
			return [SlotSet('TribalResident',True)]	
		else:
			return [SlotSet('TribalResident',False)]	

class ActioSetTribalResident(Action):
	def name(self):
		return "set_tribal_resident"

	def run(self,dispatcher,tracker,domain):
		tribalEligible = tracker.get_slot('TribalEligible')
		if tribalEligible==True:
			buttons = [
			{"payload": "/affirm_tribal", "title": "Yes"},
			{"payload": "/deny_tribal", "title": "No"},
			]
			dispatcher.utter_message( text = "Do you reside on Federally-recognized Tribal lands?",buttons = buttons)   
			return []		
		else:
			return [SlotSet('TribalResident',False),FollowupAction("edit_personal_info_check")]

class ActionEditPersonalInfoCheck(Action):
	def name(self):
		return "edit_personal_info_check"
	def run(self,dispatcher,tracker,domain):
		if tracker.get_slot('isChecked')!=True:
			res = get_info(tracker.get_slot('userid'),"d3a1b634-90a7-eb11-a963-005056a96ce9",tracker.get_slot("PackageId"),tracker.get_slot("ResidenceState"),tracker.get_slot("TribalResident"),tracker.get_slot("EligibiltyPrograms"))
			text = "⚠️Attention! Review your inputs⚠️"

			text = "⚠️Attention! Review your inputs⚠️\n\n"
			text += "First Name : " + res['message']['first_name'] + '\n\n'
			text += "Middle Name/Initial : "+res['message']['middle_name'] + '\n\n'
			text += "LastName : "+res['message']['last_name'] + '\n\n'
			text += "Suffix : "+res['message']['suffix'] + '\n\n'
			text += "Date Of Birth : "+res['message']['date'] + '\n\n'
			text += "SSN : "+res['message']['last_four_social'] + '\n\n'
			text += "Residence Address : "+res['message']['residential_address'] + '\n\n'
			text += "Apartment/Floor/Other : "+res['message']['apt_unit1'] + '\n\n'
			text += "City : "+tracker.get_slot('ResidenceCity') + '\n\n'
			text += "State : " +tracker.get_slot('ResidenceState') + '\n\n'
			text += "ZipCode : "+tracker.get_slot('ResidenceZipCode') + '\n\n'

			text+="Make sure to click `Continue Application` if all of your information is correct"	

			buttons = [{"payload":"/affirm_edit","title":"Let me think"},
					   {"payload":"/deny_edit","title":"Continue Application"}
						]			

			dispatcher.utter_message ( text = text, buttons = buttons)

			return[SlotSet("FirstName",res['message']['first_name']),SlotSet("MiddleName",res['message']['middle_name']),SlotSet("LastName",res['message']['last_name']),SlotSet("Suffix",res['message']['suffix']),SlotSet("DateOfBirth",res['message']['date']),SlotSet("SocialSecurityNo",res['message']['last_four_social']),SlotSet("ResidenceAddress",res['message']['residential_address']),SlotSet("Apt_unit1",res['message']['apt_unit1']),SlotSet("Address_nature",res['message']['address_nature']),SlotSet("isChecked",True),SlotSet("Program",res['message']['program'])]	
		else:
			#res = get_info(tracker.get_slot('userid'))
			text = "⚠️Attention! Review your inputs⚠️\n\n"
			text += ("First Name : "+tracker.get_slot("FirstName") + '\n\n')
			text += ("Middle Name/Initial : "+ tracker.get_slot("MiddleName") + '\n\n')
			text += ("LastName : "+tracker.get_slot("LastName") + '\n\n')
			text += ("Suffix : "+tracker.get_slot("Suffix") + '\n\n')
			text += ("Date Of Birth : "+tracker.get_slot("DateOfBirth") + '\n\n')
			text += ("SSN : "+tracker.get_slot("SocialSecurityNo") + '\n\n')
			text += ("Resodence Address : "+tracker.get_slot("ResidenceAddress") + '\n\n')
			text += ("Apartment/Floor/Other : "+tracker.get_slot("Apt_unit1") + '\n\n')
			text += ("City : "+tracker.get_slot('ResidenceCity') + '\n\n')
			text += ("State : " +tracker.get_slot('ResidenceState') + '\n\n')
			text += ("ZipCode : "+tracker.get_slot('ResidenceZipCode') + '\n\n')
			text+="Make sure to click `Continue Application` if all of your information is correct"	
			buttons = [{"payload":"/affirm_edit","title":"Let me think"},
					   {"payload":"/deny_edit","title":"Continue Application"}
						]			
			dispatcher.utter_message ( text = text, buttons = buttons)
			return[]	

class ActionEditPersonalInfoConfirm(Action):
	def name(self):
		return "edit_personal_info_confirm"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		if message=="/affirm_edit":
			buttons = [{"payload":"/FirstName","title":"First Name"},
					   {"payload":"/MiddleName","title":"Middle Name/Initial"},
					   {"payload":"/LastName","title":"Last Name"},
					   {"payload":"/Suffix","title":"Suffix"},
					   {"payload":"/DateOfBirth","title":"Date Of Birth"},
					   {"payload":"/SocialSecurityNo","title":"Social Security Number"},
					   {"payload":"/ResidenceAddress","title":"Address"},
					   {"payload":"/Apt_unit1","title":"Apart"},
					   {"payload":"/ResidenceCity","title":"City"},
					   {"payload":"/ResidenceState","title":"state"},
					   {"payload":"/ResidenceZipCode","title":"ZipCode"},
					]			
			dispatcher.utter_message ( text = "What would you like to edit?", buttons = buttons)
			return[]
		else:
			return [FollowupAction("validate_name_address")]	

class ActionEditPersonalInfoSelect(Action):
	def name(self):
		return "edit_personal_info_select"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		dispatcher.utter_message( text = "Please enter the value")
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
		#dispatcher.utter_message( text = "ValidateNameAddress...")
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
				buttons = [
				{"payload":"/affirm_fcra","title":"I agree"}
				]
				#uncommit in the future
				dispatcher.utter_message( text =("FcraDisclosureText -->"+ FcraDisclosureText+"\nFcraAdditionalDisclosureText -->"+FcraAdditionalDisclosureText+"\nFcraAcknowledgement -->"+FcraAcknowledgement),buttons = buttons)
				#remove in the future
				#dispatcher.utter_message(text = "FcraDisclosureText",buttons=buttons)
				#
				return []
			else:	
				return [FollowupAction("cgm_check")]
		#uncommit in the future
		else:
			if "Invalid" in res['Message']:
				dispatcher.utter_message(text = "Your information did not pass out checks!")
				return [FollowupAction("edit_personal_info_confirm")]
			elif "Validation error" in res['Message']:
				dispatcher.utter_message( text = "Oh no! WE couldn't validate your information."+str(res['ValidationErrors']) +"Please correct the error")	
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
			buttons = [{"payload":"/custom_help","title":"help"}]
			dispatcher.utter_message( text = "Oh no! Our system is having trouble with your request",buttons = buttons) 
			return[]
		elif reply == "No-Pass":
			dispatcher.utter_message( text = "Sorry! We do not currently offer coverage in your area")
			return[] 
		else:
			if ResidenceState!="CA" or eli=="Success":
				return[]	
			elif eli != "Success":
				buttons = [{"payload":"/custom_help","title":"help"}]
				dispatcher.utter_message( text = "Oh no!. Our System is having trouble with your request", buttons = buttons)
				return[]
			
class ActionlifeLinePlans(Action):
	def name(self):
		return "life_line_plans"

	def run(self,dispatcher,tracker,domain):
		PackageId = tracker.get_slot('PackageId')
		ResidenceState = tracker.get_slot('ResidenceState')
		ResidenceZip = tracker.get_slot('ResidenceZipCode')
		TribalResident = tracker.get_slot('TribalResident')
		#uncommit in the future
		res = lifeline_plan(PackageId,ResidenceState,ResidenceZip,TribalResident)
		if res!=None:
			buttons = []
			for i in range(len(res)):
				buttons.append({"payload":"/plan"+str(i+1),"title": str(res[i])})
			dispatcher.utter_message( text = "You quality for ",buttons = buttons)
			return[SlotSet("plans",res)]
		else:
			buttons = [{"payload":"/custom_help","title":"Help"}]
			dispatcher.utter_message( text = "Oh no! We could not find any plans that you qualify for.",buttons = buttons)
			return []	 

class ActionlifeLinePlansSelect(Action):
	def name(self):
		return "life_line_plans_select"
	def run(self,dispatcher,tracker,domain):
		ResidenceState = tracker.get_slot('ResidenceState')
		message = tracker.latest_message['text']
		plans = tracker.get_slot("plans")
		
		if ResidenceState=="CA":
			buttons = [{"payload":"/English","title":"English"},
				{"payload":"/Spanish","title":"Spanish"},
				{"payload":"/More","title":"More"}
			]
			dispatcher.utter_message( text = "What language do you perfer to speak? 😊",buttons = buttons)
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
				buttons = [{"payload":"/Chinese","title":"Chinese"},{"payload":"/Korean","title":"Korean"},{"payload":"/More_CK","title":"More"}]
				dispatcher.utter_message( text = "More Options",buttons = buttons)
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
				buttons = [{"payload":"/Japanese","title":"Japanese"},{"payload":"/Vietnamese","title":"Vietnamese"}]
				dispatcher.utter_message( text = "More Options",buttons = buttons)
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
		dispatcher.utter_message( text = "Do you prefer standard print, or LARGE PRINT notifications? Contact Access Wireless Customer Service directly if you would like to receive future communications from the California LifeLine Administrator in Braille.")			
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
			res	= check_nv_application_status(PackageId,last_four_social,first_name,last_name,date,residence_address,ResidenceCity,ResidenceState,ResidenceZip,TribalResident)

		#uncommit in the future
		if "ApplicationStatus" in res.keys():
			if res['ApplicationStatus'] == "ApplicationPending":
				buttons = [{"payload":"/check_status","title":"Check Status"}]
				dispatcher.utter_message( text = "Your application is still being processed by the National verifier! Click here to check its status.")
				return[]

			elif res['ApplicationStatus'] == "ApplicationNotComplete" or res['ApplicationStatus'] == "ApplicationNotFound":
				return[FollowupAction("dis_closure_configuration")]   
			else:
				buttons = [{"payload":"/affirm_application_status"},{"payload":"/deny_application_status"}]
				dispatcher.utter_message( text = "We noticed that you are already receiving a  Lifeline benefit from another provider. Would you like to transfer your service provider to Access Wireless? 😊",buttons = buttons)
				return[FollowupAction(dis_closure_configuration)]
		else: 
				return[FollowupAction(dis_closure_configuration)]

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
			dispatcher.utter_message(text = "😥 We're sad to see you go!")
			return[FollowupAction("end_chat")]	

class ActionDisClosureConfiguration(Action):
	def name(self):
		return "dis_closure_configuration"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		if message=="/affirm_application_status":
			dispatcher.utter_message( text = "Great! We're glad to have you 🤩")
		buttons = [{"payload":"/disclosure_continue","title":"Continue"}]

		dispatcher.utter_message(text ="Disclosure Web App[www.disclosure.com] (http://35.153.52.119:8000/start/{})".format(tracker.get_slot("userid")), buttons=buttons)
		return[]	

class ActionIehSelect(Action):
	def name(self):
		return "ieh_select"
	def run(self,dispatcher,tracker,domain):
		iehBool = get_ieh(tracker.get_slot("userid"))['ieh']

		if iehBool==True:
			buttons = [{"payload":"/affirm_disclosure","title":"Yes"},{"payload":"/deny_disclosure","title":"No"}]
			dispatcher.utter_message(text = "Does your spouse or domestic partner live with you AND already receive LifeLine phone service? Select NO if you do not have a spouse or partner.Select NO if your spouse or partner does not live with you.Select NO if your spouse or partner does not receive lifeline phone service?",buttons = buttons)
			return [SlotSet("ieh",iehBool)]
		else:
			return[SlotSet("ieh",iehBool),FollowupAction("submit_order")]			

class ActionLifelineService(Action):
	def name(self):
		return "life_line_service"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		if message=="/affirm_disclosure":
			dispatcher.utter_message( text = "I'm Sorry 😥 You do not qualify to apply for Lifeline because someone in your household already gets the benefit.Each household is allowed to get only ONE Lifeline")
			return [FollowupAction("end_chat")]
		else:
			buttons = [
			{"payload":"/parent","title":"Parent"},
			{"payload":"/child","title":"Child(+18)"},
			{"payload":"/otheradultrelative","title":"Other Adult Relative"},
			{"payload":"/adultroommate","title":"Adult Roommate"},
			{"payload":"/otheradult","title":"Other Adult"},
			{"payload":"/noadult","title":"No Adults"},
			]
			dispatcher.utter_message(text = "Other than a spouse or partner, do other adults (people over the age of 18 or emancipated minors) live with you at your address? If so, are they your:",buttons = buttons)
			return []
class ActionShareLivingExpenses(Action):
	def name(self):
		return "share_living_expenses"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		if message=="/parent" or message =="/child" or message=="/otheradultrelative" or message=="/adultroommate":
			buttons = [{"payload":"/affirm_share_expenses","title":"Yes"},{"payload":"/deny_share_expenses","title":"No"}]
			dispatcher.utter_message( text = "Do you share living expenses (bills, food, etc.) and share income (either your income, their income, or both incomes together) with the adult you listed above? 🏠💵",buttons = buttons)
			return [SlotSet("adultrelative",message)]
		#insert in the future about the this function now hate it 
		elif message=="/otheradult":
			dispatcher.utter_message( text = "Please specify:What is their relationship to you?")
			return [SlotSet("otheradult",message)]

		else:
			dispatcher.utter_message( text = "YES! You qualify to apply for Lifeline!🎉😁🎉")
			return [SlotSet("adultrelative",message),FollowupAction("submit_order")]		
class ActionShareExpensesConfirm(Action):
	def name(self):
		return "share_living_expenses_confirm"
	def run(self, dispatcher, tracker,domain):
		message = tracker.latest_message['text']
		if message=="/affirm_share_expenses":
			dispatcher.utter_message( text = "I'm Sorry 😥 You do not qualify to apply for Lifeline because someone in your household already gets the benefit.Each household is allowed to get only ONE Lifeline")	
			return [FollowupAction("end_chat")]
		else:
			dispatcher.utter_message( text = "YES! You qualify to apply for Lifeline!🎉😁🎉")
			return [FollowupAction("submit_order")]

class ActionSubmitOrder(Action):
	def name(self):
		return "submit_order"
	def run(self, dispatcher, tracker, domain):
		Program = tracker.get_slot("Program")
		if Program=="135p" or Program== "150p":
			dispatcher.utter_message("To continue we'll need to verify some of your income information💲")
			dispatcher.utter_message("What dollar amount is on your income proof?")
			dispatcher.utter_message("Please upload your proof of income 📰")
			return[FollowupAction("select_best_way")]

		else:
			buttons = [{"payload":"/Phone","title":"Phone"},{"payload":"/Email","title":"Email"},{"payload":"/Mail","title":"Mail"}]
			dispatcher.utter_message(text = "What is the best way to reach you? Click one of the options below",buttons = buttons)

			#return[FollowupAction("select_best_way")]
			return[SlotSet("income","1000")]
class ActionProvideIncomeInfo(Action):
	def name(self):
		return "provide_income_info"
	def run(self,dispatcher,tracker,domain):
		buttons = [{"payload":"/affirm_income","title":"Yes"},{"payload":"/deny_income","title":"No"}]
		dispatcher.utter_message( text = "Do you have more income information to provide?",buttons = buttons)
		return[]

class ActionProvideIncomeSelect(Action):
	def name(self):
		return "provide_income_select"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		if message == "/affirm_income":
			return [FollowupAction("submit_order")]			
		else:
			buttons = [{"payload":"/Phone","title":"Phone"},{"payload":"/Email","title":"Email"},{"payload":"/Mail","title":"Mail"}]
			dispatcher.utter_message(text = "What is the best way to reach you? Click one of the options below",buttons = buttons)
			#return[FollowupAction("select_best_way")]
			return[]
class ActionSelectBestWay(Action):
	def name(self):
		return "select_best_way"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		if message=="/Phone":
			dispatcher.utter_message(text = "What is your phone number? 📱It can look like this: 5417901356")
			return[SlotSet("BestWayToReachYou","phone"),SlotSet("phonesetting",True)]
		elif message=="/Mail" or message=="/Email":
			dispatcher.utter_message(text = "Please make a four digit PIN for your application(ex:like 1002)")
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
				dispatcher.utter_message(text = "Please make a four digit PIN for your application (ex:pin digit is xxxx)")
				return [SlotSet("phonenumber",phonenumber),SlotSet("phonesetting",False)]
			else:
				dispatcher.utter_message(text = "wrong phone number, please enter the phone number again! - 10 digits")	
				return[SlotSet("phonenumber",None)]
		if setting == False:
			if len(pin)==4:
				return [SlotSet("pin",pin),FollowupAction("submit_order_call")]
			else:
				dispatcher.utter_message( text = "wrong pin code, please enter the pin code again! - 4 digits")
				return [SlotSet("pin",None)]	


class ActionSubmitOrederCall(Action):
	def name(self):
		return "submit_order_call"
	def run(self,dispatcher,tracker,domain):
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

			return [FollowupAction("check_nv_eligibility")]
		else:
			#buttons = [{"payload":"/customer_help","title":"Do yo u need help"},{"payload":"/customer_restart","title":"Do you restart?"},{"payload":"/National","title":"National Questions"}]
			buttons = [{"payload":"/customer_help","title":"Do yo u need help"},{"payload":"/customer_restart","title":"Do you restart?"}]
			dispatcher.utter_message("Oh no! Your order failed:[INPUT ERROR MESSAGE] How would you like to proceed?")
			return []

class ActionCheckNvEligibility(Action):
	def name(self):
		return "check_nv_eligibility"   
	def run(self,dispatcher,tracker,domain):
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
				dispatcher.utter_message( text = "We've filled out most of your application in the National Verifier with the information you provided.")
				dispatcher.utter_message( text = "To proceed, you'll need to confirm some of your information at the National Verifier's website.")
				dispatcher.utter_message( text = "Click below ⬇ When you've completed your application, you will be finished enrolling! You have 7 minutes before this link expires")
				buttons = [
						{"payload": "/generate_new_link", "title": "continue"},
						] 
				dispatcher.utter_message(text = "here : [www.eligibilty.com]({})".format(redirect_url),buttons=buttons)
				return [SlotSet("EligibiltyUrl",redirect_url)]

			elif status == "Complete":
				return [FollowupAction("get_lifeline_Form")]

			elif status in ["PendingReview","InProgress"]:
				buttons = [
						{"payload": "/continue_pending", "title": "continue"},
						] 
				dispatcher.utter_message( text ="Your Application is Pending National Verifier Review. Click here to check the status" )
				return[]
		else:
			buttons = [
						{"payload": "/customer_help", "title": "continue"},
						] 
			dispatcher.utter_message( text = "Oh no! Your request was reject by the National Verifier.",buttons = buttons)
			return[]

class ActionCheckNVSelect(Action):
	def name(self):
		return "check_nv_select"
	def run(self,dispatcher,tracker,domain):
		message = tracker.latest_message['text']
		if message == "/generate_new_link" or message=="continue_pending":
			return [FollowupAction("check_nv_eligibility")]

class ActionGetLifeLineForm(Action):
	def name(self):
		return "get_lifeline_Form"
	def run(self,dispatcher,tracker,domain):
		PackageId = tracker.get_slot('PackageId')
		res = get_lifeline_form(PackageId)	

		if res == "Success":
			dispatcher.utter_message( text = "Here is a filled out copy of your application!")
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
				return[]   
		buttons = [
				{"payload": "/customer_help", "title": "continue"},
			]        
		dispatcher.utter_message(text = "Oh no! We are having trouble processing your application",buttons = buttons)
		return []


class ActionVerifyEligibility(Action):
	def name(self):
		return "verify_check_nv_eligibility"
	def run(self,dispatcher,tracker,domain):
		PackageId = tracker.get_slot("PackageId")
		

		res = check_nv_eligibilty(PackageId) 
		status = res['ApplicationStatus']
		#############remove in the future###############
		status = "ApplicationComplete"
		########################
		if res['Status']=="Success":
			if status == "ApplicationComplete":
				return[]
			else:
				buttons = [
					{"payload": "/customer_help", "title": "continue"},
					]        
				dispatcher.utter_message(text = "Oh no! Your application was not completed in the National Verifier",buttons = buttons)
				return []	
		else:
			buttons = [
					{"payload": "/customer_help", "title": "continue"},
					]        
			dispatcher.utter_message(text = "Oh no! Your request was rejected by the National Verifier.",buttons = buttons)
			return []

class ApplicationEndSuccess(Action):
	def name(self):
		return "end_success"
	def run(self,dispatcher,tracker,domain):
		ordernum = tracker.get_slot("OrderNumber")
		dispatcher.utter_message(text = "Congratulations!🥳Your application is complete!Thank you for choosing Access Wireless.Your order number is: "+str(ordernum)+ "We will contact you when your applications has been finalized.")
		dispatcher.utter_message(text = "Get your friends and family FREE phone and service by sharing this link:http://m.me/accesswirelesslifeline")
		return[]

class ActionEndChat(Action):
	def name(self):
		return "end_chat"
	def run(self,dispatcher,tracker,domain):
		dispatcher.utter_message(text = "The End")
		return[]


