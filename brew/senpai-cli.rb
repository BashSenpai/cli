class SenpaiCli < Formula
  include Language::Python::Virtualenv

  desc "BashSenpai command-line interface"
  homepage "https://bashsenpai.com/"
  url "https://github.com/BashSenpai/cli/archive/refs/tags/v0.79b.tar.gz"
  sha256 "e156271bff8ff1a93a6a615bf14cf8b67e6d1850781f7c43cb0deb11ae2b0239"
  license "Apache-2.0"

  depends_on "python@3.11"

  resource "certifi" do
    url "https://files.pythonhosted.org/packages/93/71/752f7a4dd4c20d6b12341ed1732368546bc0ca9866139fe812f6009d9ac7/certifi-2023.5.7.tar.gz"
    sha256 "0f0d56dc5a6ad56fd4ba36484d6cc34451e1c6548c61daad8c320169f91eddc7"
  end

  resource "charset-nomalizer" do
    url "https://files.pythonhosted.org/packages/ff/d7/8d757f8bd45be079d76309248845a04f09619a7b17d6dfc8c9ff6433cac2/charset-normalizer-3.1.0.tar.gz"
    sha256 "34e0a2f9c370eb95597aae63bf85eb5e96826d81e3dcf88b8886012906f509b5"
  end

  resource "gnureadline" do
    if Hardware::CPU.arm?
      url "https://files.pythonhosted.org/packages/83/03/65d82e9290ae8a2a3b2285dc8aebd304437a6ba7ad03823438730525ab45/gnureadline-8.1.2-cp311-cp311-macosx_11_0_arm64.whl", :using => :nounzip
      sha256 "74f2538ac15ff4ef9534823abdef077bb34c7dd343e204a36d978f09e168462f"
    else
      url "https://files.pythonhosted.org/packages/a7/f2/77195ef94f56b61ad881685e3a87cc39a9972e01ccacd555acaa001a92a0/gnureadline-8.1.2-cp311-cp311-macosx_10_9_x86_64.whl", :using => :nounzip
      sha256 "c1bcb32e3b63442570d6425055aa6d5c3b6e8b09b9c7d1f8333e70203166a5a3"
    end
  end

  resource "idna" do
    url "https://files.pythonhosted.org/packages/8b/e1/43beb3d38dba6cb420cefa297822eac205a277ab43e5ba5d5c46faf96438/idna-3.4.tar.gz"
    sha256 "814f528e8dead7d329833b91c5faa87d60bf71824cd12a7530b5526063d02cb4"
  end

  resource "requests" do
    url "https://files.pythonhosted.org/packages/9d/be/10918a2eac4ae9f02f6cfe6414b7a155ccd8f7f9d4380d62fd5b955065c3/requests-2.31.0.tar.gz"
    sha256 "942c5a758f98d790eaed1a29cb6eefc7ffb0d1cf7af05c3d2791656dbd6ad1e1"
  end

  resource "toml" do
    url "https://files.pythonhosted.org/packages/be/ba/1f744cdc819428fc6b5084ec34d9b30660f6f9daaf70eead706e3203ec3c/toml-0.10.2.tar.gz"
    sha256 "b3bda1d108d5dd99f4a20d24d9c348e91c4db7ab1b749200bded2f839ccbe68f"
  end

  resource "urllib3" do
    url "https://files.pythonhosted.org/packages/fb/c0/1abba1a1233b81cf2e36f56e05194f5e8a0cec8c03c244cab56cc9dfb5bd/urllib3-2.0.2.tar.gz"
    sha256 "61717a1095d7e155cdb737ac7bb2f4324a858a1e2e6466f6d03ff630ca68d3cc"
  end

  def install
    python = "python3.11"
    venv = virtualenv_create(libexec, python)

    resources.each do |r|
      if r.name.eql? "gnureadline"
        r.stage do
          if Hardware::CPU.arm?
            venv.pip_install "gnureadline-8.1.2-cp311-cp311-macosx_11_0_arm64.whl"
          else
            venv.pip_install "gnureadline-8.1.2-cp311-cp311-macosx_10_9_x86_64.whl"
          end
        end
      else
        venv.pip_install r
      end
    end

    system libexec/"bin/python", "setup.py", "build"
    system libexec/"bin/python", *Language::Python.setup_install_args(prefix, python)
  end

  test do
    assert_equal "New persona confirmed.", shell_output("#{bin}/senpai become default").strip
  end
end
