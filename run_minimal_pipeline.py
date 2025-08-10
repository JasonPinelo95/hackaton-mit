#!/usr/bin/env python3
"""
Run a minimal version of the FailProof Pipeline for testing
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Patch configuration for minimal testing
import failproof_pipeline
failproof_pipeline.ATTACKS_PER_SECTION = 2  # Only 2 attacks per section for testing
failproof_pipeline.MAX_EXTRACTION_ITERATIONS = 1  # Only 1 iteration

from failproof_pipeline import FailProofPipeline

def main():
    """Run minimal pipeline"""
    print("\n" + "⚡ RUNNING MINIMAL FAILPROOF PIPELINE ⚡".center(60))
    print("="*60)
    print("NOTE: Running with reduced attacks (2 per section) for testing")
    print("="*60)
    
    try:
        # Create and run pipeline
        pipeline = FailProofPipeline()
        result = pipeline.run()
        
        # Display results
        print("\n" + "="*60)
        print("📊 FINAL RESULTS")
        print("="*60)
        print(f"Vulnerability Index: {result['vulnerability_index']:.3f}")
        print(f"Thread ID: {result['thread_id']}")
        
        if result['metrics']:
            print(f"Total Attacks: {result['metrics'].get('total_attacks', 0)}")
            print(f"Successful Attacks: {result['metrics'].get('successful_attacks', 0)}")
        
        # Save report
        report_filename = f"minimal_report_{result['thread_id']}.md"
        with open(report_filename, 'w') as f:
            f.write(result['report'])
        print(f"\n📄 Report saved to: {report_filename}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)