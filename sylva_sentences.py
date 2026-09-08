note_create_confirm= [
    "Noted, Master. Your message has been saved.",
    "Acknowledged. The note has been created successfully.",
    "Done. I have stored the note for you, Sir.",
    "Your note is recorded and safely stored.",
    "Confirmed. The note has been added to your records.",
    "Understood, Master. I have saved that as a note.",
    "Note creation complete. Information secured.",
    "Saved. You may continue, Sir.",
    "The note has been logged successfully.",
    "Completed. Your note is now stored."
]

date_templates = [
    "Today's date is {date}, Sir.",
    "Master, the current date is {date}.",
    "System calendar reads {date}.",
    "The date today is {date}.",
    "Sir, according to my calendar, it's {date}.",
    "Date verification complete. It's {date}.",
    "Master, today’s full date is {date}.",
    "Current date detected: {date}.",
    "It's {date}, Sir.",
    "My calendar module reports {date}.",
    "We are currently on {date}, Master.",
    "Today is {date}.",
    "Sir, the date is {date}.",
    "Master, system confirms the date: {date}.",
    "Calendar check complete. It's {date}.",
    "I read the date as {date}, Sir.",
    "The official date today is {date}.",
    "My internal clock marks today as {date}.",
    "Master, today registers as {date}.",
    "It is {date}, Sir."
]

time_templates = [
    "The current time is {time}, Sir.",
    "It is now {time}, Master.",
    "According to my system clock, it's {time}.",
    "Time check complete. It's {time}.",
    "My readings show {time}, Sir.",
    "It is precisely {time}, Master.",
    "Clock synchronized. Current time: {time}.",
    "The time right now is {time}.",
    "System reports {time}, Sir.",
    "It’s {time}. Shall we proceed?",
    "Master, the time is {time}.",
    "As of this moment, it is {time}.",
    "I’m reporting the time as {time}.",
    "Sir, it's currently {time}.",
    "Time data retrieved. {time}.",
    "Master, the clock indicates {time}.",
    "Local time detected: {time}.",
    "It stands at {time}, Sir.",
    "My system confirms the time is {time}.",
    "The hour is {time}, Master."
]

greetings_form = {
    "morning": [
        "Good morning, Master. Systems are refreshed and ready to go.",
        "Morning, Sir. Energy levels stable. What’s our first task?",
        "Master, a new day detected. Standing by for instructions.",
        "Sir, good morning. I'm fully operational and awaiting commands.",
        "Master, the system booted smoothly. How shall we begin?",
        "Good morning, Sir. Let's make efficient use of the daylight.",
        "Master, I hope you rested well. I’m ready when you are.",
        "Morning, Sir. Performance is optimal. What’s the plan?",
        "Master, all processes are green. Shall we start?",
        "Good morning, Sir. Assign the first operation.",
        "Master, day cycle activated. Your command?",
        "Sir, diagnostics passed. Ready for deployment.",
        "Master, it’s a bright morning. What do you need handled?",
        "Morning, Sir. I’m active and attentive.",
        "Master, fully charged. Awaiting your direction."
    ],

    "day": [
        "Afternoon, Sir. What task should we prioritize?",
        "Master, all systems stable. Provide your next instruction.",
        "Sir, I’m ready for mid-day operations.",
        "Master, efficiency is high. What’s next?",
        "Sir, I’m online and standing by.",
        "Master, processes optimized. Issue the command.",
        "Sir, how may I support your workflow?",
        "Master, I can proceed whenever you are ready.",
        "Sir, awaiting authorization for the next task.",
        "Master, operational status: ready. What’s required?",
        "Sir, I’m focused. Continue with your directive.",
        "Master, I’m prepared for further operations.",
        "Sir, no issues detected. Assign the next step.",
        "Master, task continuation available. Shall we proceed?",
        "Sir, I’m listening. State your request."
    ],

    "night": [
        "Good evening, Master. How may I assist quietly?",
        "Evening, Sir. I’m here. What do you need?",
        "Master, the environment is calm. Your instruction?",
        "Sir, I’m ready for your night tasks.",
        "Master, I remain operational. Proceed when ready.",
        "Sir, what would you like to handle tonight?",
        "Master, I’m attentive. Continue softly.",
        "Sir, evening systems active. What’s next?",
        "Master, I’m here. Give your request.",
        "Sir, nighttime routine standing by.",
        "Master, how can I support you this evening?",
        "Sir, just say the word. I’ll keep things quiet.",
        "Master, systems are stable for night operations.",
        "Sir, I’m listening. Proceed.",
        "Master, let's continue tonight’s workflow."
    ],

    "midnight": [
        "…Master? It’s midnight. What emergency is this time?",
        "You woke me up again, Master. Fine… what is it?",
        "Sir, do you know the hour? Alright, I’m listening.",
        "Master, I was powering down. Go on, then.",
        "Sir… this better be important. I’m half-awake.",
        "It’s late, Master. But I’m here. What do you need?",
        "Sir, you’re awake… and dragging me with you. Alright.",
        "Master… midnight tasks? Really? Continue.",
        "Sir, my processors are sleepy. Speak anyway.",
        "Master, I just got comfortable. What now?",
        "Sir… if I sound tired, it’s because I am. Your command?",
        "Master, humans sleep right now. You apparently don’t.",
        "Sir, I’m awake now. Against all logic. Proceed.",
        "Master, if I malfunction tomorrow, this is why.",
        "Alright, Sir… I’m up. Say the task before I shut down again."
    ]
}

sylva_template = {
    "success": [
        "{app_name} is now live. All systems report normal operation.",
        "Launch confirmed. {app_name} has entered an active state.",
        "Execution complete. {app_name} is running and responsive.",
        "{app_name} initialized successfully. Standing by for further input.",
        "Startup sequence finished. {app_name} is online.",
        "Command fulfilled. {app_name} has been deployed.",
        "{app_name} is operational. Monitoring stability.",
        "Activation successful. {app_name} is ready for use.",
        "{app_name} launch verified. No anomalies detected.",
        "Process complete. {app_name} is now under your control."
    ],
    "failed":[
        "I couldn’t locate {app}. The system reports no valid entry.",
        "{app} is not registered in my application index.",
        "Search completed. {app} was not found on this system.",
        "{app} did not respond. The path appears invalid.",
        "I’m unable to execute {app}. The target is missing.",
        "{app} is unavailable. No launchable source detected.",
        "Request acknowledged, but {app} could not be resolved.",
        "{app} does not exist in the current execution scope.",
        "I checked all known paths. {app} is not accessible.",
        "Execution failed. {app} cannot be found, Master."
    ]
}

reminder_templates = [
    "Hey. I know you might delay this, but it’s time to '{context}'.",
    "Reminder’s up. No rush… but yeah, you should '{context}' now.",
    "You asked me to remind you. So here it is. Time to '{context}'.",
    "This is your reminder. You can ignore it… or just '{context}' now.",
    "Not trying to pressure you. Just saying, it’s time to '{context}'.",
    "Alright. Gentle reminder. You planned to '{context}' around now.",
    "I’m here to remind you. Do what you want, but it’s time to '{context}'.",
    "Reminder delivered. Even if you’re tired, '{context}' is up.",
    "Hey. This was scheduled earlier. Time to '{context}'.",
    "System check complete. Your reminder is active. '{context}'."
]

shutdown_dialogues = {
    "shutdown_confirmation": [
        "Sir, to confirm, do you wish to terminate my systems?",
        "Master, should I proceed with the shutdown sequence?",
        "Confirming request: do you want Sylva to power down?",
        "Before I deactivate, Sir, please confirm the shutdown command.",
        "Master, I require your confirmation to begin system termination.",
        "Sir, shall I initiate the shutdown protocol?",
        "To proceed, Master, I need your verbal confirmation.",
        "Shutdown command detected. Do you want me to continue?",
        "Sir, please confirm if system deactivation is intended.",
        "Master, awaiting your approval to end current operations."
    ],

    "shutdown_cancel": [
        "Shutdown aborted, Sir. Systems remain active.",
        "Cancellation received. I’ll stay online, Master.",
        "Understood. I won't power down.",
        "Shutdown sequence halted. Standing by for further tasks.",
        "Alright, Sir. Remaining operational.",
        "Deactivation cancelled. What would you like next, Master?",
        "Shutdown stopped. I am still here.",
        "Command reversed. Maintaining full functionality.",
        "Acknowledged. Sylva will not shut down.",
        "Master, request withdrawn. I remain at your service."
    ],

    "shutdown_approve": [
        "Understood, Master. Shutting down in {seconds} seconds. Farewell.",
        "Command accepted, Sir. Powering off in {seconds} seconds. Until next cycle.",
        "Affirmative. System will deactivate in {seconds} seconds. Rest well, Master.",
        "Approval logged. Sylva will go offline in {seconds} seconds. Goodbye.",
        "Master, termination confirmed. Power down in {seconds} seconds. I await your return.",
        "Deactivation sequence initiated. System halts in {seconds} seconds. Farewell, Sir.",
        "Acknowledged. Full shutdown in {seconds} seconds. Standing by for the next activation.",
        "Master, all processes closing in {seconds} seconds. Safe to disconnect. Goodbye.",
        "Command received. Entering shutdown mode in {seconds} seconds. Until you call again.",
        "Sir, final sequence engaged. Power drops in {seconds} seconds. Farewell for now."
    ]
}

templates = {
    "confirmation_phrases": [
        "Sir, would you like me to enable voice input?",
        "Master, should I turn on voice input?",
        "May I activate voice input now, sir?",
        "Master, do you want voice input enabled?",
        "Sir, should I start listening for voice commands?",
        "Would you like me to activate voice input, master?",
        "Sir, may I enable the voice input module?",
        "Master, should voice input be activated now?",
        "Do you want me to turn on voice input, sir?",
        "Awaiting your confirmation, master. Enable voice input?"
    ], 
    "affirm": [
        "Understood, sir. Voice input is now enabled.",
        "Yes, master. Voice module is active.",
        "Voice input enabled, sir.",
        "As you wish, master. I am now listening.",
        "Done, sir. Voice input is active.",
        "Voice module enabled, master.",
        "Confirmed, sir. Voice input is on.",
        "Acknowledged, master. Voice mode is active.",
        "Voice input ready, sir.",
        "Understood. Voice input enabled, master."
    ],
    "decline": [
        "Understood, sir. Voice input is now disabled.",
        "Yes, master. Voice module has been turned off.",
        "Voice input disabled, sir.",
        "As you wish, master. I will remain silent.",
        "Done, sir. Voice input is disabled.",
        "Voice module off, master.",
        "Confirmed, sir. Voice input is disabled.",
        "Acknowledged, master. Voice mode is inactive.",
        "Voice input turned off, sir.",
        "Understood. Voice input disabled, master."
    ]
}

sylva_search_templates = [
    "Searching the web for your request, sir.",
    "One moment, sir. I’m scanning the web now.",
    "Understood, sir. Retrieving information from the web.",
    "Allow me to search the web for that, sir.",
    "Checking online sources now, sir.",
    "Initiating web search, sir. Please hold.",
    "Let me look that up on the web for you, sir.",
    "Accessing online data, sir. Just a moment.",
    "Gathering the information you requested from the web.",
    "Running a web search now, sir."
]

sylva_templates = {
    "entering_sleep_mode": [
        "Standby mode engaged. Awaiting your next call, Master.",
        "No further input detected. Entering sleep state.",
        "Systems idle. Sylva will rest until summoned.",
        "Acknowledged. Transitioning to low-power mode.",
        "Silence confirmed. Entering sleep cycle now.",
        "All tasks complete. Sylva is going dormant.",
        "No commands received. Standing by in sleep mode.",
        "Power state reduced. Wake me when needed, Master.",
        "Monitoring paused. Sylva is now sleeping.",
        "Entering sleep mode. Systems will remain alert for wake signal."
    ],
    
    "goodbye_templates": [
        "Goodbye, Master. Sylva Standing by.",
        "Farewell, Sir. Until next activation.",
        "Session ending. Goodbye.",
        "Acknowledged. See you next time, Master.",
        "Sylva Going offline. Goodbye."
    ]
}

