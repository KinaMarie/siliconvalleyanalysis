#### SINGLE THRESHOLD VERSION
# It's inefficient to calculate and store all of the scores
# between all possible links
#
# score_function: a function that calculates a normalized
# score given investor, company, g
#
# truth is a set-like object containing all links (investor, company)
# created in the validation period
#
# threshold is a float above which values will be predicted positive
def eval_prec_recall(truth, score_function, threshold, g):
    # initialize counters
    (tp, tn, fp, fn) = (0,0,0,0)
    
    # initialize list of companies and investors
    investors = range(1, 2000)
    companies = range(2001, 4000)
    
    # iterate over all companies
    for company in companies:
        for investor in investors:
            # Calculate the score_function prediction
            p = score_function(investor, company, g)
            
            # Make a prediction based on the threshold
            link_predicted = (p > threshold)
            
            # Record if it was a true/false pos or true/false neg
            if link_predicted:
                if (investor, company) in truth:
                    tp += 1
                else:
                    fp += 1
            else:
                if (investor, company) not in truth:
                    tn += 1
                else:
                    fn += 1
    
    print (tp, tn, fp, fn)
    # calculate precision and recall
    if (tp+fp) > 0:
        precision = tp/(tp+fp)
    else:
        precision = np.NaN
    
    if (tp+fn) > 0:
        recall = tp/(tp+fn)
    else:
        recall = np.NaN
    
    return (precision, recall)
    