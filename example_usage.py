from client import PersonalAgentDualCognitionOrchestrator
import json

def test_orchestrator():
    orchestrator = PersonalAgentDualCognitionOrchestrator()
    print("=== Testing Personal Agent Dual Cognition Orchestrator Skill ===")
    
    res = orchestrator.run_benchmark_dual_cognition()
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    test_orchestrator()
