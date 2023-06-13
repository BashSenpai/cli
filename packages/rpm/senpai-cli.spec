#
# spec file for package senpai-cli
#
# Copyright 2023 Bogdan Tatarov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

Name:           senpai-cli
Version:        0.82b
Release:        1
Summary:        BashSenpai command-line interface

License:        Apache-2.0
Source0:        https://github.com/BashSenpai/cli/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-requests
BuildRequires:  python3-toml

Requires:       python3-requests
Requires:       python3-toml

%description
BashSenpai is a terminal assistant powered by ChatGPT that transforms instructions into ready-to-use commands.


%prep
%autosetup -n cli-%{version}


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
* Mon Jun 12 2023 Bogdan Tatarov <bogdan@tatarov.me> 0.82b-1
- Feature: new prompt `explain <command>` (bogdan@tatarov.me)
- Feature: animate the loading message (bogdan@tatarov.me)
- Improvement: better `--help` output (bogdan@tatarov.me)
* Wed Jun 07 2023 Bogdan Tatarov <bogdan@tatarov.me> 0.81b-1
- Update: stream prompt responses (bogdan@tatarov.me)
- Update: simplify API calls (bogdan@tatarov.me)
* Wed May 31 2023 Bogdan Tatarov <bogdan@tatarov.me> 0.80b-1
- Feature: prettier output style (bogdan@tatarov.me)
- Feature: check if there is a new version available (bogdan@tatarov.me)
- Various small bug fixes and improvements (bogdan@tatarov.me)
* Sat May 27 2023 Bogdan Tatarov <bogdan@tatarov.me> 0.79b-2
- Fix: --version shows wrong version number (bogdan@tatarov.me)
* Sat May 27 2023 Bogdan Tatarov <bogdan@tatarov.me> 0.79b-1
- Feature: send optional metadata about the user's environment (bogdan@tatarov.me)
* Sat May 27 2023 Bogdan Tatarov <bogdan@tatarov.me> 0.78b-1
- Fix: handle internal server errors on API calls (bogdan@tatarov.me)
- Fix: handle multi-line inputs in the command execution menu (bogdan@tatarov.me)
- Fix: proper color escaping for readline (bogdan@tatarov.me)
* Sat May 27 2023 Bogdan Tatarov <bogdan@tatarov.me> 0.77b-1
- Feature: better error handling on API error (bogdan@tatarov.me)
* Sat May 27 2023 Bogdan Tatarov <bogdan@tatarov.me> 0.75b-1
- Feature: menu to execute any provided command directly in the terminal
* Mon May 22 2023 Bogdan Tatarov <bogdan@tatarov.me> 0.71b-1
- various changes in metadata (bogdan@tatarov.me)
- small bug fixes (bogdan@tatarov.me)
* Mon May 22 2023 Bogdan Tatarov <bogdan@tatarov.me> 0.70b-1
- First public release (bogdan@tatarov.me)
