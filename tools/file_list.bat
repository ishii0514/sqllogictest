@echo off
setlocal
set HERE=%~dp0


pushd %HERE%

for /R ..\test %%i in (*.test)  do echo %%i

popd
endlocal