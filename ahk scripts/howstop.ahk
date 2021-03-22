#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

help() {
	#IfWinActive,ahk_exe discord.exe
	Send, {BACKSPACE}
	Send, {BACKSPACE}
	Send, {BACKSPACE}
	Send, ^k
	SendRaw, #how-log
	Send, {Enter}
	Send, how log bot stopped @candycane {Enter} from saying how {Enter}
	Send, ^k
	SendRaw, #advice
	Send, {Enter}
	Send, shut up and read this

	return
}

:*:how::
help()
return

:*:h-::
help()
return

:*:ho-::
help()
return

:*:..::
help()
return

^k::
Send, ctrl k sent

