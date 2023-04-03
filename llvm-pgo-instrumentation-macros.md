This document contains documentation of the individual llvm_pgo_instrumented_XXX
macros and how to use them.

[TOC]

# Goal 

This is a package for the LLVM maintainers of Fedora and not meant to be used by
the end-users of the LLVM toolchain. It is supposed to help in building a PGO
optimized LLVM toolchain.

The goal of the `llvm-pgo-instrumentation-macros` package is to automatically
generate a `<PACKAGE>-<TOOLCHAIN>-pgo-profdata` subpackage for any package that
gets build. The content of such a subpackage is an indexed PGO profile file.
If you don't want this, you have two options:

1. Don't install `llvm-pgo-instrumented-macros` package in the first place.
2. Specify `%global _toolchain_profile_subpackages %{nil}` in the package's spec file.

To make this work you need a PGO instrumented LLVM toolchain that will generate
PGO profiling data for you. See the `pgo_instrumented_build` build condition for
the llvm toolchain packages.

# Using the llvm_pgo_instrumentation_XXX macros

Make sure that the package you want to generate the PGO subpackage for is
compiling with clang. The easiest way is to specify this global:

    %global toolchain clang

For more information on this, see [the compiler-macros](https://docs.fedoraproject.org/en-US/packaging-guidelines/#_compiler_macros).

The `redhat-rpm-config` package has a few places in which is calls these macros
if they are defined, aka the `llvm-pgo-instrumentation-macros` package is
installed.:

    %{?llvm_pgo_instrumented_build_flags}
    %{?llvm_pgo_instrumented_spec_build_pre}
    %{?llvm_pgo_instrumented_spec_build_post}
    %{?llvm_pgo_instrumented_os_install_post}
    %{?llvm_pgo_instrumented_install}
  
The following subsections discuss each of these macros in detail:

## llvm_pgo_instrumented_build_flags

The `%llvm_pgo_instrumented_build_flags` macro is meant to be called before
invoking an instrumented binary from the LLVM toolchain. Any of those binaries
will try to write a raw profile into a location that is determined wherever it
was being built. Typically such a buildroot directory is not available when it
is executed. That's why we create a directory in `%{_builddir}/raw-pgo-profdata`
and instruct the instrumented binary to store its profiles there by specifying
the `LLVM_PROFILE_FILE`.

## llvm_pgo_instrumented_spec_build_pre

As the name suggest the `%llvm_pgo_instrumented_spec_build_pre` is meant to be
called at the beginning of the `%build` section of a spec file. This is where we
start a background process to continously collect raw PGO profile files and
merge them into a single indexed PGO profile file.

## llvm_pgo_instrumented_spec_build_post

The `%llvm_pgo_instrumented_spec_build_post` gracefully stops the background
process we've started with `%llvm_pgo_instrumented_spec_build_pre`.

## llvm_pgo_instrumented_os_install_post

The `%llvm_pgo_instrumented_os_install_post` is meant to run at the end of the
`%install` section. For one last time we collect any left-over raw profiles and
merge them into the buildroot.

## llvm_pgo_instrumented_install

The `%llvm_pgo_instrumented_install` sets up a `%package` section for the
`<PACKAGE>-<TOOLCHAIN>-pgo-profdata`. The only file that is listed for this
package is the one that is created by `%llvm_pgo_instrumented_os_install_post`.