<h1>NEURON as a Python module: Installation instructions </h1>

This is an instruction guide to install the NEURON simulator as a python module.
**These instructions are meant to be clearer for those naive to UNIX, in order to get set up on NEURON as quickly as possible.**

Other instructions are also available: 

  1. In the appendix of NEURON and Python, Hines et al. 2009, Front. In Neuroinformatics.
  https://www.frontiersin.org/articles/10.3389/neuro.11.001.2009/full

  1. At andrewdavison.info/notes/installation-neuron-python/.

<h2>Pre-UNIX Instructions</h2>

1. Download the tar.gz files from https://neuron.yale.edu/ftp/neuron/versions/alpha/	  
      1. Download iv-VERSION.tar.gz 
      1. And nrn-VERSION [] [].tar.gz

1.	Change the name of the nrn.tar.gz file to only nrn-VERSION.tar.gz 
	
    **This will make things a lot easier later on**

1.	In your home directory, create a folder called ‘neuron’

1.	Place both of the tar.gz files in this neuron folder and double click them

1.	Open the terminal

## For reference
* pwd = print working directory
* cd = change directory

<h2>UNIX Instructions: Part 1</h2>
For these instructions, I will be referring to the iv-19 version of the interviews program
and the nrn-7.6 version of the NEURON simulator. If you have different versions, then 
simply use your version numbers instead of 19 & 7.6. 


    $ pwd

    This returns /Users/local/
    ^^ copy this (highlight, cmd+c)

    $ N=’PASTE PWD/neuron/'

    $ cd $N

    $ cd iv-19

    $ ./configure --prefix=$N/iv-19
    
    
    $ make
    
    
    $ make install
    
    
    
    $ cd

    $ cd $N/nrn-7.5

    $ ./configure --prefix=’/Users/name/neuron/’ --with-iv=’/Users/name/neuron/iv-19’ --with-nrnpython
    
    

    $ make
    
    

    $ make install


<h2>UNIX Instructions: Part 2</h2>

**ENSURE THAT YOU ARE STILL IN THE NRN-7.6 DIRECTORY**

Now we need to find our CPU architecture

    $ cd

    $ uname -p

    : this should return something like iXXX [i followed by three digits]

    $ cd $N/nrn-7.6/

    $ export PATH=$N/nrn-7.6/iXXX/bin:$PATH

    $ cd src/nrnpython

    $ python setup.py install

<h2>Checking to see whether NEURON installed properly</h2>

    $ python

    >>> import neuron

    ^This should return the creator credits of NEURON. 

    >>> from neuron import h, gui 

    ^This should open the GUI


A NEURON & Python tutorial is available at 
https://neuron.yale.edu/neuron/static/docs/neuronpython/firststeps.html#


