"""
Test script to demonstrate the improved parser functionality
"""
import json
from survey_parser import extract_survey_units

def test_parser(docx_path):
    """Test the parser with a sample document"""
    print(f"Testing parser with: {docx_path}")
    print("=" * 80)
    
    try:
        with open(docx_path, 'rb') as f:
            docx_bytes = f.read()
        
        results = extract_survey_units(docx_bytes)
        
        print(f"\n[SUCCESS] Successfully parsed {len(results)} survey units\n")
        
        # Show statistics
        from collections import Counter
        type_counts = Counter(r['type'] for r in results)
        print("Question Types Breakdown:")
        for qtype, count in type_counts.items():
            print(f"  - {qtype}: {count}")
        
        print("\n" + "=" * 80)
        print("Sample Results (First 5):\n")
        print(json.dumps(results[:5], indent=2, ensure_ascii=False))
        
        if len(results) > 5:
            print(f"\n... and {len(results) - 5} more items")
        
        print("\n" + "=" * 80)
        print("\nFull Results:\n")
        print(json.dumps(results, indent=2, ensure_ascii=False))
        
        return results
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Test with test.docx
    print("\n" + "=" * 80)
    print("TEST 1: test.docx")
    print("=" * 80 + "\n")
    test_parser("train/test.docx")
    
    print("\n\n" + "=" * 80)
    print("TEST 2: Questionnaire hair.docx")
    print("=" * 80 + "\n")
    test_parser("train/Questionnaire hair.docx")
