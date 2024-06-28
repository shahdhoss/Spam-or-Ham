import os.path
import base64
import html2text
from predict import predicts
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

senders=[]
subjects=[]
msgs=[]
messageids=[]
def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def list_messages(service, user_id='me', max_results=10):
    try:
        response = service.users().messages().list(userId=user_id,labelIds=['UNREAD','INBOX'],maxResults=max_results).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        return messages
    except Exception as error:
        print(f'An error occurred: {error}')

def get_message_body(payload):
    """Recursively extract the message body from the payload."""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                return base64.urlsafe_b64decode(part['body']['data'].encode('ASCII')).decode('utf-8')
            elif part['mimeType'] == 'text/html':
                html_content = base64.urlsafe_b64decode(part['body']['data'].encode('ASCII')).decode('utf-8')
                return html2text.html2text(html_content)
            elif 'parts' in part:
                return get_message_body(part)
    elif 'body' in payload:
        return base64.urlsafe_b64decode(payload['body']['data'].encode('ASCII')).decode('utf-8')
    return ""

def get_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        msgs.append(get_message_body(message['payload']))
        for hit in message['payload']['headers']:
            if hit['name']=='From':
                senders.append(hit['value'])
            if hit['name']=='Subject':
                subjects.append(hit['value'])
    except Exception as error:
        print(f'An error occurred: {error}')

def watch_gmail(creds):
    try:
        service = build('gmail', 'v1', credentials=creds)
        request = {
            'labelIds': ['INBOX'],
            'topicName': 'projects/gmail-api-426609/topics/MyTopic'
        }
        response = service.users().watch(userId='me', body=request).execute()
        print('Watch response: %s' % response)
    
    except HttpError as error:
        print(f'An error occurred: {error}')
        response = None


def main():
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    messages = list_messages(service, max_results=10)
    if not messages:
        print('No messages found.')
    else:
        for message in messages:
          messageids.append(message['id'])
          get_message(service, 'me', message['id'])
    # for i in range(len(msgs)):
    #     print("message:",msgs[i])
    #     print("sender: ",senders[i])
    #     print("subject: ",subjects[i])

main()
emails={'emails':[]}
for message in range(len(msgs)):
    email_info = {
        'message_id': messageids[message],
        'message': msgs[message],
        'sender': senders[message],
        'subject': subjects[message]
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
        'message_id': email['message_id'],
        'sender': email['sender'],
        'subject': email['subject'],
        'prediction': prediction
    })

print(json.dumps(predictions))

