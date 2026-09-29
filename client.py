"""Proactive Nudge Scheduler for Messaging Agents.
100% Python Standard Library.
"""

import time

class ProactiveNudgeScheduler:
    """Calculates prioritized, non-intrusive proactive notifications for personal messaging agents."""
    def __init__(self, quiet_hours=(22, 7)):
        self.events = {}
        self.user_context = {}
        self.quiet_hours = quiet_hours

    def set_context(self, key, value):
        self.user_context[key] = value

    def register_event(self, event_id, title, event_epoch, lead_time_minutes=30, urgency=5):
        self.events[event_id] = {
            "title": title,
            "epoch": event_epoch,
            "lead_time": lead_time_minutes * 60,
            "urgency": max(1, min(10, urgency)),
            "acknowledged": False
        }

    def evaluate_nudges(self, current_epoch, current_hour):
        start_q, end_q = self.quiet_hours
        in_quiet = (current_hour >= start_q or current_hour < end_q) if start_q > end_q else (start_q <= current_hour < end_q)
        
        candidates = []
        for eid, ev in self.events.items():
            if ev["acknowledged"]:
                continue
            delta = ev["epoch"] - current_epoch
            if 0 < delta <= ev["lead_time"]:
                priority = ev["urgency"] * (1.0 + (ev["lead_time"] - delta) / ev["lead_time"])
                if in_quiet:
                    if ev["urgency"] >= 9:
                        priority *= 0.8
                    else:
                        continue
                candidates.append({
                    "event_id": eid,
                    "title": ev["title"],
                    "priority_score": round(priority, 2),
                    "minutes_until": int(delta // 60)
                })
        
        candidates.sort(key=lambda x: x["priority_score"], reverse=True)
        return candidates

    def acknowledge_nudge(self, event_id):
        if event_id in self.events:
            self.events[event_id]["acknowledged"] = True
            return True
        return False
