*** Settings ***

Resource   ${EXECDIR}/Resources/modules.robot

*** Variables ***
*** Keywords ***
*** Test Cases ***

TC 033 Fund Transfer Using IMPS Within ICICI Bank
    [Tags]    TC_033_Fund_Transfer_Using_IMPS_Within_ICICI_Bank
    Launch Application
        
    Authenticate User Using Login Pin
    Navigate to Dashboard Screen
    Navigate to Send Money Screen
    Navigate to Select Payee Screen
    Navigate to Fund Transfer Screen
    Validation Enter Amount Less Then 1 Rupees
    Validation Enter Amount More Than Available Balance
    Enter Amount Valid Amount On Transfer Fund Screen
    Navigate to Confirm Details Screen
    Navigate to Payment Successful Screen

