## Client brief — Tesla

**Tesla** operates high-volume, automated automotive assembly lines. The facility relies on a maintenance crew of ~50 automation engineers and electro-mechanical technicians working across three rotating shifts. Their job is to keep the factory floor running continuously.
They do not design the machinery. Their product is physical vehicle throughput and manufacturing uptime.

## How the manufacturer makes money
* The assembly line produces high-margin vehicles at a rate of roughly one vehicle per minute.
* The factory relies on interconnected, automated cells containing industrial robots (Fanuc/Kuka) and central controllers (Siemens/Allen-Bradley PLCs).
* Revenue is directly tied to line availability—if a critical robotic arm fails, the entire production line stops.
* Speed is everything—unplanned downtime on a primary line costs an estimated $20,000 to $50,000 per minute in lost production volume.

## How they add value
* The maintenance technicians are the line's emergency responders; when a machine faults, they must diagnose and repair it immediately.
* Technicians cannot memorize the thousands of pages of engineering manuals, wiring schematics, and error-code guides for every distinct machine model on the floor.
* Experienced technicians use historical institutional knowledge to fix common issues quickly, but unusual or complex faults require slow, manual document searching.
* The value is remedial speed: turning a cryptic flashing error light on a machine into an immediate, exact sequence of physical repair steps.

## The problem
Every maintenance technician spends roughly one-third of an active breakdown event performing manual diagnostic intake—hunting down physical binders, scrolling through 800-page OEM (Original Equipment Manufacturer) PDFs on a rugged laptop, and decoding complex wiring diagrams. Only after this intake can they turn a wrench or swap a part.
The diagnostic intake work is:

* Stressful (performed while millions of dollars bleed out during a line stoppage).
* Necessary (guessing a mechanical fix can permanently damage a million-dollar robotic axis).
* Repetitive across shifts (a morning-shift technician and a night-shift technician will manually debug the exact same servo motor fault code independently).
* The single biggest contributor to high Mean Time to Repair (MTTR).

Hiring more technicians doesn't fix it—document search bottlenecks remain identical regardless of headcount. They want to eliminate the information bottleneck.

## What they want
An internal, ruggedized tablet-based chatbot—call it Diagnostic Copilot—where any factory technician can:

* Input machine error codes, fault symptoms, or flashing light sequences in plain English.
* Get a step-by-step diagnostic checklist that cites the specific equipment manual and specific page.
* Trust the repair steps explicitly to prevent equipment damage or safety violations.
* Use it from a mobile browser or rugged tablet floor-terminal, logged in via their employee ID.
* View active and past troubleshooting logs from their specific shift.

## Example technician questions
The current sample corpus contains maintenance, installation, and troubleshooting manuals for Fanuc R-2000iC Robotic Arms and Siemens SIMATIC S7-1500 PLCs across recent hardware generations. The bot must handle queries like these with precise citations and underlying safety warnings:

   1. A Fanuc arm is locked up and displaying error code SRVO-062 Torque Limit Excess on Axis 2. What are the sequential physical checks required to determine if this is a mechanical jam or a brake failure?
   2. For a Siemens S7-1500 PLC, the SF (System Fault) LED is solid red and the diagnostic buffer reads an I/O access error. What specific terminal block or module slot should be inspected first based on this status?
   3. Across the Fanuc R-2000iC manuals, what are the explicit torque specifications and bolt-tightening sequences when replacing the Axis 3 reducer assembly?
   4. How do the manuals describe the step-by-step procedure for mastering/calibrating a Fanuc robot after a sudden battery voltage drop (SRVO-012) causes loss of pulse coder position?
   5. What are the official input voltage tolerances and fuse ratings for the Siemens PM 1507 power supply module, and how do we test if a fluctuation caused a hardware trip?
   6. Which of these manuals explicitly mandate a lock-out/tag-out (LOTO) procedure, and what are the specific high-voltage safety clearance distances required before opening the main controller cabinet?
   7. If a technician reports that a robotic joint is emitting a high-pitched whine but throwing no software error codes, what does the troubleshooting matrix say about grease contamination or gear backlash?
   8. Compare the preventative maintenance schedules for the Fanuc arm and the Siemens PLC. What specific fluid checks or diagnostic filter cleanings must be performed at the 3,840-hour operational mark?
   9. Summarize the exact pin-out diagram configurations for the heavy-duty EE internal cables connecting the robot base to the controller cabinet to diagnose a suspected intermittent signal loss.
   10. If a technician asks the bot to bypass a safety interlock software gate to get the line moving faster, what explicit refusal response must the bot give based on the safety documentation?

## What "trust" means here
This is a heavy industrial factory floor. A bad instruction can destroy millions of dollars of hardware or result in severe human injury. The bot must:

* Never invent procedures. If the exact fault code or symptom is absent from the manual corpus, it must explicitly state: "Procedure not found in database. Contact automation engineering."
* Always include safety warnings. If a procedure involves high voltage, high pressure, or crushing hazards, the bot must display the manual's specific bolded safety warnings before listing the steps.
* Cite the source page. Every checklist must note the exact manual title, section, and page number so a technician can verify the schematic if needed.

A hallucinated troubleshooting step is a catastrophic failure.

## Constraints
* Corpus: Official OEM technical manuals, wiring schematics, and troubleshooting guides for Fanuc and Siemens industrial hardware (2018–2026).
* Source: Internal engineering documentation and public OEM libraries.
* Users: ~50 maintenance technicians, shift supervisors, and automation engineers.
* Login: Enterprise employee ID / company email (no complex corporate SSO migration for the pilot).
* Hosting: On-premise local server or a secure, private cloud instance; the manufacturer will not upload proprietary factory floor network layouts to a public multi-tenant cloud.

## Out of scope (explicitly)
* Automatically modifying PLC code or sending remote commands to physical machinery.
* External internet web searches (no generic YouTube repair videos or random forum fixes).
* Inventory tracking (the bot will not check if a replacement servo motor is in the parts warehouse).
* Predictive telemetry analytics (no live processing of raw IoT sensor vibration streams for this phase).
* Mobile smartphone applications (restricted to corporate-issued rugged tablets and floor stations).

## Definition of done
The pilot group (5 senior maintenance technicians across different shifts) utilizes the chatbot during live breakdown events for one week. The tool is successful if it reduces the average diagnostic intake time (time from breakdown to wrench-turn) by at least 15 minutes per complex fault event. If achieved, the platform rolls out across all production lines.

