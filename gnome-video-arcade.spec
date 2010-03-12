%define gtk2_version 2.18
%define libwnck_version 2.16
%define sdlmame_data_version 0.130-1
%define gnome_icon_theme_version 2.18

### Abstract ###

Name: gnome-video-arcade
Version: 0.7.0
Release: 1%{?dist}
License: GPLv3+
Group: Applications/Emulators
Summary: GNOME Video Arcade is a MAME front-end for GNOME
URL: http://mbarnes.github.com/gnome-video-arcade/
Source: http://download.gnome.org/sources/%{name}/0.7/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

### Dependencies ###

Requires(pre): GConf2 >= 2.14
Requires(preun): GConf2 >= 2.14
Requires(post): GConf2 >= 2.14
Requires(post): scrollkeeper
Requires(postun): scrollkeeper

Requires: sdlmame
Requires: sdlmame-data >= %{sdlmame_data_version}

### Build Dependencies ###

BuildRequires: gettext
BuildRequires: gnome-doc-utils
BuildRequires: gnome-icon-theme >= %{gnome_icon_theme_version}
BuildRequires: gstreamer-plugins-base-devel
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: intltool
BuildRequires: libwnck-devel >= %{libwnck_version}
BuildRequires: perl-XML-Parser
BuildRequires: scrollkeeper
BuildRequires: sqlite-devel

# Work around libXres-devel not getting
# pulled in by libwnck-devel on Fedora 10.
BuildRequires: libXres-devel

%description
GNOME Video Arcade is a MAME front-end for GNOME.

%prep
%setup -q

%build
%configure \
	--with-category-file=%{_datadir}/mame/Catver.ini	\
	--with-history-file=%{_datadir}/mame/history.dat	\
	--with-nplayers-file=%{_datadir}/mame/nplayers.ini
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT

# Remove GTK-Doc files
rm -rf $RPM_BUILD_ROOT/%{_datadir}/gtk-doc/html/%{name}

# Remove scrollkeeper crud on F7
rm -rf $RPM_BUILD_ROOT/%{_var}

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
scrollkeeper-update -q
export GCONF_CONFIG_SOURCES=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule                             \
        %{_sysconfdir}/gconf/schemas/gnome-video-arcade.schemas \
        >& /dev/null || :
touch %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%pre
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule                       \
        %{_sysconfdir}/gconf/schemas/gnome-video-arcade.schemas \
        >& /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule                       \
        %{_sysconfdir}/gconf/schemas/gnome-video-arcade.schemas \
        >& /dev/null || :
fi

%postun
scrollkeeper-update -q
touch %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%config %{_sysconfdir}/gconf/schemas/*.schemas
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_mandir}/man1/%{name}.1*
%{?fc7:%{_datadir}/omf/%{name}}

%changelog
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
