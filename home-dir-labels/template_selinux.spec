%define relabel_files() \
restorecon -R /home/*/TARGET; \

%define selinux_policyver 35.7-1

Name:       selinux-label-MODULE
Version:    1.0
Release:    1%{?dist}
Summary:    SELinux policy module (label only) for the ~/TARGET directory

Group:      System Environment/Base
License:    AGPLv3
URL:        https://github.com/noatsecure/hardhat-selinux
Source0:    MODULE.pp
Source1:    MODULE.if

Requires: policycoreutils, libselinux-utils, hardhat_interface_macros
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
BuildArch: noarch

%description
This package installs and sets up the SELinux policy security module (label only) for the ~/TARGET directory.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}/etc/selinux/targeted/contexts/users/

%post
semodule -n -i %{_datadir}/selinux/packages/MODULE.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files
fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r MODULE
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       %relabel_files
    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/MODULE.pp
%{_datadir}/selinux/devel/include/contrib/MODULE.if
