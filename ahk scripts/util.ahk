#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

:*:_firefox::
Run, C:\Program Files\Mozilla Firefox\firefox.exe -private-window
Send, {BACKSPACE}
return

:*:_run::
Send, #r
Send, {BACKSPACE}
return

:*:_kill::
WinKill, A
Send, {BACKSPACE}
return

:*:_notepad::
Run, notepad
Send, {BACKSPACE}
return

