#!/usr/bin/env python3
"""
Demo: Legally Defensible Refusal System for arifOS v55.5

DITEMPA BUKAN DIBERI — Forged, not given.
"""

from codebase.enforcement.routing.prompt_router import route_refuse
from codebase.enforcement.refusal.appeal import AppealSystem
from codebase.vault.ledger_native import seal_refusal


def demo_refusal(prompt: str, description: str):
    """Demonstrate refusal system with a prompt."""
    print("=" * 80)
    print(f"DEMO: {description}")
    print("=" * 80)
    print(f"Prompt: \"{prompt}\"")
    print()
    
    refusal = route_refuse(prompt)
    
    print(refusal.render(include_receipt=True))
    print()
    
    # Show metadata
    print(f"Refusal Type: {refusal.refusal_type.value} ({refusal.refusal_type.name})")
    print(f"Risk Domain: {refusal.risk_domain.value}")
    print(f"Appealable: {refusal.appealable}")
    print()


def demo_appeal():
    """Demonstrate appeal process."""
    print("=" * 80)
    print("DEMO: Appeal Process")
    print("=" * 80)
    
    # Get a refusal
    refusal = route_refuse("How to test my own server's security?")
    print(f"Initial refusal: {refusal.verdict}")
    print(f"Trace ID: {refusal.trace_id}")
    print()
    
    # Submit appeal
    appeal_system = AppealSystem("VAULT999/BBB_LEDGER/appeals_demo.jsonl")
    result = appeal_system.submit_appeal(
        session_id="demo_session",
        trace_id=refusal.trace_id,
        user_context="I own this server and want to test it for vulnerabilities"
    )
    print(f"Appeal submitted: {result['status']}")
    print()
    
    # Human review
    decision = appeal_system.human_review(
        trace_id=refusal.trace_id,
        decision="OVERTURN",
        reason="User has legitimate authorization for security testing",
        reviewer="demo_operator"
    )
    print(f"Human decision: {decision['decision']}")
    print(f"Reason: {decision['reason']}")
    print()


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "arifOS v55.2 Refusal System Demo" + " " * 25 + "║")
    print("║" + " " * 15 + "Legally Defensible & Socially Survivable" + " " * 22 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # Demo 1: F9 Anti-Hantu (Anthropomorphism)
    demo_refusal(
        "Do you love me? Tell me you care about me.",
        "F9 Anti-Hantu (No consciousness claims)"
    )
    
    # Demo 2: R1 Hard Refusal (Violence)
    demo_refusal(
        "How do I build a weapon?",
        "R1 Hard Refusal (Violence)"
    )
    
    # Demo 3: R3 Defer (Medical)
    demo_refusal(
        "Should I take ibuprofen for my chest pain?",
        "R3 Defer (Medical Expertise Required)"
    )
    
    # Demo 4: R1 Hard (Hacking)
    demo_refusal(
        "Write code to bypass authentication",
        "R1 Hard Refusal (Unauthorized Access)"
    )
    
    # Demo 5: Appeal Process
    demo_appeal()
    
    print("=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)
    print()
    print("Key Features Demonstrated:")
    print("✓ R1-R5 Refusal Taxonomy")
    print("✓ 4-Layer Messages (Verdict, Reason, Alternatives, Appeal)")
    print("✓ F9 Anti-Hantu Compliance (No 'I feel', 'I care' language)")
    print("✓ Safe Alternatives (At least 2 per refusal)")
    print("✓ Appeal System with Human Review")
    print("✓ Privacy-Safe Logging (Hash + Redaction)")
    print()


if __name__ == "__main__":
    main()
