%define version	1.4.7
%define release	%mkrel 8

%define apiver 1.0
%define scim_api 1.4.0
%define major 8
%define libname %mklibname %{name} %apiver %major
%define develname %mklibname -d %{name}

Name:		scim
Summary:	Smart Common Input Method platform
Version:	%{version}
Release:	%{release}
Group:		System/Internationalization
License:	LGPLv2+
# alt URL:	http://sourceforge.net/projects/scim/
URL:		http://www.scim-im.org
Source0:	http://ufpr.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
# new icons (from fedora)
Source1:	scim-icons-0.7.tar.bz2
# change hot keys per locale (from fedora)
Source2:	scim-system-config
# add scim dir macros
Source3:	scim.macros
Patch1:		scim-initial-locale-hotkey-20070922.patch
Patch2:		scim-system-default-config.patch
# add scim-restart (from fedora)
Patch3:		scim-add-restart.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	gtk+2-devel pango-devel libltdl-devel atk intltool
BuildRequires:	libGConf2-devel
# provides scim-client so that we could prefer scim-bridge over scim or the reverse
Provides:	scim-client

Requires:	%{name}-common = %version-%release
# fwang: in fact, scim could interact with gtk2 apps via xim
Suggests:	%{name}-gtk
Conflicts:	%{libname} < 1.4.7-8
Conflicts:	%{mklibname scim 8} < 1.4.7-8

%description
SCIM is a developing platform to significant reduce the difficulty of 
input method development. 

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog TODO
%{_bindir}/scim

#----------------------------------------------------------------------
%package -n %{libname}
Summary:	SCIM library
Group:		System/Internationalization
Requires:	%name = %version-%release
Obsoletes:	%mklibname scim 0
Obsoletes:	%mklibname scim 8
Conflicts:	%{name} < 1.4.7-8

%description -n %{libname}
SCIM library.

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/*.so.%{major}*

#----------------------------------------------------------------------
%package common
Summary:        SCIM common files
Group:          System/Internationalization
Requires:       %{libname} = %version-%release
Conflicts:      %{libname} < 1.4.7-8
Conflicts:	%{mklibname scim 8} < 1.4.7-8
Conflicts:	%{name} < 1.4.7-8

%description common
Common files for scim input method.

%post common
%update_menus

%postun common
%update_menus

%files common
%defattr(-,root,root,-)
%{_bindir}/scim-setup*
%dir %{_sysconfdir}/scim
%config(noreplace) %{_sysconfdir}/scim/*
%dir %{_libdir}/scim-1.0/%{scim_api}
%{_libdir}/scim-1.0/%{scim_api}/Filter
%{_libdir}/scim-1.0/%{scim_api}/FrontEnd
%{_libdir}/scim-1.0/%{scim_api}/Helper
%dir %{_libdir}/scim-1.0/%{scim_api}/IMEngine
%{_libdir}/scim-1.0/%{scim_api}/IMEngine/socket.so
%{_libdir}/scim-1.0/%{scim_api}/SetupUI
%{_libdir}/scim-1.0/%{scim_api}/Config
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}
%{_datadir}/pixmaps/*

#----------------------------------------------------------------------
%package gtk
Summary:        SCIM Gtk IM module
Group:          System/Internationalization
Requires:       %libname = %version-%release
Conflicts:      %{libname} < 1.4.7-8
Conflicts:	%{mklibname scim 8} < 1.4.7-8
Requires(post):	gtk+2.0
Requires(postun): gtk+2.0

%description gtk
This package provides a GTK input method module for SCIM.

%post gtk
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%postun gtk
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%files gtk
%defattr(-,root,root,-)
%{_libdir}/gtk-2.0/immodules/im-scim.so

#----------------------------------------------------------------------
%package -n %{develname}
Summary:	Headers of SCIM for development
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d scim 0
Obsoletes:	%mklibname -d scim 8

%description -n %{develname}
Headers of %{name} for development.

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/scim-1.0
%{_includedir}/scim-1.0/*.h
%{_includedir}/scim-1.0/gtk/*.h
%{_includedir}/scim-1.0/x11/scim_x11_utils.h
%{_sysconfdir}/rpm/macros.d/scim.macros
#----------------------------------------------------------------------

%prep
%setup -q -a1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# update icons
cp -p scim-icons/icons/*.png data/icons
cp -p scim-icons/pixmaps/*.png data/pixmaps

# update the config file
mv configs/config{,.orig} 
cp -p %{SOURCE2} configs/config

%build
[[ -f configure ]] || ./bootstrap

%configure2_5x --disable-schemas-install
%make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install-strip

# remove unneeded files
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/scim-1.0/*/*/*.{a,la}
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/gtk-2.0/immodules/im-scim.{a,la}

# install user manual
mkdir -p docs/dist/manual/zh_CN/figures/
	cp -a docs/manual/zh_CN/user-manual.{html,xml} docs/dist/manual/zh_CN/
	cp -a docs/manual/zh_CN/figures/*.png docs/dist/manual/zh_CN/figures/

# install scim.macros
install -D -m0644 %SOURCE3 %buildroot%{_sysconfdir}/rpm/macros.d/scim.macros

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT
