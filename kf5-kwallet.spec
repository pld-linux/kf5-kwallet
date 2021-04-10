# TODO:
# Not packaged:
# - build with kf5-gpgmepp
%define		kdeframever	5.81
%define		qtver		5.14.0
%define		kfname		kwallet

Summary:	Safe desktop-wide storage for passwords
Name:		kf5-%{kfname}
Version:	5.81.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	6f041165cf080b6dd51adaa81cda5596
URL:		http://www.kde.org/
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.5
BuildRequires:	gpgme-c++-devel >= 1:1.7.0
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	kf5-kconfig-devel >= %{version}
BuildRequires:	kf5-kconfigwidgets-devel >= %{version}
BuildRequires:	kf5-kcoreaddons-devel >= %{version}
BuildRequires:	kf5-kdbusaddons-devel >= %{version}
BuildRequires:	kf5-kdoctools-devel >= %{version}
BuildRequires:	kf5-ki18n-devel >= %{version}
BuildRequires:	kf5-knotifications-devel >= %{version}
BuildRequires:	kf5-kservice-devel >= %{version}
BuildRequires:	kf5-kwidgetsaddons-devel >= %{version}
BuildRequires:	kf5-kwindowsystem-devel >= %{version}
BuildRequires:	libgcrypt-devel >= 1.5.0
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt5DBus >= %{qtver}
Requires:	Qt5Gui >= %{qtver}
Requires:	Qt5Widgets >= %{qtver}
Requires:	gpgme-c++ >= 1:1.7.0
Requires:	kf5-dirs
Requires:	kf5-kconfig >= %{version}
Requires:	kf5-kconfigwidgets >= %{version}
Requires:	kf5-kcoreaddons >= %{version}
Requires:	kf5-kdbusaddons >= %{version}
Requires:	kf5-ki18n >= %{version}
Requires:	kf5-knotifications >= %{version}
Requires:	kf5-kservice >= %{version}
Requires:	kf5-kwidgetsaddons >= %{version}
Requires:	kf5-kwindowsystem >= %{version}
Requires:	libgcrypt >= 1.5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
This framework contains two main components:
- Interface to KWallet, the safe desktop-wide storage for passwords on
  KDE work spaces.
- The kwalletd used to safely store the passwords on KDE work spaces.

The library can be built alone, without kwalletd, by setting the
`BUILD_KWALLETD` option to `OFF`.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Gui-devel >= %{qtver}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%ninja_build

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/kwalletd5
%attr(755,root,root) %{_bindir}/kwallet-query
%ghost %{_libdir}/libKF5Wallet.so.5
%attr(755,root,root) %{_libdir}/libKF5Wallet.so.*.*
%ghost %{_libdir}/libkwalletbackend5.so.5
%attr(755,root,root) %{_libdir}/libkwalletbackend5.so.*.*
%{_datadir}/dbus-1/interfaces/kf5_org.kde.KWallet.xml
%{_datadir}/dbus-1/services/org.kde.kwalletd5.service
%{_datadir}/knotifications5/kwalletd.notifyrc
%{_datadir}/kservices5/kwalletd5.desktop
%{_datadir}/qlogging-categories5/kwallet.categories
%{_datadir}/qlogging-categories5/kwallet.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KWallet
%{_includedir}/KF5/kwallet_version.h
%{_libdir}/cmake/KF5Wallet
%{_libdir}/libKF5Wallet.so
%{_libdir}/libkwalletbackend5.so
%{qt5dir}/mkspecs/modules/qt_KWallet.pri
%{_mandir}/man1/kwallet-query.1*
