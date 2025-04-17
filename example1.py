import os
from constants import Openai_key
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import SequentialChain
import streamlit as st

# Set API key
os.environ["OPENAI_API_KEY"] = Openai_key

# Streamlit UI
st.title(' Port Security Analyzer')
input_text = st.text_input(" Enter a port number (e.g., 22, 80, 443) or protocol (e.g., FTP, SSH)")

# PROMPT 1 – What is the port used for?
port_usage_prompt = PromptTemplate(
    input_variables=['port'],
    template="What is port or protocol {port} commonly used for in networking?"
)
port_usage_memory = ConversationBufferMemory(input_key='port', memory_key='port_usage_history')

# PROMPT 2 – What are the security risks if this port is open?
port_risk_prompt = PromptTemplate(
    input_variables=['usage'],
    template="What are the common security vulnerabilities or attacks that happen if {usage} is open to the internet? Include any known injections or exploits."
)
port_risk_memory = ConversationBufferMemory(input_key='usage', memory_key='risk_history')

# PROMPT 3 – How to mitigate the risks and secure the port?
port_mitigation_prompt = PromptTemplate(
    input_variables=['risk'],
    template="How can we mitigate the risks related to {risk} and secure the system from such attacks?"
)
port_mitigation_memory = ConversationBufferMemory(input_key='risk', memory_key='mitigation_history')

# LLM setup
llm = OpenAI(temperature=0.7)

# Chains
chain1 = LLMChain(llm=llm, prompt=port_usage_prompt, verbose=True, output_key='usage', memory=port_usage_memory)
chain2 = LLMChain(llm=llm, prompt=port_risk_prompt, verbose=True, output_key='risk', memory=port_risk_memory)
chain3 = LLMChain(llm=llm, prompt=port_mitigation_prompt, verbose=True, output_key='mitigation', memory=port_mitigation_memory)

# Sequential Chain
parent_chain = SequentialChain(
    chains=[chain1, chain2, chain3],
    input_variables=['port'],
    output_variables=['usage', 'risk', 'mitigation'],
    verbose=True
)

# On user input
if input_text:
    response = parent_chain({'port': input_text})
    st.subheader("Port/Protocol Usage:")
    st.write(response['usage'])

    st.subheader(" Risks & Exploits:")
    st.write(response['risk'])

    st.subheader("Mitigation & Hardening Steps:")
    st.write(response['mitigation'])

    with st.expander('Usage Memory'): 
        st.info(port_usage_memory.buffer)

    with st.expander('Risk Memory'): 
        st.info(port_risk_memory.buffer)

    with st.expander(' Mitigation Memory'): 
        st.info(port_mitigation_memory.buffer)
