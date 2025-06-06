echo "Installer for argx for C"
echo "REQUIREMENTS:"
echo "1) SWIG"
echo "2) Python3"
echo "3) C++ compiler (GCC, Clang)"
echo "4) Check the official README and documentation for more information"
echo "Press <CTRL + C> to cancel or TYPE THE PYTHON VERSION TO CONTINUE (Ex: 3.13)"

read pythonVersion

if [ "$pythonVersion" == "" ]; then
	pythonVersion="3.13"
fi

echo "[ * ] PYTHON VERSION SET TO: $pythonVersion"

mkdir -p tmp/ build/ build/python build/obj

touch build/__init__.py

git clone "https://www.github.com/pcannon09/argx.git" ./tmp/argx
cd ./tmp/argx
git checkout tags/1.0.2-build
cd ../../

rm -rf ./tmp/argx/.git/

set -e

### MAKE AND GEN ###
echo "[ GENERATING ]"
swig -c++ -python -DARGX_AS_PYTHON_PACKAGE -cpperraswarn -outdir build -o build/argx_py_wrap.cxx module.i

echo "[ COMPILING ]"
echo "[ COMPILING ] tmp/argx/src/Argx.cpp" ; g++ -std=c++11 -D ARGX_AS_PYTHON_PACKAGE -fPIC -c tmp/argx/src/Argx.cpp -I/usr/include/python$pythonVersion -o build/obj/Argx.o
echo "[ COMPILING ] tmp/argx/src/ARGXAddError.cpp" ; g++ -std=c++11 -D ARGX_AS_PYTHON_PACKAGE -fPIC -c tmp/argx/src/ARGXAddError.cpp -I/usr/include/python$pythonVersion -o build/obj/ARGXAddError.o

echo "[ BUILDING ] ./build/argx_py_wrap.cxx" ; g++ -std=c++11 -D ARGX_AS_PYTHON_PACKAGE -fPIC -c build/argx_py_wrap.cxx -I/usr/include/python$pythonVersion -o build/obj/argx_py_wrap.o

echo "[ LINKING ]"
g++ -std=c++11 -D ARGX_AS_PYTHON_PACKAGE -shared build/obj/argx_py_wrap.o build/obj/Argx.o build/obj/ARGXAddError.o -o build/_argx_py.so

echo "[ OK ] You can now use ARGX-PY"

while true; do
    echo "Remove \`tmp/\` directory? Y/n?"

    read answer

    if [ "$answer" = "Y" ]; then
        rm -r ./tmp/

		echo "[ DONE ]"
        exit

    elif [ "$answer" = "n" ]; then
    	echo "[ OK ]"
        exit

    else
        echo "[ ERR ] Please answer Y/n"
    fi
done
