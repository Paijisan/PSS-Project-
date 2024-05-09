; testing week view
Send cls {Enter}
Send py PSSController.py
Send {Enter}
; test transient task printing
Send 1 
Send {Enter}
Send Transient Task 1 {Enter}
Send Appointment 
Send {Enter}
Send 12 {Enter}
Send 1 {Enter}
Send 19990202 {Enter}
Send {Enter}
Send {Enter}
Send {Enter}
; test daily recurring task printing
Send 1 
Send {Enter}
Send Recurring Daily Task {Enter}
Send Class 
Send {Enter}
Send 13 {Enter}
Send 1 {Enter}
Send 19990202 {Enter}
Send 20000101 {Enter}
Send 1 {Enter}
Send {Enter}
; test weekly recurring task printing
Send 1 
Send {Enter}
Send Recurring Weekly Task {Enter}
Send Class 
Send {Enter}
Send 14 {Enter}
Send 1 {Enter}
Send 19990201 {Enter}
Send 20000101 {Enter}
Send 7 {Enter}
Send {Enter}
; test antitask
Send 1
Send {Enter}
Send Antitask {Enter}
Send Cancellation 
Send {Enter}
Send 13 {Enter}
Send 1 {Enter}
Send 19990203 {Enter}
Send {Enter}
Send {Enter}
Send Recurring Daily Task {Enter}
; show day schedule
Send 2
Send {Enter}
Send 19990214 {Enter}
; show week schedule
Send 3
Send {Enter}
Send 19990214
Send {Enter}
; show month schedule
Send 4
Send {Enter}
Send 19990202
Send {Enter}