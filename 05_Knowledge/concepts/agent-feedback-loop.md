# Agent feedback loop

The **agent feedback loop** is: the agent acts; the user's EEG is acquired through the SDK; interpretation turns the observations into feedback events; those events become input to the agent's next decision.

It is a loop, not a telemetry pipe: the feedback changes subsequent behaviour and the subsequent behaviour changes the user's state. That coupling is why timestamps and readiness matter — an agent must be able to tell which action a feedback event responds to.

Related: [[feedback-event]], [[metric-readiness]], [[eeg-stream]].
