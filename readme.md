# TA-LIB docs
https://github.com/mrjbq7/ta-lib/blob/master/docs/index.md

# Install Environment
````
C:\ProgramData\Anaconda3
conda env list


conda install -c conda-forge ta-lib

pip install TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
(https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)
````

## TA-LIB installation options for Linux (Google CoLab)
https://stackoverflow.com/questions/49648391/how-to-install-ta-lib-in-google-colab

Build from sources:
````
!wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz 
!tar xvzf ta-lib-0.4.0-src.tar.gz
import os
os.chdir('ta-lib') # Can't use !cd in co-lab
!./configure --prefix=/usr
!make
!make install
os.chdir('../')
!pip install TA-Lib
````
A bit faster:
````
!wget https://launchpad.net/~mario-mariomedina/+archive/ubuntu/talib/+files/libta-lib0_0.4.0-oneiric1_amd64.deb -qO libta.deb
!wget https://launchpad.net/~mario-mariomedina/+archive/ubuntu/talib/+files/ta-lib0-dev_0.4.0-oneiric1_amd64.deb -qO ta.deb
!dpkg -i libta.deb ta.deb
!pip install ta-lib
````
#### run for VS Code
jupyter notebook --no-browser --NotebookApp.allow_origin_pat=https://.*vscode-cdn\.net
jupyter notebook --no-browser --NotebookApp.allow_origin='*'
