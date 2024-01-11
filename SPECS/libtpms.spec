%global gitdate   20211126
%global gitversion 1ff6fe1f43

Name:           libtpms
Version:        0.9.1
Release:        2.%{gitdate}git%{gitversion}%{?dist}

Summary: Library providing Trusted Platform Module (TPM) functionality
License:        BSD
Url:            http://github.com/stefanberger/libtpms
Source0:        libtpms-%{gitdate}.tar.xz
ExcludeArch:    i686
Patch0003:      0001-tpm2-When-writing-state-initialize-s_ContextSlotMask.patch
Patch0004:      0001-tpm2-Check-size-of-buffer-before-accessing-it-CVE-20.patch

BuildRequires:  openssl-devel
BuildRequires:  pkgconfig gawk sed
BuildRequires:  automake autoconf libtool bash coreutils gcc-c++
BuildRequires:  git
BuildRequires:  make

%description
A library providing TPM functionality for VMs. Targeted for integration
into Qemu.

%package        devel
Summary:        Include files for libtpms
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description   devel
Libtpms header files and documentation.

%prep
%autosetup -S git -n %{name}-%{gitdate}
%build
NOCONFIGURE=1 sh autogen.sh
%configure --disable-static --with-tpm2 --without-tpm1 --with-openssl
%make_build

%check
make check

%install
%make_install
find %{buildroot} -type f -name '*.la' | xargs rm -f -- || :

%ldconfig_scriptlets

%files
%license LICENSE
%doc README CHANGES
%{_libdir}/lib*.so.*

%files devel
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%changelog
* Tue Mar 21 2023 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.9.1-2.20211126git1ff6fe1f43
- Backport "tpm2: Check size of buffer before accessing it" (CVE-2023-1017 & CVE-2023-1018)
  Resolves: rhbz#2173964
  Resolves: rhbz#2173970

* Thu Jul 28 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.9.1-1.20211126git1ff6fe1f43
- Backport s_ContextSlotMask initialization fix
  Resolves: rhbz#2111433

* Thu Dec 09 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.9.1-0.20211126git1ff6fe1f43
- Rebase to 0.9.1 (sync with RHEL9)
  Resolves: rhbz#2029355

* Tue Aug 31 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.7.4-6.20201106git2452a24dab
- Fix CVE-2021-3746 libtpms: out-of-bounds access via specially crafted TPM 2 command packets
  Resolves: rhbz#1999307

* Mon Jun 28 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.7.4-5.20201106git2452a24dab
- Fix CVE-2021-3623: out-of-bounds access when trying to resume the state of the vTPM
  Fixes: rhbz#1976816

* Wed Mar 17 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.7.4-4.20201106git2452a24dab
- tpm2: CryptSym: fix AES output IV
  Fixes: rhbz#1942904

* Fri Feb 19 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 0.7.4-3.20201106git2452a24dab
- Add git as build dependency
  Related: rhbz#1858821

* Wed Feb 17 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.7.4-2.20201106git2452a24dab
- tpm2: Return properly sized array for b parameter for NIST P521 (HLK) #180 
  Fixes: rhbz#1858821

* Fri Nov  6 18:46:36 +04 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.7.4-1.20201106git2452a24dab
- Follow stable-0.7.0 branch to v0.7.4 with security-related fixes.
  Fixes: rhbz#1893444

* Tue Aug 18 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.7.3-1.20200818git1d392d466a
- Update to v0.7.3 stable, fixes rhbz#1868447
- (includes "tpm2: fix PCRBelongsTCBGroup for PCClient")

* Thu May 28 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.7.2-1.20200527git7325acb477
- Update to v0.7.2 stable snapshot, fixes rhbz#1809676
- exclude i686 build
- Following stable-0.7.0 branch for TPM 2 related fixes: RSA decryption,
  PSS salt length, symmetric decryption (padding)
- Under certain circumstances an RSA decryption could cause a buffer overflow causing
  termination of the program (swtpm)
- Following stable-0.7.0 branch for TPM 2 related fixes; v0.7.1 + gcc related patch
- elliptic curve fixes
- MANUFACTURER changed from "IBM " to "IBM"
- gcc 10 related fix
- Following stable-0.7.0 branch for TPM 1.2 related bugfix

* Fri Oct 18 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.7.0-1.20191018gitdc116933b7
- RHEL8.1.1 update
- Update to v0.7.0 stable snapshot

* Tue Apr 16 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.6.1-0.20190121git9dc915572b.2
- RHEL8.1 build

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-0.20190121git9dc915572b.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Stefan Berger <stefanb@linux.ibm.com> - 0.6.1-0.20190121git9dc915572b
- Libtpms was updated to rev. 150 of TPM 2.0 code
- following branch stable-0.6.0

* Tue Dec 11 2018 Stefan Berger <stefanb@linux.ibm.com> - 0.6.0-0.20181211gitba56737b93
- Following bugfixes in libtpms

* Wed Oct 31 2018 Stefan Berger <stefanb@linux.ibm.com> - 0.6.0-0.20181031git0466fcf6a4
- Following improvements in libtpms

* Tue Sep 18 2018 Stefan Berger <stefanb@linux.vnet.ibm.com - 0.6.0-0.20180918gite8e8633089
- Fixed changelog

* Mon Sep 17 2018 Stefan Berger <stefanb@linux.vnet.ibm.com - 0.6.0-0.20180917gite8e8633089
- Build snapshot from git after libtpms fix.

* Fri Sep 14 2018 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.6.0-0.20180914git4111bd1bcf
- Build snapshot from git, simplify spec

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 16 2014 Stefan Berger - 0.5.2-3
- do not include libtpms.la in rpm

* Mon Jul 14 2014 Stefan Berger - 0.5.2-2
- Added patches

* Mon Jun 30 2014 Stefan Berger - 0.5.2-1
- Updated to version 0.5.2
- coverity fixes
- fixes for ARM64 using __aarch64__

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-20.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Stefan Berger - 0.5.1-18
- Ran autoreconf for support of aarch64
- Checking for __arm64__ in code

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 17 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.5.1-15
- Add dist tag as required by package guidelines

* Fri Jan 27 2012 Stefan Berger - 0.5.1-14
- fix gcc-4.7 compilation problem

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Dan Horák <dan[at]danny.cz> - 0.5.1-12
- fix build on secondary arches

* Wed Nov 2 2011 Stefan Berger - 0.5.1-11
- added (lib)gmp as runtime dependency

* Sat Oct 8 2011 Stefan Berger - 0.5.1-10
- internal fixes; callback fixes

* Tue Aug 30 2011 Stefan Berger - 0.5.1-9
- new directory structure and build process

* Tue Jul 12 2011 Stefan Berger - 0.5.1-8
- added pkgconfig as build dependency
- enabling __powerpc__ build following Bz 728220

* Wed May 25 2011 Stefan Berger - 0.5.1-7
- increasing NVRAM area space to have enough room for certificates

* Wed May 25 2011 Stefan Berger - 0.5.1-6
- adding libtpms.pc pkg-config file

* Wed Apr 13 2011 Stefan Berger - 0.5.1-5
- adding BuildRequires for nss-softokn-freebl-static
- several libtpms-internal changes around state serialization and 
  deserialization
- fixes to libtpms makefile (makefile-libtpms)
- adding build_type to generate a debug or production build
- need nss-devel to have nss-config

* Tue Mar 08 2011 Stefan Berger - 0.5.1-4
- small fixes to libtpms makefile

* Fri Feb 25 2011 Stefan Berger - 0.5.1-3
- removing release from tar ball name
- Use {?_smp_mflags} for make rather than hardcoding it
- Fixing post and postun scripts; removing the scripts for devel package
- Fixing usage of defattr
- Adding version information into the changelog headers and spaces between the changelog entries
- Adding LICENSE, README and CHANGELOG file into tar ball and main rpm
- Removing clean section
- removed command to clean the build root
- adding library version to the libries required for building and during
  runtime
- Extended Requires in devel package with {?_isa}

* Fri Feb 18 2011 Stefan Berger - 0.5.1-2
- make rpmlint happy by replacing tabs with spaces
- providing a valid URL for the tgz file
- release is now 2 -> 0.5.1-2

* Mon Jan 17 2011 Stefan Berger - 0.5.1-1
- Update version to 0.5.1

* Fri Jan 14 2011 Stefan Berger - 0.5.0-1
- Changes following Fedora review comments

* Thu Dec 2 2010 Stefan Berger
- Small tweaks after reading the FedoreCore packaging requirements

* Tue Nov 16 2010 Stefan Berger
- Created initial version of rpm spec files
- Version of library is now 0.5.0
- Debuginfo rpm is built but empty -- seems to be a known problem
  Check https://bugzilla.redhat.com/show_bug.cgi?id=209316
