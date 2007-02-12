%define		mod_name	macro
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module to allow macros in apache config files
Summary(pl.UTF-8):   Moduł do apache pozwalający używać makr w konfiguracji
Name:		apache-mod_%{mod_name}
Version:	1.1.8
Release:	1
License:	Apache
Group:		Networking/Daemons
Source0:	http://www.cri.ensmp.fr/~coelho/mod_macro/mod_%{mod_name}-%{version}.tar.bz2
# Source0-md5:	0dc994b9eedaf7ec31ec038ed33a9f10
URL:		http://www.cri.ensmp.fr/~coelho/mod_macro/
BuildRequires:	apache-devel >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
Apache module to allow macros in apache config files.

%description -l pl.UTF-8
Moduł do apache pozwalający używać makr w plikach konfiguracyjnych.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
