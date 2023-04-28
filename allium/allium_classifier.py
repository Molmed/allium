import pandas as pd
import numpy as np
from .helpers import predict_proba

class AlliumClassifier():
    def predictionsNSC(self, subtype_groups, model, discoverydf, discoverypheno, clinicaldatalist, unique_genedf, 
                   subtypecol, ids, name, datatype, signature_mode = 'all',
                   imputation = None, to_json = False):
                   
    
        """ 
        Arguments:
    
        --model: A dictionary containing a fitted NSC classifier model per subtype--discoverydf: pandas dataframe num_samples x num_features for the dataset the predictions will be made on
        --descoverydf: pandas dataframe num_samples x num_features for the dataset used for the discovery phase
        --discoverypheno: pandas dataframe num_samples x clinical features for discovery df; leave empty if not applicable
        --clinicaldatalist: list of clinical features of interest to include on the output dataframe; leave empty if not applicable
        --unique_genedf: pandas dataframe all genes per subtype
        --subtypecol: the column with the subtypes from unique_genedf DataFrame to retrieve the signatures per subtype
        --ids: the ID name column for the signatures
        --name: name of the predictions column
        --datatype: e.g. DNAm or GEX so as to create a subtype group column with the appropriate prefix
        --signature_mode: If all, then all signatures are used for each classifier, otherwise each classifier uses their own signatures
        --imputation: If None then it will be on GEX mode, else will use as impute the exported imputer for imputing the DNAm data
        
        Returns:
        
        --ungen: dataframe with predictions on the desired cohort for each classifier 
        along with their corresponding probability score for each classifier's subtype

        """

        if imputation == None: # GEX mode
            #subtype_groups = groupings(DNAm = False)
            pass
            
        else: # DNAm mode
            #subtype_groups = groupings(DNAm = True)
            discoverydf = discoverydf[unique_genedf[ids].to_list()]
            discoverydf = pd.DataFrame(imputation.transform(discoverydf), columns = discoverydf.columns, index = discoverydf.index)
        if not clinicaldatalist: # in case there is no clinical info - completely blind samples or unavaibable for use
            ungen = pd.DataFrame(index = (discoverydf.index))
        else:
            ungen = pd.DataFrame(discoverypheno[clinicaldatalist], columns = clinicaldatalist, index = (discoverypheno.index))
        
        ######################################### Subtype group (N = 12) loop #####################################################
        for subtype in list(subtype_groups.keys()):
            ############################### ONE vs REST approach for the subtype groups ##########################################
            print('Starting with subtype group {}'.format(subtype))
            if signature_mode == 'all':
                sub_genes = unique_genedf[ids].to_list() # subtype specific signatures
            else:
                sub_genes = unique_genedf[unique_genedf[subtypecol] == subtype][ids].to_list() # subtype specific signatures
    
            # create label decoder manually so at the always set other as the 0 class; otherwise the encoding will take place in 
            # alphabetical order          
            decoder = {0: 'other', 1: subtype}
            # Model prediction
            clfall = model[subtype]
            clfall.predict_proba = predict_proba.__get__(clfall)
            encodingsdf = pd.DataFrame(clfall.predict(discoverydf[sub_genes]), columns = ['encodings'])
            # decode the predictions
            unpreds = encodingsdf.encodings.map(decoder).values 
            probas = clfall.predict_proba(discoverydf[sub_genes])
            #probas = predict_proba(clfall, discoverydf[sub_genes]) #another way to call it
            ungen[subtype+'.classifier.pred'] = unpreds
            ungen[subtype+'.classifier.proba'] = probas[:, 1]
            ######################### ONE vs ONE classifier for groups with 2 subtype members ############################
            separation_subs = subtype_groups[subtype]
            if len(separation_subs) == 2:
                subtype_sep = separation_subs[0]+'_vs_'+separation_subs[1]
                if signature_mode == 'all':
                    sub_genes = unique_genedf[ids].to_list() # subtype specific signatures
                else:
                    sub_genes = unique_genedf[unique_genedf[subtypecol] == subtype_sep][ids].to_list() # subtype specific signatures
                newdf = ungen[ungen[subtype+'.classifier.pred'] == subtype].copy()
                #newdf['subtypes'] = newdf[subtype+'.classifier.pred']
                if not newdf.empty: # avoid to move forward to subtype level if all the predictions for the groups predicted as other
                    print('-------Start one vs one approach-----------')
                    print('---------------{} vs {}---------------'.format(separation_subs[0], separation_subs[1]))
                    Xnew = discoverydf.reindex(newdf.index)
                    label_decoder = {}
                    for i, sub in enumerate(separation_subs):
                        label_decoder[i] = sub
                    # Model prediction
                    clfall = model[subtype_sep]
                    clfall.predict_proba = predict_proba.__get__(clfall)
                    encodingsdf = pd.DataFrame(clfall.predict(Xnew[sub_genes]), columns = ['encodings'])
                    # decode the predictions
                    unpreds = encodingsdf.encodings.map(label_decoder).values 
                    probas = clfall.predict_proba(Xnew[sub_genes])
                    newdf[subtype_sep +'.classifier.pred'] = unpreds
                    indices = newdf.index.to_list()
                    # add the columns to the ungen dataframe
                    ungen.loc[indices, subtype_sep +'.classifier.pred'] = newdf.loc[indices, subtype_sep +'.classifier.pred']
                    for i, sub in enumerate(separation_subs):
                        newdf[sub + '.classifier.proba'] = probas[:, i]
                        ungen.loc[indices, sub +'.classifier.proba'] = newdf.loc[indices, sub +'.classifier.proba']
                else: # if group proba < 0.5 so the classifier doesn't move to subtype level (keep the columns though)
                    for i, sub in enumerate(separation_subs):
                        ungen[sub +'.classifier.proba'] = np.nan
            ############################### Multiclass classifier for groups with >2 subtype members ###################
            elif len(separation_subs) > 2:
                newdf = ungen[ungen[subtype+'.classifier.pred'] == subtype].copy()
                #newdf['subtypes'] = newdf[subtype+'.classifier.pred']
                if not newdf.empty: # avoid to move forward to subtype level if all the predictions for the groups predicted as other
                    print('-------Start multiclass approach-----------')
                    Xnew = discoverydf.reindex(newdf.index)
                    label_decoder = {}
                    for i, sub in enumerate(separation_subs):
                        label_decoder[i] = sub
                    if signature_mode == 'all':
                        sub_genes = unique_genedf[ids].to_list() # subtype specific signatures
                    else:
                        sub_genes = unique_genedf[unique_genedf[subtypecol].isin(separation_subs)][ids].to_list()# subtype specific signatures
                    # Model prediction
                    clfall = model['Overall_' + subtype]
                    clfall.predict_proba = predict_proba.__get__(clfall)
                    encodingsdf = pd.DataFrame(clfall.predict(Xnew[sub_genes]), columns = ['encodings'])
                    # decode the predictions
                    unpreds = encodingsdf.encodings.map(label_decoder).values 
                    probas = clfall.predict_proba(Xnew[sub_genes])
                    # create the multiclass prediction column and probability columns
                    indices = newdf.index.to_list()
                    newdf['Overall_' + subtype + '.classifier.pred'] = unpreds
                    ungen.loc[indices, 'Overall_' + subtype + '.classifier.pred'] = newdf.loc[indices, 'Overall_' + subtype + '.classifier.pred']
                    for i, sub in enumerate(separation_subs):
                        newdf[sub + '.classifier.proba'] = probas[:, i]
                        ungen.loc[indices, sub + '.classifier.proba'] = newdf.loc[indices, sub + '.classifier.proba']
                else: # if group proba < 0.5 so the classifier doesn't move to subtype level (keep the columns though)
                    for i, sub in enumerate(separation_subs):
                        ungen[sub +'.classifier.proba'] = np.nan
        ### Group conditions 
        conditions = ungen.loc[:, (ungen.columns.str.endswith('pred'))&
                                                    (~ungen.columns.str.contains('vs'))&
                            (~ungen.columns.str.contains('Overall_aneuploidy.classifier.pred'))] 
        ungen['#predicted.classes'] = (conditions != 'other').sum(axis = 1)
        finalpreds = []
        finalpreds_explained = [] # group level
        proba_explained = []
        finalpreds_explained2 = [] # subtype level
        proba_explained2 = []
        '''Create single/multi/unknown class based on the predicted classes value
        Additionally include: detailed predictions column so as to be easier to identify
        multiclasses, as well as a probability detailed column in both group and subtype level'''
        for rows in conditions.iterrows():
            if ungen.loc[ungen.index == rows[0], '#predicted.classes'].values == 1:
                singlecases = rows[1].unique()[rows[1].unique()!= 'other'][0]
                finalpreds.append(singlecases)
                finalpreds_explained.append(singlecases)
                singlepreds = str(round(ungen.loc[rows[0], singlecases + '.classifier.proba'], 4))
                proba_explained.append(singlepreds)
                ########## Subtype level ########
                if singlecases in list(subtype_groups.keys()) and len(subtype_groups[singlecases]) == 2:
                    clfs = subtype_groups[singlecases][0]+ '_vs_' + subtype_groups[singlecases][1]
                    subtypepredictions = ungen.loc[rows[0], clfs + '.classifier.pred']
                    finalpreds_explained2.append(subtypepredictions)
                    sub_preds = str(round(ungen.loc[rows[0], subtypepredictions + '.classifier.proba'], 4))
                    proba_explained2.append(sub_preds)
                elif singlecases in list(subtype_groups.keys()) and len(subtype_groups[singlecases]) > 2:
                    subtypepredictions = ungen.loc[rows[0],'Overall_aneuploidy.classifier.pred']
                    finalpreds_explained2.append(subtypepredictions)
                    sub_preds = str(round(ungen.loc[rows[0], subtypepredictions + '.classifier.proba'], 4))
                    proba_explained2.append(sub_preds)
                else:
                    finalpreds_explained2.append(singlecases)
                    proba_explained2.append(singlepreds)     
            elif ungen.loc[ungen.index == rows[0], '#predicted.classes'].values > 1:
                finalpreds.append('multiclass')
                multicases = list(rows[1].unique()[rows[1].unique()!= 'other'])
                finalpreds_explained.append(', '.join(multicases))
                multiclassifiers = [m + '.classifier.proba' for m in multicases]
                multipreds = [str(round(x, 4)) for x in ungen.loc[rows[0], multiclassifiers].values]
                proba_explained.append(', '.join(multipreds))
                ############# Subtype level #########
                multicases2 = []
                for multi in multicases:
                    if multi in list(subtype_groups.keys()) and len(subtype_groups[multi]) == 2:
                        clfs = subtype_groups[multi][0]+ '_vs_' + subtype_groups[multi][1]
                        subtypepredictions = ungen.loc[rows[0], clfs + '.classifier.pred']
                        multicases2.append(subtypepredictions)
                    elif multi in list(subtype_groups.keys()) and len(subtype_groups[multi]) > 2:
                        subtypepredictions = ungen.loc[rows[0],'Overall_aneuploidy.classifier.pred']
                        multicases2.append(subtypepredictions)
                    else:
                        multicases2.append(multi)        
                finalpreds_explained2.append(', '.join(multicases2))
                multiclassifiers2 = [m + '.classifier.proba' for m in multicases2]
                multipreds2 = [str(round(x, 4)) for x in ungen.loc[rows[0], multiclassifiers2].values]
                proba_explained2.append(', '.join(multipreds2))   
            elif ungen.loc[ungen.index == rows[0], '#predicted.classes'].values == 0:
                finalpreds.append('no_class')
                finalpreds_explained.append('no_class')
                proba_explained.append('<0.5')
                finalpreds_explained2.append('no_class')
                proba_explained2.append('<0.5')
        ungen[name] = finalpreds
        ungen['Subtype detailed_v1'] = finalpreds_explained
        ungen['Probability detailed_v1'] = proba_explained
        ungen['Subtype detailed_v2'] = finalpreds_explained2
        ungen['Probability detailed_v2'] = proba_explained2
        ungen.drop(ungen.columns[ungen.columns.str.endswith('pred')], axis = 1, inplace = True)
        ungen.drop(ungen.columns[ungen.columns.str.contains('vs')], axis = 1, inplace = True)
        ### part II : Multiclass to single class: keep the prediction with the highest probability score #####
        predictions_up = []
        numclasses_new = []
        probabilities_final = []
        predictions_final = []
        comments = []
        # The selection will be made based on the group probabilities
        for data, preds, numclasses, finalsubs, preds_sub in zip(ungen['Subtype detailed_v1'], ungen['Probability detailed_v1'],
                                            ungen['#predicted.classes'], ungen['Subtype detailed_v2'],  
                                                    ungen['Probability detailed_v2']):
            if numclasses > 1:
                probs = [float(p) for p in preds.split(', ')]
                classes = data.split(', ')
                # selection based on highest group score
                max_index = np.argmax(probs, axis = -1)
                predictions_up.append(classes[max_index])
                numclasses_new.append(1)
                ## subtype level ##
                subtype_probs = [float(p) for p in preds_sub.split(', ')]
                classes_subs = finalsubs.split(', ')
                probabilities_final.append(subtype_probs[max_index])
                predictions_final.append(classes_subs[max_index])
                if subtype_probs[max_index] < 0.7: # check the probability of the selected subtype group per patient
                    comments.append('Manual check is required')
                else:
                    comments.append('Passed control')
            else:
                predictions_up.append(data)
                numclasses_new.append(numclasses)
                probabilities_final.append(preds_sub)
                predictions_final.append(finalsubs)
                if preds_sub == '<0.5': # check the probability of the selected subtype group per patient
                    comments.append('No class prediction')
                else:
                    if float(preds_sub) < 0.7: # check the probability of the selected subtype group per patient
                        comments.append('Manual check is required')
                    else:
                        comments.append('Passed control')       
        ungen[datatype + '_subtype_groups'] = predictions_up 
        ungen['#classes.updated'] = numclasses_new 
        ungen[datatype + '_probability_V2'] = probabilities_final
        ungen[datatype + '_subtype_V2'] = predictions_final    
        ungen[datatype + '_subtype_comments'] = comments
        
        # drop the aiding columns
        ungen.drop(['Subtype detailed_v2', 'Probability detailed_v2'], axis = 1, inplace = True)

        if to_json:
            return ungen.to_json(orient="index")

        return ungen
