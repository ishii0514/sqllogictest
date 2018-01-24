setlocal
set HERE=%~dp0

pushd %HERE%

set SLT_HOST=w2012r2-logsv
set SLT_PORT=6001
set SLT_USER=Administrator
set SLT_PWD=

set TARGET_FILE=..\test_ea2\select1.test
call sqllogictest -odbc "DRIVER={Dr.Sum EA 4.2 ODBC Driver};SERVER=%SLT_HOST%;PORT=%SLT_PORT%;DATABASE=slt;UID=%SLT_USER%;PWD=%SLT_PWD%" -verify %TARGET_FILE% 2>%TARGET_FILE%_res
set TARGET_FILE=..\test_ea2\select2.test
call sqllogictest -odbc "DRIVER={Dr.Sum EA 4.2 ODBC Driver};SERVER=%SLT_HOST%;PORT=%SLT_PORT%;DATABASE=slt;UID=%SLT_USER%;PWD=%SLT_PWD%" -verify %TARGET_FILE% 2>%TARGET_FILE%_res
set TARGET_FILE=..\test_ea2\select3.test
call sqllogictest -odbc "DRIVER={Dr.Sum EA 4.2 ODBC Driver};SERVER=%SLT_HOST%;PORT=%SLT_PORT%;DATABASE=slt;UID=%SLT_USER%;PWD=%SLT_PWD%" -verify %TARGET_FILE% 2>%TARGET_FILE%_res
set TARGET_FILE=..\test_ea2\select4.test
call sqllogictest -odbc "DRIVER={Dr.Sum EA 4.2 ODBC Driver};SERVER=%SLT_HOST%;PORT=%SLT_PORT%;DATABASE=slt;UID=%SLT_USER%;PWD=%SLT_PWD%" -verify %TARGET_FILE% 2>%TARGET_FILE%_res
set TARGET_FILE=..\test_ea2\select5.test
call sqllogictest -odbc "DRIVER={Dr.Sum EA 4.2 ODBC Driver};SERVER=%SLT_HOST%;PORT=%SLT_PORT%;DATABASE=slt;UID=%SLT_USER%;PWD=%SLT_PWD%" -verify %TARGET_FILE% 2>%TARGET_FILE%_res




set TARGET_FOLDER=..\test_ea2\evidence
for /R %TARGET_FOLDER% %%i in (*.test) do call sqllogictest -odbc "DRIVER={Dr.Sum EA 4.2 ODBC Driver};SERVER=%SLT_HOST%;PORT=%SLT_PORT%;DATABASE=slt;UID=%SLT_USER%;PWD=%SLT_PWD%" -verify %%i 2>%%i_res

set TARGET_FOLDER=..\test_ea2\index\between
for /R %TARGET_FOLDER% %%i in (*.test) do call sqllogictest -odbc "DRIVER={Dr.Sum EA 4.2 ODBC Driver};SERVER=%SLT_HOST%;PORT=%SLT_PORT%;DATABASE=slt;UID=%SLT_USER%;PWD=%SLT_PWD%" -verify %%i 2>%%i_res

set TARGET_FOLDER=..\test_ea2\index\commute
for /R %TARGET_FOLDER% %%i in (*.test) do call sqllogictest -odbc "DRIVER={Dr.Sum EA 4.2 ODBC Driver};SERVER=%SLT_HOST%;PORT=%SLT_PORT%;DATABASE=slt;UID=%SLT_USER%;PWD=%SLT_PWD%" -verify %%i 2>%%i_res

set TARGET_FOLDER=..\test_ea2\index\delete
for /R %TARGET_FOLDER% %%i in (*.test) do call sqllogictest -odbc "DRIVER={Dr.Sum EA 4.2 ODBC Driver};SERVER=%SLT_HOST%;PORT=%SLT_PORT%;DATABASE=slt;UID=%SLT_USER%;PWD=%SLT_PWD%" -verify %%i 2>%%i_res

set TARGET_FOLDER=..\test_ea2\index\in
for /R %TARGET_FOLDER% %%i in (*.test) do call sqllogictest -odbc "DRIVER={Dr.Sum EA 4.2 ODBC Driver};SERVER=%SLT_HOST%;PORT=%SLT_PORT%;DATABASE=slt;UID=%SLT_USER%;PWD=%SLT_PWD%" -verify %%i 2>%%i_res
popd
endlocal