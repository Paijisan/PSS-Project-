; testing week view
Send cls {Enter}
Send .\PSSController.py {Enter}
Sleep 100
; test transient task printing
Send 1 
Send {Enter}
Send Transient Task 1 {Enter}
Send Transient 
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
Send recurring 
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
Send recurring 
Send {Enter}
Send 14 {Enter}
Send 1 {Enter}
Send 19990202 {Enter}
Send 20000101 {Enter}
Send 7 {Enter}
Send {Enter}
Send 3 
Send {Enter}
Send 19990202 {Enter}