*** Settings ***

Resource   ${EXECDIR}/Resources/modules.robot

*** Variables ***
*** Keywords ***
*** Test Cases ***

Test Keywords
    Launch Application
    @{elements} =    Create List    Full test
    Wait Until Elements Are Visible     @{elements}    screenshot_name=5gmark-landing.png
    Press Element    text=Speed
    Sleep    3
    Press Element    text=_reminder


        
    # Authenticate User Using Login Pin
    # Navigate to Dashboard Screen
    # Navigate to Send Money Screen
    # Navigate to Select Payee Screen
    # Navigate to Fund Transfer Screen
    # Validation Enter Amount Less Then 1 Rupees
    # Validation Enter Amount More Than Available Balance
    # Enter Amount Valid Amount On Transfer Fund Screen
    # Navigate to Confirm Details Screen
    # Navigate to Payment Successful Screen

