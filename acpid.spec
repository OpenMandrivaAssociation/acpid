Summary:		ACPI kernel daemon and control utility
Name:			acpid
Version:		2.0.17
Release:		1
License:		GPLv2+
Group:			System/Servers
Epoch:			2
URL:			http://www.tedfelix.com/linux/acpid-netlink.html
Source0:		http://www.tedfelix.com/linux/%{name}-%{version}.tar.xz
Source2:		acpid.service
Source3:		acpid.config
ExclusiveArch:		%{ix86} ia64 x86_64 amd64
BuildRequires:		systemd-units
Requires(post):		rpm-helper
Requires(post):		chkconfig >= 1.3.37-3mdv
Requires(preun):	rpm-helper
Conflicts:		suspend-scripts < 1.27-2mdv2007.1

%description
The ACPI specification defines power and system management functions
for each computer, in a generic manner. The ACPI daemon coordinates
the management of power and system functions when ACPI kernel
support is enabled (kernel 2.3.x or later).

%prep
%setup -q

%build
%configure2_5x
%serverbuild_hardened
# Don't use standard optflag, correct LDFLAGS
#sed -i -e "/^OPT = /d"  -e "1iLDFLAGS = -pie %{ldflags}" Makefile
#OPT="%{optflags} -fPIC" %make

%make

%install
%makeinstall_std
mkdir -p %{buildroot}%{_unitdir}
install -m755 %{SOURCE2} %{buildroot}%{_unitdir}

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/acpid

install -d %{buildroot}%{_sysconfdir}/acpi/actions
install -d -m 755 %{buildroot}%{_sysconfdir}/acpi/events

%post
if [ $1 -eq 1 ]; then
    /bin/systemctl enable %{name}.service > /dev/null 2>&1 || :
fi

%_post_service %{name} %{name}.service

%postun
%_postun_unit %{name}.service

%preun
%_preun_service %{name} %{name}.service

%files
%doc README TODO Changelog
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/acpid
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man8/*
%{_unitdir}/acpid.service
%dir %{_sysconfdir}/acpi/actions
%dir %{_sysconfdir}/acpi/events
