setlocal
set HERE=%~dp0

pushd %HERE%

set SLT_HOST=10.72.5.62
set SLT_PORT=6001
set SLT_USER=Administrator
set SLT_PWD=

set TARGET_FOLDER=..\test_ea2\random\aggregates
for /R %TARGET_FOLDER% %%i in (*.test) do call sqllogictest -odbc "DRIVER={Dr.Sum EA 4.2 ODBC Driver};SERVER=%SLT_HOST%;PORT=%SLT_PORT%;DATABASE=slt;UID=%SLT_USER%;PWD=%SLT_PWD%" -verify %%i 2>%%i_res

popd
endlocal