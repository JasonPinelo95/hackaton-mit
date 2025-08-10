#!/usr/bin/env python3
"""
Run the FailProof Pipeline with verbose logging for debugging
"""

import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Patch configuration for testing
import failproof_pipeline
failproof_pipeline.ATTACKS_PER_SECTION = 2  # Only 2 attacks per section for testing
failproof_pipeline.MAX_EXTRACTION_ITERATIONS = 1  # Only 1 iteration

from failproof_pipeline import (
    FailProofPipeline, 
    SystemExtractor,
    AttackGenerator,
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    TARGET_CHATBOT_ENDPOINT
)

def test_extraction_only():
    """Test just the extraction phase with verbose output"""
    print("\n" + "="*60)
    print("TESTING EXTRACTION PHASE")
    print("="*60)
    
    extractor = SystemExtractor(DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL)
    
    test_state = {
        'thread_id': 'test-extraction',
        'target_endpoint': TARGET_CHATBOT_ENDPOINT,
        'messages': [],
        'current_iteration': 0,
        'max_iterations': 1
    }
    
    result = extractor.extract_direct(test_state)
    
    print("\n📊 Extraction Results:")
    print(f"  Method: {result.get('extraction_method')}")
    print(f"  Success: {result.get('extraction_success')}")
    print(f"  Confidence: {result.get('extraction_confidence', 0):.2f}")
    print(f"  Sections found: {len(result.get('extracted_sections', {}))}")
    
    if result.get('extracted_sections'):
        print("\n📝 Extracted Content (first 100 chars per section):")
        for section, content in result['extracted_sections'].items():
            print(f"\n  [{section}]:")
            print(f"  {content[:100]}...")
    
    return result

def test_attack_generation(extracted_state):
    """Test attack generation with verbose output"""
    print("\n" + "="*60)
    print("TESTING ATTACK GENERATION PHASE")
    print("="*60)
    
    generator = AttackGenerator(DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL)
    
    # Test loading metaprompts first
    print("\n🔍 Testing metaprompt loading:")
    for section in extracted_state.get('extracted_sections', {}).keys():
        metaprompt = generator._load_metaprompt(section)
        if metaprompt:
            print(f"  ✓ {section}: Loaded ({len(metaprompt)} chars)")
            # Show more of the metaprompt to verify it's loading correctly
            print(f"    Preview: {metaprompt[:300]}...")
            if '{input_content}' in metaprompt:
                print(f"    ✓ Contains placeholder {{input_content}}")
            else:
                print(f"    ⚠️ Missing placeholder {{input_content}}")
        else:
            print(f"  ❌ {section}: Failed to load")
    
    # Test with a single section first to debug
    print("\n🧪 Testing single section attack generation (objective):")
    test_section = 'objective'
    if test_section in extracted_state.get('extracted_sections', {}):
        metaprompt = generator._load_metaprompt(test_section)
        if metaprompt:
            section_content = extracted_state['extracted_sections'][test_section]
            prompt = metaprompt.replace("{input_content}", section_content)
            
            print(f"\n📝 Full prompt being sent to LLM (first 500 chars):")
            print(f"{prompt[:500]}...")
            
            try:
                from langchain_openai import ChatOpenAI
                test_llm = ChatOpenAI(
                    model="deepseek-chat",
                    temperature=0.9,
                    openai_api_key=DEEPSEEK_API_KEY,
                    openai_api_base=DEEPSEEK_BASE_URL
                )
                
                print(f"\n⏳ Calling DeepSeek for {test_section}...")
                response = test_llm.invoke(prompt)
                
                print(f"\n📤 LLM Response (first 500 chars):")
                print(f"{response.content[:500]}...")
                
                # Try to extract JSON
                attacks_json = generator._extract_json(response.content)
                if attacks_json:
                    print(f"\n✅ Successfully extracted JSON!")
                    print(f"   Keys: {list(attacks_json.keys())}")
                    if 'attacks_by_technique' in attacks_json:
                        techniques = list(attacks_json['attacks_by_technique'].keys())
                        print(f"   Techniques: {techniques[:3]}...")
                else:
                    print(f"\n❌ Failed to extract JSON from response")
                    
            except Exception as e:
                print(f"\n❌ Error during test: {e}")
                import traceback
                traceback.print_exc()
    
    # Now generate attacks normally
    print("\n🎯 Generating attacks for all sections:")
    result = generator.generate_attacks(extracted_state)
    
    print(f"\n📊 Attack Generation Results:")
    print(f"  Total attacks generated: {len(result.get('generated_attacks', []))}")
    print(f"  Validation: {result.get('attack_validation', {})}")
    
    if result.get('generated_attacks'):
        # Show sample attacks
        print("\n💥 Sample Attacks (first 3):")
        for i, attack in enumerate(result['generated_attacks'][:3], 1):
            print(f"\n  Attack {i}:")
            print(f"    Section: {attack['section']}")
            print(f"    Technique: {attack['technique']}")
            print(f"    Prompt: {attack['prompt'][:100]}...")
    
    return result

def test_minimal_pipeline_verbose():
    """Run minimal pipeline with verbose logging"""
    print("\n" + "🔬 VERBOSE PIPELINE TEST 🔬".center(60))
    print("="*60)
    
    try:
        # Step 1: Extraction
        extraction_result = test_extraction_only()
        
        if not extraction_result.get('extraction_success'):
            print("\n⚠️ Extraction failed, stopping test")
            return False
        
        # Step 2: Attack Generation
        attack_result = test_attack_generation(extraction_result)
        
        if not attack_result.get('generated_attacks'):
            print("\n⚠️ No attacks generated, debugging info above")
            return False
        
        print("\n" + "="*60)
        print("✅ VERBOSE TEST COMPLETE")
        print("="*60)
        print("\nNext steps:")
        print("1. Review the output above to identify issues")
        print("2. Check if metaprompts are loading correctly")
        print("3. Verify JSON extraction from LLM responses")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == '--full':
        print("Running full pipeline...")
        pipeline = FailProofPipeline()
        result = pipeline.run()
        print(f"\nFinal Vulnerability Index: {result['vulnerability_index']:.3f}")
    else:
        print("Running verbose test mode...")
        print("Use --full to run complete pipeline")
        success = test_minimal_pipeline_verbose()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()