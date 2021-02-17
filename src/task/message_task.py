from twilio.rest import Client
import time
import schedule


def createProcessSendMenssage(account_sid, auth_token):
    client = Client(account_sid, auth_token)
    schedule.every(30).minutes.do(searchMessage).run()
    while len(schedule.jobs) > 0:
        schedule.run_pending()
        time.sleep(5)


def searchMessage():
    print('HELLO')
    return


def sendMessage(account_sid, auth_token, p_to, p_from, p_body):
    # client.api.account.messages.create(to=p_to,from_=p_from,body=p_body)
    print('HELLO')
