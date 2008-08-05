Summary:		ACPI kernel daemon and control utility
Name:			acpid
Version:		1.0.6
Release:		%manbo_mkrel 5
License:		GPL
Group:			System/Servers
Epoch:			2
URL:			http://acpid.sourceforge.net
Source0:		http://unc.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.bz2
Source1:		acpid.rc
Patch0:			acpid-kernel-acpi-h.patch
Patch1:			acpid-1.0.6-ignore-rpmnew.patch
# patches from RH
Patch2:			acpid-1.0.6-warning.patch
Patch4:			%{name}-1.0.6-makefile.patch
Patch5:			acpid-1.0.6-fd.patch
Patch6:			acpid-1.0.6-log.patch
ExclusiveArch:		%{ix86} ia64 x86_64 amd64
Requires(post):		rpm-helper
Requires(preun):	rpm-helper
Conflicts:		suspend-scripts < 1.27-2mdv2007.1
BuildRoot:		%{_tmppath}/%{name}-%{version}-buildroot

%description
The ACPI specification defines power and system management functions
for each computer, in a generic manner. The ACPI daemon coordinates
the management of power and system functions when ACPI kernel
support is enabled (kernel 2.3.x or later).

%prep 
%setup -q

%patch0 -p1
%patch1 -p1 -b .rpmnew
%patch2 -p1 -b .warning
%patch4 -p1 -b .optflags
%patch5 -p1 -b .fd
%patch6 -p1 -b .log

%build
%serverbuild
%make

%install
%makeinstall_std INSTPREFIX=%{buildroot}

mkdir -p %{buildroot}/%{_initrddir}
install -m755 %{SOURCE1} %{buildroot}%{_initrddir}/acpid

install -d %{buildroot}%{_sysconfdir}/acpi/actions

%clean
rm -rf %{buildroot}

%post
%_post_service acpid

%preun
%_preun_service acpid

%files
%defattr(-,root,root)
%doc README TODO Changelog
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man8/*
%{_initrddir}/acpid
%dir %{_sysconfdir}/acpi/actions
