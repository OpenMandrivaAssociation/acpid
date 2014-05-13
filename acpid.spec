Summary:		ACPI kernel daemon and control utility
Name:			acpid
Epoch:			2
Version:		2.0.22
Release:		2
License:		GPLv2+
Group:			System/Servers
Url:			http://sourceforge.net/projects/acpid2/
Source0:		http://downloads.sourceforge.net/acpid2/%{name}-%{version}.tar.xz
Source1:		acpid.socket
Source2:		acpid.service
Source3:		acpid.config
ExclusiveArch:		%{ix86} ia64 x86_64 amd64 %arm
BuildRequires:		systemd-units
Requires(post,preun,postun):	rpm-helper

%description
The ACPI specification defines power and system management functions
for each computer, in a generic manner. The ACPI daemon coordinates
the management of power and system functions when ACPI kernel
support is enabled (kernel 2.3.x or later).

%prep
%setup -q

%build
%serverbuild_hardened
%configure2_5x

%make

%install
%makeinstall_std
mkdir -p %{buildroot}%{_unitdir}
install -m644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_unitdir}

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/acpid

install -d %{buildroot}%{_sysconfdir}/acpi/actions
install -d -m 755 %{buildroot}%{_sysconfdir}/acpi/events

%post
if [ $1 -eq 1 ]; then
    /bin/systemctl enable %{name}.service > /dev/null 2>&1 || :
fi

%systemd_post %{name}.socket %{name}.service

%preun
%systemd_preun %{name}.socket %{name}.service

%postun
%systemd_postun_with_restart %{name}.socket %{name}.service

%files
%doc README TODO Changelog
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/acpid
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man8/*
%{_unitdir}/acpid.service
%dir %{_sysconfdir}/acpi/actions
%dir %{_sysconfdir}/acpi/events

