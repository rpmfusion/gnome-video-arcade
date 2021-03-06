%define gtk3_version 3.0
%define libwnck3_version 2.91.6
%define mame_data_version 0.130-1

### Abstract ###

Name: gnome-video-arcade
Version: 0.8.6
Release: 2%{?dist}
License: GPLv3+
Group: Applications/Emulators
Summary: GNOME Video Arcade is a MAME front-end for GNOME
URL: http://mbarnes.github.com/gnome-video-arcade/
Source: http://download.gnome.org/sources/%{name}/0.8/%{name}-%{version}.tar.xz

### Dependencies ###

Requires: mame
Requires: mame-data >= %{mame_data_version}

### Build Dependencies ###

BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: gsettings-desktop-schemas-devel
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: intltool
BuildRequires: libX11-devel
BuildRequires: libsoup-devel
BuildRequires: libwnck3-devel >= %{libwnck3_version}
BuildRequires: perl-XML-Parser
BuildRequires: sqlite-devel
BuildRequires: yelp-tools

%description
GNOME Video Arcade is a MAME front-end for GNOME.

%prep
%setup -q

%build
export MAME=/usr/bin/mame
%configure \
    --with-category-file=%{_datadir}/mame/Catver.ini \
    --with-history-file=%{_datadir}/mame/history.dat \
    --with-nplayers-file=%{_datadir}/mame/nplayers.ini
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

# Remove GTK-Doc files
rm -rf $RPM_BUILD_ROOT/%{_datadir}/gtk-doc/html/%{name}

%find_lang %{name} --with-gnome

%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &> /dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/GConf/gsettings/%{name}.convert
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/glib-2.0/schemas/org.gnome.VideoArcade.gschema.xml
%{_mandir}/man1/%{name}.1*

%changelog
* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Apr 16 2017 Sérgio Basto <sergio@serjux.com> - 0.8.6-1
- Update gnome-video-arcade to 0.8.6

* Mon Sep 14 2015 Matthew Barnes <mbarnes@redhat.com> - 0.8.5-1
- Update to 0.8.5

* Wed Aug 26 2015 Matthew Barnes <mbarnes@redhat.com> - 0.8.4-1
- Update to 0.8.4

* Mon Sep 24 2012 Matthew Barnes <mbarnes@redhat.com> - 0.8.3-2
- Require mame instead of sdlmame.

* Thu Feb 16 2012 Matthew Barnes <mbarnes@redhat.com> - 0.8.3-1
- Update to 0.8.3

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jan 15 2012 Matthew Barnes <mbarnes@redhat.com> - 0.8.1-1
- Update to 0.8.1
- Drop libX11 patch.

* Sun May 15 2011 Matthew Barnes <mbarnes@redhat.com> - 0.8.0-1
- Update to 0.8.0

* Mon May 31 2010 Matthew Barnes <mbarnes@redhat.com> - 0.7.1-1
- Update to 0.7.1
- Add build requirement for unique-devel.

* Thu Mar 11 2010 Matthew Barnes <mbarnes@redhat.com> - 0.7.0-1
- Update to 0.7.0
- Bump gtk2_version to 2.18.
- Add gstreamer-plugins-base build requirement.

* Sat Jan 23 2010 Matthew Barnes <mbarnes@redhat.com> - 0.6.8-1
- Update to 0.6.8

* Sun Apr 26 2009 Matthew Barnes <mbarnes@redhat.com> - 0.6.7-1
- Update to 0.6.7

* Sun Apr 05 2009 Matthew Barnes <mbarnes@redhat.com> - 0.6.6-2
- Explicitly require libXres-devel to work around a build issue in F-10.

* Sun Apr 05 2009 Matthew Barnes <mbarnes@redhat.com> - 0.6.6-1
- Update to 0.6.6
- Update URL tag to GitHub home page.
- Update Source tag to download.gnome.org.
- Add --with-nplayers-file configure option.
- Require sdlmame-data >= 0.130-1 for nplayers.ini (#416).

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.6.5-2
- rebuild for new F11 features

* Fri Nov 21 2008 Matthew Barnes <mbarnes@redhat.com> - 0.6.5-1
- Update to 0.6.5

* Sat Sep 27 2008 Matthew Barnes <mbarnes@redhat.com> - 0.6.4-1
- Update to 0.6.4

* Tue Aug 19 2008 Matthew Barnes <mbarnes@redhat.com> - 0.6.3-3
- Fix name of category file (Catver.ini, not catver.ini).

* Tue Jul 29 2008 Matthew Barnes <mbarnes@redhat.com> - 0.6.3-2
- First upload to rpmfusion.
- Add build requirement for intltool.

* Sun Jun 29 2008 Matthew Barnes <mbarnes@redhat.com> - 0.6.3-1
- Update to 0.6.3

* Mon Jun 16 2008 Matthew Barnes <mbarnes@redhat.com> - 0.6.2-1
- Update to 0.6.2
- Add build requirement for libwnck-devel.

* Sun May 25 2008 Matthew Barnes <mbarnes@redhat.com> - 0.6.1.1-1
- Update to 0.6.1.1

* Sat May 17 2008 Matthew Barnes <mbarnes@redhat.com> - 0.6.1-1
- Update to 0.6.1

* Sat Apr 19 2008 Matthew Barnes <mbarnes@redhat.com> - 0.6.0-1
- Update to 0.6.0
- Bump GTK+ requirement to 2.12.

* Sun Mar 02 2008 Matthew Barnes <mbarnes@redhat.com> - 0.5.6-2
- Add build requirement for gnome-icon-theme.

* Sat Mar 01 2008 Matthew Barnes <mbarnes@redhat.com> - 0.5.6-1
- Update to 0.5.6

* Fri Jan 11 2008 Matthew Barnes <mbarnes@redhat.com> - 0.5.5-1
- Update to 0.5.5

* Thu Dec 27 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.4-1
- Update to 0.5.4
- Require sdlmame-data >= 0.122-2 for catver.ini (#125).

* Sun Dec 09 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.3-3
- Fix a scrollkeeper issue on Fedora 7 (patch by Ian Chapman).

* Sat Dec 08 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.3-2
- Use full URL for Source tag, add missing BRs, install ChangeLog.

* Mon Dec 03 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.3-1
- Initial packaging for Dribble repository.
