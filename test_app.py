import unittest
import json
from app import app, mysql

class FlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Clean up the database
        self.app_context.pop()

    def test_create_user_and_chat(self):
        print()
        print("-----------------------------")
        print()
        print("TEST CASE: test_create_user_and_chat")
        # Create a new user
        response = self.app.post('/new', 
                                 data=json.dumps({'name': 'John Doe'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        response_data = json.loads(response.data)
        user_uuid = response_data['uuid']
        self.assertIsNotNone(user_uuid)

        # Verify the user is in the database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE uuid = %s", (user_uuid,))
        user = cursor.fetchone()
        print(f"User in DB: {user}")
        self.assertIsNotNone(user)
        self.assertEqual(user[1], 'John Doe')

        # Start a chat with the created user
        response = self.app.post('/message', 
                                 data=json.dumps({
                                     'chat_id': user_uuid,
                                     'sender': 'user',
                                     'message': 'My patient has a headache.'
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response_data = json.loads(response.data)
        self.assertIn('response', response_data)
        self.assertIsNotNone(response_data['response'])

        # Verify the message is in the database
        cursor.execute("SELECT * FROM messages WHERE user_uuid = %s", (user_uuid,))
        messages = cursor.fetchall()
        print(f"Messages in DB: {messages}")
        self.assertEqual(len(messages), 2)  # One user message and one bot response
        cursor.close()

    def test_clear_chat_history(self):
        print()
        print("-----------------------------")
        print()
        print("TEST CASE: test_clear_chat_history")

        # Create a new user
        response = self.app.post('/new', 
                                 data=json.dumps({'name': 'Jane Doe'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        response_data = json.loads(response.data)
        user_uuid = response_data['uuid']
        self.assertIsNotNone(user_uuid)

        # Start a chat with the created user
        self.app.post('/message', 
                      data=json.dumps({
                          'chat_id': user_uuid,
                          'sender': 'user',
                          'message': 'My patient has a cough.'
                      }),
                      content_type='application/json')

        # Clear chat history
        response = self.app.delete(f'/messages/{user_uuid}')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'Chat history cleared')

        # Verify the chat history is cleared
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM messages WHERE user_uuid = %s", (user_uuid,))
        messages = cursor.fetchall()
        print(f"Messages in DB after clearing: {messages}")
        self.assertEqual(len(messages), 1)  # Only the initial prompt should remain
        cursor.close()

    def test_get_messages(self):
        print()
        print("-----------------------------")
        print()
        print("TEST CASE: test_get_messages")
        # Create a new user
        response = self.app.post('/new', 
                                 data=json.dumps({'name': 'Alice'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        response_data = json.loads(response.data)
        user_uuid = response_data['uuid']
        self.assertIsNotNone(user_uuid)

        # Start a chat with the created user
        self.app.post('/message', 
                      data=json.dumps({
                          'chat_id': user_uuid,
                          'sender': 'user',
                          'message': 'What are the side effects of Atocor 5 Tablet?'
                      }),
                      content_type='application/json')

        # Get messages
        response = self.app.get(f'/messages/{user_uuid}')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 2)  # One user message and one bot response

        messages = response_data
        self.assertEqual(messages[0]['sender'], 'user')
        self.assertEqual(messages[0]['message'], 'What are the side effects of Atocor 5 Tablet?')
        self.assertEqual(messages[1]['sender'], 'bot')
        self.assertIn('side effects', messages[1]['message'])

if __name__ == '__main__':
    unittest.main()
