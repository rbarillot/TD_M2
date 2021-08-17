FROM jvail/plantgl-jupyter:1.1.0

ARG NB_USER=jovyan
ARG NB_UID=1000

COPY . /home/${NB_USER}
USER root
RUN chown -R ${NB_UID} /home/${NB_USER}
RUN pip install https://github.com/openalea/mtg
WORKDIR /home/${NB_USER}

USER ${NB_USER}
