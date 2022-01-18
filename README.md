<div align="center">

## PyTorch Lightning Template

</div>

# Initialize project

Get W&B API key from https://wandb.ai/authorize

```bash
conda init bash
pip install -r requirements.txt
wandb login
```

# Install RDKit

Install with official document (ver 2021.09.1) → [RDKit Document](https://www.rdkit.org/docs/Install.html)
```bash
conda install -c conda-forge rdkit
```

# How to run original code

## Make directories
```bash
cd original
mkdir data/[dataset]/processed/
mkdir vae_model/
```

## Deriving Vocabulary (???)

```bash
python fast_jtnn/mol_tree.py < data/moses/train.txt
```

## Preprocess for dataset

```bash
python preprocess.py @preprocess.config
python vae_train.py @vae_train.config
```

In progress ...
