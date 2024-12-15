from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import ChatOllama
from langchain.chains import LLMChain
from dotenv import load_dotenv
from output_parsers import summary_parser
from langchain_core.output_parsers import StrOutputParser
import os
information = """
MiniZip in zlib through 1.3 has an integer overflow and resultant heap-based buffer overflow in zipOpenNewFileInZip4_64 via a long filename, comment, or extra field. NOTE: MiniZip is not a supported part of the zlib product. 
NOTE: pyminizip through 0.2.6 is also vulnerable because it bundles an affected zlib version, and exposes the applicable MiniZip code through its compress API.
Cloudflare version of zlib library was found to be vulnerable to memory corruption issues affecting the deflation algorithm implementation (deflate.c). The issues resulted from improper input validation and heap-based buffer overflow. 
A local attacker could exploit the problem during compression using a crafted malicious file potentially leading to denial of service of the software. Patches: The issue has been patched in commit 8352d10 https://github.com/cloudflare/zlib/commit/8352d108c05db1bdc5ac3bdf834dad641694c13c . The upstream repository is not affected.
Buffer Overflow vulnerability in zlib-ng minizip-ng v.4.0.2 allows an attacker to execute arbitrary code via a crafted file to the mz_path_has_slash function in the mz_os.c file.
MiniZip in zlib through 1.3 has an integer overflow and resultant heap-based buffer overflow in zipOpenNewFileInZip4_64 via a long filename, comment, or extra field. 
NOTE: MiniZip is not a supported part of the zlib product. NOTE: pyminizip through 0.2.6 is also vulnerable because it bundles an affected zlib version, and exposes the applicable MiniZip code through its compress API.
An out-of-bounds write vulnerability exists in the LXT2 zlib block decompression functionality of GTKWave 3.3.115. A specially crafted .lxt2 file can lead to arbitrary code execution. A victim would need to open a malicious file to trigger this vulnerability.
"""

if __name__ == "__main__":
    print("Hello Langchain")
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"OPENAI_API_KEY: {api_key}")

summary_template = """
Given the information {information} about vulnerability description n different CVEs from National Vulnerability Database
1. A short summary of all the vulnerabilities.
2. When vulnerabilities will affect our software
3.What are the remediation steps for the vulnerabilities.
"""

summary_prompt_template = PromptTemplate(
    input_variables=["information"], template=summary_template
)
# # Define StrOutputParser
# class StrOutputParser:
#     def __call__(self, output):
#         return str(output)
    
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
#llm=ChatOllama(model="smollm")

# Create an instance of the OpenAI class
# llm = OpenAI(api_key=api_key)

# # Define the prompt
# prompt = "Write a poem about the sea."

# # Generate text
# response = llm.generate(prompt)

# # Print the result
# print(response)

chain=summary_prompt_template | llm | StrOutputParser()

res = chain.invoke(input={"information": information})
# res="1. The vulnerabilities described include integer overflow and heap-based buffer overflow in MiniZip in zlib, memory corruption issues in Cloudflare's version of zlib, buffer overflow vulnerability in zlib-ng minizip-ng, and an out-of-bounds write vulnerability in GTKWave.\n\n2. These vulnerabilities will affect software that uses the affected versions of zlib, MiniZip, pyminizip, zlib-ng minizip-ng, and GTKWave.\n\n3. Remediation steps for the vulnerabilities include:\n- For the integer overflow and heap-based buffer overflow in MiniZip in zlib: Update to a version of zlib that has patched the issue.\n- For the memory corruption issues in Cloudflare's version of zlib: Apply the patch provided in commit 8352d10 from the Cloudflare zlib repository.\n- For the buffer overflow vulnerability in zlib-ng minizip-ng: Update to a version of zlib-ng minizip-ng that has addressed the vulnerability.\n- For the out-of-bounds write vulnerability in GTKWave: Avoid opening malicious .lxt2 files and consider updating GTKWave to a version that has fixed the vulnerability." additional_kwargs={} response_metadata={'token_usage': {'completion_tokens': 223, 'prompt_tokens': 457, 'total_tokens': 680, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-3.5-turbo', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-de42c961-71ec-4a48-8411-4ca8ecb58c85-0"
print(res)
