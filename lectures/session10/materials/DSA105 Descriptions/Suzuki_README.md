## Suzuki coupling data
Source: Nevado research group, extracted 16-06-2023

Description:
This dataset contains data on Suzuki reactions mined from lab journal entries in the Nevado group. The set includes SMILES strings of starting materials, reagents (bases, catalyst, (ligand)) and some solvents and the product.
Numerical data includes the reaction scale, the equivalents of all components and the yield, which is the variable of interest.

Experiments were performed by different people in a manual manner in different setups over a time span of several years. Analogue entries were digitized prior to the extraction from the ELN.

### Columns explained
| Column name              | Description                                             |
|:-------------------------|:--------------------------------------------------------|
| modifier                 | last modifier's shortname                               |
| elnCode                  | Identifier of experimenter                              |
| nrInLabJournal           | Nr of the entry in the ELN (chemjournal.chem.uzh.ch)    |
| reactionTitle            | Tag for the reaction type                               |
| refAmount / mol          | scale of the reaction in mol                            |
| Reactant1 - Smiles       | SMILES string of starting material 1                    |
| Reactant1 - CAS Nr       | CAS registry number of starting material 1              |
| Reactant1 - equiv.       | Stoichiometric equivalents for SM 1                     |
| Reactant2 - Smiles       | SMILES string of starting material 2                    |
| Reactant2 - CAS Nr       | CAS registry number of starting material 1              |
| Reactant2 - equiv.       | SMILES string of starting material 2                    |
| Reagent1 - Smiles        | SMILES string of reagent1 (base/catalyst)               |
| Reagent1 - CAS Nr        | CAS registry number of reagent1 (base/catalyst)         |
| Reagent1 - equiv.        | Stoichiometric equivalents for reagent1 (base /catalyst)|
| Reagent2 - Smiles        | SMILES string of reagent1 (base/catalyst)               |
| Reagent2 - CAS Nr        | CAS registry number of reagent1 (base/catalyst)         |
| Reagent2 - equiv.        | Stoichiometric equivalents for reagent1 (base/catalyst) |
| Reagent3 - Smiles        | SMILES string of reagent1 (base/catalyst)               |
| Reagent3 - CAS Nr        | CAS registry number of reagent1 (base/catalyst)         |
| Reagent3 - equiv.        | Stoichiometric equivalents for reagent1 (base/catalyst) |
| Solvent1 - Smiles        | SMILES string of solvent1                               |
| Solvent1 - CAS Nr        | CAS registry number of solvent1                         |
| Solvent1 - Volume / mL   | Amount of solvent1 in mL                                |
| Solvent2 - Smiles        | SMILES string of solvent2                               |
| Solvent2 - CAS Nr        | CAS registry number of solvent2                         |
| Solvent2 - Volume / mL   | Amount of solvent2 in mL                                |
| Product1 - Smiles        | SMILES string of product1                               |
| Product1 - Yield         | Product yield in %                                      |


