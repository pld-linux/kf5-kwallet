# TODO:
# Not packaged:
# - build with kf5-gpgmepp
#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeframever	5.116
%define		qt_ver		5.15.2
%define		kfname		kwallet

Summary:	Safe desktop-wide storage for passwords
Summary(pl.UTF-8):	Bezpieczny schowek na hasła dla całego środowiska
Name:		kf5-%{kfname}
Version:	5.116.0
Release:	2
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	2e24331b2a1e6253c18d45481ae9f90d
URL:		https://kde.org/
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5DBus-devel >= %{qt_ver}
BuildRequires:	Qt5Gui-devel >= %{qt_ver}
BuildRequires:	Qt5Test-devel >= %{qt_ver}
BuildRequires:	Qt5Widgets-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gpgmepp-devel >= 1:1.7.0
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
BuildRequires:	qca-qt5-devel
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
# allow using also kf6-kwallet-service (for parallel install of kf5-kwallet and kf6-kwallet)
Requires:	%{name}-service >= %{version}-%{release}
Requires:	Qt5DBus >= %{qt_ver}
Requires:	Qt5Gui >= %{qt_ver}
Requires:	Qt5Widgets >= %{qt_ver}
Requires:	gpgmepp >= 1:1.7.0
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

%description -l pl.UTF-8
Ten szkielet składa się z dwóch komponentów:
- interfejsu do KWallet - bezpiecznego schowka na hasła dla przestreni
  roboczych KDE
- usługi kwalletd służącej do bezpiecznego przechowywania haseł w
  przestrzeniach roboczych KDE

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Gui-devel >= %{qt_ver}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%package service
Summary:	KWallet server and query interface
Summary(pl.UTF-8):	Serwer KWallet i interfejs do zapytań
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Conflicts:	kf6-kwallet

%description service
KWallet server and query interface.

%description service -l pl.UTF-8
Serwer KWallet i interfejs do zapytań.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# kwallet-query and kwalletd5 domains
%find_lang %{kfname} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libKF5Wallet.so.*.*.*
%ghost %{_libdir}/libKF5Wallet.so.5
%attr(755,root,root) %{_libdir}/libkwalletbackend5.so.*.*.*
%ghost %{_libdir}/libkwalletbackend5.so.5
%{_datadir}/dbus-1/interfaces/kf5_org.kde.KWallet.xml
%{_datadir}/qlogging-categories5/kwallet.categories
%{_datadir}/qlogging-categories5/kwallet.renamecategories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF5Wallet.so
%{_libdir}/libkwalletbackend5.so
%{_includedir}/KF5/KWallet
%{_libdir}/cmake/KF5Wallet
%{qt5dir}/mkspecs/modules/qt_KWallet.pri

%files service
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kwallet-query
%attr(755,root,root) %{_bindir}/kwalletd5
%{_datadir}/dbus-1/services/org.kde.kwalletd5.service
%{_datadir}/knotifications5/kwalletd5.notifyrc
%{_datadir}/kservices5/kwalletd5.desktop
%{_desktopdir}/org.kde.kwalletd5.desktop
%{_mandir}/man1/kwallet-query.1*
