# RNAport
#This pipeline provide the port for running RNA ref and RNA denovo pipeline
chenjunhui/RNAport is licensed under the

GNU General Public License v3.0
Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.

RNAport  provide the port for running RNA reference or RNA denovo pipeline basing on project
====

Installation
===
This RNAport were tested by python 3.6 under Linux wh-login-13-1.wh.hpc system. The software depends on click and xlrd packages.</br>
You can install it by pip or raw code just as the following command.

Raw code installation
------------------------------------------
```
git clone https://github.com/chenjunhui/RNAport
cd RNAport  &&  python3.6  setup.py  install  --user  --prefix=$PREFIX_PATH ($PREFIX_PATH should be included PYTHONPATH, if not, you should export PYHTONPATH="$PREFIX_PATH/lib/python3.6/site-packages")
```
Install  by pip
-------------------------------------------
```
export PYHTONPATH="$PREFIX_PATH/lib/python3.6/site-packages"
pip  install  --install-option="--prefix=$PREFIX_PATH"  RNAport==1.0
```
usage
======================================================================================================
The port contain 3 subcommands: getdata, rnadenvo and rnarefcfg. if you install it successfully. Then you can run it
as following
```
export PATH="$PREFIX_PATH/bin:$PATH"
RNAport  --help
```
Usage: RNAport [OPTIONS] COMMAND [ARGS]...

  Welcome to use the RNAKit for preparing config of RNA pipeline. :param
  verbosity: :param version: :return: Contact: chenjunhui@genomics.cn

Options:
  -v, --verbosity [info|debug]  Verbosity level, default=info.
  --version                     Print version number
  -h, --help                    Show this message and exit.

Commands:
  getdata    get raw data list for RNA reference pipeline
  rnadenvo
  rnarefcfg  ...
