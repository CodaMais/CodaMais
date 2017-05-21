# Project name.
PROJECT_NAME = 'CodaMais'

# GENERAL FIELD CONSTANTS.
NULL_FIELD = 0

# USERNAME FIELDS.
USERNAME = 'Username'
USERNAME_FIELD_LENGTH = 12
USERNAME_MIN_LENGTH = 6
USERNAME_MAX_LENGHT = 12
USER_IMAGE = 'user_default.png'

# USERNAME VALIDATION MESSAGES.
USERNAME_REGISTERED = 'Nickname already registered'
USERNAME_SIZE = 'Username must be between 6 and 12 characteres'
USERNAME_FORMAT = 'Your name must have just letters'

# FIRST NAME FIELDS.
FIRST_NAME_FIELD_LENGTH = 30
FIRST_NAME = 'First name'

# FIRST NAME VALIDATION MESSAGES
FIRST_NAME_SIZE = 'Your name exceeds 30 characteres'
FIRST_NAME_CHARACTERS = 'Your name can\'t have special characters'

# PASSWORDS FIELDS.
PASSWORD_CONFIRMATION = 'Password Confirmation'
PASSWORD = 'Password'
PASSWORD_RECOVER = 'Recuperação de Senha'
PASSWORD_CHANGE = 'Mudar senha'
PASSWORD_FIELD_LENGTH = 30
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 12
PASSWORD_CONFIRMATION = 'Password confirmation'
NEW_PASSWORD = 'New password'

# PASSWORD VALIDATION MESSAGES.
PASSWORD_SIZE = 'Password must be between 8 and 12 characters'
PASSWORD_NOT_EQUAL = 'Passwords do not match.'

# EMAIL FIELDS.
EMAIL = 'Email'
EMAIL_FIELD_LENGTH = 30

# EMAIL VALIDATION MESSAGES.

EMAIL_REGISTERED = 'This Email has been already registered'
EMAIL_FORMAT = 'Enter a valid email address'
EMAIL_NOT_REGISTERED = 'This email has not been already registered'

# ACCOUNT VERIFICATION EMAIL INFO.
EMAIL_CONFIRMATION_SUBJECT = 'Confirmação da Conta'
EMAIL_CONFIRMATION_BODY = """
                          Ola %s,obrigado por se registrar.
                          Para ativar sua conta clique nesse link em menos de
                          48 horas: http://127.0.0.1:8000/user/confirm/%s
                          """
PASSWORD_RECOVER_SUBJECT = 'Recuperar senha'
PASSWORD_RECOVER_BODY = """
                         Usuario: %s
                         Para recuperar sua senha clique nesse link em menos de
                         48 horas: http://127.0.0.1:8000/user/recover/%s
                          """
CODAMAIS_EMAIL = 'codamaisapp@gmail.com'


# BUTTON NAMES
CONFIRM_BUTTON = 'Confirm'

# USER IMAGE FIELDS.
USER_IMAGE_FIELD = 'User image'

# SCORE FIELD
SCORE_MIN_LENGTH = 0
