setlocal
set HERE=%~dp0

pushd %HERE%

rem set TARGET_FOLDER=..\test2
set TARGET_FOLDER=..\test2\index

for /R %TARGET_FOLDER% %%i in (*.test) do sqllogictest -odbc "DRIVER={Dr.Sum EA 4.2 ODBC Driver};SERVER=w2012r2-logsv;PORT=6001;DATABASE=slt;UID=Administrator;PWD=" -verify %%i 2>%%i_res

popd
endlocal