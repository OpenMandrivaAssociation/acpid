Summary:		ACPI kernel daemon and control utility
Name:			acpid
Version: 		1.0.4
Release:		%mkrel 13
License:		GPL
Group:			System/Servers
Epoch:			2

Source0:		http://unc.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.bz2
Source1:		acpid.rc
Patch0:			acpid-kernel-acpi-h.patch
Patch1:			acpid-1.0.4-ignore-rpmnew.patch
Patch2:                 acpid-1.0.4-warning.patch
Patch3:			acpid-1.0.4-noclose.patch
URL:			http://acpid.sourceforge.net/
BuildRoot:		%{_tmppath}/%{name}-buildroot
ExclusiveArch:		%{ix86} ia64 x86_64 amd64
Requires(post):		rpm-helper
Requires(preun):		rpm-helper
Conflicts: suspend-scripts < 1.27-2mdv2007.1

%description
The ACPI specification defines power and system management functions
for each computer, in a generic manner.  The ACPI daemon coordinates
the management of power and system functions when ACPI kernel
support is enabled (kernel 2.3.x or later).

%prep 
%setup -q
%patch -p1
%patch1 -p1 -b .rpmnew
%patch2 -p1
%patch3 -p1 -b .noclose

%build
%serverbuild
%make

cat > %{name}.logrotate <<EOF

/var/log/acpid {
    missingok
    compress
    postrotate
        service acpid reload
    endscript
}
EOF

%install
mkdir -p $RPM_BUILD_ROOT/%_sbindir
install -m755 acpid $RPM_BUILD_ROOT/%_sbindir
mkdir -p $RPM_BUILD_ROOT/%_mandir/man8
install -m644 acpid.8 $RPM_BUILD_ROOT/%_mandir/man8

mkdir -p $RPM_BUILD_ROOT/%{_initrddir}
install -m755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/acpid

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/
install -m644 %{name}.logrotate $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/%{name}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service acpid

%preun
%_preun_service acpid

%files
%defattr(-,root,root)
%doc README
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_sbindir}/*
%{_mandir}/man8/*
%config(noreplace) %{_initrddir}/acpid
%dir %{_sysconfdir}/acpi/actions


