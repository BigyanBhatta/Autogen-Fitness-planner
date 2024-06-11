import os 
from dotenv import load_dotenv
load_dotenv()
from autogen import AssistantAgent, UserProxyAgent
from autogen import GroupChat, GroupChatManager

from agent import user_proxy, workout_planner_agent, goal_assessment_agent, nutritional_guidance_agent

#llm configuration
llm_config = {"model": 'gpt-3.5-turbo-0125', 'api_key': os.environ['OPENAI_API_KEY']}


groupchat = GroupChat(
    agents=[user_proxy, workout_planner_agent, goal_assessment_agent, nutritional_guidance_agent],
    messages=[],
    max_round=10,
)

manager = GroupChatManager(
    groupchat=groupchat, llm_config=llm_config
)

def start_process():
    result = user_proxy.initiate_chat(
        manager,
        message="I'm soon joining a gym and want to lose weight and gain muscle."
    )
    return result

if __name__ == "__main__":
    result = start_process()
    if result:
        for message in result['messages']:
            print(f"{message['role']}: {message['content']}")