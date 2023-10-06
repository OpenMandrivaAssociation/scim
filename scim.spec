%global optflags %{optflags} -Wno-c++11-narrowing

# The bootstrap script inside the source tree already does this
%define _disable_rebuild_configure 1

%bcond_with qt4
%define apiver 1.0
%define scim_api 1.4.0
%define major 8
%define oldlibname %mklibname %{name} %apiver %major
%define libname %mklibname %{name}
%define libxname %mklibname %{name}-x11utils
%define libgname %mklibname %{name}-gtkutils
%define develname %mklibname -d %{name}
%define develxname %mklibname -d %{name}-x11utils
%define develgname %mklibname -d %{name}-gtkutils

Name:		scim
Summary:	Smart Common Input Method platform
Version:	1.4.18
Release:	5
Group:		System/Internationalization
License:	LGPLv2+
URL:		https://github.com/scim-im
Source0:	https://github.com/scim-im/scim/archive/%{version}.tar.gz
# new icons (from fedora)
Source1:	scim-icons-0.7.tar.bz2
# change hot keys per locale (from fedora)
Source2:	scim-system-config
# add scim dir macros
Source3:	scim.macros
Patch0:		scim-1.4.14-compile.patch
Patch1:		scim-initial-locale-hotkey-20070922.patch
Patch5:		scim-1.4.7-support-more-utf8-locales.patch
BuildRequires:	pkgconfig(gdk-2.0) pkgconfig(pango) libtool-devel pkgconfig(atk) intltool

Requires:	%{name}-common = %version-%release
# fwang: in fact, scim could interact with gtk2 apps via xim
#Suggests:	%{name}-gtk
Conflicts:	%{libname} < 1.4.7-8
Conflicts:	%{mklibname scim 8} < 1.4.7-8

%description
SCIM is a developing platform to significant reduce the difficulty of 
input method development. 

%files
%doc AUTHORS COPYING README ChangeLog TODO
%{_bindir}/scim

#----------------------------------------------------------------------
%package -n %{libname}
Summary:	SCIM library
Group:		System/Internationalization
Requires:	%name-common = %version
Obsoletes:	%mklibname scim 0
Obsoletes:	%mklibname scim 8
Conflicts:	%{name} < 1.4.7-8
%rename %{oldlibname}

%description -n %{libname}
SCIM library.

%files -n %{libname}
%{_libdir}/libscim-1.0.so.%{major}*

#----------------------------------------------------------------------
%package -n %{libxname}
Summary:	SCIM X11 utility library
Group:		System/Internationalization
Requires:	%{libname} = %{EVRD}

%description -n %{libxname}
SCIM X11 utility library.

%files -n %{libxname}
%{_libdir}/libscim-x11utils-1.0.so.%{major}*

#----------------------------------------------------------------------
%package -n %{libgname}
Summary:	SCIM GTK utility library
Group:		System/Internationalization
Requires:	%{libname} = %{EVRD}

%description -n %{libgname}
SCIM GTK utility library.

%files -n %{libgname}
%{_libdir}/libscim-gtkutils-1.0.so.%{major}*

#----------------------------------------------------------------------
%package common
Summary:        SCIM common files
Group:          System/Internationalization
Requires:       %{libname} = %version-%release
Conflicts:      %{libname} < 1.4.7-8
Conflicts:	%{mklibname scim 8} < 1.4.7-8
Conflicts:	%{name} < 1.4.7-10

%description common
Common files for scim input method.

%files common -f %name.lang
%_bindir/scim-im-agent
%{_bindir}/scim-setup
%{_bindir}/scim-config-agent
%dir %{_sysconfdir}/scim
%config(noreplace) %{_sysconfdir}/scim/*
%{_libdir}/scim-1.0/scim-helper-launcher
%{_libdir}/scim-1.0/scim-helper-manager
%{_libdir}/scim-1.0/scim-launcher
%dir %{_libdir}/scim-1.0/%{scim_api}
%{_libdir}/scim-1.0/%{scim_api}/Filter
%{_libdir}/scim-1.0/%{scim_api}/FrontEnd
%dir %{_libdir}/scim-1.0/%{scim_api}/IMEngine
%{_libdir}/scim-1.0/%{scim_api}/IMEngine/socket.so
%{_libdir}/scim-1.0/%{scim_api}/IMEngine/rawcode.so
%{_libdir}/scim-1.0/%{scim_api}/Config
%{_datadir}/%{name}

#----------------------------------------------------------------------
%package gtk
Summary:	GTK input panel and configuration tools for scim
Group:          System/Internationalization
Requires:	%{name}-common = %{EVRD}

%description gtk
GTK input panel and configuration tools for scim

%files gtk
%{_libdir}/scim-1.0/scim-panel-gtk
%{_libdir}/scim-1.0/%{scim_api}/SetupUI
%{_libdir}/scim-1.0/%{scim_api}/Helper
%{_datadir}/applications/*.desktop
%{_datadir}/control-center-2.0/capplets/scim-setup.desktop
%{_datadir}/pixmaps/*

#----------------------------------------------------------------------
%package gtk2
Summary:        SCIM Gtk 2.x IM module
Group:          System/Internationalization
Requires:       %libname = %version-%release
Conflicts:      %{libname} < 1.4.7-8
Conflicts:	%{mklibname scim 8} < 1.4.7-8
Requires(post,postun):	gtk+2.0

%description gtk2
This package provides a GTK 2.x input method module for SCIM.

%post gtk2
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%postun gtk2
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%files gtk2
%defattr(-,root,root,-)
%{_libdir}/gtk-2.0/*/immodules/im-scim.so

#----------------------------------------------------------------------
%package gtk3
Summary:        SCIM Gtk 3.x IM module
Group:          System/Internationalization
Requires:       %libname = %version-%release
Conflicts:      %{libname} < 1.4.7-8
Conflicts:	%{mklibname scim 8} < 1.4.7-8
BuildRequires:	pkgconfig(gtk+-3.0)

%description gtk3
This package provides a GTK 3.x input method module for SCIM.

%files gtk3
%defattr(-,root,root,-)
%{_libdir}/gtk-3.0/*/immodules/im-scim.so

#----------------------------------------------------------------------
%if %{with qt4}
%package qt
Summary:        SCIM Qt IM module
Group:          System/Internationalization
Requires:       %libname = %version-%release
Conflicts:      %{libname} < 1.4.7-8
Conflicts:	%{mklibname scim 8} < 1.4.7-8
BuildRequires:	qt4-devel

%description qt
This package provides a Qt input method module for SCIM.

%files qt
%{_libdir}/qt4/plugins/inputmethods/im-scim.so
%endif

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
%{_libdir}/libscim-1.0.so
%{_libdir}/pkgconfig/scim.pc
%dir %{_includedir}/scim-1.0
%{_includedir}/scim-1.0/*.h
%{_sysconfdir}/rpm/macros.d/scim.macros

#----------------------------------------------------------------------
%package -n %{develxname}
Summary:	Headers of SCIM for development
Group:		Development/C
Requires:	%{libxname} = %{EVRD}
Requires:	%{develname} = %{EVRD}

%description -n %{develxname}
Headers of %{name} for development.

%files -n %{develxname}
%{_libdir}/libscim-x11utils-1.0.so
%{_libdir}/pkgconfig/scim-x11utils.pc
%{_includedir}/scim-1.0/x11

#----------------------------------------------------------------------
%package -n %{develgname}
Summary:	Headers of SCIM for GTK development
Group:		Development/C
Requires:	%{libgname} = %{EVRD}
Requires:	%{develxname} = %{EVRD}

%description -n %{develgname}
Headers of %{name} for GTK development.

%files -n %{develgname}
%{_libdir}/libscim-gtkutils-1.0.so
%{_libdir}/pkgconfig/scim-gtkutils.pc
%{_includedir}/scim-1.0/gtk
#----------------------------------------------------------------------

%prep
%setup -q -a1
%patch0 -p1 -b .compile~
%patch1 -p1 -b .hotkey~
%patch5 -p0 -b .utf8~

# update icons
cp -p scim-icons/icons/*.png data/icons
cp -p scim-icons/pixmaps/*.png data/pixmaps

# update the config file
mv configs/config{,.orig} 
cp -p %{SOURCE2} configs/config

%build
#export CC=gcc
#export CXX=g++
#export LIBS="-lX11"
./bootstrap
%configure --disable-static --enable-ld-version-script
%make

%install
%makeinstall_std

# remove unneeded files
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/scim-1.0/*/*/*.{a,la}
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/gtk-2.0/immodules/im-scim.{a,la}

# install scim.macros
install -D -m0644 %SOURCE3 %buildroot%{_sysconfdir}/rpm/macros.d/scim.macros

%find_lang %{name}
