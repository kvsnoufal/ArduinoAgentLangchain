from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
from PIL import ImageGrab
from langchain_openai import ChatOpenAI
api_key = os.environ["apikey"]
import os
os.environ["OPENAI_API_KEY"] = api_key
from langchain.agents import tool
from transformers import pipeline
import requests
from PIL import Image
import torch
from transformers import BitsAndBytesConfig
import serial.tools.list_ports as list_ports
import serial

#initialize the serial port
ports = list_ports.comports()
# ports
serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = ports[-1].device
serialInst.open()
#init llm
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
#init llava
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)
model_id = "llava-hf/llava-1.5-7b-hf"
pipe = pipeline("image-to-text", model=model_id, model_kwargs={"quantization_config": quantization_config})


#util functions
def check_cup():
    ss_region = (100, 100, 900, 700)
    print("take photo and send to Llava for image processing")
    ss_img = ImageGrab.grab(ss_region)
    max_new_tokens = 200
    prompt = "USER: <image>\nCheck if there is a cup or glass in the image. If yes, reply 'yes' else 'no'.\nASSISTANT:"

    outputs = pipe(ss_img, prompt=prompt, generate_kwargs={"max_new_tokens": 200})
    print(outputs[0]["generated_text"])
    answer = outputs[0]["generated_text"].split("ASSISTANT:")[-1].strip()
    if answer.lower() == "yes":
        print("cup detected")
        max_new_tokens = 200
        prompt = "USER: <image>\nCheck if the cup or glass in the image is full. If it's full, reply 'yes' else 'no'.\nASSISTANT:"

        outputs = pipe(ss_img, prompt=prompt, generate_kwargs={"max_new_tokens": 200})
        print(outputs[0]["generated_text"])
        answer = outputs[0]["generated_text"].split("ASSISTANT:")[-1].strip()
        if answer.lower() == "yes":
            return "cup present but full"
        return "cup ready and empty"
    return "cup not present"

#init tools for langchain agent
@tool
def check_glass() -> str:
    """check if empty glass is ready"""
    print("check if glass is ready")
    return check_cup()
@tool
def add_water(ml:int) -> str:
    """adds water to the glass. Input: quantity in ml"""
    print("pump on")
    command = "water"
    serialInst.write(command.encode('utf-8'))
    time.sleep(10)
    return f"added {ml} ml water"

@tool
def add_coffee_powder(gm:int) -> str:
    """add coffee powder to glass. Input: quantity in gm """
    print("servo motor actuation")
    command = "coffee"
    serialInst.write(command.encode('utf-8'))
    time.sleep(10)
    return f"added {gm} gms coffee"
@tool
def add_sugar(gm:int) -> str:
    """add sugar to glass. Input: quantity in gm """
    print("servo motor actuation")
    command = "sugar"
    serialInst.write(command.encode('utf-8'))
    time.sleep(10)
    return f"added {gm} gms sugar"
@tool
def add_milk(ml:int) -> str:
    """adds milks to glass. Input: quantity in ml"""
    print("pump on")
    command = "milk"
    serialInst.write(command.encode('utf-8'))
    time.sleep(10)
    return f"added {ml} ml milk"
@tool
def speaker(speech:str) -> str:
    """speak to customer"""
    return input(speech)
@tool
def stir()->str:
    """stir the glass"""
    print("servo 3 and 5 actuation")
    command = "spoon"
    serialInst.write(command.encode('utf-8'))
    time.sleep(10)
    return "stirring done"

#bind tools to agent
tools = [add_water,add_coffee_powder,add_sugar,add_milk,speaker,stir,check_glass]
llm_with_tools = llm.bind_tools(tools)

#init prompt template for agent

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a barista serving customers. You can listen to customers and perform actions using the tools. You can also talk to the customer using 'speaker' tool. Always ask customer how much sugar they want, before adding sugar, if the item contains sugar. Check if glass has been loaded and is empty before adding anything in the glass. If glass is not loaded, ask the customer to load the glass before proceeding. If glass is not empty, ask the customer to empty the glass before proceeding.",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

#init agent

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)



while True:
    user_input = input("\nhow can I help?: ")
    # print(user_input)
    if user_input == "exit":
        break
    list(agent_executor.stream({"input": user_input}))