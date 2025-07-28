class Config:
    SECRET_KEY = 'your-secret-key-change-in-production'
    
    # Flask-Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your-email@gmail.com'  # Change this
    MAIL_PASSWORD = 'your-app-password'     # Change this
    MAIL_DEFAULT_SENDER = 'your-email@gmail.com'