Name:           vpnc
# call ./rpm/generate_version_tag.sh to generate the name of the version tag
# when pulling upstream updates
Version:        0.5.3
Release:        0
Summary:        IPSec VPN client compatible with Cisco equipment
License:        GPL-2.0-or-later AND BSD-2-Clause
URL:            https://github.com/streambinder/vpnc
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  pkgconfig(libgcrypt) > 1.1.90

%description
A VPN client compatible with Cisco's EasyVPN equipment.

Supports IPSec (ESP) with Mode Configuration and Xauth.  Supports only
shared-secret IPSec authentication, 3DES, MD5, and IP tunneling.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Man pages for %{name}.

%package pcf2vpnc
Summary:   Convert VPN-config files from pcf to vpnc-format
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch

%description pcf2vpnc
%{summary}.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

# Build hybrid support
sed 's|^#OPENSSL|OPENSSL|g' -i Makefile

%build
export CFLAGS="%{optflags} -fPIC"
# FIXME replace with %{%build_ldflags} when available 
export LDFLAGS="$RPM_OPT_FLAGS -fPIC"

make \
    PREFIX=/usr

%install
make install \
	DESTDIR=%{buildroot} \
	PREFIX=/usr


mv %{buildroot}%{_sysconfdir}/%{name}/default.conf \
   %{buildroot}%{_docdir}/%{name}/example.conf

# Packaged later using %license
rm -rf %{buildroot}%{_defaultlicensedir}/%{name}/LICENSE


# Unused, vpnc scripts are not packaged
rm -rf %{buildroot}%{_usr}/lib/systemd/system/vpnc@.service


%files
%defattr(-,root,root)
%license LICENSE
%license LICENSE.BSD2
%dir %{_sysconfdir}/%{name}
%{_sbindir}/%{name}
%{_bindir}/cisco-decrypt
%{_sbindir}/%{name}-disconnect

%files pcf2vpnc
%{_bindir}/pcf2vpnc
%{_mandir}/man1/pcf2vpnc.*

%files doc
%defattr(0644,root,root)
%{_mandir}/man8/%{name}.*
%{_mandir}/man1/cisco-decrypt.*
%doc %{_docdir}/%{name}/About.md
%doc %{_docdir}/%{name}/FAQ.md
%doc %{_docdir}/%{name}/Installation.md
%doc %{_docdir}/%{name}/example.conf

