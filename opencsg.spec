%define major   1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define debug_package %nil

Name:           opencsg
Version:        1.4.0
Release:        1
Summary:        Library for Constructive Solid Geometry using OpenGL
Group:          System/Libraries
# license.txt contains a linking exception for CGAL
License:        GPLv2+ with exceptions
URL:            http://www.opencsg.org/
Source0:        http://www.opencsg.org/OpenCSG-%{version}.tar.gz
Patch0:         %{name}-build.patch

BuildRequires:  dos2unix
BuildRequires:  freeglut-devel
BuildRequires:  pkgconfig(glew)

%description
OpenCSG is a library that does image-based CSG rendering using OpenGL.

#----------------------------------------------------------------------------

%package -n     %{libname}
Summary:        Library for Constructive Solid Geometry using OpenGL
Group:          System/Libraries

%description -n %{libname}
OpenCSG is a library that does image-based CSG rendering using OpenGL.

CSG is short for Constructive Solid Geometry and denotes an approach to model
complex 3D-shapes using simpler ones. I.e., two shapes can be combined by
taking the union of them, by intersecting them, or by subtracting one shape
of the other.

%files -n       %{libname}
%doc changelog.txt doc/* license.txt
%{_libdir}/lib%{name}.so.%{major}*

#----------------------------------------------------------------------------

%package -n     %{devname}
Summary:        OpenCSG development files
Group:          Development/C++
Requires:       %{libname} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{devname}
Development files for OpenCSG.

%files -n       %{devname}
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so

#----------------------------------------------------------------------------

%prep
%setup -q -n OpenCSG-%{version}
%apply_patches

# Use system glew
rm -rf glew/


%build
# we don't want to install qt4 here
# just build wihtout qmake4
sed -i 's|-rpath,../lib|-rpath,/usr/lib|' src/Makefile
# use _cc
sed -i 's|g++|%{__cxx}|g' src/Makefile
sed -i 's|gcc|%{__cc}|g' src/Makefile
pushd src
%make

%install
# No make install
chmod g-w lib/*
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
cp -pP lib/* %{buildroot}%{_libdir}/
cp -p include/%{name}.h %{buildroot}%{_includedir}/
