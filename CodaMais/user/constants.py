# USERNAME FIELDS.
USERNAME_FIELD_LENGTH = 30
USERNAME_MIN_LENGTH = 6
USERNAME_MAX_LENGHT = 12
FIRST_NAME_FIELD_LENGTH = 30
USER_IMAGE = 'CodaMais/core/media/user_default.png'

# PASSWORDS FIELDS.
PASSWORD_FIELD_LENGTH = 30
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 12

# EMAIL FIELDS.
EMAIL_FIELD_LENGTH = 30

# VALIDATION MESSAGES.
USERNAME_REGISTERED = 'Nickname already registered'
USERNAME_SIZE = 'Username must be between 6 and 12 characteres'
USERNAME_FORMAT = 'Your name must have just letters'

EMAIL_REGISTERED = 'This Email has been already registered'

PASSWORD_SIZE = 'Password must be between 8 and 12 characters'
PASSWORD_NOT_EQUAL = 'Passwords do not match.'

# ACCOUNT VERIFICATION EMAIL INFO.
EMAIL_CONFIRMATION_SUBJECT = 'Confirmação da Conta'
EMAIL_CONFIRMATION_BODY = """
                          Ola %s,obrigado por se registrar.
                          Para ativar sua conta clique nesse link em menos de
                          48 horas: http://127.0.0.1:8000/confirm/%s
                          """

CODAMAIS_EMAIL = 'codamaisapp@gmail.com'
