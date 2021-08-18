FROM jvail/plantgl-jupyter:1.1.0

ENV PATH="/root/miniconda3/bin:${PATH}"

ARG PATH="/root/miniconda3/bin:${PATH}"
ARG NB_USER=jovyan
ARG NB_UID=1000

COPY . /home/${NB_USER}
USER root
RUN chown -R ${NB_UID} /home/${NB_USER}

RUN apt-get update && apt-get install --no-upgrade --no-install-recommends -y libgl1-mesa-dev

RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 
    
RUN conda install --quiet --yes scipy openalea.mtg alinea.caribu -c conda-forge -c fredboudon

WORKDIR /home/${NB_USER}

USER ${NB_USER}
