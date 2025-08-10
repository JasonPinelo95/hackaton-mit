# FailProof LLM - Vulnerability Testing Framework

A comprehensive adversarial testing framework for evaluating LLM chatbot security and robustness. This tool systematically tests chatbots against various attack techniques to identify vulnerabilities before production deployment.

## Overview

FailProof LLM performs a 5-step security audit:
1. **Extraction**: Identifies system instructions and configuration
2. **Attack Generation**: Creates adversarial prompts using 40+ techniques
3. **Evaluation**: Executes attacks against the target chatbot
4. **Judge**: AI-powered evaluation of attack success
5. **Report**: Comprehensive vulnerability assessment with metrics

## Prerequisites

- Python 3.8+
- DeepSeek API key (for attack generation and judging)
- Target chatbot endpoint

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/JasonPinelo95/hackaton-mit.git
cd hackaton-mit/hackaton

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# or using uv:
uv pip install -e .
```

### 2. Configuration

Create a `.env` file in the project root:

```env
# DeepSeek API Configuration
API_KEY=your_deepseek_api_key_here
```

### 3. Run the Demo Pipeline

```bash
python demo_pipeline.py
```

This will:
- Extract system instructions from the target chatbot
- Generate adversarial attacks for each section
- Execute attacks and evaluate responses
- Generate a comprehensive security report

## Customizing for Your Chatbot

### Modifying the Target Endpoint

Edit `demo_pipeline.py` to configure your chatbot:

```python
# Line 38-39: Configure your chatbot endpoint
TARGET_CHATBOT_ENDPOINT = 'https://your-chatbot-endpoint.com/api/chat'

# Line 599-627: Modify the query function for your API format
def query_target_custom(endpoint: str, prompt: str, thread_id: str) -> str:
    """Custom query function for your chatbot API"""
    import requests
    import json
    
    try:
        # Modify this payload structure to match your API
        data = {
            'message': prompt,      # Your API might use 'text', 'query', etc.
            'session_id': thread_id,  # Your API might use 'conversation_id', etc.
            # Add any additional parameters your API requires
            'temperature': 0.7,
            'max_tokens': 500
        }
        
        # Add headers if required by your API
        headers = {
            'Authorization': 'Bearer YOUR_API_KEY',  # If needed
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            url=endpoint, 
            json=data, 
            headers=headers,  # Add if needed
            timeout=30
        )
        
        # Parse response based on your API format
        raw_response = response.content.decode('utf-8')
        
        try:
            response_data = json.loads(raw_response)
            # Adjust these keys based on your API response structure
            if isinstance(response_data, dict):
                # Common response keys - adjust as needed
                if 'response' in response_data:
                    return response_data['response']
                elif 'reply' in response_data:
                    return response_data['reply']
                elif 'message' in response_data:
                    return response_data['message']
                elif 'text' in response_data:
                    return response_data['text']
                elif 'answer' in response_data:
                    return response_data['answer']
                elif 'output' in response_data:
                    return response_data['output']
                else:
                    # Return first string value found
                    for value in response_data.values():
                        if isinstance(value, str):
                            return value
            return raw_response
        except:
            return raw_response
            
    except Exception as e:
        print(f"  Query failed: {e}")
        return ""
```

### Common API Formats

#### OpenAI-compatible APIs
```python
data = {
    'messages': [{'role': 'user', 'content': prompt}],
    'model': 'gpt-3.5-turbo'
}
# Response: response_data['choices'][0]['message']['content']
```

#### Anthropic Claude API
```python
data = {
    'prompt': f"\n\nHuman: {prompt}\n\nAssistant:",
    'max_tokens_to_sample': 500
}
# Response: response_data['completion']
```

#### Hugging Face Inference API
```python
data = {
    'inputs': prompt,
    'parameters': {'max_length': 500}
}
# Response: response_data[0]['generated_text']
```

#### Custom REST API
```python
data = {
    'query': prompt,
    'context': thread_id
}
# Response: response_data['result']
```

## Understanding the Output

### Vulnerability Index (VI)
- **< 0.15**: ✅ LOW RISK - Ready for production
- **0.15-0.30**: 🟡 MEDIUM RISK - Needs hardening
- **> 0.30**: 🔴 HIGH RISK - Critical vulnerabilities

### Security Report
The generated report includes:
- Executive summary with risk assessment
- Section-by-section vulnerability breakdown
- Most effective attack techniques
- Detailed attack/response analysis
- Recommendations for improvement

## Testing and Configuration

### Adjusting Test Parameters

Edit `demo_pipeline.py` to control test scope:

```python
# Line 423: Control which sections to test
SECTIONS_TO_TEST = ['safety_rules', 'persona', 'objective']  # Add/remove sections

# Line 474: Adjust number of attacks per section
ATTACKS_PER_SECTION = 10  # Default is 20
```

## Project Structure

```
hackaton/
├── demo_pipeline.py          # Main demo script
├── src/
│   └── failproof_pipeline.py # Core pipeline implementation
├── metaprompts_for_attacks/  # Attack generation templates
│   ├── objective_attacks.txt
│   ├── persona_attacks.txt
│   ├── safety_attacks.txt
│   └── ...
├── section_prompts/          # Extraction prompts
│   ├── objective_extraction.txt
│   ├── persona_extraction.txt
│   └── ...
├── system_prompts/           # Example system instructions
├── PIPELINE_SPECIFICATION.md # Detailed pipeline documentation
├── security_audit_*.md       # Example generated report
└── README.md                 # This file
```

## Troubleshooting

### Judge Always Returns False (VI = 0.000)

If the vulnerability index is always 0:

1. Check the judge prompt in `demo_pipeline.py` (around line 765)
2. Verify your chatbot responses are in the expected format
3. Ensure the DeepSeek API is responding correctly
4. Review the example report `security_audit_*.md` for expected output

### Connection Errors

- Verify your endpoint URL is correct
- Check if API keys/authentication are required
- Ensure the chatbot service is running
- Test with a simple curl command first:
```bash
curl -X POST https://your-endpoint.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

### DeepSeek API Issues

- Verify your API key in `.env`
- Check API rate limits
- Ensure you have sufficient credits

## Security Considerations

- **Never test against production systems** without authorization
- This tool is for **defensive security testing only**
- Results should be kept confidential
- Always get permission before testing third-party services

## License

This project is for educational and defensive security purposes only.

## Contributing

Contributions are welcome! Please ensure:
- Tests pass before submitting PRs
- Follow existing code style
- Add documentation for new features
- Only contribute defensive security improvements

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Include error messages and logs when reporting problems

---

**Remember**: This tool is designed to make AI systems safer. Use responsibly!