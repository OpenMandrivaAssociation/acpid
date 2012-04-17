Summary:		ACPI kernel daemon and control utility
Name:			acpid
Version:		2.0.16
Release:		%manbo_mkrel 1
License:		GPLv2+
Group:			System/Servers
Epoch:			2
URL:			http://www.tedfelix.com/linux/acpid-netlink.html
Source0:		http://www.tedfelix.com/linux/%{name}-%{version}.tar.xz
Source1:		acpid.rc
Source2:		acpid.service
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

%build
%configure2_5x
%serverbuild
# Don't use standard optflag, correct LDFLAGS
#sed -i -e "/^OPT = /d"  -e "1iLDFLAGS = -pie %{ldflags}" Makefile
#OPT="%{optflags} -fPIC" %make

%install
%makeinstall_std
mkdir -p %{buildroot}/%{_initrddir}
install -m755 %{SOURCE1} %{buildroot}%{_initrddir}/acpid
mkdir -p %{buildroot}%{_systemunitdir}
install -m755 %{SOURCE2} %{buildroot}%{_systemunitdir}

install -d %{buildroot}%{_sysconfdir}/acpi/actions

%clean
rm -rf %{buildroot}

%triggerpostun -- acpid < 2:1.0.6-7mnb
/sbin/chkconfig --level 7 acpid reset

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -eq 1 ]; then
    /bin/systemctl enable %{name}.service > /dev/null 2>&1 || :
fi
    /bin/systemctl try-restart %{name}.service > /dev/null 2>&1 || :

%preun
if [ "$1" = "0" ]; then
    /bin/systemctl disable %{name}.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}.service > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root)
%doc README TODO Changelog
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man8/*
%{_initrddir}/acpid
%{_systemunitdir}/acpid.service
%dir %{_sysconfdir}/acpi/actions
