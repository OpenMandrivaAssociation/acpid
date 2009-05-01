Summary:		ACPI kernel daemon and control utility
Name:			acpid
Version:		1.0.10
Release:		%manbo_mkrel 1
License:		GPLv2+
Group:			System/Servers
Epoch:			2
URL:			http://acpid.sourceforge.net
Source0:		http://unc.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source1:		acpid.rc
Patch1:			acpid-1.0.6-ignore-rpmnew.patch
# patches from RH
Patch4:			acpid-1.0.8-makefile.patch
ExclusiveArch:		%{ix86} ia64 x86_64 amd64
Requires(post):		rpm-helper
Requires(post):		chkconfig >= 1.3.37-3mdv
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

%patch1 -p1 -b .rpmnew
%patch4 -p1 -b .optflags

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

%triggerpostun -- acpid < 2:1.0.6-7mnb
/sbin/chkconfig --level 7 acpid reset

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
