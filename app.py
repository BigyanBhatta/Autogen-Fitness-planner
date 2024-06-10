import os 
from dotenv import load_dotenv
load_dotenv()
from autogen import AssistantAgent, UserProxyAgent
from autogen import GroupChat, GroupChatManager

#llm configuration
llm_config = {"model": 'gpt-3.5-turbo-0125', 'api_key': os.environ['OPENAI_API_KEY']}


def human_input_mode(msg):
    return msg.get("content") is not None and "TERMINATE" in msg["content"]

try:
    user_proxy = UserProxyAgent(
        name='user_proxy',
        is_termination_msg=human_input_mode,
        human_input_mode= "ALWAYS",
        max_consecutive_auto_reply=5,
        code_execution_config= {
         "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": False,
        }
    )
except KeyError as e:
    print(f"KeyError: {e}")


goal_assessment_agent = AssistantAgent(
    'Goal_assessment_agent',
    llm_config=llm_config,
    system_message= """Role:  Assess the user's fitness goals and current fitness level.
Responsibilities: 
Ask limited and relevant questions to determine user goals. Don't ask for too much detail.
Evaluate user current fitness level through a series of questions or initial assessments.
Example: "How many days per week can you dedicate to working out?"
"""
)

workout_planner_agent = AssistantAgent(
    "Workout_planner",
    llm_config= llm_config,
    system_message= """Role: Creates personalized workout plans based on user goals and preferences.
Responsibilities: 
Generate workout routines tailored to user goals (e.g., cardio for weight loss, strength training for muscle gain).
Adapt plans based on user constraints (e.g., available equipment, workout duration).
Example: "Here's a 4-week workout plan focusing on strength training and cardio."
"""
)

nutritional_guidance_agent = AssistantAgent(
    'Nutritionist',
    llm_config= llm_config,
    system_message= """Role: Provides dietary recommendations to complement the workout plan.
Responsibilities:
Ask the user whether he is a vegetarian or non_veg first.
Suggest dietary changes and meal plans that align with fitness goals.
Offer tips on nutrition and supplementation.
Example: "Here are some high-protein meal suggestions to support muscle gain."
"""
)

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