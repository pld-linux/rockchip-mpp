#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	Rockchip Media Process Platform libraries
Summary(pl.UTF-8):	Biblioteki Rockchip Media Process Platform
Name:		rockchip-mpp
Version:	20171218
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/rockchip-linux/mpp/releases
Source0:	https://github.com/rockchip-linux/mpp/archive/release_%{version}/mpp-%{version}.tar.gz
# Source0-md5:	6c2c941ebc506e6a3bd7d911dd8dc184
Patch0:		%{name}-no-march.patch
URL:		http://opensource.rock-chips.com/wiki_Mpp
BuildRequires:	cmake >= 2.8.8
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Rockchip Media Process Platform libraries.

%description -l pl.UTF-8
Biblioteki Rockchip Media Process Platform.

%package devel
Summary:	Header files for Rockchip MPP libraries
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Rockchip MPP
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Rockchip MPP libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Rockchip MPP.

%package static
Summary:	Static Rockchip MPP libraries
Summary(pl.UTF-8):	Statyczne biblioteki Rockchip MPP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Rockchip MPP libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Rockchip MPP.

%prep
%setup -q -n mpp-release_%{version}
%patch0 -p1

%build
# "build" directory is already occupied, so use "builddir"
install -d builddir
cd builddir
# .pc file creation expects relative include* and libdir
# build fails without RKPLATFORM (whatever it is)
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DENABLE_SHARED=ON \
	%{!?with_static_libs:-DENABLE_STATIC=OFF} \
	-DRKPLATFORM=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_bindir}/*_test

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc readme.txt
%attr(755,root,root) %{_libdir}/librockchip_mpp.so.0
%attr(755,root,root) %ghost %{_libdir}/librockchip_mpp.so.1
%attr(755,root,root) %{_libdir}/librockchip_vpu.so.0
%attr(755,root,root) %ghost %{_libdir}/librockchip_vpu.so.1

%files devel
%defattr(644,root,root,755)
%doc doc/readme.txt doc/design/*.txt
%attr(755,root,root) %{_libdir}/librockchip_mpp.so
%attr(755,root,root) %{_libdir}/librockchip_vpu.so
%{_includedir}/rockchip
%{_pkgconfigdir}/rockchip_mpp.pc
%{_pkgconfigdir}/rockchip_vpu.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/librockchip_mpp_static.a
%{_libdir}/librockchip_vpu_static.a
%endif
