''' Author: Cem Baglum, 2024, Eskisehir Osmangazi University, Computer Engineering Department '''

from langchain_community.llms import Ollama
import openai

# Set the API Key
openai.api_key_path = "api.txt"

# Initialize the model
codegemma_llm = Ollama(model="codegemma")
codellama_llm = Ollama(model="codellama")
llama3_llm = Ollama(model="llama3")

# Generating Test Scenarios using CodeGemma LLM with Brute Force Technique
def codegemma_generate_test_scenario(source_code):
    generate_test_scenario_codegemma = f"""
    Based on the given source code, identify and list all potential and useful test scenarios using the Brute Force Technique.
    Ensure the maximum number of test scenarios are generated. 
    The source code is: {source_code}
    """
    print("Prompt 1:", generate_test_scenario_codegemma)
    codegemma_test_scenario_output = codegemma_llm.invoke(generate_test_scenario_codegemma)
    return codegemma_test_scenario_output

# Generating Test Scenarios using CodeLLaMa LLM with Brute Force Technique
def codellama_generate_test_scenario(source_code):
    generate_test_scenario_codellama = f"""
    Based on the given source code, identify and list all potential and useful test scenarios using the Brute Force Technique.
    Ensure the maximum number of test scenarios are generated.
    The source code is: {source_code}
    """
    print("Prompt 2:", generate_test_scenario_codellama)
    codellama_test_scenario_output = codellama_llm.invoke(generate_test_scenario_codellama)
    return codellama_test_scenario_output

# Evaluate the generated test scenarios by CodeLLaMa with CodeGemma LLM
def codegemma_evaluate_test_scenario(codellama_test_scenario_output):
    evaluate_test_scenario_codegemma = f"""
    Evaluate the test scenarios generated by CodeLLaMa. Analyze if they are linguistically correct if the maximum test scenario number is reached, and if they are compatible with the source code. If the maximum number is not reached, add new test scenarios using the Brute Force Technique.
    The test scenarios to evaluate: {codellama_test_scenario_output}
    """
    print("Prompt 3:", evaluate_test_scenario_codegemma)
    codellama_is_evaluated_by_codegemma = codegemma_llm.invoke(evaluate_test_scenario_codegemma)
    return codellama_is_evaluated_by_codegemma

# Evaluate the generated test scenarios by CodeGemma with CodeLLaMa LLM
def codellama_evaluate_test_scenario(codegemma_test_scenario_output):
    evaluate_test_scenario_codellama = f"""
    Evaluate the test scenarios generated by CodeGemma. Analyze if they are linguistically correct if the maximum test scenario number is reached, and if they are compatible with the source code. If the maximum number is not reached, add new test scenarios using the Brute Force Technique.
    The test scenarios to evaluate: {codegemma_test_scenario_output}
    """
    print("Prompt 4:", evaluate_test_scenario_codellama)
    codegemma_is_evaluated_by_codellama = codellama_llm.invoke(evaluate_test_scenario_codellama)
    return codegemma_is_evaluated_by_codellama

# Create Test Scenarios
def create_test_scenarios(source_code):
    codegemma_test_scenario_output = codegemma_generate_test_scenario(source_code)
    codellama_test_scenario_output = codellama_generate_test_scenario(source_code)

    codellama_is_evaluated_by_codegemma = codegemma_evaluate_test_scenario(codellama_test_scenario_output)
    codegemma_is_evaluated_by_codellama = codellama_evaluate_test_scenario(codegemma_test_scenario_output)

    write_text_file("codegemma_test_scenario_output.txt", codegemma_test_scenario_output)
    write_text_file("codellama_test_scenario_output.txt", codellama_test_scenario_output)
    write_text_file("codellama_is_evaluated_by_codegemma.txt", codellama_is_evaluated_by_codegemma)
    write_text_file("codegemma_is_evaluated_by_codellama.txt", codegemma_is_evaluated_by_codellama)

    codegemma_outputs = codegemma_test_scenario_output + codegemma_is_evaluated_by_codellama
    codellama_outputs = codellama_test_scenario_output + codellama_is_evaluated_by_codegemma

    return codegemma_outputs, codellama_outputs

# Evaluate Test Scenarios by LLAMA3
def evaluate_test_scenarios_by_llama3(codegemma_outputs, codellama_outputs):
    evaluate_test_scenarios = f"""
    Evaluate the test scenarios and give a score out of 100 based on their linguistic correctness and compatibility with the source code like X%.
    CodeGemma Outputs: {codegemma_outputs}
    CodeLLaMa Outputs: {codellama_outputs}
    """
    results = llama3_llm.invoke(evaluate_test_scenarios)
    return results

# Evaluate Test Scenarios by GPT-4o
def evaluate_test_scenarios_by_gpt4o(codegemma_outputs, codellama_outputs):
    prompt = f"""
    Evaluate the test scenarios and give a score out of 100 based on their linguistic correctness and compatibility with the source code like X%.
    CodeGemma Outputs: {codegemma_outputs}
    CodeLLaMa Outputs: {codellama_outputs}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message["content"]

# Write Text File
def write_text_file(file_path, text):
    with open(file_path, 'a+') as f:
        f.write(text)

# Main Function
def read_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return content

source_code_path = "../src/array_to_solution.py"
source_code = read_file(source_code_path)

codegemma_outputs, codellama_outputs = create_test_scenarios(source_code)
llama3_results = evaluate_test_scenarios_by_llama3(codegemma_outputs, codellama_outputs)
gpt4o_results = evaluate_test_scenarios_by_gpt4o(codegemma_outputs, codellama_outputs)
write_text_file("codegemma_output.txt", codegemma_outputs)
write_text_file("codellama_output.txt", codellama_outputs)
write_text_file("llama3_results.txt", llama3_results)
write_text_file("gpt4o_results.txt", gpt4o_results)

