Name:       sudo
Summary:    Execute some commands as root
Version:    1.9.16p2
Release:    1
License:    ISC
URL:        https://github.com/sailfishos/sudo
Source0:    %{name}-%{version}.tar.gz
Source1:    sudo.pamd
Source2:    01_keep_zypp_logfile
BuildRequires:  pam-devel

%description
Sudo is a command that allows users to execute some commands as root.
The /etc/sudoers file (edited with 'visudo') specifies which users have
access to sudo and which commands they can run. Sudo logs all its
activities to syslogd, so the system administrator can keep an eye on
things. Sudo asks for the password for initializing a check period of a
given time N (where N is defined at installation and is set to 5
minutes by default).


%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build

%configure --disable-static \
    --disable-log-server \
    --libexecdir=%{_libexecdir}/sudo \
    --docdir=%{_docdir}/%{name} \
    --with-noexec=%{_libexecdir}/sudo/sudo_noexec.so \
    --with-pam \
    --with-logfac=auth \
    --with-insults \
    --with-all-insults \
    --with-ignore-dot \
    --with-tty-tickets \
    --enable-shell-sets-home \
    --enable-tmpfiles.d=%{_libdir}/tmpfiles.d \
    --enable-warnings \
    --with-sudoers-mode=0440 \
    --with-env-editor \
    --with-secure-path=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/sbin:/usr/sbin:/root/bin

%make_build

%install
make install DESTDIR=%{buildroot} install_uid=`id -u` install_gid=`id -g` sudoers_uid=`id -u` sudoers_gid=`id -g`

install -d -m 755 %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/sudo
install -d -m 755 %{buildroot}%{_sysconfdir}/sudoers.d
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sudoers.d/01_keep_zypp_logfile
rm -rf %{buildroot}/usr/share/locale
rm -rf %{buildroot}%{_mandir}
rm -f %{buildroot}/usr/include/sudo_plugin.h
rm -f %{buildroot}%{_sysconfdir}/sudoers.dist

%files
%license LICENSE.md
%doc %{_docdir}/%{name}
%config(noreplace) %attr(0440,root,root) %{_sysconfdir}/sudoers
%{_sysconfdir}/sudoers.d/01_keep_zypp_logfile
%dir %{_sysconfdir}/sudoers.d
%config %{_sysconfdir}/pam.d/sudo
%attr(4755,root,root) %{_bindir}/sudo
%attr(4755,root,root) %{_bindir}/sudoedit
%{_bindir}/sudoreplay
%{_sbindir}/visudo
%{_bindir}/cvtsudoers
%{_libexecdir}/sudo
%{_libdir}/tmpfiles.d/sudo.conf
%attr(0640,root,root) %config(noreplace) /etc/sudo.conf
