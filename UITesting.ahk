; testing viewer
Send cls {Enter}
Send py PSSController 
Send {Tab}
Send {Enter}
; create transient task 
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
; create daily recurring task 
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
; create weekly recurring task
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
; create antitask
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
Send 19990401
Send {Enter}
; show month schedule
Send 4
Send {Enter}
Send 19990202
Send {Enter}