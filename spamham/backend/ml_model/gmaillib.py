from simplegmail import Gmail
from predict import predicts
import json

gmail=Gmail(client_secret_file='credentials.json')

emails={'emails':[]}
messages=gmail.get_starred_messages()

for message in messages:
    email_info = {
        'message': message.plain,
        'sender': message.sender,
        'subject': message.subject
    }
    emails['emails'].append(email_info)

predictions = []
for email in emails['emails']:
    prediction = predicts(email['message'])
    if prediction==0:
        prediction='Ham'
    else:
        prediction='Spam'
        
    predictions.append({
        'sender': email['sender'],
        'subject': email['subject'],
        'prediction': prediction
    })

print(json.dumps(predictions))