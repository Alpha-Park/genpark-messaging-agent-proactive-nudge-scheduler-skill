# genpark-messaging-agent-proactive-nudge-scheduler-skill

> Proactive Contextual Nudge Scheduler for Messaging-Native Personal AI Agents. 100% Python Standard Library.

Distilled from cutting-edge personal assistants (**Poke**, **Caddy**), this skill enables messaging agents to transition from reactive question-answering into proactive life-context assistants.

## Architecture

```mermaid
flowchart TD
    EventIngest["Upcoming Event Feed (Calendar / Flight / Delivery)"] --> LeadWindow{"Delta <= Lead Time?"}
    LeadWindow -- No --> Wait["Hold in Event Registry"]
    LeadWindow -- Yes --> QuietCheck{"Current Hour in Quiet Hours?"}
    QuietCheck -- Yes (Urgency < 9) --> Suppress["Suppress / Buffer Nudge"]
    QuietCheck -- Yes (Urgency >= 9) --> UrgentBypass["Priority Bypass (80% Weight)"]
    QuietCheck -- No --> PriorityCalc["Compute Priority Score: Urgency * (1 + Progress)"]
    PriorityCalc & UrgentBypass --> Dispatch["Dispatch Micro-Nudge via iMessage/WhatsApp"]
```

## Features
- **100% Python Standard Library**: Zero external dependencies, highly auditable and embeddable.
- **Dynamic Priority Decay & Urgency Scaling**: Accurately computes when a reminder is most salient.
- **Quiet-Hours Smart Gating**: Automatically halts low-priority notifications between night hours while permitting critical emergency bypasses.
