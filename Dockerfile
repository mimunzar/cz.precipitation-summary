FROM    continuumio/miniconda3
WORKDIR /home/app

COPY environment.yml .
RUN  conda update -n base -c defaults conda \
    && conda env create -p miniconda/ -f environment.yml \
    && conda clean -ay \
    && conda init bash
    #^ Build environment first so changes to the source don't trigger reinstallation

COPY scripts/ scripts/
RUN  chmod +x scripts/start_in_env.sh

COPY src/ src/
ENTRYPOINT ["scripts/start_in_env.sh", "miniconda/"]

