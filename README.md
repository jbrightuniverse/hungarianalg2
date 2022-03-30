A Python 3 implementation of the Hungarian Algorithm for optimal matching in bipartite weighted graphs, upgraded to run faster.

Based on the graph theory implementation in [these notes](http://www.cse.ust.hk/~golin/COMP572/Notes/Matching.pdf) combined with the matrix interpretation in [these notes](https://montoya.econ.ubc.ca/Econ514/hungarian.pdf). Also derives from [these](https://github.com/jbrightuniverse/FastHungarianAlgorithm) [repos](https://github.com/jbrightuniverse/hungarianalg).

For a detailed overview, see [this Jupyter notebook](https://github.com/jbrightuniverse/Hungarian-Algorithm-No.-5/blob/main/HungarianAlgorithm.ipynb).

# Usage

Installation: `pip install git+https://github.com/jbrightuniverse/hungarianalg2`

Import: `from hungarianalg2.alg import hungarian`

Function call: `result = hungarian(matrix)`

Properties:
- Optimal Matching: `result.match`
- Revenues: `result.revenues`
- Row Weights: `result.row_weights`
- Col Weights: `result.col_weights`
- Total Revenue: `result.revenue_sum`

See `example.py` for a comprehensive example.

NOTE: This version appears to resolve the decimals issue faced by the original version of this algorithm; however, this has not been thoroughly tested.
