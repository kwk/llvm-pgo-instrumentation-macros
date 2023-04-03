Name:       llvm-pgo-instrumentation-macros
Version:    0.0.1
Release:    1%{?dist}
Summary:    Provides llvm_pgo_instrumented_XXX macros
URL:        https://pagure.io/llvm-snapshot-builder
License:    Apache-2.0
BuildArch:  noarch
Requires:   inotify-tools

Source0:    llvm-pgo-instrumentation-macros.md
Source1:    macros.llvm-pgo-instrumentation
Source2:    pgo-background-merge.sh
Source3:    LICENSE

%global debug_package %{nil}
%global rrcdir /usr/lib/rpm/redhat

%description
Provides llvm_pgo_instrumented_XXX macros to be used in the "redhat-rpm-config"
package to tap into the build system and automatically generate a
"<PACKAGE>-<TOOLCHAIN>-pgo-profdata" subpackage. This subpackage will contain
indexed PGO profiling data. Make sure that you have a PGO instrumented
LLVM toolchain before installing the "llvm-pgo-instrumentation-macros" package.

%prep
# Not strictly necessary but allows working on file names instead
# of source numbers in install section
%setup -c -T
cp -p %{sources} .

%build

%install
mkdir -p %{buildroot}%{rrcdir}
install -p -m0644 -D macros.llvm-pgo-instrumentation %{buildroot}%{_rpmmacrodir}/macros.llvm-pgo-instrumentation
install -p -m 755 -t %{buildroot}%{rrcdir} pgo-background-merge.sh

%files
%license LICENSE
%doc llvm-pgo-instrumentation-macros.md
%dir %{rrcdir}
%{_rpmmacrodir}/macros.llvm-pgo-instrumentation
%{rrcdir}/pgo-background-merge.sh
%attr(0755,-,-) %{rrcdir}/pgo-background-merge.sh

%changelog
* Mon Apr 03 2023 Konrad Kleine <kkleine@redhat.com> - 0.0.1-1
- Initial Release
