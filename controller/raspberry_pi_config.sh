sudo apt-get update --fix-missing
sudo apt-get upgrade
sudo apt-get install python-pyaudio python3-pyaudio
sudo apt-get install portaudio19-dev python-all-dev

sudo pip install pyaudio --upgrade
sudo pip install SpeechRecognition

sudo apt-get install alsa-tools alsa-utils

sudo apt-get install flac


# Configure USB audio device
# Run lsusb to ensure the "C-Media Electronics, Inc. Audio Adapter" is detected
# rm -rf ~/.asoundrc
# Comment out dtparam=audio=on in /boot/config.txt to disable the default audio out.
# Comment out options snd-usb-audio index=-2 in /lib/modprobe.d/aliases.conf to give higher precedence to the USB audio controller.
# Remove the pulseaudio config from alsa audio:
#     rm -rf /usr/share/alsa/alsa.conf.d/50-pulseaudio.conf
#     rm -rf /usr/share/alsa/alsa.conf.d/99-pulseaudio-default.conf.example
#     rm -rf /usr/share/alsa/alsa.conf.d/pulse.conf
