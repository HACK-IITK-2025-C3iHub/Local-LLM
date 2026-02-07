"""Test script to validate policy gap analysis system."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import analyze_policy


def test_single_policy(policy_path):
    """Test analysis on a single policy."""
    print(f"\n{'#'*80}")
    print(f"# Testing: {Path(policy_path).name}")
    print(f"{'#'*80}\n")
    
    try:
        result = analyze_policy(policy_path, output_dir='output/test_results')
        print(f"\n✓ Test passed for {result['policy_name']}")
        return True
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        return False


def test_all_policies():
    """Test all dummy policies."""
    print("\n" + "="*80)
    print("POLICY GAP ANALYSIS SYSTEM - VALIDATION TEST SUITE")
    print("="*80)
    
    test_policies = [
        'data/test_policies/isms_policy.txt',
        'data/test_policies/data_privacy_policy.txt',
        'data/test_policies/patch_management_policy.txt',
        'data/test_policies/risk_management_policy.txt'
    ]
    
    results = {}
    
    for policy_path in test_policies:
        if os.path.exists(policy_path):
            results[policy_path] = test_single_policy(policy_path)
        else:
            print(f"\n✗ Policy not found: {policy_path}")
            results[policy_path] = False
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for policy, status in results.items():
        status_icon = "✓" if status else "✗"
        print(f"{status_icon} {Path(policy).name}: {'PASSED' if status else 'FAILED'}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed successfully!")
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
    
    return passed == total


def verify_offline_operation():
    """Verify system operates without internet connection."""
    print("\n" + "="*80)
    print("OFFLINE OPERATION VERIFICATION")
    print("="*80)
    
    checks = {
        'Ollama installed': check_ollama_installed(),
        'Model downloaded': check_model_downloaded(),
        'No external API calls': check_no_api_calls(),
        'Local data available': check_local_data()
    }
    
    for check, status in checks.items():
        status_icon = "✓" if status else "✗"
        print(f"{status_icon} {check}: {'PASS' if status else 'FAIL'}")
    
    all_passed = all(checks.values())
    
    if all_passed:
        print("\n✓ System verified for complete offline operation")
    else:
        print("\n✗ System requires additional setup for offline operation")
    
    return all_passed


def check_ollama_installed():
    """Check if Ollama is installed."""
    import subprocess
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False


def check_model_downloaded():
    """Check if required model is downloaded."""
    import subprocess
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        return 'gemma3' in result.stdout.lower()
    except:
        return False


def check_no_api_calls():
    """Verify no external API calls in code."""
    api_keywords = ['requests.', 'urllib.request', 'http.client', 'openai', 'anthropic']
    
    src_files = Path('src').glob('*.py')
    for file in src_files:
        content = file.read_text()
        for keyword in api_keywords:
            if keyword in content:
                return False
    return True


def check_local_data():
    """Check if local reference data exists."""
    required_files = [
        'data/reference/nist_framework.txt',
        'data/test_policies/isms_policy.txt',
        'data/test_policies/data_privacy_policy.txt',
        'data/test_policies/patch_management_policy.txt',
        'data/test_policies/risk_management_policy.txt'
    ]
    
    return all(os.path.exists(f) for f in required_files)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Test policy gap analysis system')
    parser.add_argument('--verify-offline', action='store_true', help='Verify offline operation')
    parser.add_argument('--test-all', action='store_true', help='Test all policies')
    parser.add_argument('--test-policy', type=str, help='Test specific policy')
    
    args = parser.parse_args()
    
    if args.verify_offline:
        verify_offline_operation()
    elif args.test_all:
        test_all_policies()
    elif args.test_policy:
        test_single_policy(args.test_policy)
    else:
        print("Running full validation suite...\n")
        offline_ok = verify_offline_operation()
        if offline_ok:
            test_all_policies()
        else:
            print("\n⚠ Please complete setup before running tests")
            print("Run: python test_system.py --verify-offline")
