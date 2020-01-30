@echo off
SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
::%1 is mean first script parameter or switch
if "%~1"=="" (
	echo You need to pass a port as a parameter. Example %~n0 port
	pause
	goto :EOF
)

set hostFilePath="c:\Windows\System32\drivers\etc\hosts"
set ContainerPort=%1

for /f "USEBACKQ" %%a in (`docker-machine ip`) do set DockerIP=%%a
for /f "tokens=3 delims=: USEBACKQ" %%b in (`find /c "%DockerIP%" %hostFilePath%`) do (
	if /I "%%b"==" 0" (echo %DockerIP% localhost >> %hostFilePath%)
)
netsh interface portproxy add v4tov4 listenport=%ContainerPort% listenaddress=127.0.0.1 connectaddress=%DockerIP% connectport=%ContainerPort%
netsh interface portproxy add v6tov4 listenport=%ContainerPort% listenaddress=::1 connectaddress=%DockerIP% connectport=%ContainerPort% 
netsh interface portproxy show v4tov4
netsh interface portproxy show v6tov4
::"netsh interface portproxy show v4tov4" allows you to view current port redirection
::"netsh interface portproxy delete v4tov4 listenport=%ContainerPort% listenaddress=127.0.0.1" allows you to remove port redirection
ping -n 10 127.0.0.1 > nul