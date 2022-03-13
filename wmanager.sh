#!/bin/bash

echo-blue () {
    echo -e "\e[34m\e[1m$1\e[0m"
}

echo-red () {
    echo -e "\e[31m\e[1m$1\e[0m"
}

echo-blue "#############################"
echo-blue "## Setting up dependencies ##"
echo-blue "#############################"

sudo apt install xserver-xorg libwlroots-dev libpangocairo-1.0-0 \
python3-xcffib python3-cairocffi python3-dbus python3-dbus-next python3-psutil \
python3-ewmh python3-fuzzywuzzy

echo-blue "#########################"
echo-blue "## Installing managers ##"
echo-blue "#########################"

sudo apt install polybar rofi compton nitrogen

echo-blue "#####################"
echo-blue "## Setting up rofi ##"
echo-blue "#####################"

git clone https://github.com/emanuelep57/Qminimize.git ~/.local/bin/qmm
cp ~/.local/bin/qmm/Qminimize ~/.local/bin/Qminimize
rm -rf ~/.local/bin/qmm
chmod +x ~/.local/bin/Qminimize

cp rofi ~/.config/

echo-blue "######################"
echo-blue "## Installing qtile ##"
echo-blue "######################"

pip3 install qtile

echo-blue "######################"
echo-blue "## Setting up qtile ##"
echo-blue "######################"

sudo cp qtile.desktop /usr/share/xsessions/qtile.desktop

chmod +x qtile/autostart.sh
cp qtile ~/.config/
