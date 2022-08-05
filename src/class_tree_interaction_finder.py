import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
from sklearn import tree

from sklearn.datasets import load_iris
iris = load_iris()
df = pd.concat([pd.DataFrame(iris.data), pd.Series(iris.target)],
                axis = 1)
df.columns = iris.feature_names + ['target']
df['target'] = (df['target'] == 1).astype(int)
target = 'target'
n_trees = 100
feature_fraction = 0.7
lower_pt = 0.1
upper_pt = 0.1
lower_dev = 0.1
suffix_output = 'tree'

def class_tree_interaction_finder(
    df, 
    target, 
    n_trees = 100, 
    feature_fraction = 1,
    lower_pt = 0.1, 
    upper_pt = 0.1, 
    lower_dev = 0.1,
    suffix_output = 'tree') -> pd.DataFrame:
    '''
    
    Parameters
    ----------
    df : pd.DataFrame
        the main frame of data where the target and explanatory variables reside
    target : str
        the name of the binary target column
    n_trees : int
        number of trees to test. Default: 100
    feature_fraction : double
        between 0 and 1. Will randomly select a subset of features on each tree if feature_fraction is smaller than 1.Default = 1.
    lower_pt : double
        between 0 and 1. what is the max target penetration required to keep a node as a low penetration node. Default = 0.1
    upper_pt : double
        greater than 0, what is the min target penetration index required to keep a node as a high penetration node? Default = 0.1
    lower_dev : double
        greater than 0, the lower threshold for the deviance of the nodes accepted. Default = 0.1
    suffix_output : str
        suffix to the output columns

    Returns
    -------
    A (possibly empty) data.frame with the list of leaves interactions

    Example
    -------



    '''
    
    
    # Test the inputs
    if not isinstance(n_trees, (int)):
        raise TypeError("The input 'n_trees' is not of the correct format. Needs an integer.")

    if not (feature_fraction, (int, float)):
        raise TypeError("The input 'feature_fraction' is not of the correct format. Needs an numerical.")
    if (feature_fraction <= 0) | (feature_fraction > 1):
        raise ValueError("The input 'feature_fraction' needs to be between 0 and 1")

    if not (lower_pt, (int, float)):
        raise TypeError("The input 'lower_pt' is not of the correct format. Needs an numerical.")
    if (lower_pt <= 0) | (lower_pt > 1):
        raise ValueError("The input 'lower_pt' needs to be between 0 and 1.")

    if not (upper_pt, (int, float)):
        raise TypeError("The input 'upper_pt' is not of the correct format. Needs an numerical.")
    if (upper_pt <= 0) :
        raise ValueError("The input 'upper_pt' needs to be above 0.")

    if not (lower_dev, (int, float)):
        raise TypeError("The input 'lower_dev' is not of the correct format. Needs an numerical.")
    if (lower_dev <= 0) :
        raise ValueError("The input 'lower_dev' needs to be above 0.")

    if( (not is_numeric_dtype(df[target])) | ( min(df[target]) != 0 ) | ( max(df[target]) != 1 )):
        raise ValueError("The target fiel is not a binary numerical columns 0/1")

    for col in df.columns:
        if (not is_numeric_dtype(df[col])):
            raise ValueError(f"The column '{col}' is not numerical")

    # creates an output data for 'good' tree leaves

    feature_leaves = pd.DataFrame(
        { 'node_booleans' : pd.Series(dtype='str'),
          'target_penetration' : pd.Series(dtype='float'),
          'deviance' : pd.Series(dtype='float'),
          'total_weight' : pd.Series(dtype='float')})


    # asserts the main dataset
    main_data = df.copy()
    # removes target field from data to avoid random selection
    main_data.drop([target], axis = 1, inplace = True)

    # creates the number of trees specified by the function
    for i in range(1,n_trees+1):
        
        # randomly selects the requested number of fields for this tree
        tree_data = main_data.sample(
            frac = feature_fraction,
            axis = 1)

         
        clf = tree.DecisionTreeClassifier(
            min_samples_split = 30,
            ccp_alpha = 0.001
        )
        clf = clf.fit(tree_data, df[target])

        # stores the tree's output
        # tree_frame <- clf.tree_.Tree
        # tree_frame$node_id <- row.names(tree_frame)
        # tree_frame$target_penetration <- (tree_frame$dev / tree_frame$wt) / mean(df[[target]])

# n_nodes = clf.tree_.node_count
# children_left = clf.tree_.children_left
# children_right = clf.tree_.children_right
# feature = clf.tree_.feature
# threshold = clf.tree_.threshold

# node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
# is_leaves = np.zeros(shape=n_nodes, dtype=bool)
# stack = [(0, 0)]  # start with the root node id (0) and its depth (0)
# while len(stack) > 0:
#     # `pop` ensures each node is only visited once
#     node_id, depth = stack.pop()
#     node_depth[node_id] = depth

#     # If the left and right child of a node is not the same we have a split
#     # node
#     is_split_node = children_left[node_id] != children_right[node_id]
#     # If a split node, append left and right children and depth to `stack`
#     # so we can loop through them
#     if is_split_node:
#         stack.append((children_left[node_id], depth + 1))
#         stack.append((children_right[node_id], depth + 1))
#     else:
#         is_leaves[node_id] = True

# print(
#     "The binary tree structure has {n} nodes and has "
#     "the following tree structure:\n".format(n=n_nodes)
# )
# for i in range(n_nodes):
#     if is_leaves[i]:
#         print(
#             "{space}node={node} is a leaf node.".format(
#                 space=node_depth[i] * "\t", node=i
#             )
#         )
#     else:
#         print(
#             "{space}node={node} is a split node: "
#             "go to node {left} if X[:, {feature}] <= {threshold} "
#             "else to node {right}.".format(
#                 space=node_depth[i] * "\t",
#                 node=i,
#                 left=children_left[i],
#                 feature=feature[i],
#                 threshold=threshold[i],
#                 right=children_right[i],
#             )
#         )

#     # subset the nodes to only include nodes meeting the criteria
#     # keeps only terminal nodes with high/low penetration and high deviance
#     tree_frame <- subset(tree_frame,
#                          ncompete == 0 &
#                            (target_penetration < lower_pt |
#                               target_penetration > upper_pt) &
#                            dev > lower_dev)

#     # tidies up the tree frame into final results
#     tree_results <- data.frame(node_booleans = as.character(rpart::path.rpart(tree,
#                                                                        tree_frame$node_id,
#                                                                        print.it = F)),
#                                target_penetration = tree_frame$target_penetration,
#                                deviance = tree_frame$dev,
#                                total_weight = tree_frame$wt,
#                                stringsAsFactors = F)

#     # binds results from this tree to the main output
#     feature_leaves <- rbind(feature_leaves, tree_results)

#     # de-duplicate as we go along
#     feature_leaves <- feature_leaves[!duplicated(feature_leaves), ]

#     # print progress status
#     print(paste("Tree #",
#                 i,
#                 ", features so far:",
#                 nrow(feature_leaves)))

#   }

#   if (nrow(feature_leaves) > 0) { # instances with nodes (albeit possibly single field nodes)

#     # order the output with the highest target penetration at the top
#     feature_leaves <- feature_leaves[order(feature_leaves$target_penetration,
#                                            decreasing = T), ]

#     # begin feature function creation
#     # remove irrelevant characters from start of script (e.g. root syntax)
#     feature_leaves$node_feature <- substr(feature_leaves$node_booleans,
#                                           11,
#                                           nchar(feature_leaves$node_booleans))
#     # remove the slashes, spaces and speech marks added by the package
#     feature_leaves$node_feature <- gsub('[\"]',
#                                         '',
#                                         feature_leaves$node_feature)
#     # extract each feature from the tree output
#     feature_leaves$node_feature <- lapply(feature_leaves$node_feature,
#                                           function(x) paste(paste("df$",
#                                                                   unlist(strsplit(x, ",")),
#                                                                   sep = ""),
#                                                             collapse = " & "))

#     feature_leaves$node_feature <- gsub('df[:$:]\\s',
#                                         'df$',
#                                         feature_leaves$node_feature)
#     feature_leaves$node_feature <- gsub('[)]',
#                                         '',
#                                         feature_leaves$node_feature)

#     # convert this to string
#     feature_leaves$node_feature <- as.character(feature_leaves$node_feature)

#     # wrap the string in an ifelse statement
#     feature_leaves$node_feature <- paste("df$",
#                                          suffix_output,
#                                          "_",
#                                          1 : nrow(feature_leaves),
#                                          " <- ",
#                                          "ifelse(",
#                                          feature_leaves$node_feature,
#                                          ", 1, 0)",
#                                          sep = "")



#     # remove one field trees
#     # a leaf is based on one feature/field if it contains no &s to state multiple fields
#     feature_leaves$multi_field <- grepl('&', feature_leaves$node_feature)
#     feature_leaves <- subset(feature_leaves, feature_leaves$multi_field == TRUE)
#     feature_leaves$multi_field <- NULL

#     # remove the node_booleans as formatted version now exists
#     remove_me <- which(feature_leaves$node_booleans == 'root')

#     if(length(remove_me) != 0){
#       feature_leaves <- feature_leaves[-remove_me,]
#     }
#     feature_leaves$node_booleans <- NULL
#     return(feature_leaves)
#   } else { # instance without nodes
#     return(
#       data.frame( target_penetration = double(),
#                   deviance = double(),
#                   total_weight = double(),
#                   node_feature = character())

#     )
#   }