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
Requires:	vpnc = %{version}-%{release}
Requires:	usermode

%description consoleuser
Allows the console user to run the IPSec VPN client directly without
switching to the root account.

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
chmod 0644 $RPM_BUILD_ROOT%{_mandir}/man8/vpnc.8
install -m 0600 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/vpnc/default.conf
mkdir -p $RPM_BUILD_ROOT%{_var}/run/vpnc
install -Dp -m 0644 %{SOURCE2} \
    $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/vpnc
install -Dp -m 0644 %{SOURCE3} \
    $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/vpnc-disconnect
install -Dp -m 0644 %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/vpnc
install -Dp -m 0644 %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/vpnc-disconnect
install -m 0755 %{SOURCE5} \
    $RPM_BUILD_ROOT%{_sbindir}/vpnc-helper
mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/vpnc
ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/vpnc-disconnect
install -Dp -m 0644 %{SOURCE6} \
    $RPM_BUILD_ROOT%{_sysconfdir}/event.d/vpnc-cleanup
rm -f $RPM_BUILD_ROOT%{_datadir}/doc/vpnc/COPYING

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d
install -m 0644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d/vpnc-tmpfiles.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README COPYING pcf2vpnc pcf2vpnc.1
%dir %{_sysconfdir}/vpnc
%config(noreplace) %{_sysconfdir}/vpnc/vpnc-script
%config(noreplace) %{_sysconfdir}/vpnc/default.conf
%config(noreplace) %{_sysconfdir}/event.d/vpnc-cleanup
%{_sysconfdir}/tmpfiles.d/vpnc-tmpfiles.conf
%{_sbindir}/vpnc
%{_bindir}/cisco-decrypt
%{_sbindir}/vpnc-disconnect
%{_mandir}/man8/vpnc.*
%{_mandir}/man1/cisco-decrypt.*

%files consoleuser
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/security/console.apps/vpnc*
%config(noreplace) %{_sysconfdir}/pam.d/vpnc*
%{_bindir}/vpnc*
%{_sbindir}/vpnc-helper

