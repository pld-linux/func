%define		subver	.3
Summary:	Fedora Unified Network Controller
Name:		func
Version:	0.13
Release:	1
License:	GPLv2+
Group:		Applications/System
Source0:	https://hosted.fedoraproject.org/projects/func/attachment/wiki/FuncReleases/%{name}-%{version}.tar%{subver}.gz?format=raw
# Source0-md5:	adf06e92209e2576bd44fa64641b8733
Source1:	%{name}-funcd.init
Source2:	%{name}-certmaster.init
Patch0:		%{name}-setup.patch
URL:		https://hosted.fedoraproject.org/projects/func/
BuildRequires:	python >= 1:2.5
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-pyOpenSSL
%pyrequires_eq	python-libs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
func is a remote api for mangement, configation, and monitoring of
systems.

%prep
%setup -q
%patch0 -p1

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d/funcd

python setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/funcd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/certmaster

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add certmaster
/sbin/chkconfig --add funcd

%preun
if [ "$1" = "0" ]; then
	%service certmaster stop
	%service funcd stop
	/sbin/chkconfig --del certmaster
	/sbin/chkconfig --del funcd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/funcd
%attr(755,root,root) %{_bindir}/func
%attr(755,root,root) %{_bindir}/certmaster
%attr(755,root,root) %{_bindir}/certmaster-ca
%attr(755,root,root) %{_bindir}/func-inventory
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/minion-acl.d/
# TODO: move %{_sysconfdir}/pki into FHS? It's used for key storage
%dir %{_sysconfdir}/pki
%dir %{_sysconfdir}/pki/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/func/minion.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/func/certmaster.conf
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/func_rotate
%attr(754,root,root) /etc/rc.d/init.d/certmaster
%attr(754,root,root) /etc/rc.d/init.d/funcd
%{py_sitescriptdir}/func-%{version}-py*.egg-info
%{py_sitescriptdir}/func
%{_mandir}/man1/*.1*
