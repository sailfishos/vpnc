Name:           vpnc
Version:        0.5.3
Release:        2

Summary:        IPSec VPN client compatible with Cisco equipment

Group:          Applications/Internet
License:        GPLv2+
URL:            http://www.unix-ag.uni-kl.de/~massar/vpnc/
Source0:        http://www.unix-ag.uni-kl.de/~massar/vpnc/%{name}-%{version}.tar.gz
Source1:        generic-vpnc.conf
Source2:	vpnc.consolehelper
Source3:	vpnc-disconnect.consolehelper
Source4:	vpnc.pam
Source5:	vpnc-helper
Source6:	vpnc-cleanup
Source7:	vpnc-tmpfiles.conf
Patch2:		vpnc-0.5.3-cloexec.patch
Patch3:		vpnc-0.5.1-dpd.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libgcrypt-devel > 1.1.90
Requires:       iproute

%description
A VPN client compatible with Cisco's EasyVPN equipment.

Supports IPSec (ESP) with Mode Configuration and Xauth.  Supports only
shared-secret IPSec authentication, 3DES, MD5, and IP tunneling.

%package consoleuser
Summary:	Allows console user to run the VPN client directly
Group:		Applications/Internet
Requires:	%{name} = %{version}-%{release}
Requires:	usermode

%description consoleuser
Allows the console user to run the IPSec VPN client directly without
switching to the root account.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
Man pages for %{name}.

%prep
%setup -q
%patch2 -p1 -b .cloexec
%patch3 -p1 -b .dpd

%build
CFLAGS="$RPM_OPT_FLAGS -fPIE" LDFLAGS="$RPM_OPT_FLAGS -pie" make PREFIX=/usr 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT" PREFIX=/usr
rm -f $RPM_BUILD_ROOT%{_bindir}/pcf2vpnc
chmod 0644 pcf2vpnc
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/pcf2vpnc.1
install -m 0600 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/default.conf
mkdir -p $RPM_BUILD_ROOT%{_var}/run/%{name}
install -Dp -m 0644 %{SOURCE2} \
    $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/%{name}
install -Dp -m 0644 %{SOURCE3} \
    $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/%{name}-disconnect
install -Dp -m 0644 %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/%{name}
install -Dp -m 0644 %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/%{name}-disconnect
install -m 0755 %{SOURCE5} \
    $RPM_BUILD_ROOT%{_sbindir}/%{name}-helper
mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/%{name}
ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/%{name}-disconnect
install -Dp -m 0644 %{SOURCE6} \
    $RPM_BUILD_ROOT%{_sysconfdir}/event.d/%{name}-cleanup

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d
install -m 0644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d/%{name}-tmpfiles.conf

rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m0644 -t $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} \
        ChangeLog README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%license COPYING
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}-script
%config(noreplace) %{_sysconfdir}/%{name}/default.conf
%config(noreplace) %{_sysconfdir}/event.d/%{name}-cleanup
%{_sysconfdir}/tmpfiles.d/%{name}-tmpfiles.conf
%{_sbindir}/%{name}
%{_bindir}/cisco-decrypt
%{_sbindir}/%{name}-disconnect

%files consoleuser
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}*
%config(noreplace) %{_sysconfdir}/pam.d/%{name}*
%{_bindir}/%{name}*
%{_sbindir}/%{name}-helper

%files doc
%defattr(0644,root,root)
%{_mandir}/man8/%{name}.*
%{_mandir}/man1/cisco-decrypt.*
%{_docdir}/%{name}-%{version}
