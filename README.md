# Decision Tree
### Using the ID3 algorithm
### Requirement: Python 3
### Datasets:
    http://archive.ics.uci.edu/ml/datasets/Tic-Tac-Toe+Endgame
    http://archive.ics.uci.edu/ml/datasets/Chess+%28King-Rook+vs.+King-Pawn%29
    
## Split Dataset
* split2.py - splits dataset into 2 files - training.csv (~80%) and test.csv (~20%)
* split.p - splits dataset into 3 files (used for pruning) - training.csv (~60%), validate.csv (~20%), and test.csv (~15%)

## Commands
#### split.py and split2.py
Requires a parameters passed via the command line: Filename as dataset (first argument)
Example:
```
python3 split.py kr-vs-kp.csv
```
#### id3.py
Accepts parameters passed via the command line:
* Filename for training (first argument) required
* '-w' for changing class value (in this case, it's used for kr-vs-kp.csv),'positive' and 'negative' by default
* '-p' for pruning the tree
* '-r' for using gain ratio
Example:
```
python3 id3.py -w
python3 id3.py -w -p -r
```
