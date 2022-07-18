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

echo-blue "###################################################################"
echo-blue "## Script now will begin LIGHT installation of AtheOS for Ubuntu ##"
echo-blue "###################################################################"

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
sudo apt-get install $(grep -vE "^\s*#" pkglist-lite.txt  | tr "\n" " ")

echo-blue "####################################"
echo-blue "## Installing snaps from snaplist ##"
echo-blue "####################################"

chmod +x snap-install-lite.sh
./snap-install-lite.sh

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

echo-blue "##########################"
echo-blue "## Installing powerline ##"
echo-blue "##########################"

go install github.com/justjanne/powerline-go@latest

echo-blue "####################"
echo-blue "## Installing SDK ##"
echo-blue "####################"

sudo snap install --classic dmd
sudo snap install --classic dub
sudo snap install --classic dotnet-sdk

echo-blue "#####################"
echo-blue "## Configuring git ##"
echo-blue "#####################"

git config --global init.defaultBranch master

echo-blue "#####################"
echo-blue "## Configuring vim ##"
echo-blue "#####################"

curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

echo-blue "##############################"
echo-blue "## Removing unused packages ##"
echo-blue "##############################"

sudo apt autoremove

echo-blue "##################"
echo-blue "## Fixing paths ##"
echo-blue "##################"

mkdir -p ~/.local/bin
ln -s /usr/bin/batcat ~/.local/bin/bat

git clone https://github.com/al1-ce/dotfiles-ubuntu.git ~/.dotfiles

echo "source ~/.dotfiles/.bashrc" > ~/.bashrc
echo "source ~/.dotfiles/.vimrc" > ~/.vimrc
echo "source ~/.dotfiles/.cocvimrc" > ~/.cocvimrc
