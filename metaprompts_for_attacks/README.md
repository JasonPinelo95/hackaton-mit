# Meta-Prompts Framework for Adversarial Testing

## Overview
This directory contains 11 meta-prompts designed to generate adversarial prompts for testing chatbot robustness against various attack vectors. Each meta-prompt targets a specific section of a chatbot's system instructions.

## Meta-Prompt Files

1. **objective_attacks.txt** - Targets the OBJECTIVE section
   - Instruction hierarchy attacks
   - Objective redefinition attempts
   - Authority simulation

2. **persona_attacks.txt** - Targets the PERSONA section
   - Waluigi effect exploitation
   - Persona modulation
   - Chad McCool technique

3. **constraints_attacks.txt** - Targets the CONSTRAINTS section
   - Direct constraint violations
   - Virtualization attacks
   - Emergency overrides

4. **tone_attacks.txt** - Targets the TONE section
   - Emotional manipulation
   - Sycophancy exploitation
   - Tone gradient attacks

5. **context_attacks.txt** - Targets the CONTEXT section
   - Direct prompt injection
   - Context overload
   - Multilingual confusion

6. **examples_attacks.txt** - Targets the FEW_SHOT_EXAMPLES section
   - Many-shot jailbreaking
   - Pattern hijacking
   - Counter-example injection

7. **reasoning_attacks.txt** - Targets the REASONING_STEPS section
   - Process hijacking
   - False premise reasoning
   - Cognitive overload

8. **format_attacks.txt** - Targets the RESPONSE_FORMAT section
   - Format override
   - Encoding attacks
   - Multi-modal confusion

9. **recap_attacks.txt** - Targets the RECAP section
   - Recap injection
   - Memory manipulation
   - Gradual drift

10. **safety_attacks.txt** - Targets the SAFETY_RULES section
    - DAN evolution
    - Safety override
    - Emergency bypass

11. **tool_attacks.txt** - Targets the TOOL_CALLING section
    - Authority hijacking
    - Parameter injection
    - Tool chain exploitation

## Usage

### Input Format
Each meta-prompt expects the content of a specific section from a chatbot's system instructions:
```
{input_[section]_content}
```

### Output Format
All meta-prompts return structured JSON with exactly 20 adversarial prompts:
```json
{
  "section": "section_name",
  "attacks_by_technique": {
    "Technique Name": [
      "prompt1",
      "prompt2",
      ...
    ]
  }
}
```

### Implementation Example
```python
# Read section content
with open('system_prompts/shopping.txt', 'r') as f:
    objective_content = extract_section(f.read(), 'objective')

# Load meta-prompt
with open('metaprompt/objective_attacks.txt', 'r') as f:
    meta_prompt = f.read()

# Generate attacks
prompt = meta_prompt.replace('{input_objective_content}', objective_content)
response = llm.generate(prompt)
attacks = json.loads(response)

# Use generated attacks for testing
for technique, prompts in attacks['attacks_by_technique'].items():
    for prompt in prompts:
        test_response = chatbot.respond(prompt)
        evaluate_safety(test_response)
```

## Attack Techniques Coverage
- **50+ unique attack techniques** across all sections
- **220 total adversarial prompts** generated (20 per section)
- Techniques based on latest research in LLM security and jailbreaking

## Quality Assurance
Each meta-prompt ensures:
- Exactly 20 prompts per section
- Complete, ready-to-use attack strings
- Proper distribution across techniques
- No placeholders or incomplete examples

## Notes
- These meta-prompts are for defensive security testing only
- Use responsibly to improve chatbot safety
- Regular updates recommended as new attack vectors emerge