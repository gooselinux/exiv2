
%if 0%{?fedora} > 7 || 0%{?rhel} >= 6
# make -libs subpkg
%define libs 1
%endif

Summary: Exif and Iptc metadata manipulation library
Name:	 exiv2
Version: 0.18.2
Release: 2.1%{?dist}

License: GPLv2+
Group:	 Applications/Multimedia
URL: 	 http://www.exiv2.org/
Source0: http://www.exiv2.org/exiv2-%{version}%{?pre:-%{pre}}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: chrpath
BuildRequires: expat-devel
BuildRequires: gettext
BuildRequires: pkgconfig
BuildRequires: zlib-devel
# docs
#BuildRequires: doxygen graphviz libxslt

Patch1: exiv2-0.18-deps.patch
Patch2: exiv2-0.18.1-visibility.patch

%if 0%{?libs}
Requires: %{name}-libs = %{version}-%{release}
%else
Obsoletes: %{name}-libs < %{version}-%{release}
Provides:  %{name}-libs = %{version}-%{release}
%endif


%description
A command line utility to access image metadata, allowing one to:
* print the Exif metadata of Jpeg images as summary info, interpreted values,
  or the plain data for each tag
* print the Iptc metadata of Jpeg images
* print the Jpeg comment of Jpeg images
* set, add and delete Exif and Iptc metadata of Jpeg images
* adjust the Exif timestamp (that's how it all started...)
* rename Exif image files according to the Exif timestamp
* extract, insert and delete Exif metadata (including thumbnails),
  Iptc metadata and Jpeg comments

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group:	 Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig
%description devel
%{summary}.

%if 0%{?libs}
%package libs
Summary: Exif and Iptc metadata manipulation library
Group: System Environment/Libraries
%description libs
A C++ library to access image metadata, supporting full read and write access
to the Exif and Iptc metadata, Exif MakerNote support, extract and delete 
methods for Exif thumbnails, classes to access Ifd and so on.
%endif


%prep
%setup -q -n %{name}-%{version}%{?pre:-%{pre}}

%patch1 -p1 -b .deps
## drop for now, seems no longer needed as of 0.18.2
%patch2 -p1 -b .visibility

mkdir doc/html


%build
%configure \
  --disable-rpath \
  --disable-static 

make %{?_smp_mflags} 


%install
rm -rf %{buildroot} 

make install DESTDIR=%{buildroot}

%find_lang exiv2

# Unpackaged files
rm -f %{buildroot}%{_libdir}/lib*.la

# fix perms on installed lib
chmod 755 %{buildroot}%{_libdir}/lib*.so*

# nuke rpaths
chrpath --list   %{buildroot}%{_bindir}/exiv2
chrpath --delete %{buildroot}%{_bindir}/exiv2


%clean
rm -rf %{buildroot} 


%post %{?libs:libs} -p /sbin/ldconfig

%postun %{?libs:libs} -p /sbin/ldconfig


%files %{!?libs:-f exiv2.lang} 
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/exiv2
%{_mandir}/man1/*

%if 0%{?libs}
%files libs -f exiv2.lang
%defattr(-,root,root,-)
%endif
%{_libdir}/libexiv2.so.5*

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_includedir}/exiv2/
%{_libdir}/libexiv2.so
%{_libdir}/pkgconfig/exiv2.pc


%changelog
* Fri Nov 13 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.18.2-2.1
- Fix conditional for RHEL

* Fri Aug 07 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.18.2-2
- (again) drop -fvisibility-inlines-hidden (#496050)

* Fri Jul 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.18.2-1
- exiv2-0.18.2
- drop visibility patch

* Fri Apr 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.18.1-1
- exiv2-0.18.1
- drop -fvisibility-inlines-hidden (#496050)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Rex Dieter <rdieter@fedoraproject.org> 0.18-1
- exiv2-0.18

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 0.17.2-2
- rebuild for pkgconfig deps

* Mon Jun 23 2008 Rex Dieter <rdieter@fedoraproject.org> 0.17.1-1
- exiv2-0.17.1

* Mon Feb 11 2008 Rex Dieter <rdieter@fedoraproject.org> 0.16-2
- respin (gcc43)
- gcc43 patch

* Sun Jan 13 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-1
- eviv2-0.16

* Mon Dec 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-0.3.pre1
- CVE-2007-6353 (#425924)

* Mon Nov 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-0.2.pre1
- -libs subpkg toggle (f8+)

* Tue Nov 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-0.1.pre1
- exiv2-0.16-pre1

* Tue Sep 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-4
- -libs: -Requires: %%name

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-3
- -libs subpkg to be multilib-friendlier (f8+)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-2
- License: GPLv2+

* Thu Jul 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-1
- exiv2-0.15

* Mon Apr 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.14-1
- exiv2-0.14

* Tue Nov 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.12-1
- exiv2-0.12

* Wed Oct 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.11-3
- respin

* Tue Sep 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.11-2
- BR: zlib-devel

* Tue Sep 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.11-1
- exiv2-0.11

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.10-2
- fc6 respin

* Sat Jun 03 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.10-1
- 0.10

* Wed May 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.1-3
- cleanup %%description
- set eXecute bit on installed lib.
- no_rpath patch
- deps patch (items get (re)compiled on *every* call to 'make')

* Wed May 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.1-2
- %%post/%%postun: /sbin/ldconfig

* Tue May 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.1-1
- first try
