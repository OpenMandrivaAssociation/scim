%define version	1.4.5
%define release	%mkrel 3

%define libname_orig lib%{name}
%define libname %mklibname %{name} 8

Name:		scim
Summary:	Smart Common Input Method platform
Version:	%{version}
Release:	%{release}
Group:		System/Internationalization
License:	LGPL
# alt URL:	http://sourceforge.net/projects/scim/
URL:		http://www.scim-im.org
Source0:	http://ufpr.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.bz2

# new icons (from fedora)
Source1:	scim-icons-0.6.tar.bz2

# change hot keys per locale (from fedora)
Patch1:		scim-initial-locale-hotkey-186861.patch
Patch2:		scim-system-default-config.patch

# add scim-restart (from fedora)
Patch3:		scim-add-restart.patch

# Patches from openSUSE
# Novell bug#232014
Patch4:		scim-1.4.5-fix-for-openoffice.patch
# Novell bug#224796
Patch5:		scim-1.4.5-compose-key-fix.patch

Patch6:		scim-1.4.5-do-not-return-random-data-in-a-function.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires:		pango
Requires:		%{libname} = %{version}
Requires:		gtk+2.0 >= 2.4.4-2mdk
Requires(pre):		%_bindir/gtk-query-immodules-2.0
BuildRequires:		gtk+2-devel pango-devel libltdl-devel atk intltool
BuildRequires:		libGConf2-devel

%description
SCIM is a developing platform to significant reduce the difficulty of 
input method development. 


%package -n %{libname}
Summary:	SCIM library
Group:		System/Internationalization
Provides:		%{libname_orig} = %{version}-%{release}
Requires:		scim
Obsoletes:		libscim0

%description -n %{libname}
SCIM library.

%package -n %{libname}-devel
Summary:	Headers of SCIM for development
Group:		Development/C
Requires:		%{libname} = %{version}
Provides:		%{name}-devel = %{version}-%{release}
Provides:		%{libname_orig}-devel = %{version}-%{release}
Obsoletes:		libscim0-devel

%description -n %{libname}-devel
Headers of %{name} for development.

%prep
%setup -q -a1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p0
%patch6 -p1

# update icons
cp -p scim-icons/icons/*.png data/icons
cp -p scim-icons/pixmaps/*.png data/pixmaps

%build
[[ -f configure ]] || ./bootstrap

%configure2_5x --disable-schemas-install

%make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install-strip

mkdir -p ${RPM_BUILD_ROOT}/%{_libdir}/scim-1.0/{Config,FrontEnd,IMEngine,SetupUI,Helper}

# remove unneeded files
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/scim-1.0/*/*/*.{a,la}
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/gtk-2.0/immodules/im-scim.{a,la}

# install user manual
mkdir -p docs/dist/manual/zh_CN/figures/
	cp -a docs/manual/zh_CN/user-manual.{html,xml} docs/dist/manual/zh_CN/
	cp -a docs/manual/zh_CN/figures/*.png docs/dist/manual/zh_CN/figures/

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname}
/sbin/ldconfig
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%postun -n %{libname}
/sbin/ldconfig
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib


%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING README ChangeLog TODO
%doc docs/dist/manual/zh_CN
%dir %{_sysconfdir}/scim
%dir %{_datadir}/scim
%dir %{_datadir}/scim/icons
%config(noreplace) %{_sysconfdir}/scim/*
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/control-center-2.0/capplets/*
%{_datadir}/pixmaps/*.png
%{_datadir}/scim/icons/*.png
%{_libexecdir}/scim*/[^1]*

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%dir %{_libdir}/scim-1.0/Config
%dir %{_libdir}/scim-1.0/FrontEnd
%dir %{_libdir}/scim-1.0/SetupUI
%{_libdir}/lib*.so.*
%{_libdir}/scim-1.0/*/*/*.so
%{_libdir}/gtk-2.0/immodules/im-scim.so

%files -n %{libname}-devel
%defattr(-,root,root)
%doc COPYING
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/scim-1.0/*.h
%{_includedir}/scim-1.0/gtk/*.h
%{_includedir}/scim-1.0/x11/scim_x11_utils.h


