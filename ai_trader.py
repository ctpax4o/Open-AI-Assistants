import dontshareconfig as d  # open ai key is in here like this key = 'jkklj;j'
from openai import OpenAI

client = OpenAI(api_key=d.key)

# Create the assistant
assistant = client.beta.assistants.create(
    name='AI Trader',
    instructions='you are a quant researcher...',
    tools=[{'type': 'code_interpreter'}],
    model='gpt-4-1106-preview'
)
print('Assistant created....')

# Create a thread
thread = client.beta.threads.create()
print('Thread created...')

# Create a message in the thread
message_response = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content='find me a trading strategy...'
)
print('Message created...')

# Access the content of the message
message_content = message_response.content[0].text.value
print("AI's response to message:", message_content)

# Create a run
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions='please address the user as king moon dev...'
)
print('Run created...')

# Retrieve the run
retrieved_run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
)
print('Run retrieved...')

# Assuming that 'retrieved_run' has a similar structure as 'message_response'
# Access the content of the run
# run_content = retrieved_run.some_attribute_here  # Update this line based on actual structure
# print("AI's response to run:", run_content)

# List messages in the thread
messages = client.beta.threads.messages.list(thread_id=thread.id)
print('Messages listed...')

# Iterate through the messages using the appropriate method
# Assuming 'messages' has an 'items' method to get the list of messages
for message in messages.items():
    # Access and print the content of each message
    # Update this line based on the actual structure of the message object
    message_content = message.content[0].text.value
    print("Message Content:", message_content)
