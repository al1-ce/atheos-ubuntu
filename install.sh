#!/bin/bash

echo-blue () {
    echo -e "\e[34m\e[1m$1\e[0m"
}

echo-red () {
    echo -e "\e[31m\e[1m$1\e[0m"
}

if [ "$(id -u)" = 0 ]; then
    echo-red "#####################################################################"
    echo-red "## This script MUST NOT be run as root user since it makes changes ##"
    echo-red "## to the \$HOME directory of the \$USER executing this script.    ##"
    echo-red "#####################################################################"
    exit 1
fi

echo-blue "#############################################################"
echo-blue "## Script now will begin installation of AtheOS for Ubuntu ##"
echo-blue "#############################################################"

while true; do
    read -p "Do you want to continue? [y/n]" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
    esac
done

echo-blue "############################################################"
echo-blue "## Syncing the repos and installing packages from pkglist ##"
echo-blue "############################################################"

sudo apt update
sudo apt-get install $(grep -vE "^\s*#" pkglist.txt  | tr "\n" " ")

echo-blue "####################################"
echo-blue "## Installing snaps from snaplist ##"
echo-blue "####################################"

sudo snap install $(grep -vE "^\s*#" snaplist.txt  | tr "\n" " ")

echo-blue "#########################"
echo-blue "## Installing homebrew ##"
echo-blue "#########################"

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

echo-blue "#########################################"
echo-blue "## Installing packages outside of repo ##"
echo-blue "#########################################"

wget https://github.com/clangen/musikcube/releases/download/0.97.0/musikcube_standalone_0.97.0_x86_64.deb
sudo dpkg -i musikcube_standalone_0.97.0_x86_64.deb
sudo apt-get install -f
rm musikcube_standalone_0.97.0_x86_64.deb

echo-blue "######################"
echo-blue "## Installing fonts ##"
echo-blue "######################"

wget https://github.com/microsoft/cascadia-code/releases/download/v2111.01/CascadiaCode-2111.01.zip
unzip CascadiaCode-2111.01.zip
sudo mkdir -p /usr/share/fonts/truetype/cascadia
sudo cp ttf/*ttf /usr/share/fonts/truetype/cascadia/
rm -rf otf ttf woff2

echo-blue "##########################"
echo-blue "## Installing powerline ##"
echo-blue "##########################"

go install github.com/justjanne/powerline-go@latest

echo-blue "####################"
echo-blue "## Installing SDK ##"
echo-blue "####################"

curl -fsS https://dlang.org/install.sh
curl -fsS https://dot.net/v1/dotnet-install.sh

echo-blue "#################################"
echo-blue "## Configuring desktop display ##"
echo-blue "#################################"

while true; do
    read -p "Do you want to install sddm? [y/n]" yn
    case $yn in
        [Yy]* ) sudo apt install sddm; break;;
        [Nn]* ) break;;
    esac
done

echo-blue "#########################"
echo-blue "## Configuring konsole ##"
echo-blue "#########################"

mkdir -p ~/.kde/share/config/konsole/
cp -r konsole/ ~/.kde/share/config/konsole/

while true; do
    read -p "Do you want to change default terminal? [y/n]" yn
    case $yn in
        [Yy]* ) sudo update-alternatives --config x-terminal-emulator; break;;
        [Nn]* ) break;;
    esac
done

echo-blue "#####################"
echo-blue "## Configuring git ##"
echo-blue "#####################"

git config --global init.defaultBranch master

echo-blue "##############################"
echo-blue "## Removing unused packages ##"
echo-blue "##############################"

sudo apt autoremove

echo-blue "##################"
echo-blue "## Fixing paths ##"
echo-blue "##################"

mkdir -p ~/.local/bin
ln -s /usr/bin/batcat ~/.local/bin/bat

echo-blue "######################"
echo-blue "## Configuring grub ##"
echo-blue "######################"

reconf-grub () {
    sudo mkdir -p /boot/grub/themes/
    sudo cp -r shodan-grub/ /boot/grub/themes/Shodan/
    sudo echo 'GRUB_THEME="/boot/grub/themes/Shodan/theme.txt"' >> /etc/default/grub
    sudo echo 'GRUB_GFXMODE="1920x1080"' >> /etc/default/grub
    sudo update-grub
}

while true; do
    read -p "Do you want to install shodan grub theme? [y/n]" yn
    case $yn in
        [Yy]* ) reconf-grub; break;;
        [Nn]* ) break;;
    esac
done

echo-blue "########################"
echo-blue "## Configuring bashrc ##"
echo-blue "########################"

git clone git@github.com:al1-ce/dotfiles-ubuntu.git ~/.dotfiles

echo "source ~/.dotfiles/.bashrc" > ~/.bashrc
echo "source ~/.dotfiles/.vimrc" > ~/.vimrc
echo "source ~/.dotfiles/.cocvimrc" > ~/.cocvimrc

echo-blue "###########################"
echo-blue "## Installation complete ##"
echo-blue "###########################"

while true; do
    read -p "Do you want to reboot? [y/n]" yn
    case $yn in
        [Yy]* ) shutdown -r 0; break;;
        [Nn]* ) srcrc; exit;;
    esac
done
