2026-08-05

Goal: Add multi-transformer support

Completed: 
- Converted Transformer object to transformer list
- added TX-101, TX-102, TX-103
- updated telemetry collection loops for list alteration

Issues: 
- Health report only displayed tx-103 
    Root cause was due to indentation outside of loop. and old code that only showed the last transformer

Next session: 
- improve event state transitions


2026-09-05

Goal: Improve event state transitions and add documentation '

Completed:
- Added decisions,engineering,roadmap, and architecture.md(s) 
-

Issues: Started documentation today so most changes have to be remembered and added at future date
event state handling would flood the terminal with endless data instead of the specific historical data

Lessons learned: Make a habbit of adding documention and making git commits

Next session: complete event state tranisiton


2026-09-09

GOal: complete implementation of improved event state transition

completed: added new_status, and previous_status(also properly used previous_status over previous_health_status so data will show the correct state needed) (Later date change prevous_health_status to hold persistant health status rather than hard coded "normal" in)


lessons learned: Learned the value of testing and implemented new iterations. test for bugs and get it working, then implemenet an optimized way with seperation of concerns to keep clean code and create code that works and can be scaled. 


Next session: Add an operators dashboard



2026-09-16

Goal: Add an operator Dashboard

Completed: Added a basic operator dashboard to be used for the actual web-based dashboard

Next Session: add a system summary to optimise what operators see so only the most important information is shown in proper order of severity.

Lesson learned: Frequent testing at ever section of the project can allow you to fix formatting errors and create the best project possible, The more errors you fix before you get to the end product means a more optimized and precise project.



2026-09-17

Goal: create a new operator dasboard and add a dashboard health to display the actual health status of the transformer

Completed: Added display_operator_dashboard and rearranged where the display call is located within while true loop to bottom of the loop. created a dictionary for dashboard_health to allow the dictionary to be populated the analyzed by the display operator dashboard. added asset_id and health to the def display dashboard function to allow equiptment health to be viewed.

lessons learned: Understanding placement of code in a systems mindset to troubleshoot errors in code that might not be shown in the terminal as an error but rather the feautre did not meet the sharholder requirements. The more I work with code the more the patterns make themselves known.

Next session: Add an overall system status to the operator display

2026-09-21

Goal: Add an overall system status to operator display and active alarm section

Completed: Added an overall system status to view total amount of events.

Lessons learned:Adding a counter and linking that coutner to display_health which contains the collected events needed, can give an operator dashboard a cleaner and more effective way at looking at problems that need to be addressed. Adding an active alarm system allows the dashboard to be even cleaner by keeping alarms up until they are cleared instwad on constatly filling the dashboard with events.  .values() only gives the value of a dictionary, while .items() gives the key and value of that dictionary (Side note: .keys() return only the key)

Next session: Real Alarm management system


2026-09-24 

Goal: Implement a realistic alarm management system that distinguishes between the different states of an alarm from created, active, acknowledged and cleared.

Completed: Added a alarm managment system that include new alarm, cleared,

Lessons Learned: Created an active alarm dictionary to allow it to be filled with health_status, health_reason under dashboard_health dictionary. the active alarm will create a table if no active alarm is up and if status != normal. adding feautures like new alarm and cleared alarm took some time due to trying to test whether the added code to clear the alarm works. I was dealing with the random numbers and aggregate functions used to simulate these conditions was causing the values to increase due to incorrect configuration of that code (will revise at future point) Good tip is to clear substation.db and run the code again until it can produce the correct new alarm and clear. (PATIENCE IN TESTING)

Next Session: Make the dashboard use active_alarms


2026-09-25:


Goal: Make the dashboard make use of active_alarms section to allow for an alarm severity feature. currently it just shows a cleared state when it goes to normal. This makes for better state tracking, instead of what is != normal it now shows what alarms are currently active.

Create a new controlled simulator for better testing


lessons learned: Seperation of responsibilities when it comes to how some functions are used and recreated to have cleaner architecture. for example, allowing the dashboard to show the output of active alarms instead of coming from health. health had the same type of code if != normal then show status and reason. however our active alarms already contained this type of feature. instead of having two seperated feautures doing the same thing I replaced it with a call to active alarms, and parsed active alarms within the def dashboard and its call.

my attempt at creating a controlled simulator led to the first iteration being stability. I changed values of the randint to a smaller range and the simulation stopped increasing exponentially. then I created a new update inside tranformer.py to simulate normal, overload, and recovery numbers. this was accomplished by putting simulation_mode inside the init class and make three new simulation_mode normal,recovery,etc.  inside update function. then we call that inside main.py where I set up the equipment by adding transformers[0].simulation_mode=normal and set one for each transformer so I can control what simulation feature I want to see. next was the implementation of the limit. by placing an if temp < 100 it stops the temp from rising to exponetial heights and allows for better testing environment. 

creating scenario cycle to allow program to run without continously stopping and resarting, 
this was accomlplished by adding self.scenario_cycle = 0 otherwise known as a counter. then I set up a if scenario >= 10: enter recovery mode, then from recovery mode it enters normal mode. the testing involed making sure eac iteration worked before adding another feature. first I tested to make sure cycles poped up in the terminal, after that I had to investigate whether the cycle would automatically go thorugh all the iteration and print the required messages. such as alarm clear when it reaches normal.

Next session: Finish the scenario cycle by allowing full transition into each mode, then add an event managment system to record all alarms and changes.


2026-09-27

GOAL: Complete implementation of scenario cycle and begin work on event management

completed: finished the automatic scenario cycle by adding a limit to scenario cycles within recovery mode once this limit is reached it sets self.simulation mode to NORMAL.

next I added the event history, which is populated with active alarms. I created a dictionary to hold the active alarms and added event_history into the def operator display and its call within main.py. starting to see a design pattern form. 

then I corrected an error because I used a slice that formatted a list instead of a dictionary. A list is more practical for creating a list of events that took place rather than usign a dictionary due to the usage of the information. for instance active alarm uses a dictionary to find specfic information ro be used while event history is just recording the alarsm from acrive alarms and we only need to see what happened rather than a specic data point.

Next session: Upgrade event history to include more useful information


2026-09-28

Goal: add timestamps and sceanrio changes to event history.

Completed: Added timestamps to event history, added transitions to event history

lesson learned: adding timestamp works but adding from datime import datetime which loads in the module datetime and allows us to use some predefined functions like datetime.now() then we format our event_history to iclude the varaible timestamp = datetime.now().strftime. which is hold the current datetime formatted in a text format in a varaible called timestamp. then we add that to our event_history.append with asset_id to include {timestamp}

Then the next problem was converting the timestamp into a dictionary due to how much easier retrival would be now that its formated into data rather than searching through unformatted stirngs.

to accomplish this, I convertered event_history.append into a dictionary instead of f""{}

Had an issue where I updated the readme on GITHUB manually then when I tried to push my timestamp upgrade i ran into an error. this error was due to a conflict of merging errors, github has an change that wasnt pulled so to fix this you have to git pull origin master, press esc to accept the default message type :wq and press enter to save the merge, then git push origin master to complete the commit. my url also changed to GridWatch so i had to use git remote set-url origin [url] to change that.

when adding a dictionary you can use this syntax to create a dictionary and loop through the variable to populate the dictionary 
previous_modes = {
    transformer.asset_id: transformer.simulation_mode
    for transformer in transformers
}

compared to this 
previous_modes = {}

for transformer in transformers:

    previous_modes[transformer.asset_id] = transformer.simulation_mode

next session: update Gridwatch to use sql database instead of memory for event history


2026-09-29

Goal: Configure event_history to use sql instead of event_history[]

completed: commited transformer event tracking , and implemented first iteration of changeover to using sql

Lessons learnerd: During the early sage of the project I used a event_history[] to store event_history to be displayed in the dashboard. however, having both built in memory and sql memory is redundant so using the sql memory which is persistant, makes more sense. To fix this i had to delete the event_history built in memory, then i had to remove event_history from funcions and calls containing it. finally, I added a loop that prints events[5],[4],[1],[2], these numbers reference the database.py get events parameters.

I ran into another problem where my dashboard was displaying a mix of health report data (Normal, Watch, Warning) and operational event (Mode change new alarm, alarm cleared) WIth the dashboard we want a architecture that has health reports reporting health specific information, while operational records significant operator/systems events. mode change | overload-> recoery or tx-102 | new alarm| warning. my dashboard was mixing TX-103 | NORMAL | Transformer operating normally. to accomplish this i had to go to if health_status != previous_status: inserevent. so this was giving health status information into the events table which is where the operational changes happen. (Think what does the operator need to see based on the architecture)

Next Session: Finish testing event_history and upgrade the alarm transition


2026-09-30

Goal: Update the alarm tranisition to start all transformers at normal and set automatic state transitions from there.

Completed: 

lessons learned: understanding where to add code logically. I had to think logically about where to add this automatic transition into an overload state. after run_monitor cylce() which collects all the reading then update the scenario cycle. this is where is add if transformer[1].scenario cycle == 5: then set simulation mode to overload.

then i ran into a problem with not getting the full transition back into normal to get the alarm clear. I had to go into transformer.py and change the threshold from if scenario_cycle >20 -> 10 tjen i changed it to 5. However, i ran into a problem with the terminal always reseting bac kto 5 into overload. to fix this I deleted the previous_mode code which set the set the simulation od based on the cycles. i changes it into a dictionary setting each transformer to normal, then i set the transformer[2] simulation mode to OVERLOAD. now the code catches the mode change from normal to overload, into recovry, into normal which shows alarm clear.

then I needed to save the alarm system to the database, I did this by addin insert_event to new alarm and alarm clear section. also alarm clear would del the active alarm so I had to save the active alarm as previous_alarm_status to save that information into the insert event.

2026-10-02

Goal: Add the foundational cybersecurity features

Completed: Added basic asset inventory

Lessons learned: reiterated the creation of a class serperated in one folder. called in main.py. I then created a list of assets called security_asset[] (TEMPORARY) inserted their attributes as it aigns with its class then printed a messegae to check if it works.


2026-10-03

GOAL: Set up the database

completed: Added insert and get security events to database.py, and added those to main.py import

lessons learned: Another example of patterns and following the same architerture as previous setups. We had to create the database create table for sevurity events and had to create the insert and get security events. I also used a test shown below to see if the it will print the proper message to prove my database was created properly.
insert_security_event(
    "RTU-001",
    "FAILED_LOGIN",
    "MEDIUM",
    "UNKNOWN_USER",
    "Multiple failed login attempts detected",
    "OPEN",
    str(datetime.now())
)

security_events = get_security_events()

print()
print("===== SECURITY EVENTS =====")

for event in security_events:
    print(event)


2026-10-06

Goal: Start phase 2: authenication monitoring

Completed:

Lessons learned: Started by adding a class with a constructor authentication.py, then called that into main.py with import from syntax. after that I created a list auth_events = [] w/ 1 success and 2 failed to test the import. i printed a message for event in auth_events: with three parameters user,target,and result.

then i created a failed login which links the evens in auth_events with a new dictionary knowk as failed_login_counts. basically the code is if the auth_event result == failure then take the current failed_login_counts and add the new failed login counts +1 to the dictionary failed_login_counts[event.username] failed_login_counts.get(event.username, 0) +1 then for username, count in failed_login_counts.items():

    print(
        f"{username}: {count}"
    )
Which is the snytax needed to print the key and value of a dictionary. you need .items() otherwise you would only get values or keys.

after that I added a login threshold which is accomplished by adding a failed_login_threshold = 3 before the login counter and insde of your print for your login_count dictinary you add if count >= failed_login_threshold:

        print(
            f"SECURITY ALERT: "
            f"{username} reached the failed login threshold"
        )
currently I only have 2 events that hold failed, so next step was to add 1 more auth_event with a failure result to trigger an alert

i then added a database insert_security event to capture the events in a persistant database rather than in-memory

then I added a failed_login_targets = {} to capture the specific events that for username, count in failed_login_counts.items(): would lose

then inside if event.result == failed I added failed_login_targets.setdefault(
            event.username,
            []
        ).append(
            event.target_asset
        )
which takes the event username, and appens the target asset it attempted to acces inside the failed login targets distionary and saves them their. {
    "unknown_user": [
        "HMI-001",
        "RTU-001"
    ]
}

