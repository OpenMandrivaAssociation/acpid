Summary:	ACPI kernel daemon and control utility
Name:		acpid
Epoch:		2
Version:	2.0.33
Release:	1
License:	GPLv2+
Group:		System/Servers
Url:		http://sourceforge.net/projects/acpid2/
Source0:	http://downloads.sourceforge.net/acpid2/%{name}-%{version}.tar.xz
Source1:	acpid.socket
Source2:	acpid.service
Source3:	acpid.config
# https://sourceforge.net/p/acpid2/tickets/14/
Patch0:		acpid-2.0.32-kacpimon-dynamic-connections.patch
ExclusiveArch:	%{ix86} ia64 %{x86_64} amd64 %{armx} riscv64
BuildRequires:	systemd-macros
%systemd_requires

%description
The ACPI specification defines power and system management functions
for each computer, in a generic manner. The ACPI daemon coordinates
the management of power and system functions when ACPI kernel
support is enabled (kernel 2.3.x or later).

%prep
%autosetup -p1

%build
%serverbuild_hardened
%configure
%make_build

%install
%make_install
mkdir -p %{buildroot}%{_unitdir}
install -m644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_unitdir}

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/acpid

install -d %{buildroot}%{_sysconfdir}/acpi/actions
install -d -m 755 %{buildroot}%{_sysconfdir}/acpi/events

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-acpid.preset << EOF
enable acpid.socket
EOF

%post
%systemd_post %{name}.socket

%preun
%systemd_preun %{name}.socket

%postun
%systemd_postun_with_restart %{name}.socket

%files
%doc %{_docdir}/%{name}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/acpid
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man8/*
%{_presetdir}/86-acpid.preset
%{_unitdir}/acpid.service
%{_unitdir}/acpid.socket
%dir %{_sysconfdir}/acpi/actions
%dir %{_sysconfdir}/acpi/events
