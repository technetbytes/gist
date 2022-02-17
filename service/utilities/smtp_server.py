import smtplib , ssl

def get_context():
    context = ssl.create_default_context()
    return context

def init_smtp_server(config=None):
    try:
        # Initialize smtp server
        print(" init smtp server")
        if config is not None:
            sender_email = config.get_complete_property('smtp_server','username')
            sender_pass = config.get_complete_property('smtp_server','password')
            gateway = config.get_complete_property('smtp_server','gateway')
            port = config.get_complete_property('smtp_server','port')
        else:
            from config.setting import Config
            sender_email = Config.get_complete_property('smtp_server','username')
            sender_pass = Config.get_complete_property('smtp_server','password')
            gateway = Config.get_complete_property('smtp_server','gateway')
            port = Config.get_complete_property('smtp_server','port')

        smtp_server = smtplib.SMTP_SSL(gateway, port)
        smtp_server.ehlo() # Can be omitted, To identify yourself to the server
        smtp_server.login(sender_email, sender_pass)
        print("Login in smtp server ...")
    except Exception as e:
        # Print any error messages to stdout
        print("error :- ",e)
    return smtp_server