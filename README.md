# ECAL-DISPLAY, a Simple Tool for Event Display of DarkSHINE XY–Crossing ECAL

## Description
This program was designed for the event display of DarkSHINE ECAL, with $x$–$y$ crossing structure, which is the same as that in [dss-ecal](https://github.com/phys-jychen/dss-ecal).

**Remember:** The parameters of this program and dss-ecal are exactly the same! Therefore, the input ROOT files had better be directly obtained from dss-ecal.

## Environment
- Python: 3.11.5
- Matplotlib: 3.7.2
- NumPy: 1.24.3
- UpROOT: 5.1.1

This program was designed with the above environment. Other environments have not been fully tested.

## Installation and Usage
Very simple. Execute
```shell
git clone git@github.com:phys-jychen/ecal-display.git
```
to clone the repository.

Before executing, you probably need to modify the files. The terms include: name and path of the input ROOT file, ID of the event to be displayed, output figure file name, etc.

If you need an event display with hit energy also displayed (more recommended): In the directory your have installed, run
```shell
python event_display.py
```
to obtain a figure of event display, which will be saved in `figs/`.

If you only need an event display of the positions of the hits: Similar to the method shown above, execute
```shell
python display.py
```
to obtain a figure of event display, which will also be saved in `figs/`.
