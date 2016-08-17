setlocal
set HERE=%~dp0

pushd %HERE%

set TARGET_FOLDER=..\test_ea

set SLT_HOST=w2012r2-logsv
set SLT_PORT=6001
set SLT_USER=Administrator
set SLT_PWD=

for /R %TARGET_FOLDER% %%i in (*.test) do sqllogictest -odbc "DRIVER={Dr.Sum EA 4.2 ODBC Driver};SERVER=%SLT_HOST%;PORT=%SLT_PORT%;DATABASE=slt;UID=%SLT_USER%;PWD=%SLT_PWD%" -verify %%i 2>%%i_res

popd
endlocal