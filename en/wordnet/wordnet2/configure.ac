#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.59)
AC_INIT(WordNet, 2.1, [wordnet@princeton.edu], wordnet)
AC_CONFIG_SRCDIR([config.h.in])
AC_CONFIG_HEADER([config.h])

AC_PREFIX_DEFAULT([/usr/local/WordNet-2.1])

# Checks for programs.
AC_PROG_CC
AC_PROG_RANLIB
AC_PROG_INSTALL

# Checks for header files.
AC_HEADER_STDC
AC_CHECK_HEADERS([locale.h malloc.h stdlib.h string.h])

# Checks for typedefs, structures, and compiler characteristics.

# Checks for library functions.
AC_FUNC_MALLOC
AC_CHECK_FUNCS([strchr strdup strrchr strstr strtol])

# Set HAVE_LANGINFO_CODESET if nl_langinfo is found

AC_LANGINFO_CODESET

AM_INIT_AUTOMAKE(WordNet, 2.1)

SC_PATH_TCLCONFIG
SC_PATH_TKCONFIG
SC_LOAD_TCLCONFIG
SC_LOAD_TKCONFIG

# This doesn't do anything
AC_CONFIG_COMMANDS([default])

AC_CONFIG_FILES(Makefile dict/Makefile doc/Makefile doc/html/Makefile doc/man/Makefile doc/pdf/Makefile doc/ps/Makefile include/Makefile src/Makefile lib/Makefile lib/wnres/Makefile)

AC_OUTPUT

AC_MSG_RESULT(
[
WordNet is now configured

  Installation directory:               ${prefix}

  To build and install WordNet:

    make
    make install

  To run, environment variables should be set as follows:

    PATH - include ${bindir}
    WNHOME - if not using default installation location, set to ${prefix}

    See INSTALL file for details and additional environment variables
    which may need to be set on your system.

])
