import sys, json
from client import PersonalAgentDualCognitionOrchestrator

def handle_mcp():
    orchestrator = PersonalAgentDualCognitionOrchestrator()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(orchestrator.run_benchmark_dual_cognition(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-personal-agent-dual-cognition-orchestrator-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "orchestrate_personal_turn", "description": "Execute unified personal agent turn.", "inputSchema": {"type": "object", "properties": {"ambient_context": {"type": "object"}, "raw_input": {"type": "string"}}}},
                    {"name": "evaluate_cognitive_budget", "description": "Monitor and cap token expenditure.", "inputSchema": {"type": "object"}},
                    {"name": "synthesize_ambient_decision_packet", "description": "Compile ambient, episodic, proactive, and typed actions.", "inputSchema": {"type": "object"}},
                    {"name": "run_benchmark_dual_cognition", "description": "Run comprehensive dual-cognition benchmark.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "orchestrate_personal_turn":
                    res = orchestrator.orchestrate_personal_turn(args.get("ambient_context", {}), args.get("raw_input", ""))
                elif tname == "evaluate_cognitive_budget":
                    res = orchestrator.evaluate_cognitive_budget()
                elif tname == "synthesize_ambient_decision_packet":
                    res = orchestrator.synthesize_ambient_decision_packet(args.get("meta_sensors", {}), args.get("muse_memory", {}), args.get("instinct_candidate", {}), args.get("jev_route", {}))
                else:
                    res = orchestrator.run_benchmark_dual_cognition()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "
")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "
")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
