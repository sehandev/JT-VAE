FROM pytorch/pytorch:1.10.0-cuda11.3-cudnn8-devel

ARG DEBIAN_FRONTEND=noninteractive

# https://github.com/deluan/zsh-in-docker
COPY zsh-in-docker.sh .
RUN sh zsh-in-docker.sh \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions

RUN conda install -c conda-forge rdkit

ENTRYPOINT ["tail", "-f", "/dev/null"]