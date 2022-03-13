#!/bin/bash

echo-blue () {
    echo -e "\e[34m\e[1m$1\e[0m"
}

echo-red () {
    echo -e "\e[31m\e[1m$1\e[0m"
}

echo-blue "#########################"
echo-blue "## Adding kubuntu repo ##"
echo-blue "#########################"

sudo add-apt-repository ppa:kubuntu-ppa/backports
sudo apt update

echo-blue "#######################"
echo-blue "## Installing plasma ##"
echo-blue "#######################"

sudo apt install kde-plasma-desktop
