Summary:	Fedora Unified Network Controller
Summary(pl.UTF-8):	FUNC - jednolite sterowanie sieciowe Fedory
Name:		func
Version:	0.21
Release:	0.2
License:	GPL v2+
Group:		Applications/System
Source0:	http://people.fedoraproject.org/~mdehaan/files/func/%{name}-%{version}.tar.gz
# Source0-md5:	715638833720c85076fe04cd2e31fc32
Source1:	%{name}-funcd.init
Patch0:		%{name}-setup.patch
URL:		https://hosted.fedoraproject.org/func/
BuildRequires:	python
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	certmaster >= 0.19
Requires:	python-pyOpenSSL
%pyrequires_eq	python-libs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FUNC (Fedora Unified Network Controller) is a remote API for
management, configation, and monitoring of systems.

%description -l pl.UTF-8
FUNC (Fedora Unified Network Controller) to zdalne API do
zarządzania, konfiguracji i monitorowania systemów.

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
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/funcd

%py_postclean

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
%attr(755,root,root) %{_bindir}/func-create-module
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/func_rotate
%attr(754,root,root) /etc/rc.d/init.d/funcd
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/func/minion.conf
%dir %{py_sitescriptdir}/func
%dir %{py_sitescriptdir}/func/minion
%dir %{py_sitescriptdir}/func/minion/modules
%dir %{py_sitescriptdir}/func/minion/modules/netapp
%dir %{py_sitescriptdir}/func/minion/modules/netapp/vol
%dir %{py_sitescriptdir}/func/overlord
%dir %{py_sitescriptdir}/func/overlord/cmd_modules
%dir %{py_sitescriptdir}/func/overlord/modules
%{py_sitescriptdir}/func/*.py[co]
%{py_sitescriptdir}/func/minion/*.py[co]
%{py_sitescriptdir}/func/minion/modules/*.py[co]
%{py_sitescriptdir}/func/minion/modules/netapp/*.py[co]
%{py_sitescriptdir}/func/minion/modules/netapp/vol/*.py[co]
%{py_sitescriptdir}/func/overlord/*.py[co]
%{py_sitescriptdir}/func/overlord/cmd_modules/*.py[co]
%{py_sitescriptdir}/func/overlord/modules/*.py[co]

%{_mandir}/man1/*.1*

%dir /var/log/func
