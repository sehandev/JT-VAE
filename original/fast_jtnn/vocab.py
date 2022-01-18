# Standard
import copy

# 3rd Party
from rdkit.Chem import MolFromSmiles


class Vocab:
    """
    Parameters:
        penzynes (list): list of 5-membered ring
        benzynes (list): list of 6-membered ring
    """
    penzynes = ['C1=C[NH]C=C1', 'C1=C[NH]C=N1', 'C1=C[NH]N=C1', 'C1=C[NH]N=N1', 'C1=COC=C1', 'C1=COC=N1', 'C1=CON=C1', 'C1=CSC=C1', 'C1=CSC=N1', 'C1=CSN=C1', 'C1=CSN=N1', 'C1=NN=C[NH]1', 'C1=NN=CO1', 'C1=NN=CS1', 'C1=N[NH]C=N1', 'C1=N[NH]N=C1', 'C1=N[NH]N=N1', 'C1=NN=N[NH]1', 'C1=NN=NS1', 'C1=NOC=N1', 'C1=NON=C1', 'C1=NSC=N1', 'C1=NSN=C1']
    benzynes = ['C1=CC=CC=C1', 'C1=CC=NC=C1', 'C1=CC=NN=C1', 'C1=CN=CC=N1', 'C1=CN=CN=C1', 'C1=CN=NC=N1', 'C1=CN=NN=C1', 'C1=NC=NC=N1', 'C1=NN=CN=N1']

    def __init__(self, smiles_list):
        self.vocab = smiles_list
        self.vmap = {x: i for i, x in enumerate(smiles_list)}
        self.slot_list = [self.get_slot(smiles) for smiles in smiles_list]

        self.update_ring_list()

    @staticmethod
    def get_slot(smiles):
        mol = MolFromSmiles(smiles)

        slot = []
        for atom in mol.GetAtoms():
            slot.append((atom.GetSymbol(), atom.GetFormalCharge(), atom.GetTotalNumHs()))

        return slot

    def update_ring_list(self):
        ring_5_list = ['C1=NCCN1', 'C1=NNCC1']
        ring_6_list = ['C1=CCNCC1']

        for smiles in self.vocab:
            if smiles.count('=') >= 2:
                num_atoms = MolFromSmiles(smiles).GetNumAtoms()
                if num_atoms == 5:
                    ring_5_list.append(smiles)
                elif num_atoms == 6:
                    ring_6_list.append(smiles)

        Vocab.penzynes = ring_5_list
        Vocab.benzynes = ring_6_list

    def get_index(self, smiles):
        return self.vmap[smiles]

    def get_smiles(self, idx):
        return self.vocab[idx]

    def get_slots(self, idx):
        return copy.deepcopy(self.slot_list[idx])

    def size(self):
        return len(self.vocab)
