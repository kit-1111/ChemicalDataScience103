## Biotransformation rates in activated sludge
Source: FERRET database, Fenner team. Extracted on 14/04/2026.

This dataset contains biomass-corrected biotransformation rates (kbio), 
calculated from observed biotransformation rates (kobs) 
using the amound of Total Suspended Solids (TSS) as a biomass indicator.
Experiments were performed by different people (person_name) for mostly 
pesticides and pharmaceuticals.
The target variable of interest is log-transformed kbio, log_kbio.

### Columns explained
| Column name              | Description                                             |
|:-------------------------|:--------------------------------------------------------|
| sub_id                   | kinetic status (P, D, BT, …)                            |
| sub_id                   | Substance ID in FERRET DB                               |
| kinetic_status           | kinetic status (P, D, BT, …)                            |
| sorption	               | Sorption observed? (y/n)                                |
| abiotic                  | Abiotic transformation? (y/n)                           |
| R2                       | R2 of fit to calculate kobs                             |
| comment                  | Indication on censoring direction, if applicable (<, >) |
| p_value                  | p_value of fit to calculate kobs                        |
| cds_code	               | name of conditions under which experiment was performed |
| Normal WWTP conditions   | normal WWTP conditions? (y/n)                           |
| TSS (g/L)                | Biomass as total suspended solids                       |
| kobs_lower_threshold	   | lower threshold of kobs calculation                     |
| kobs_upper_threshold	   | upper threshold of kobs calculation                     |
| duration                 | Test duration                                           |
| person_name              | Name of the person responsible for experiments          |
| uchem_id	               | Uchem ID                                                |
| inchi_id	               | InChI Key                                               |
| substance_class          | Substance class in COSOMI                               |
| compound_name            | Compound name                                           |
| smiles                   | SMILES string                                           |
| cas                      | CAS number                                              |
| kbio	                   | reported kbio [days]                                    |
| kbio_upper_threshold	   | upper threshold of kbio calculation                     |
| kbio_lower_threshold	   | lower threshold od kbio calculation                     |
| log_kbio	               | log-transformed kbio [log(days)]                        |

