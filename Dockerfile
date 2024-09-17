FROM ubuntu:18.04

WORKDIR /app

# Install conda
RUN apt-get update
RUN apt-get install -y wget bzip2 build-essential

RUN mkdir -p /app/miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O /app/miniconda3/miniconda.sh
RUN /bin/bash /app/miniconda3/miniconda.sh -b -u -p /app/miniconda3
RUN ls /app/miniconda3/miniconda.sh
ENV PATH=/app/miniconda3/bin:$PATH
RUN rm /app/miniconda3/miniconda.sh

# Add prereqs
RUN conda update conda
RUN conda update --all
RUN conda config --append channels conda-forge

# Create the environment:
COPY environment.yml /app/environment.yml
RUN conda env create -f /app/environment.yml

# Make RUN commands use the new environment:
RUN conda init
RUN echo "conda activate allium" >> /app/.bashrc
ENV PATH=/app/miniconda3/envs/allium/bin:$PATH
