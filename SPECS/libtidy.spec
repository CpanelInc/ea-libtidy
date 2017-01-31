
%define libname libtidy

%define snap 20091203

Name:    tidy
Summary: Utility to clean up and pretty print HTML/XHTML/XML
Version: 0.99.0
Release: 31.%{snap}%{?dist}

Group:   Applications/Text
License: W3C
URL:     http://tidy.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: tidy-%{snap}cvs.tar.gz
Source1: tab2space.1

Patch0: tidy-20091203cvs-format.patch

BuildRequires: libtool
BuildRequires: doxygen
BuildRequires: libxslt

Requires: %{libname}%{?_isa} = %{version}-%{release}

%description
When editing HTML it's easy to make mistakes. Wouldn't it be nice if
there was a simple way to fix these mistakes automatically and tidy up
sloppy editing into nicely layed out markup? Well now there is! Dave
Raggett's HTML TIDY is a free utility for doing just that. It also
works great on the atrociously hard to read markup generated by
specialized HTML editors and conversion tools, and can help you
identify where you need to pay further attention on making your pages
more accessible to people with disabilities.

%package -n %{libname}
Summary: Shared libraries for %{name}
Group:   System Environment/Libraries
%description -n %{libname}
%{summary}.

%package -n %{libname}-devel
Summary: Development files for %{name}
Group:   Development/Libraries
Obsoletes: tidy-devel < 0.99.0-10
Provides:  tidy-devel = %{version}-%{release}
Requires: %{libname}%{?_isa} = %{version}-%{release}
%description -n %{libname}-devel
%{summary}.


%prep
%setup -q -n %{name}
%patch0 -p1 -b .format

# htmldocs included in cvs checkout
#setup -q -n %{name} -T -D -b1

sh build/gnuauto/setup.sh


%build
%configure \
  --disable-static \
  --disable-dependency-tracking

make %{?_smp_mflags}

# api docs
doxygen htmldoc/doxygen.cfg

# make doc steps gleaned from build/gmake/Makefile
pushd htmldoc
../console/tidy -xml-config > tidy-config.xml
../console/tidy -xml-help   > tidy-help.xml
xsltproc -o tidy.1 tidy1.xsl tidy-help.xml
xsltproc -o quickref.html quickref-html.xsl tidy-config.xml
popd


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

install -p -m644 -D htmldoc/tidy.1 $RPM_BUILD_ROOT%{_mandir}/man1/tidy.1
install -p -m644  %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1/

## Unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la


%clean
rm -rf $RPM_BUILD_ROOT

%check
cp test/testone.sh{,~}
sed -i 's|TIDY=../bin/tidy|TIDY=../console/tidy|' test/testone.sh
cd test
./testall.sh
mv testone.sh{~,}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc htmldoc/*.html htmldoc/*.css htmldoc/*.gif
%{_bindir}/tab2space
%{_bindir}/tidy
%{_mandir}/man1/tidy.1*
%{_mandir}/man1/tab2space.1*

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/libtidy-0.99.so.0*

%files -n %{libname}-devel
%defattr(-,root,root,-)
%doc htmldoc/api/*
%{_includedir}/*.h
%{_libdir}/libtidy.so


%changelog
* Tue Dec 03 2013 Pavel Raiskup <praiskup@redhat.com> - 0.99.0-31.20091203
- silence gcc's warnings for -Werror=format-string (#1037356)

* Thu Oct 10 2013 Pavel Raiskup <praiskup@redhat.com> - 0.99.0-30.20091203
- enable testsuite during package build

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-29.20091203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Pavel Raiskup <praiskup@redhat.com> - 0.99.0-28.20091203
- add manual page for tab2space

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-27.20091203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-26.20091203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Rex Dieter <rdieter@fedoraproject.org> 0.99.0-25.20091203
- rebuild 2, the wrath of doxygen (#831423)

* Thu Jun 14 2012 Rex Dieter <rdieter@fedoraproject.org> 0.99.0-24.20091203
- rebuild fyand (for yet another newer doxygen) (#831423)

* Wed Jun 13 2012 Rex Dieter <rdieter@fedoraproject.org> 0.99.0-23.20091203
- rebuild for newer doxygen, avoid html doc multilib conflict (#831423)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-22.20091203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-21.20091203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.99.0-20.20091203
- 20091203 snapshot
- spec housecleaning
- Tidy erroniously removes whitespace, causing mangled text (#481350)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-19.20070615
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-18.20070615
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 11 2008 Rex Dieter <rdieter@fedoraproject.org> 0.99.0-17.20070615
- respin (gcc43)

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.99.0-16.20070615
- respin (BuildID)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.99.0-15.20070615
- License: W3C

* Tue Jul 31 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.99.0-14.20070615
- BR: libtool (again)

* Mon Jul 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.99.0-13.20070615
- 2007-06-15 snapshot

* Wed Feb 28 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.99.0-12.20070228
- 2007-02-28 snapshot

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.99.0-11.20051025
- fc6 respin

* Wed Jul 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.99.0-10.20051025
- fc6 respin

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Fri Jan 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.99.0-9.20051025
- libtidy returns to be multilib friendly

* Wed Oct 26 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.99.0-8.20051025
- Update to 051025 and docs to 051020

* Tue Aug  9 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.99.0-7.20050803
- -devel: Provides: libtidy-devel (#165452)

* Tue Aug  9 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.99.0-6.20050803
- cleanup doc generation
- add/restore missing docs (manpage, quickref.html)

* Mon Aug  8 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.99.0-5.20050803
- Update to 050803 and docs to 050705
- simplify (fedora.us bug #2071)
- drop missing manpage

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.99.0-4.20041214
- rebuild on all arches

* Fri Apr  8 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Dec 16 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-2.20041214
- Update to 041214 and docs to 041206.
- Build with dependency tracking disabled.

* Sun Oct  3 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040916
- Update to 040916 and docs to 040810.

* Fri Aug 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040811
- Update to 040811, patches applied upstream.

* Wed Jul 28 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040720
- Update to 040720.
- Add partial fix (still incorrect for XHTML 1.1) for usemap handling.

* Mon Jul  5 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040704
- Update to 040704.

* Fri Jun 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040622
- Update to 040622.

* Sat Jun  5 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040603
- Update to 040603.

* Sat May 15 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040514
- Update to 040514.

* Sun May  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040318
- Update docs to 040317, and generate API docs ourselves.

* Fri Mar 19 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040318
- Update to 040318.

* Tue Mar 16 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040315
- Update to 040315.

* Mon Mar 15 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040314
- Update to 040314.

* Sun Mar 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040313
- Update to 040313.

* Sun Feb  8 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040205
- Update to 040205.

* Wed Feb  4 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040202
- Update to 040202.

* Sun Feb  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040130
- Update to 040130.

* Sun Jan 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040124
- Update to 040124.
- Honor optflags more closely.

* Sun Jan 11 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040110
- Update to 040110.

* Thu Jan  8 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040106
- Update to 040106.

* Tue Jan  6 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040104
- Update to 040104.

* Sun Nov  2 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20031101
- Update to 031101.

* Thu Oct 30 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20031029
- Update to 031029.

* Fri Oct  3 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20031002
- Update to 031002.

* Sat Sep 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20030926
- Update to 030926.

* Wed Sep  3 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20030901
- Update to 030901.

* Sat Aug 16 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20030815
- Update to 030815.

* Sat Aug  2 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20030801
- Update to 030801.

* Mon Jul 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20030716
- First build.
