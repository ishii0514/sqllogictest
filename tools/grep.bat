setlocal
set HERE=%~dp0

rem pushd %HERE%

set SEARCH_FILES=*.test
set SEARCH_WORD="UPDATE"
set OUTPUT_FILE=grep_result.txt

for /R .\ %%i in (%SEARCH_FILES%)  do find %SEARCH_WORD% %%i >>%OUTPUT_FILE%

rem popd
endlocal