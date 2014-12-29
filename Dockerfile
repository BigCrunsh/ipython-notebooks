FROM ubuntu:trusty

MAINTAINER Christoph Sawade <christoph@sawade.me>

# apt
RUN apt-get update
RUN apt-get install -y python-software-properties
RUN apt-get update

# base
RUN apt-get install -y wget unzip pkg-config libyaml-dev git openssh-client make

# base ipython packages
RUN apt-get install -y ipython ipython-notebook python-numpy python-pip \
  python-matplotlib python-pandas python-nose pandoc
RUN apt-get install -y gfortran libopenblas-dev liblapack-dev

# python
RUN pip install --upgrade scipy
RUN pip install patsy
RUN pip install statsmodels
RUN pip install bokeh
RUN pip install pylint==1.2.0
RUN apt-get install -y python-pygraphviz

# mount
RUN echo cd /srv/analysis > ~/.bashrc

ADD . /srv/analysis
