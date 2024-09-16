*** Settings ***

Resource    ${EXECDIR}/VariableFiles/variables.robot
Resource    ${EXECDIR}/Resources/appium.robot

*** Keywords ***

Authenticate User Using Login Pin
    Press Element    ${login_pin_id}
    Enter Number    ${login_pin_id}    ${login_pin}
    PressKey    ${keycode_enter}

Navigate to Dashboard Screen
    Validate Screen    ${send_money_icon_cug}
    Assert Presence    ${my_saving_account}
    Assert Presence    ${view_balance}

Navigate to Send Money Screen
    Press Element    ${send_money_icon_cug}
    Assert Presence    ${search_add_payee}

Navigate to Select Payee Screen
    Assert Presence    ${search_add_payee}
    Press Element    ${search_add_payee}
    Validate Screen    ${SELECT_PAYEE_SCREEN}
    Assert Presence    ${search_payee_search_payee}
    Press Element    ${search_payee_search_payee}
    Enter Number    ${search_payee_search_payee}    ${select_payee_search_icon_on_select_payee}
    Assert Presence    ${search_payee_result_click_cug}
    Press Element    ${search_payee_result_click_cug}

Navigate to Scheduled Payment Select Payee Screen
    Validate Screen    ${SELECT_PAYEE_SCREEN}
    Assert Presence    ${search_payee_search_payee}
    Press Element    ${search_payee_search_payee}
    Enter Number    ${search_payee_search_payee}    ${select_payee_search_icon_on_select_payee}
    Assert Presence    ${search_payee_result_click_cug}
    Press Element    ${search_payee_result_click_cug}

Validation Enter Amount Less Then 1 Rupees
    Enter Number    ${enter_amount_id_cug}    ${invalid_amount}
    Assert Presence    ${error_amount_validation_cug}
    Element Disabled    ${confirm_id}  
    Clear Element Text    ${enter_amount_id_cug}

Validation Enter Amount More Than Available Balance
    Enter Number    ${enter_amount_id_cug}    ${invalid_exceeded_amount}
    Assert Presence    ${balance_validation_cug}
    Element Disabled    ${confirm_id}
    Clear Element Text    ${enter_amount_id_cug}

Navigate to Fund Transfer Screen
    Validate Screen    ${FUND_TRANSFER_SCREEN}
    Press Element    ${enter_amount_id_cug}

Enter Amount Valid Amount On Transfer Fund Screen
    Enter Number    ${enter_amount_id_cug}    ${amount}
    Element Should Not Visible    ${balance_validation_cug}
    Assert Presence    ${confirm_id}
    Press Element    ${add_comment}
    Enter Number    ${add_comment}    ${comment_TEXT}
    Assert Presence    ${add_comment}
    Press Element    ${coffee}
    Press Element    ${confirm_id}

Navigate to Confirm Details Screen
    Assert Presence    ${amount_id_cug}
    Assert Presence    ${search_payee_name}
    Assert Presence    ${tv_bank_name_cug}
    Assert Presence    ${tv_from_name_cug}
    Assert Presence    ${tv_pay_type_label_cug}
    Assert Presence    ${tv_bank_name_cug}
    Assert Presence    ${tv_from_name_cug}
    Assert Presence    ${tv_pay_type_label_cug}
    Swipe SeekBar To Right    ${SEEK_BAR}

Navigate to Payment Successful Screen
    Validate Screen    ${PAYMENT_SUCCESFUL_SCREEN}
    Assert Presence    ${payment_successfull_msg_cug}
    Assert Presence    ${payment_successfull_amount_cug}
    Assert Presence    ${payment_successfull_comment_cug}
    Assert Presence    ${payment_successfull_payee_name_cug}
    Assert Presence    ${payment_successfull_sender_name_cug}
    Assert Presence    ${payment_successfull_sender_account_no_cug}
    Assert Presence    ${payment_successfull_account_type_cug}
    Assert Presence    ${payment_successfull_paid_at_cug}
    Assert Presence    ${payment_successfull_trans_id_cug}
    Assert Presence    ${payment_successfull_copy_cug}
    Assert Presence    ${payment_successfull_mark_fav_cug}
    Assert Presence    ${payment_successfull_share_cug}
    Assert Presence    ${payment_successfull_payment_option_cug}

Navigate to One Time Payment Successful Screen
    Validate Screen    ${ONE_TIME_PAYMENT_SUCCESSFULLY_SCHEDULED}

Navigate to Fund Transfer Screen NEFT To Other Bank Schedule Pay One Time
    Validate Screen    ${FUND_TRANSFER_SCREEN}
    Enter Number    ${enter_amount_id_cug}    ${enter_amount}
    Press Element    ${pay_now_dropdown}
    Press Element    ${schedule_pay_button_xpath}
    Press Element    ${select_date_xpath}
    Press Element    ${date} 
    Press Element    ${calender_ok_button_xpath}
    Enter Number    ${add_comment}    ${comment_TEXT}
    Press Element    ${coffee}
    Assert Presence    ${confirm_id}
    Press Element    ${confirm_id}

Close ICICI Application
    Close Application

Go Back And Close the App
    PressKey    4    10

Navigate to Confirm Details Screen NEFT to OB
    Validate Screen    ${CONFIRM_DETAIL_SCREEN}
    Press Element    ${imps}
    Press Element    ${neft}
    Swipe SeekBar To Right    ${SEEK_BAR}

Navigate to Edit Details
    Validate Screen    ${CONFIRM_DETAIL_SCREEN}
    Press Element    ${imps}
    Press Element    ${neft}
    Assert Presence    ${close_button_xpath}
    Press Element    ${close_button_xpath}
    Validate Screen    ${FUND_TRANSFER_SCREEN}
    Assert Presence    ${edit_icon_xpath}
    Press Element    ${edit_icon_xpath}
    Validate Screen    ${SELECT_PAYEE_SCREEN}

Navigate to Edit Select Payee Screen
    Validate Screen    ${SELECT_PAYEE_SCREEN}
    Assert Presence    ${search_payee_search_payee}
    Press Element    ${search_payee_search_payee}
    Enter Number    ${search_payee_search_payee}    ${select_payee_search_icon_on_select_payee}
    Assert Presence    ${search_payee_result_click_cug}
    Press Element    ${search_payee_result_click_cug}

Navigate to NEFT Fund Transfer Screen
    Validate Screen    ${FUND_TRANSFER_SCREEN}
    Press Element    ${enter_amount_id_cug}
    Enter Number    ${enter_amount_id_cug}    ${neft_amount}
    Element Should Not Visible    ${balance_validation_cug}
    Assert Presence    ${confirm_id}
    Press Element    ${add_comment}
    Enter Number    ${comment_TEXT}
    Assert Presence    ${add_comment}
    Press Element    ${coffee}
    Press Element    ${confirm_id}

Navigate to RTGS Fund Transfer Screen
    Validate Screen    ${FUND_TRANSFER_SCREEN}
    Press Element    ${enter_amount_id_cug}
    Enter Number    ${enter_amount_id_cug}    ${rtgs_amount}
    Element Should Not Visible    ${balance_validation_cug}
    Assert Presence    ${confirm_id}
    Press Element    ${add_comment}
    Enter Number    ${add_comment}    ${comment_TEXT}
    Assert Presence    ${add_comment}
    Press Element    ${coffee}
    Press Element    ${confirm_id}

Navigate to Grid Confirmation
    Validate Screen    ${GRID_CONFIRMATION}
    Assert Presence    ${grid_confirmation_first_input_field_xpath}
    Enter Number    ${grid_pin}
    Assert Presence    ${grid_confirmation_confirm_button_xpath}
    Press Element    ${grid_confirmation_confirm_button_xpath}

Navigate to Add Favourite
    Validate Screen    ${PAYMENT_SUCCESFUL_SCREEN}
    Assert Presence    ${payment_successfull_mark_fav_cug}
    Press Element    ${payment_successfull_mark_fav_cug}
    Validate Screen    ${PAYEE_SUCESSFULLY_ADDED_FAVOURITES_SCREEN_XPATH}

Navigate to Schedule New Payment
    Assert Presence    ${schedule_new_payment_button_xpath}
    Press Element    ${schedule_new_payment_button_xpath}
    Validate Screen    ${SELECT_PAYEE_SCREEN}
    Assert Presence    ${search_payee_search_payee}
    Press Element    ${search_payee_search_payee}
    Enter Number    ${search_payee_search_payee}    ${select_payee_search_icon_on_select_payee}
    Assert Presence    ${search_payee_result_click_cug}
    Press Element    ${search_payee_result_click_cug}
    Validate Screen    ${SCHEDULE_NEW_PAYMENT_SCREEN} 

Navigate to Scheduled Payments
    Press Element    ${scheduled_payments_button_xpath}
    Validate Screen    ${SCHEDULED_PAYMENTS_SCREEN}

Navigate to Select Edit Scheduled Payment
    Press Element    ${select_payee_edit_schedule_payment}
    Validate Screen    ${SCHEDULED_PAYMENTS_DETAILS}

Navigate to Select ICICI Scheduled Payment
    Press Element    ${select_icici_payee_delete_schedule_payment}
    Validate Screen    ${SCHEDULED_PAYMENTS_DETAILS}

Navigate to Select NEFT Scheduled Payment
    Press Element    ${select_neft_payee_delete_schedule_payment}
    Validate Screen    ${SCHEDULED_PAYMENTS_DETAILS}

Navigate to Select RTGS Scheduled Payment
    Press Element    ${select_rtgs_payee_delete_schedule_payment}
    Validate Screen    ${SCHEDULED_PAYMENTS_DETAILS}

Navigate to Edit Scheduled Payments Details
    Assert Presence    ${edit_schedule_payment_select_scheduled_payment_xpath}
    Press Element    ${edit_schedule_payment_select_scheduled_payment_xpath}
    Validate Screen    ${SCHEDULED_PAYMENTS_DETAILS}

Navigate to Validate Delete and Edit Button
    Assert Presence    ${scheduled_payments_details_edit_button_xpath}
    Assert Presence    ${scheduled_payments_details_delete_button_xpath}

Navigate to Edit Schedule Payment
    Press Element    ${scheduled_payments_details_edit_button_xpath}
    Validate Screen    ${EDIT_PAYMENT_SCREEN}  

Navigate to Cancel Edit Schedule Payment
    Assert Presence    ${edit_schedule_payment_cancel_button_xpath}
    Press Element    ${edit_schedule_payment_cancel_button_xpath}
    Validate Screen    ${SCHEDULED_PAYMENTS_DETAILS}

Navigate to Delete Schedule Payment
    Press Element    ${scheduled_payments_details_delete_button_xpath}
    Validate Screen    ${DELETE_SCHEDULED_PAYMENT}

Navigate to Cancel Delete Schedule Payment
    Assert Presence    ${delete_scheduled_payments_cancel_button_xpath}
    Press Element    ${delete_scheduled_payments_cancel_button_xpath}
    Validate Screen    ${SCHEDULED_PAYMENTS_DETAILS}

Navigate to Scheduled Payments Successfully Deleted
    Press Element    ${delete_scheduled_payments_delete_button_xpath}
    Validate Screen    ${SCHEDULE_PAYMENT_SUCCESSFULLY_DELETED}

Navigate to Edit Scheduled Payments
    Assert Presence    ${edit_schedule_payment_amount_input_xpath}
    Press Element    ${edit_schedule_payment_amount_input_xpath}
    PressKey    ${backspace}    3
    Enter Text By Keycode    ${enter_amount}   
    PressKey    ${device_back_button}
    Assert Presence    ${edit_schedule_payment_payment_date_input_id} 
    Press Element    ${edit_schedule_payment_payment_date_input_id} 
    Validate Screen    ${CALENDER_SCREEN}
    Press Element    ${date_edit} 
    Press Element    ${calender_ok_button_xpath}
    Press Element    ${confirm_id}

Navigate to Payment Successfully Modified Screen
    Validate Screen    ${SCHEDULE_PAYMENT_SUCCESSFULLY_MODIFIED}

Navigate to Recurring Payment
    Enter Number    ${enter_amount_id_cug}    ${enter_amount}
    Press Element    ${select_date_xpath}
    Validate Screen    ${CALENDER_SCREEN}
    Press Element    ${date}
    Press Element    ${calender_ok_button_xpath}
    Press Keycode    ${device_back_button}
    Press Element    ${make_recurring_checkbox_xpath}
    Element Disabled    ${confirm_id}  
    Press Element    ${payment_frequency_dropdown_xpath}
    Press Element    ${payment_frequency_monthly_xpath}
    Press Element    ${no_of_payments_input_xpath}
    Enter Number    ${no_of_payments_input_xpath}    ${no_of_payment}
    Press Keycode    ${device_back_button}
    Press Element    ${coffee}
    Assert Presence    ${confirm_id}
    Press Element    ${confirm_id}

Navigate to Recurring Payment Successful Screen
    Validate Screen    ${RECURRING_PAYMENT_SUCESSFULLY_SCHEDULED}
    Assert Presence    ${payment_success_payee_name} 

Navigate to Add Your Favourite
    Press Element    ${add_favourite_xpath}
    Validate Screen    ${MANAGE_FAVOURITES_SCREEN}

Navigate to Add Favourite Payee
    Press Element    ${add_favourite_payee_xpath}
    Validate Screen    ${ADD_FAVORITES_SCREEN}
    Assert Presence    ${add_favourite_payee_screen_title_xpath_cug}

Navigate to Manage Favourite
    Press Element    ${manage_button_xpath}
    Validate Screen    ${MANAGE_FAVOURITES_SCREEN}

Navigate to Remove Favourite
    Press Element    ${payee_option_id}
    Validate Screen    ${payee_option_popup_cug}
    Assert Presence    ${remove_favourite_button_xpath}
    Press Element    ${remove_favourite_button_xpath}

Navigate to Remove Favourite Confirmation
    Validate Screen    ${remove_favourite_button_xpath}
    Assert Presence    ${remove_favourites_confirmation_cancel_xpath_cug}
    Assert Presence    ${remove_favourites_confirmation_remove_button_xpath_cug}
    Press Element    ${remove_favourites_confirmation_remove_button_xpath_cug}

Navigate to Remove Favourite Success Screen
    Validate Screen    ${REMOVE_FAVOURITES_SUCESSFULLY_SCREEN}
    Assert Presence    ${remove_favourite_success_screen_tittle_xpath_cug}
    Assert Presence    ${remove_favourites_success_green_tick_xpath_cug}

Navigate to Add Favourite Button
    Press Element    ${add_favorite_star_icon}
    Validate Screen    ${FAVOURITES_ADDED_SUCCESSFULLY}

Navigate to Device Back to Success Page
    Press Keycode    ${device_back_button}
    Validate Screen    ${MANAGE_FAVOURITES_SCREEN}

Navigate to App Back Button
    Press Element    ${app_back_button_xpath_cug}
    Assert Presence    ${search_add_payee}

Navigate to Recent Transaction
    Swipe Scroll To Top    ${recent_transaction_text_xpath}
    Validate Screen    ${RECENT_TRANSACTION_SCREEN}
    Press Element By ResourceId    ${repayment_button_xpath_id}    
    Validate Screen    ${FUND_TRANSFER_SCREEN}
    Press Element    ${bills}
    Press Element    ${confirm_id}
    Log To Console    ${add_new_payee_add_payee_name}
    Log To Console    ${add_new_payee_add_payee_account_number_payee_name}

Navigate to Your Payee Screen
    Press Element    ${send_money_manage_icon_xpath_cug}
    Validate Screen    ${YOUR_PAYEE_SCREEN}

Navigate to Select Payee Bank
    Press Element    ${your_payees_add_new_payee_cug}
    Validate Screen    ${SELECT_PAYEE_BANK_SCREEN}

Navigate to Add New ICICI Payee
    Press Element    ${select_payee_bank_icici_bank_icon_xpath_cug}
    Validate Screen    ${ADD_NEW_PAYEE_SCREEN}

Navigate to Add New Other Bank Payee
    Press Element    ${select_payee_bank_hdfc_bank_icon_xpath_cug}
    Validate Screen    ${ADD_NEW_PAYEE_SCREEN}

Entering Payee Account Number
    Enter Text By Keycode    ${add_new_payee_add_payee_account_number_payee_name}

Retyping Payee Account Number
    Enter Text By Keycode    ${add_new_payee_add_payee_account_number_payee_name}
    Assert Presence By ResourceId    ${verified_tick_id}

Entering Payee Name
    Press Element    ${add_icici_bank_payee_name}
    Enter Text By Keycode    ${add_new_payee_add_payee_name}

Entering Payee Nick Name
    Press Keycode    ${device_back_button}
    Press Element    ${add_icici_bank_payee_nick_name}
    Assert Presence    ${add_icici_bank_payee_nick_name}
    Enter Text By Keycode         ${add_new_payee_add_payee_name}

Navigate to Isafe Screen
    Press Element    ${add_icici_bank_payee_name}
    Assert Presence By ResourceId    com.csam.icici.bank.imobile:id/checkBox
    Validate Screen    ${Isafe_xpath_cug}
    Assert Presence    ${make_recurring_checkbox_xpath}
    Press Element    ${make_recurring_checkbox_xpath}
    Press Element    ${add_new_payee_isafe_skip_button_id_cug}
    Enter Text By Keycode    ${add_new_payee_add_payee_name}

Navigation to Authenticate With OTP Screen
    Assert Presence    ${add_new_payee_authenticate_with_otp_xpath_cug}
    Press Element    ${add_new_payee_authenticate_with_otp_xpath_cug}    
    Validate Screen    ${ALERT_I_UNDERSTAND_SCREEN}
    Assert Presence    ${alert_new_payee_understand_button_xpath_cug}
    Press Element    ${alert_new_payee_understand_button_xpath_cug} 

Navigate to Verify OTP
    Validate Screen    ${VERIFY_OTP_SCREEN}

Navigate to Payee Successfully Added
    Validate Screen    ${PAYEE_ADDED_SUCESSFULLY_SCREEN}
    Assert Presence    ${payee_successfully_added_back_to_payments_button_xpath_cug}

Navigate to Search for Payee
    Press Element    ${search_payee_search_payee}
    Enter Text By Keycode    ${add_new_payee_add_payee_name}

Navigate to Delete Payee Options Screen
    Press Element    ${payee_option_id}
    Validate Screen    ${your_payeee_payee_option_popup_cug}
    Press Element    ${your_payees_delete_payee_button_xpath_cug}

Navigate to Delete Payee Confirmation
    Validate Screen    ${DELETE_CONFIRMATION_SCREEN}
    Assert Presence    ${delete_payee_confirmation_cancel_button_id_cug} 
    Assert Presence    ${delete_payee_confirmation_yes_button_xpath_cug}
    Press Element    ${delete_payee_confirmation_yes_button_xpath_cug}

Navigate to Payee Successfully Deleted
    Validate Screen    ${PAYEE_SUCCESSFULLY_DELETED_SCREEN}
    Assert Presence    ${payee_successfully_deleted_back_to_transfer_button_xpath_cug} 

Validation Minimum 5 Digit Required
    Press Element    ${payee_account_number}
    Enter Text By Keycode    ${four_digit}   
    Assert Presence By ResourceId    ${minimum_5_digit_error_id}
    Clear Element Text    ${payee_account_number}

Validation Entered Account Numbers Do Not match
    Press Element    ${retype_payee_account_number}
    Enter Text By Keycode    ${mismatch_digit}
    Assert Presence By ResourceId    ${mismatch_account_munber_error_id}
    Clear Element Text      ${retype_payee_account_number}

Navigate to Back to Payments
    Assert Presence    ${payee_successfully_deleted_back_to_transfer_button_xpath_cug}
    Press Element    ${payee_successfully_deleted_back_to_transfer_button_xpath_cug}
    Assert Presence    ${search_add_payee}

Navigate to Search Deleted Payee Name
    Assert Presence    ${search_add_payee}
    Press Element    ${search_add_payee}
    Validate Screen    ${SELECT_PAYEE_SCREEN}
    Assert Presence    ${search_payee_search_payee}
    Press Element    ${search_payee_search_payee}
    Enter Text By Keycode    ${add_new_payee_add_payee_name}
    Assert Presence    ${no_payee_found_xpath}

