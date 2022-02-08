import smtplib , ssl

def get_context():
    context = ssl.create_default_context()
    return context

def init_smtp_server(config):
    try:
        # Initialize smtp server
        print(" init smtp server")
        sender_email = config['smtp_server']['username']
        sender_pass = config['smtp_server']['password']
        smtp_server = smtplib.SMTP_SSL(config['smtp_server']['gateway'], config['smtp_server']['port'])
        smtp_server.ehlo() # Can be omitted, To identify yourself to the server
        smtp_server.login(sender_email, sender_pass)
        print("Login in smtp server ...")
    except Exception as e:
        # Print any error messages to stdout
        print("error :- ",e)
    return smtp_server