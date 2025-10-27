TELEGRAM_BOT_TOKEN = "8269352590AAGWuBZdoIRPeiedUkdOH4xsfHPdDhGrzhM"
ECAP_LOGIN_URL = "https://webprosindia.com/vignanpharma/default.aspx"
ECAP_ACADEMIC_REGISTER_URL = "https://webprosindia.com/vignanpharma/StudentAcademicRegistration.aspx"
ECAP_ATTENDANCE_URL = "https://webprosindia.com/vignanpharma/StudentMaster.aspx"

import os
ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")
 # paste your encryption key here as a string
SESSION_TIMEOUT = 86400  # 24 hours
ADMIN_USER_ID = None

ACADEMIC_REGISTER_COLUMNS = {
    "subject_name": 1,      # Column 2 (index 1)
    "attended_held": -2,    # Last-2nd column
    "current_day": -3,      # Last-3rd column
    "percentage": -1        # Last column
}

ATTENDANCE_FORM_FIELDS = {
    "radio_till_now": "rdoTillNow",           # Till now radio button name
    "show_button": "btnShow",                 # Show button name
    "viewstate": "__VIEWSTATE",               # Hidden field ASP.NET
    "eventvalidation": "__EVENTVALIDATION"    # Hidden field ASP.NET
}
