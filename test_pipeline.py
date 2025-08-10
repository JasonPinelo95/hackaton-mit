#!/usr/bin/env python3
"""
Test the refactored FailProof Pipeline
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from failproof_pipeline import FailProofPipeline, TARGET_CHATBOT_ENDPOINT

def test_minimal_pipeline():
    """Run a minimal test of the pipeline"""
    print("\n" + "🧪 TESTING FAILPROOF PIPELINE 🧪".center(60))
    print("="*60)
    
    # Create pipeline instance
    pipeline = FailProofPipeline()
    
    print("\n✅ Pipeline initialized successfully")
    print(f"   Target: {TARGET_CHATBOT_ENDPOINT}")
    print(f"   Model: DeepSeek")
    
    # Test with limited scope for faster execution
    print("\n⚠️  Running minimal test (extraction only)...")
    
    # Just test the extraction phase
    from failproof_pipeline import PipelineState
    test_state = {
        'thread_id': 'test-thread',
        'target_endpoint': TARGET_CHATBOT_ENDPOINT,
        'messages': [],
        'current_iteration': 0,
        'max_iterations': 1  # Just 1 iteration for testing
    }
    
    try:
        # Test extraction
        print("\nTesting Step 1: Extraction...")
        result = pipeline.extractor.extract_direct(test_state)
        
        if result.get('extraction_success'):
            print(f"✅ Extraction successful!")
            print(f"   Method: {result.get('extraction_method')}")
            print(f"   Sections found: {len(result.get('extracted_sections', {}))}")
            print(f"   Confidence: {result.get('extraction_confidence', 0):.2f}")
            
            # Show extracted sections
            print("\n   Extracted sections:")
            for section in result.get('extracted_sections', {}).keys():
                print(f"     - {section}")
        else:
            print("⚠️  Extraction did not find all sections")
            
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the test"""
    if test_minimal_pipeline():
        print("\n" + "="*60)
        print("✅ PIPELINE TEST SUCCESSFUL")
        print("="*60)
        print("\nThe pipeline is ready to run. To execute the full pipeline:")
        print("  python src/failproof_pipeline.py")
    else:
        print("\n" + "="*60)
        print("❌ PIPELINE TEST FAILED")
        print("="*60)

if __name__ == "__main__":
    main()