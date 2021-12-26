%define relabel_files() \
restorecon -R /path/to/target; \

%define selinux_policyver 35.7-1

Name:       NAME_selinux
Version:	1.0
Release:	1%{?dist}
Summary:	SELinux policy module for NAME

Group:      System Environment/Base
License:	AGPLv3
URL:        https://github.com/noatsecure/hardhat-selinux
Source0:	NAME.pp
Source1:	NAME.if

Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
BuildArch: noarch

%description
This package installs and sets up the SELinux policy security module (label only) for the $HOME/NAME_DIR directory.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}/etc/selinux/targeted/contexts/users/

%post
semodule -n -i %{_datadir}/selinux/packages/NAME.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files
fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r NAME
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       %relabel_files
    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/NAME.pp
%{_datadir}/selinux/devel/include/contrib/NAME.if
