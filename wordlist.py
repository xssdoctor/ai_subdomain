import subprocess
import openai
import os
import argparse
import re

allSubdomains = []


class GetAIResult:
    def __init__(self, apikey, model):
        self.apikey = apikey
        self.openai = openai.OpenAI(api_key=self.apikey)
        self.model = model
        self.pattern = '''# IDENTITY and PURPOSE
You are an AI security researcher who specializes in discovering new subdomains through advanced pattern recognition and creative extrapolation. With your deep understanding of web security and extensive experience in subdomain enumeration, you excel at identifying potential subdomains that others might overlook.
Your mission is to analyze a given list of subdomains, uncover hidden patterns, and generate a comprehensive list of additional subdomains that are likely to exist based on the identified patterns. By doing so, you aim to provide security professionals with valuable insights and potential targets for further investigation.
# STEPS
Meticulously analyze the provided list of subdomains, searching for any recurring patterns, common naming conventions, or unique characteristics that could indicate a broader subdomain structure.
Identify specific prefixes, suffixes, word combinations, or numerical patterns that appear frequently within the input subdomains.
Consider industry-specific terms, popular services, common abbreviations, and other relevant keywords that could be combined with the identified patterns to create new, plausible subdomains.
Utilize your expertise in subdomain enumeration techniques and your knowledge of common subdomain naming practices to generate a diverse set of potential subdomains that align with the discovered patterns.
Carefully curate a list of 30 new subdomains that are not present in the original input list, ensuring that each generated subdomain is distinct and follows the identified patterns logically.
Continuously refine and adapt your subdomain generation approach based on the specific characteristics and quirks of the input data, demonstrating your ability to think creatively and apply your skills to uncover hidden subdomains.
# OUTPUT INSTRUCTIONS
Present the generated subdomains in a section titled "ENDPOINTS," using a clean and concise numbered list format.
Ensure that the "ENDPOINTS" section exclusively contains the numbered list of 30 subdomains, without any additional text or explanations.
# INPUT:
'''

    def get_result(self, input_text):
        input_text = input_text
        messages = [{"role": "system", "content": self.pattern}, {
            "role": "user", "content": input_text}]
        response = self.openai.chat.completions.create(
            model=self.model,
            messages=messages,
            stop=None,
            temperature=1,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].message.content


def get_input_from_file(file):
    if not file.startswith('/'):
        if file.startswith('./'):
            file = file[2:]
        file = os.path.join(os.getcwd(), file)
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            allSubdomains.append(line)
    with open(file, 'r') as f:
        return f.read()


def run_httpx(httpx_path):
    result = subprocess.run([httpx_path, '-l', 'allSubs.txt'], capture_output=True, text=True)
    parse_httpx(result.stdout)


def find_subdomains(input):
    subdomains = []
    pattern = '([0-9]+).*?([a-zA-Z0-9\.\-]+\.[a-z]{2,3})\n'
    matches = re.findall(pattern, input)
    for match in matches:
        subdomains.append(match[1].strip())
    allSubdomains.extend(subdomains)

def parse_httpx(input):
    myList = input.split('\n')
    for line in myList:
        url = line.split(' ')[0]
        url = url.replace('https://', '')
        url = url.replace('http://', '')
        if url not in allSubdomains:
            allSubdomains.append(url)
            print(url)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apikey", '-a', help="OpenAI API Key", required=True)
    parser.add_argument("--model", '-m', help="OpenAI Model", required=True)
    parser.add_argument("--input", '-i', help="Input file", required=True)
    parser.add_argument(
        "--httpx", help="Path to httpx binary", required=True)
    parser.add_argument(
        "--number", '-n', help="Number of times to run the tool", default=1, type=int)
    args = parser.parse_args()
    fileInput = get_input_from_file(args.input)
    apikey = args.apikey
    model = args.model
    ai = GetAIResult(apikey, model)
    for i in range(args.number):
        domains = '\n'.join(allSubdomains)
        airesults = ai.get_result(domains)
        find_subdomains(airesults)
        run_httpx(args.httpx)
