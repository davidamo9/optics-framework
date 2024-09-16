*** Settings ***
Library     AppiumLibrary
Library     Process
Library     ${EXECDIR}/Lib/AppiumHelper.py
Library     Collections
Library     String

*** Variables ***

# Initialize from environment variables
${APPIUM_SERVER_URL}    http://127.0.0.1:4723
# ${APP_PACKAGE}          com.csam.icici.bank.imobile
# ${APP_ACTIVITY}         com.csam.icici.bank.imobile.IMOBILE
${APP_PACKAGE}          com.agence3pp
${APP_ACTIVITY}         qosi.fr.usingqosiframework.splashscreen.SplashscreenActivity
${PLATFORM_NAME}        Android
${PLATFORM_VERSION}     11
${DEVICE_SERIAL}        0e98db54

# Global
${test_step_name}    ${EMPTY}

*** Keywords ***

Open Appium Session
    Open Application  ${APPIUM_SERVER_URL}
    ...  platformName=${PLATFORM_NAME}
    ...  platformVersion=${PLATFORM_VERSION}
    ...  udid=${DEVICE_SERIAL}
    ...  appActivity=${APP_ACTIVITY}
    ...  appPackage=${APP_PACKAGE}
    ...  automationName=UiAutomator2
    ...  newCommandTimeout=60000
    ...  usePrebuiltWDA=true
    ...  useNewWDA=false
    ...  autoGrantPermissions=true
    ...  autoAcceptAlerts=true
    ...  noReset=true
    ...  appium:ignoreHiddenApiPolicyError=true


Launch App
    Execute Script    mobile:launchApp {'appPackage': '${APP_PACKAGE}', 'appActivity': '${APP_ACTIVITY}'}


Launch Application
    Open Appium Session
    Sleep    5
    Capture Screenshot With Timestamp    session-started
    # Launch App
    # Sleep    5
    # Capture Screenshot With Timestamp    icici-launched
    # # [Arguments]     ${APP_PACKAGE}           ${APP_ACTIVITY}
    # Open Application  ${APPIUM_SERVER_URL}
    # ...  platformName=${PLATFORM_NAME}
    # ...  platformVersion=${PLATFORM_VERSION}
    # ...  appActivity=${APP_ACTIVITY}
    # ...  appPackage=${APP_PACKAGE}
    # ...  udid=${DEVICE_SERIAL}
    # ...  usePrebuiltWDA=true
    # ...  automationName=UiAutomator2
    # ...  newCommandTimeout=60000
    # ...  useNewWDA=false
    # ...  autoGrantPermissions=true
    # ...  autoAcceptAlerts=true
    # ...  noReset=true

    # # Add proper delay to ensure the app is launched
    # Sleep    10
    # Capture Screenshot With Timestamp    icici-launched
    # Sleep    2

    #TODO: Wait until specified element is found instead of static sleep

Close and Terminate Application
    [Arguments]    ${APP_PACKAGE}
    # Close the application gracefully using Appium
    Close Application
    Sleep    5
    # Terminate the application using adb force-stop
    Run Process    adb    shell    am force-stop ${APP_PACKAGE}
    Log    Application ${APP_PACKAGE} terminated.
    Sleep    5

Wait Until Elements Are Visible
    [Arguments]    @{elements_texts}    ${timeout}=30s    ${screenshot_name}=annotated_screenshot.png
    # Loop through each element text
    FOR    ${element_text}    IN    @{elements_texts}
        # Wait until the page contains the element text
        Wait Until Page Contains    ${element_text}    ${timeout}
        Log    Element with text "${element_text}" is visible
    END
    
    # After all elements are found, annotate them in the screenshot
    Capture And Annotate Multiple Elements    ${elements_texts}    ${screenshot_name}

Press Element
    [Arguments]    ${text}
    ${result}=    Get Element Attributes By Text    text=${text}

    Log    ${result}
    Tap Element By Attributes    attributes=${result}
    Sleep     2

Press Element by Text
    [Arguments]    ${text}
    ${result}=    Get Element Attributes By Text    text=${text}

    Log    ${result}
    Tap Element By Attributes    attributes=${result}
    Sleep     2

Press Home Button
    Execute Script    mobile: pressKey    keycode=${3}

Press Back Button
    Execute Script    mobile: pressKey    keycode=${4}

Press App Switch Button
    Execute Script    mobile: pressKey    keycode=${187}


Swipe Up
    [Documentation]    Swipes up from the bottom to the top of the screen.
    ${window_size}=    Get Window Size
    ${width}=    Set Variable    ${window_size['width']}
    ${height}=    Set Variable    ${window_size['height']}
    ${start_x}=    Evaluate    ${width} / 2
    ${start_y}=    Evaluate    ${height} * 0.8
    ${end_x}=      Set Variable    ${start_x}
    ${end_y}=      Evaluate    ${height} * 0.2
    Swipe    ${start_x}    ${start_y}    ${end_x}    ${end_y}    800


Element Tree
    #Crop All Interactable Elements    screenshot_name=input-elements.png    output_dir=input_elements    annotate=${True} 
    ${result}=     Get Clickable Elements With Attributes
    Log    ${result}

Set Checkbox State
    [Arguments]    ${state}
    Log    ${result}
    AppiumHelper.Set Checkbox State   ${state} 
    Sleep    2

Get Middle Of Bounds
    [Arguments]    ${element_data}
    ${bounds}    Get From Dictionary    ${element_data}    bounds
    Log    Bounds: ${bounds}

    # Remove the square brackets and split by commas and square brackets to get the coordinates
    ${bounds}    Replace String    ${bounds}    [    EMPTY
    ${bounds}    Replace String    ${bounds}    ]    EMPTY
    ${coordinates}    Split String    ${bounds}    ,

    # Extract the coordinates from the split result
    ${x1}    Set Variable    ${coordinates[0]}
    ${y1}    Set Variable    ${coordinates[1]}
    ${x2}    Set Variable    ${coordinates[2]}
    ${y2}    Set Variable    ${coordinates[3]}

    # Convert to integers
    ${x1}    Convert To Integer    ${x1}
    ${y1}    Convert To Integer    ${y1}
    ${x2}    Convert To Integer    ${x2}
    ${y2}    Convert To Integer    ${y2}

    # Calculate the middle of the bounds
    ${middle_x}    Evaluate    (${x1} + ${x2}) / 2
    ${middle_y}    Evaluate    (${y1} + ${y2}) / 2

    # Log and return the middle coordinates
    Log    Middle X: ${middle_x}, Middle Y: ${middle_y}
    [Return]    ${middle_x}    ${middle_y}

Long Press Element by Text
    [Arguments]    ${text}
    ${result}=    Get Element Attributes By Text    text=${text}

    Log    ${result}
    # ${middle_x}    ${middle_y}    Get Middle Of Bounds    ${result}
    # Log    ${middle_x}
    # Log    ${middle_y}
    @{firstFinger}   Create List    539    1049
    @{fingerPositions}  Create List    @{firstFinger}

    Tap With Positions    3000    @{fingerPositions}
    # Tap Element By Attributes    attributes=${result}
    Sleep     2

