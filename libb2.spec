#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	gomp		# OpenMP support
#
Summary:	C library providing BLAKE2b, BLAKE2s, BLAKE2bp, BLAKE2sp
Summary(pl.UTF-8):	Biblioteka C udostępniająca algorytmy BLAKE2b, BLAKE2s, BLAKE2bp, BLAKE2sp
Name:		libb2
Version:	0.98.1
Release:	1
License:	CC0 v1.0
Group:		Libraries
#Source0Download: https://github.com/BLAKE2/libb2/releases
Source0:	https://github.com/BLAKE2/libb2/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	dedace2ae596f37752943d99392ed100
Patch0:		%{name}-opt.patch
URL:		https://github.com/BLAKE2/libb2
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.9
BuildRequires:	libtool >= 2:2
%if %{with gomp}
BuildRequires:	gcc >= 6:4.2
BuildRequires:	libgomp-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C library providing BLAKE2b, BLAKE2s, BLAKE2bp, BLAKE2sp.

%description -l pl.UTF-8
Biblioteka C udostępniająca algorytmy BLAKE2b, BLAKE2s, BLAKE2bp,
BLAKE2sp.

%package devel
Summary:	Header files for BLAKE2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki BLAKE2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for BLAKE2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki BLAKE2.

%package static
Summary:	Static BLAKE2 library
Summary(pl.UTF-8):	Statyczna biblioteka BLAKE2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static BLAKE2 library.

%description static -l pl.UTF-8
Statyczna biblioteka BLAKE2.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-native \
	%{!?with_gomp:--disable-openmp} \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no external dependencies, obsolete by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libb2.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_libdir}/libb2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libb2.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libb2.so
%{_includedir}/blake2.h
%{_pkgconfigdir}/libb2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libb2.a
%endif
