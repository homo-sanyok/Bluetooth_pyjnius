#!/bin/sh

# Keep this script in sync with python-config.in

exit_with_usage ()
{
    echo "Usage: $0 --prefix|--exec-prefix|--includes|--libs|--cflags|--ldflags|--extension-suffix|--help|--abiflags|--configdir|--embed"
    exit $1
}

if [ "$1" = "" ] ; then
    exit_with_usage 1
fi

# Returns the actual prefix where this script was installed to.
installed_prefix ()
{
    RESULT=$(dirname $(cd $(dirname "$1") && pwd -P))
    if which readlink >/dev/null 2>&1 ; then
        if readlink -f "$RESULT" >/dev/null 2>&1; then
          RESULT=$(readlink -f "$RESULT")
        fi
    fi
    echo $RESULT
}

prefix_real=$(installed_prefix "$0")

# Use sed to fix paths from their built-to locations to their installed-to
# locations. Keep prefix & exec_prefix using their original values in case
# they are referenced in other configure variables, to prevent double
# substitution, issue #22140.
prefix="/usr/local"
exec_prefix="/usr/local"
exec_prefix_real=${prefix_real}
includedir=$(echo "${prefix}/include" | sed "s#$prefix#$prefix_real#")
libdir=$(echo "${exec_prefix}/lib" | sed "s#$prefix#$prefix_real#")
CFLAGS=$(echo "-fPIC -DANDROID -D__ANDROID_API__=24" | sed "s#$prefix#$prefix_real#")
VERSION="3.8"
LIBM="-lm"
LIBC=""
SYSLIBS="$LIBM $LIBC"
ABIFLAGS=""
LIBS="-lpython3.8 -ldl  -lsqlite3 -lffi -lcrypto1.1 -lssl1.1 -lz -lm $SYSLIBS"
LIBS_EMBED="-lpython${VERSION}${ABIFLAGS} -ldl  -lsqlite3 -lffi -lcrypto1.1 -lssl1.1 -lz -lm $SYSLIBS"
BASECFLAGS=" -mfloat-abi=softfp -mfpu=vfpv3-d16 -Wno-unused-result -Wsign-compare -Wunreachable-code"
LDLIBRARY="libpython$(LDVERSION).so"
OPT="-DNDEBUG -g -fwrapv -O3 -Wall"
PY_ENABLE_SHARED="1"
LDVERSION="$(VERSION)$(ABIFLAGS)"
LIBDEST=${prefix_real}/lib/python${VERSION}
LIBPL=$(echo "$(prefix)/lib/python3.8/config-$(VERSION)$(ABIFLAGS)" | sed "s#$prefix#$prefix_real#")
SO=".cpython-38.so"
PYTHONFRAMEWORK=""
INCDIR="-I$includedir/python${VERSION}${ABIFLAGS}"
PLATINCDIR="-I$includedir/python${VERSION}${ABIFLAGS}"
PY_EMBED=0

# Scan for --help or unknown argument.
for ARG in $*
do
    case $ARG in
        --help)
            exit_with_usage 0
        ;;
        --embed)
            PY_EMBED=1
        ;;
        --prefix|--exec-prefix|--includes|--libs|--cflags|--ldflags|--extension-suffix|--abiflags|--configdir)
        ;;
        *)
            exit_with_usage 1
        ;;
    esac
done

if [ $PY_EMBED = 1 ] ; then
    LIBS="$LIBS_EMBED"
fi

for ARG in "$@"
do
    case "$ARG" in
        --prefix)
            echo "$prefix_real"
        ;;
        --exec-prefix)
            echo "$exec_prefix_real"
        ;;
        --includes)
            echo "$INCDIR $PLATINCDIR"
        ;;
        --cflags)
            echo "$INCDIR $PLATINCDIR $BASECFLAGS $CFLAGS $OPT"
        ;;
        --libs)
            echo "$LIBS"
        ;;
        --ldflags)
            LIBPLUSED=
            if [ "$PY_ENABLE_SHARED" = "0" ] ; then
                LIBPLUSED="-L$LIBPL"
            fi
            echo "$LIBPLUSED -L$libdir $LIBS"
        ;;
        --extension-suffix)
            echo "$SO"
        ;;
        --abiflags)
            echo "$ABIFLAGS"
        ;;
        --configdir)
            echo "$LIBPL"
        ;;
esac
done
