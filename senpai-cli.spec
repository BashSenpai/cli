Name:           senpai-cli
Version:        0.75b
Release:        1%{?dist}
Summary:        BashSenpai command-line interface

License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-requests
BuildRequires:  python3-toml

#Requires:       python3-requests
#Requires:       python3-toml

%description
BashSenpai is a terminal assistant powered by ChatGPT that transforms instructions into ready-to-use commands.


%prep
%autosetup


%build
%py3_build


%install
%py3_install


%files
%doc README.md
%license LICENSE
%{_bindir}/senpai
%{python3_sitelib}/senpai_cli-*.egg-info/
%{python3_sitelib}/senpai/


%changelog
* Fri May 27 2023 Bogdan Tatarov <bogdan@tatarov.me>
- Feature: menu to execute any provided command directly in the terminal
* Mon May 22 2023 Bogdan Tatarov <bogdan@tatarov.me> 0.71b-1
- various changes in metadata (bogdan@tatarov.me)
- small bug fixes (bogdan@tatarov.me)
  (bogdan@tatarov.me)

* Mon May 22 2023 Bogdan Tatarov <bogdan@tatarov.me> 0.70b-1
- First public release
  (bogdan@tatarov.me)
