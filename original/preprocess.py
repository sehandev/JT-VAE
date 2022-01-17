# Standard
from argparse import ArgumentParser
from tqdm import tqdm
from multiprocessing import Pool
import pickle

# 3rd Party
from rdkit import RDLogger

# Project
from fast_jtnn.mol_tree import MolTree


def tensorize(
    smiles: str,
    is_assemble: bool = True,
) -> list:
    """Tensorize function

    Args:
        smiles (str): O=C1OCCC1Sc1nnc(-c2c[nH]c3ccccc23)n1C1CC1
        is_assemble (bool): assemble or not

    Returns:
        fast_jtnn.mol_tree.MolTree
    """
    mol_tree = MolTree(smiles)
    mol_tree.recover()

    if is_assemble:
        mol_tree.assemble()

        for node in mol_tree.nodes:
            # node: fast_jtnn.mole_tree.MolTreeNode
            # node.label: str (ex: [CH3:5][CH2:6][NH:6][CH3:7])
            # node.cands: list (ex: ['[CH3:5][CH:6]([NH2:6])[NH2:7]', '[CH3:5][CH2:6][NH:6][CH3:7]'])

            if node.label not in node.cands:
                node.cands.append(node.label)

    # TODO why should we delete them?
    # Delete mol_tree's mol
    del mol_tree.mol
    for node in mol_tree.nodes:
        del node.mol

    return mol_tree


if __name__ == '__main__':
    lg = RDLogger.logger()
    lg.setLevel(RDLogger.CRITICAL)

    parser = ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('-t', '--train', dest='train_path')
    parser.add_argument('-n', '--split', dest='num_splits', default=10, type=int)
    parser.add_argument('-j', '--jobs', dest='njobs', default=8, type=int)
    args = parser.parse_args()

    data = []
    with open(args.train_path) as train_file:
        line_list = train_file.readlines()  # length: 1584663
        for line in tqdm(line_list):
            smiles = line.strip(' \r\n')
            data.append(smiles)

    all_data = []
    pool = Pool(args.njobs)
    for result in tqdm(pool.imap_unordered(tensorize, data), total=len(data)):
        all_data.append(result)

    split_length = (len(all_data) + args.num_splits - 1) // args.num_splits

    for split_index in range(args.num_splits):
        st = split_index * split_length
        sub_data = all_data[st:st+split_length]

        with open('pkl/tensors-%d.pkl' % split_index, 'wb') as f:
            pickle.dump(sub_data, f, pickle.HIGHEST_PROTOCOL)
