
*************To do change the text:*************


1)FlowChart1:

- text: "Hello!👋 I am a bot and I'm here to help.What is your Zip Code?"
  
  /root/analyzer.py - row 22,25

- text: "That Zip Code was not valid. Please enter a valid zip code."
  
  /root/analyzer.py - row 46


- text: "Great! That was a valid zip code! 🎉"  
 
    /root/analyzer.py - row 44


2)FlowChart2

- text: "Please enter your email address? (Ex: example@mail.com) 💬"

    /root/analyzer.py - row 44


- text: "That email address was not valid. Please enter a working email address. (Ex: example@mail.com)"  
  
    /root/analyzer.py - row 67,70


- text: "Thank You! This will just take a few seconds You are on your way to a FREE phone!📱"

    /root/analyzer.py - row 65


3)FlowChart3

- text: "Please enter a valid ZipCode."(Restart  part)

    /root/analyzer.py - row 80


- text: "Sorry! We currently do not offer any service plans for the ZIP CODE {currentchat.ResidenceZip} area. Please try with other ZipCode. : Enter zip code again!"

      /root/script.py - row 84


- text: "Oh no! Our system is having trouble with your application"

      /root/script.py - row 81


- text: "An agent will reach out shortly! Thank you for your patience."  

      /root/analyzer.py - row 86


4)FlowChart4

- text: "Do you reside on Federally-recognized Tribal lands?"
  
      /root/analyzer.py - row 92

- text: ""Confirm your information again?""  

      /root/analyzer.py - row 99,113,120

- text: "Do you reside on Federally-recognized Tribal lands?"

      /root/analyzer.py - row 126


- text: "Please Enter the "+ incoming_message + " again"

      /root/analyzer.py - row 160

- text: "Would you like to edit anything else?"(FlowChart)="Contine"(Code)

      /root/analyzer.py - row 202

- text: "CGMChecks"(when the user click the "Application Continue" Button)

      /root/analyzer.py - row 208

- text: "Oh no! WE couldn't validate your information.[ERROR MESSAGE] Please correct the error"  

      /root/analyzer.py - row 147


- text: "Your information did not pass out checks! [Error Message]"  

      /root/analyzer.py - row 145


5)FlowChart5

- text: "Oh no! Our system is having trouble with your request [ERROR MESSAGE}"  

      /root/analyzer.py - row 220


- text: "Let's start Lisfeline"
  
      /root/analyzer.py - row 229,233

- text: "An agent will reach out shortly!""

      /root/script.py - row 105,109


- text: "Sorry! We do not currently offer coverage in your area."

      /root/analyzer.py - row 224


- text: "Oh no! Our system is having trouble with your request"

      /root/analyzer.py - row 237


6)FlowChart6

- text: "Oh no! We could not find any plans that you qualify for."

      /root/analyzer.py - row 254


- text: "An agent will reach out shortly! Thank you for your patience."

  domain.yml - row 303

- text: "You qualify for "

      /root/analyzer.py - row 245


- text: "What language do you prefer to speak? 😊"
 
        /root/analyzer.py - row 264,281,294

- text: "Track ApplicationStatus..."

        /root/analyzer.py - row 268


- text: "Do you prefer standard print, or LARGE PRINT notifications? Contact Access Wireless Customer Service directly if you would like to receive future communications from the California LifeLine Administrator in Braille."

        /root/analyzer.py - row 277.303


- text: "Your application is still being processed by the National verifier! Click here to check its status."  

        /root/analyzer.py - row 313


- text: "We noticed that you are already receiving a  Lifeline benefit from another provider. would you like to transfer your service provider to Access Wireless? 😊"

        /root/analyzer.py - row 321

- text: "DisclosuresConfiguration"

        /root/analyzer.py - row 325

- text: "😥 We're sad to see you go!"  

        /root/analyzer.py - row 337


-text: "Great! We're glad to have you 🤩"  

        /root/analyzer.py - row 333



7)FlowChart7

- text: "Does your spouse or domestic partner live with you AND already receive LifeLine phone service? Select NO if you do not have a spouse or partner. Select NO if your spouse or partner does not live with you. Select NO if your spouse or partner does not receive lifeline phone service?"

        /root/analyzer.py - row 351

- text: "SubmitOrdering..."

        /root/analyzer.py - row 355

-text: "Other than a spouse or partner, do other adults (people over the age of 18 or emancipated minors) live with you at your address? If so, are they your:"  

        /root/analyzer.py - row 367


- text: "Do you share living expenses (bills, food, etc.) and share income (either your income, their income, or both incomes together) with the adult you listed above? 🏠💵"

        /root/analyzer.py - row 386,405


- text: "I'm Sorry 😥 You do not qualify to apply for Lifeline because someone in your household already gets the benefit. Each household is allowed to get only ONE Lifeline."  

        /root/analyzer.py - row 362,394


- text: "YES! You qualify to apply for Lifeline!🎉😁🎉"

        /root/analyzer.py - row 381,398



8)FlowChrt8

- text: "To continue we'll need to verify some of your income information"

        /root/analyzer.py - row 413,417

- text: "what dollar amount is on your income proof?"
        
        /root/script.py - row 152

- text: "Please upload your proof of income?"
       
        /root/script.py - row 156

- text: "Do you have more income information to provide" 
        
        /root/script.py - row 162

- text: "Please Input the correct Income"

        /root/script.py - row 164

- text: "What's the best way to reach you? Click one of the options below"

        /root/analyzer.py - row 419,430


- text: "What is your phone number? 📱It can look like this: 5417901356"

        /root/analyzer.py - row 444


- text: "Verify all numbers and 10 digits long"

        /root/analyzer.py - row 461


- text: "Please make a four digit PIN for your application(ex:like 1002)"  

        /root/analyzer.py - row 450


- text:  "Verify all numbers and 4 digits long"

        /root/analyzer.py - row 472

- text: "SubmitOrder Call Checking"

        /root/analyzer.py - row 470

- text: "Oh no! Your order failed:  How would you like to proceed?"

        /root/analyzer.py - row 483


- text: "An agent will reach out shortly! Thank you for your patience."

        /root/script.py - row 125

        /root/analyzer.py - row 497

-text: "Please restart!!"

        /root/analyzer.py - row 493



9)FlowChart9

- text: "Oh no! Your request was reject by the National Verifier."

        /root/analyzer.py - row 530


- text: "An agent will reach out shortly! Thank you for your patience."

        /root/script.py - row 195


- text: "Your Application is Pending National Verifier Review. Click here to check the status"  

        /root/analyzer.py - row 526


- text: "We've filled out most of your application in the National Verifier with the information you provided.To proceed, you'll need to confirm some of your information at the National Verifier's website.Click below ⬇ When you've completed your application, you will be finished enrolling!
 You have 7 minutes before this link expires."

        /root/analyzer.py - row 517


- text: "If the above link didn't work, click here to make another!"

        /root/analyzer.py - row 561



10)FlowChart10

- text: "Here is a filled out copy of your application!"  

        /root/script.py - row 2571


11)FlowChart11

- text: "Oh no! We are having trouble processing your application"

        /root/script.py - row 211


- text: "An agent will reach out shortly! Thank you for your patience."

        /root/script.py - row 216



12)FlowChart12

- text: "Oh no! Your request was rejected by the National Verifier."

        /root/script.py - row 234


- text: "An agent will reach out shortly! Thank you for your patience."

        /root/script.py - row 240


- text: "Oh no! Your application was not completed in the National Verifier"  

        /root/script.py - row 230



13)FlowChart13  

- text: "Congratulations!🥳Your application is complete!Thank you for choosing Access Wireless.Your order number is: [ORDER NUM}We will contact you when your applications has been finalized.
Get your friends and family FREE phone and service by sharing this link:

http://m.me/accesswirelesslifeline"

        /root/script.py - row 244,248


*************To start*************

1)Run the Server

python3 manage.py migrate

nohup python3 manage.py runserver 0:8000 $

2)Kill the process

ps -fA | grep python

kill -9 <PID>     
