@echo off
rem 指定フォルダ配下のファイルを再帰的に削除する
setlocal
set HERE=%~dp0


pushd %HERE%

for /R ..\test_ea %%i in (*.test_res)  do echo %%i

popd
endlocal