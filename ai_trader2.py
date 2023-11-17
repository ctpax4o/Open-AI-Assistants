# using our new Swarm Assistants AI 
# https://chat.openai.com/g/g-RnBKKiEhD-swarm-assistants-ai
# name ideas - HIVE 

import dontshareconfig as d  # open ai key is in here like this key = 'jkklj;j'
from openai import OpenAI

client = OpenAI(api_key=d.key)

def create_assistant(name, instructions):
    response = client.beta.assistants.create(
        model='gpt-4-1106-preview',
        name=name,
        instructions=instructions
    )
    return response.id  # Return the assistant ID

def interact_with_assistant(assistant_id, message):
    thread = client.beta.threads.create()
    message_response = client.beta.threads.messages.create(
        thread_id=thread.id,
        role='user',
        content=message
    )

    # Retrieve the message object
    retrieved_message = client.beta.threads.messages.retrieve(
        thread_id=thread.id,
        message_id=message_response.id
    )

    return process_message(retrieved_message)

def process_message(message):
    message_content = message.content[0].text
    annotations = message_content.annotations
    citations = []

    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(annotation.text, f' [{index}]')
        if (file_citation := getattr(annotation, 'file_citation', None)):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
        elif (file_path := getattr(annotation, 'file_path', None)):
            cited_file = client.files.retrieve(file_path.file_id)
            citations.append(f'[{index}] Click <here> to download {cited_file.filename}')

    message_content.value += '\n' + '\n'.join(citations)
    return message_content.value


research_assistant = create_assistant(
    name="Research Assistant",
    instructions="Research and summarize Bitcoin trading strategies."
)

def research_strategies():
    print("Researching trading strategies...")
    response = interact_with_assistant(research_assistant, "Find Bitcoin trading strategies.")
    print(response)

# Define similar functions for backtesting_assistant and optimization_assistant
def main():
    research_strategies()
    # Add calls for backtesting and optimization

main()
