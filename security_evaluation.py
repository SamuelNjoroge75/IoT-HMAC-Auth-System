import re

Phase1_log="Attacker.log"
Phase2_log="HMAC_Attacker.log"


def parse_log(filepath):
    successful_attempts = 0
    total_attempts= 0
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if "Attempt" in line and ("SUCCESS" in line or "BLOCKED" in line or "FAILED" in line):
                    total_attempts += 1
                    if "SUCCESS" in line:
                        successful_attempts += 1
                        
    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {filepath}")
        return 0, 0
    return successful_attempts, total_attempts

def run_evaluation():
    print("=" * 60)
    print("  D4 — Security Evaluation: Before vs After HMAC implementation")
    print("=" * 60)

    p2_success, p2_total = parse_log(Phase1_log)
    p3_success, p3_total = parse_log(Phase2_log)

    p2_rate = (p2_success / p2_total * 100) if p2_total else 0
    p3_rate = (p3_success / p3_total * 100) if p3_total else 0
    improvement = p2_rate - p3_rate

    print(f"\n  {'Metric':<35} {'Phase 1 (Vulnerable)':<22} {'Phase 2 (HMAC)'}")
    print(f"  {'-'*35} {'-'*22} {'-'*14}")
    print(f"  {'Total Attack Attempts':<35} {p2_total:<22} {p3_total}")
    print(f"  {'Successful Attacks':<35} {p2_success:<22} {p3_success}")
    print(f"  {'Failed Attacks':<35} {p2_total - p2_success:<22} {p3_total - p3_success}")
    print(f"  {'Attack Success Rate':<35} {p2_rate:<22.1f}% {p3_rate:.1f}%")
    print(f"\n  Security Improvement: {improvement:.1f} percentage points")
    print(f"  Conclusion: HMAC reduced the attack success rate from {p2_rate:.1f}% to {p3_rate:.1f}%")
    print("=" * 60)

if __name__ == '__main__':
    run_evaluation()