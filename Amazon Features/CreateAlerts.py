from twilio.rest import Client

account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

message = client.messages.create(
    body="New deal found: {} with {} discount!".format(deal['title'], deal['discount']),
    from_='+1234567890',
    to='+0987654321'
)

print(message.sid)
