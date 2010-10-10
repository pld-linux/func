Summary:	Fedora Unified Network Controller
Summary(pl.UTF-8):	FUNC - jednolite sterowanie sieciowe Fedory
Name:		func
Version:	0.25
Release:	0.1
License:	GPL v2+
Group:		Applications/System
Source0:	http://people.fedoraproject.org/~alikins/files/func/%{name}-%{version}.tar.gz
# Source0-md5:	892252004f122c61bb58bb4607553ffe
Source1:	%{name}-funcd.init
Patch0:		%{name}-setup.patch
URL:		https://fedorahosted.org/func/
BuildRequires:	python
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	certmaster >= 0.25
Requires:	python-pyOpenSSL
Requires:	python-simplejson
%pyrequires_eq	python-libs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FUNC (Fedora Unified Network Controller) is a remote API for
management, configation, and monitoring of systems.

%description -l pl.UTF-8
FUNC (Fedora Unified Network Controller) to zdalne API do zarządzania,
konfiguracji i monitorowania systemów.

%prep
%setup -q
%patch0 -p1

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/log/func}
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/funcd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add funcd
%service funcd restart

%preun
if [ "$1" = "0" ]; then
	%service funcd stop
	/sbin/chkconfig --del funcd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/funcd
%attr(755,root,root) %{_bindir}/func
%attr(755,root,root) %{_bindir}/func-inventory
%attr(755,root,root) %{_bindir}/func-build-map
%attr(755,root,root) %{_bindir}/func-transmit
%attr(755,root,root) %{_bindir}/func-create-module
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/func_rotate
%attr(754,root,root) /etc/rc.d/init.d/funcd
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/async_methods.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/minion.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/overlord.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/modules/Bridge.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/modules/Test.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/modules/Vlan.conf
%{_mandir}/man1/*.1*
%{py_sitescriptdir}/func
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/func-*.egg-info
%endif
%dir /var/log/func
