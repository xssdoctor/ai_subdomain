# ai_subdomain
generates unique subdomain names and runs httpx on them

# installation

requires openai and httpx
```bash
git clone https://github.com/xssdoctor/ai_subdomain.git
cd ai_subdomain
pip3 install openai
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
```

# usage

```bash
python3 wordlist.py -h
usage: wordlist.py [-h] --apikey APIKEY --model MODEL --input INPUT --httpx
                   HTTPX [--number NUMBER]

optional arguments:
  -h, --help            show this help message and exit
  --apikey APIKEY, -a APIKEY
                        OpenAI API Key
  --model MODEL, -m MODEL
                        OpenAI Model
  --input INPUT, -i INPUT
                        Input file
  --httpx HTTPX         Path to httpx binary
  --number NUMBER, -n NUMBER
                        Number of times to run the tool
```
