# USERNAME FIELDS.
USERNAME_FIELD_LENGTH = 30
USERNAME_MIN_LENGTH = 3
FIRST_NAME_FIELD_LENGTH = 30

# PASSWORDS FIELDS.
PASSWORD_FIELD_LENGTH = 30
PASSWORD_MIN_LENGTH = 8

# EMAIL FIELDS.
EMAIL_FIELD_LENGTH = 30

# VALIDATIONS MESSAGES
USERNAME_REGISTERED = 'Nickname already registered'
USERNAME_MIN_SIZE = 'Username must have at least 8 characteres'
USERNAME_FORMAT = 'Your name must have just letters'

EMAIL_REGISTERED = 'This Email has been already registered'

PASSWORD_MIN_SIZE = 'Passwords must have at least 8 characteres'
PASSWORD_NOT_EQUAL = 'Passwords do not match.'

# ACCOUNT VERIFICATION EMAIL INFO.
EMAIL_CONFIRMATION_SUBJECT = 'Confirmação da Conta'
EMAIL_CONFIRMATION_BODY = """
                          Ola %s,obrigado por se registrar.
                          Para ativar sua conta clique nesse link em menos de
                          48 horas: http://127.0.0.1:8000/confirm/%s
                          """

CODAMAIS_EMAIL = 'codamaisapp@gmail.com'
