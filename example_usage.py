from client import ProactiveNudgeScheduler
import time

now = int(time.time())
scheduler = ProactiveNudgeScheduler(quiet_hours=(22, 7))

# Register upcoming events
scheduler.register_event("EV_FLIGHT", "Boarding Flight UA234", event_epoch=now + 1200, lead_time_minutes=30, urgency=9)
scheduler.register_event("EV_STANDUP", "Weekly Team Standup", event_epoch=now + 900, lead_time_minutes=20, urgency=4)

# Evaluate at current time (assume 14:00 daytime)
active_nudges = scheduler.evaluate_nudges(now, current_hour=14)
print("Daytime Active Nudges:")
for n in active_nudges:
    print(f" - [{n['priority_score']}] {n['title']} (in {n['minutes_until']}m)")

# Acknowledge flight
scheduler.acknowledge_nudge("EV_FLIGHT")
print("Remaining unacknowledged:", len(scheduler.evaluate_nudges(now, current_hour=14)))
