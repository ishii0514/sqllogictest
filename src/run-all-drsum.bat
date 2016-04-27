setlocal
set HERE=%~dp0

pushd %HERE%

for /R ..\test2 %%i in (*.test) do sqllogictest -odbc "DRIVER={Dr.Sum EA 4.2 ODBC Driver};SERVER=localhost;PORT=6001;DATABASE=slt;UID=Administrator;PWD=" -verify %%i 2>%%i_res

popd
endlocal