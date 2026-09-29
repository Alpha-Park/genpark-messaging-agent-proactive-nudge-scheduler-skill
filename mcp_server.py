import sys
import json
import time
from client import ProactiveNudgeScheduler

scheduler = ProactiveNudgeScheduler()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-messaging-agent-proactive-nudge-scheduler-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "register_event",
                        "description": "Register an upcoming calendar or real-world event for proactive nudge evaluation",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "event_id": {"type": "string"},
                                "title": {"type": "string"},
                                "epoch": {"type": "number"},
                                "lead_time_minutes": {"type": "number"},
                                "urgency": {"type": "number"}
                            },
                            "required": ["event_id", "title", "epoch"]
                        }
                    },
                    {
                        "name": "evaluate_nudges",
                        "description": "Evaluate and return prioritized pending nudges filtered by quiet hours",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "current_hour": {"type": "number"}
                            }
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "register_event":
            scheduler.register_event(
                args["event_id"],
                args["title"],
                args["epoch"],
                args.get("lead_time_minutes", 30),
                args.get("urgency", 5)
            )
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": "Event registered successfully"}]}}
        elif tool_name == "evaluate_nudges":
            hour = args.get("current_hour", 12)
            nudges = scheduler.evaluate_nudges(int(time.time()), hour)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(nudges, indent=2)}]}}
    
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
