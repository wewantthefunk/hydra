APP_NAME = 'Hydra'

DB_LOCATION = "data/user_db.db"

USE_ENCRYPTION = False

PRIVATE_KEY = None
MAIL = None
VERIFIED_ACCOUNT = 1
UNVERIFIED_ACCOUNT = 0

PUBLIC_EVENT = 0
PRIVATE_EVENT = 1

ATTENDEE = 99
ORGANIZER = 50
ADMIN_USER = 1
SUPER_USER = 0

USER_EMAIL_COL = 3
USER_NAME_COL = 1
USER_ID_COL = 0
USER_TYPE_COL = 4
USER_PASSPHRASE_COL = 2
USER_IS_VERIFIED_COL = 5
USER_VERIFICATION_CODE_COL = 6
USER_IS_ACTIVE_COL = 7

EVENT_ALLOW_ANONYMOUS_SIGNUPS_COL = 10
EVENT_PAYMENT_COST_COL = 13
EVENT_END_DATE_COL = 3
EVENT_END_TIME_COL = 5
EVENT_ID_COL = 0
EVENT_INVITE_TYPE_COL = 8
EVENT_INVITE_CODE_COL = 9
EVENT_LOCATION_COL = 7
EVENT_MAX_ATTENDEES_COL = 6
EVENT_NAME_COL = 1
EVENT_PAYMENT_TYPE_COL = 12
EVENT_REQUIRE_SIGNUPS_COL = 11
EVENT_SKU_COL = 14
EVENT_START_DATE_COL = 2
EVENT_START_TIME_COL = 4

EVENT_OWNER_EVENT_ID_COL = 2
EVENT_OWNER_OWNER_ID_COL = 1
EVENT_OWNER_ID_COL = 0

SESSION_USER_NAME_COL = 0
SESSION_TOKEN_COL = 1
SESSION_ISSUED_COL = 2

RESULT_OK = 200
RESULT_INVALID_REQUEST = 400
RESULT_UNVERIFIED_ACCOUNT = 401
RESULT_FORBIDDEN = 403
RESULT_NOT_FOUND = 404
RESULT_ALREADY_ATTENDING = 406
RESULT_ALREADY_VERIFIED = 406
RESULT_CONFLICT = 409
RESULT_SERVER_ERROR = 500

EVENT_OWNER = 0
EVENT_PUBLIC = 1
EVENT_ATTENDEE = 2