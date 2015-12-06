#DON'T FORGET TO CHECK FOR IGNORE EDGES THAT ALREADY EXIST
# We want to factor our code so that it is efficient for simple multiprocessing
#
# Given a LIST of investors, a SINGLE company, calculate the number of TP/TN/FP/FN
# and return as a counter. This is meant to run inside of eval_prec_recall.
def company_score_pred_eval(truth, score_function, threshold, g, company, investors):
    result = Counter()
    for investor in investors:
        # Calculate the score_function score
        score = score_function(investor, company, g)

        # Make a prediction based on the threshold
        link_predicted = (score > threshold)

        # Record if it was a true/false pos or true/false neg
        if link_predicted:
            if (investor, company) in truth:
                result['tp'] += 1
            else:
                result['fp'] += 1
        else:
            if (investor, company) not in truth:
                result['tn'] += 1
            else:
                result['fn'] += 1
    
    return result
    

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
    full_results = Counter({'tp':0, 'tn':0, 'fp':0, 'fn':0})
    
    # initialize list of companies and investors
    investors = range(1, 2000)
    companies = range(2001, 4000)
    
    # iterate over all companies
    for company in companies:
        full_results = full_results + company_score_pred_eval(truth, score_function, 
                                                              threshold, g, company, 
                                                              investors)

    print full_results
    (tp, tn, fp, fn) = (full_results["tp"], full_results["tn"], full_results["fp"], full_results["fn"])
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

# Test Eval/Prec/Recall 
random_truth = set(map(lambda x: (random.randint(1,2000), random.randint(1001, 4000)), range(1,1000)))
%time eval_prec_recall(random_truth, rand_score, 0.8, [])
