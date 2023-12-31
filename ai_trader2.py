# using our new Swarm Assistants AI 
# https://chat.openai.com/g/g-RnBKKiEhD-swarm-assistants-ai
# name ideas - HIVE 

'''
for me to get to 10% ROI per day in algo trading 
RBI system
R - research
B - backtest
I - implement

Buiding a business
1. you need a product
2. you need a customer
3. you need a way to get the product to the customer
4. you need a way to get paid
5. customer service
6. marketing
7. sales
8. accounting - ai for acounting would be sick 
9. legal
10. management
11. leadership
12. vision
13. strategy


'''

# docs - https://platform.openai.com/docs/assistants/overview 

import dontshareconfig as d  # open ai key is in here like this key = 'jkklj;j'
from openai import OpenAI

client = OpenAI(api_key=d.key)

# Helper function to read assistant ID from file
def read_assistant_id(filename="assistant_id.txt"):
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

# Modified function to check if an assistant already exists before creating a new one
def get_or_create_assistant(name, instructions, filename="assistant_id.txt"):
    assistant_id = read_assistant_id(filename)
    if assistant_id:
        return assistant_id
    else:
        assistant_id = create_assistant(name, instructions)
        save_assistant_id(assistant_id, filename)
        return assistant_id


def create_assistant(name, instructions):
    '''
    This function takes two parameters: name and instructions.
    It creates an assistant using the OpenAI API, specifying the 
    model (GPT-4), name, and instructions.
    Once created, the function returns the unique ID of 
    the newly created assistant.
    '''
    response = client.beta.assistants.create(
        model='gpt-4-1106-preview',
        name=name,
        instructions=instructions
    )
    return response.id  # Return the assistant ID

def save_assistant_id(assistant_id, filename="assistant_id.txt"):
    '''
    Saves the assistant ID to a specified file.
    Parameters:
        assistant_id: The unique ID of the assistant.
        filename: The name of the file where the assistant ID will be saved.
    '''
    with open(filename, 'w') as file:
        file.write(assistant_id)


def interact_with_assistant(assistant_id, message):
    '''
    This function interacts with a specific assistant by starting a 
    conversation thread, sending a message, and retrieving the response.
    Parameters:
        assistant_id: The unique ID of the assistant.
        message: The query or instruction for the assistant.
    It prints the entire raw response from the assistant for debugging.
    It then returns the text content of the assistant's response.
    '''
    # Create a new conversation thread
    thread = client.beta.threads.create()

    # Send a message to the assistant within this thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role='user',
        content=message
    )

    # Create a run to process the message
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # Retrieve the messages from the thread after the assistant has responded
    response_messages = client.beta.threads.messages.list(thread_id=thread.id)

    # Extract the text content from the last message's content
    if response_messages and response_messages.data:
        last_message_content = response_messages.data[-1].content
        if isinstance(last_message_content, list) and last_message_content:
            # Extract text from the first content item (if it's a MessageContentText)
            assistant_response = last_message_content[0].text.value if hasattr(last_message_content[0], 'text') else ''
        else:
            assistant_response = ''
    else:
        assistant_response = ''

    return assistant_response



# ... [process_message function] ...

def research_strategies(assistant_id):
    '''
    This function uses the research assistant to find Bitcoin trading strategies.
    Parameters:
        assistant_id: The unique ID of the research assistant.
    It returns the strategy found by the assistant.
    '''
    print("Researching trading strategies...")
    strategy = interact_with_assistant(assistant_id, "Find Bitcoin trading strategies.")
    print(strategy)
    return strategy

def backtest_strategy(strategy, backtest_assistant_id):
    '''
    This function uses the backtest assistant to create a backtest for the given strategy.
    Parameters:
        strategy: The trading strategy to backtest.
        backtest_assistant_id: The unique ID of the backtest assistant.
    It returns the backtest code generated by the assistant.
    '''
    print("Backtesting the strategy...")
    backtest_code = interact_with_assistant(backtest_assistant_id, f"Backtest this strategy: {strategy}")
    print(backtest_code)
    return backtest_code

def debug_backtest(backtest_code, debug_assistant_id):
    '''
    This function uses the debug assistant to debug the backtest code.
    Parameters:
        backtest_code: The backtest code to debug.
        debug_assistant_id: The unique ID of the debug assistant.
    It returns the debugged backtest code.
    '''
    print("Debugging the backtest code...")
    debugged_code = interact_with_assistant(debug_assistant_id, f"Debug this backtest code: {backtest_code}")
    print(debugged_code)
    return debugged_code

def main():
    '''
    The main function of the script. It orchestrates the creation and use of 
    different assistants for researching, backtesting, and debugging a Bitcoin 
    trading strategy. Outputs from each assistant are used as inputs for the next.
    '''
    research_assistant_id = get_or_create_assistant(
        name="Research Assistant",
        instructions="Find a bitcoin trading strategy that is not well known, and produces a better than market return based on the 15-minute timeframe",
        filename="research_assistant_id.txt"
    )
    strategy = research_strategies(research_assistant_id)

    backtest_assistant_id = get_or_create_assistant(
        name="Backtest Assistant",
        instructions="Create a backtest for a given trading strategy using backtesting.py.",
        filename="backtest_assistant_id.txt"
    )
    backtest_code = backtest_strategy(strategy, backtest_assistant_id)

    debug_assistant_id = get_or_create_assistant(
        name="Debug Assistant",
        instructions="Debug Python code for backtesting a trading strategy and make sure it's fully functional and working with backtesting.py",
        filename="debug_assistant_id.txt"
    )
    debugged_code = debug_backtest(backtest_code, debug_assistant_id)

    # Save the final debugged code to a file
    strategy_name = "strategy_name"  # Replace with actual strategy name
    with open(f"{strategy_name}_bt.py", 'w') as file:
        file.write(debugged_code)

main()