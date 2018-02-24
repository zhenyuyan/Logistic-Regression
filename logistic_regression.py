import math,sys
#import time

def create_dic_Y_thetaM(filename):
    f = open(filename,"r")
    Y = []
    dicX = {};
    dicY = {}
    index = 1
    X = []
    Y_catgory = []
    indexX = 0
    for row in f:
        if row.split("\t")[0] != "\n":
            if dicX.has_key(row.split("\t")[0]) == False:
               dicX[row.split("\t")[0]] = str(indexX)
               indexX = indexX + 1
            X.append(row.split("\t")[0])
            Y.append(row.split("\t")[1].strip("\n"))
            dicY[row.split("\t")[1].strip("\n")] = "1"
        index = index + 1

    thetaM = [[0 for row in range(len(dicX) + 1)] for col in range(len(dicY))]
    #print dicX[X[10]]
    for key in dicY:
        Y_catgory.append(key)
    #print Y_catgory
    Y_catgory.sort()
    f.close()
    return dicX,X,Y,thetaM,Y_catgory

def I(Y,k,i,Y_catgory):
    if Y[i] == Y_catgory[k]:
        return 1
    else:
        return 0

def gradient_decent_k(X,Y,dicX,Y_catgory,thetaM,i):
    low_item = 0
    up_item = 0
    index = 0
    word_position = int(dicX[X[i]]) + 1
    #print "this word's position is" ,word_position
    while index < len(thetaM):
        low_item_inner =  thetaM[index][word_position]  + thetaM[index][0]
        low_item = low_item + math.exp(low_item_inner)
        index = index + 1
    for k in range(len(thetaM)):
        up_item = math.exp(thetaM[k][word_position] + thetaM[k][0])
        #print up_item,thetaM[k][word_position],thetaM[k][0],low_item
        scalar = -(I(Y,k,i,Y_catgory) - up_item/low_item)
        #print "scalar is", scalar, "I is", I(Y,k,i,Y_catgory)
        j = 0
        while j < len(thetaM[k]):
            if j == word_position or j == 0:
                thetaM[k][j] = thetaM[k][j] - 0.5 * scalar
            j = j + 1
    return thetaM

def iterate(dicX,X,Y,thetaM,Y_catgory):
    #dicX,X,Y,thetaM,Y_catgory = create_dic_Y_thetaM(train_filename)
    for i in range(len(X)):
            thetaM = gradient_decent_k(X,Y,dicX,Y_catgory,thetaM,i)
            #print thetaM
    return thetaM

def negtive_likelihood(X,Y,dicX,Y_catgory,thetaM):
    #print thetaM
    l = 0
    for i in range(len(X)):
        for k in range(len(thetaM)):
            index = 0
            low_item = 0
            up_item = 0
            word_position = int(dicX[X[i]]) + 1
            while index < len(thetaM):
                low_item_inner =  thetaM[index][word_position]  + thetaM[index][0]
                low_item = low_item + math.exp(low_item_inner)
                index = index + 1
            up_item = math.exp(thetaM[k][word_position] + thetaM[k][0])
            #print "k is", k
            #print "up,lower are ",up_item,low_item
            l = l + I(Y,k,i,Y_catgory) * math.log(up_item/low_item)
            #print l
            #print "l I are ",l,I(Y,k,i,Y_catgory)
    likelihood = - l /(len(X))
    return likelihood

def prediction(X,Y,dicX,thetaM,Y_catgory,i):
    # the ith word in the X matrix
    word_position = int(dicX[X[i]]) + 1
    P = []
    low_item = 0
    for k in range(len(thetaM)):
        up_item = thetaM[k][0] + thetaM[k][word_position]
        P.append(up_item)
    #print P
    #print P.index(max(P))
    return P.index(max(P))

def output_labels(dicX,X,thetaM,Y_catgory,test_filename,open_file_name):
    #print Y_catgory
    f0 = open(test_filename,'r')
    i = 0
    f1 = open(open_file_name,'wb')
    for line in f0:
        if line != '\n':
            word = line.split("\t")[0]
            which_class = prediction(X,Y_catgory,dicX,thetaM,Y_catgory,i)
            i = i + 1
            #print 'the class is ',which_class,Y_catgory[which_class]
            f1.write(Y_catgory[which_class]+ '\n')
        else:
            f1.write('\n')
    f1.close()
    f0.close()

def calculate_errorate(original_file,label_file):
    f1 = open(original_file,'r')
    f2 = open(label_file,'r')
    lines1 = f1.readlines()
    lines2 = f2.readlines()
    if len(lines1) != len(lines2):
        print "error"
    i = 0
    error = 0
    total_words = 0
    while i < len(lines1):
        if lines1[i] != '\n':
            total_words = total_words + 1
            if str(lines1[i].split("\t")[1].strip("\n")) != str(lines2[i]).strip("\n"):
                #print lines1[i].split("\t")[1].strip("\n"),lines2[i]
                error = error + 1
        i = i + 1
    #print 'error, total_words',error,total_words
    error_rate = float(float(error)/float(total_words))
    return error_rate

def create_dic_Y_thetaM_M2(filename):
    f = open(filename,"r")
    Y = []
    dicX = {}
    dicX_pre = {}
    dicX_aft = {}
    dicY = {}
    index = 1
    X = []
    Y_catgory = []
    indexX = 0
    for row in f:
        if row.split("\t")[0] != "\n":
            if dicX.has_key(row.split("\t")[0]) == False:
               dicX[row.split("\t")[0]] = str(indexX)
               dicX_pre[row.split("\t")[0]] = str(indexX)
               dicX_aft[row.split("\t")[0]] = str(indexX)
               indexX = indexX + 1
            X.append(row.split("\t")[0])
            Y.append(row.split("\t")[1].strip("\n"))
            dicY[row.split("\t")[1].strip("\n")] = "1"
        else:
            Y.append('\n')
            X.append('\n')
        #index = index + 1
    dicX_pre['BOS'] = len(dicX)
    dicX_aft['EOS'] = len(dicX)
    thetaM = [[0 for row in range(3 * len(dicX) + 3)] for col in range(len(dicY))]
    #print dicX[X[10]]
    for key in dicY:
        Y_catgory.append(key)
    #print Y_catgory
    Y_catgory.sort()
    f.close()
    return dicX,dicX_pre,dicX_aft,X,Y,thetaM,Y_catgory


def gradient_decent_k_M2(X,Y,dicX,dicX_pre,dicX_aft,Y_catgory,thetaM,i):
    cur_word = X[i].split("\t")[0]
    #print cur_word
    if cur_word != '\n':
        pre_word = ''
        aft_word = ''
        if i == 0:
            pre_word = 'BOS'
            aft_word = X[i + 1].split("\t")[0]
        elif i == len(X) - 1:
            pre_word = X[i - 1].split("\t")[0]
            aft_word = 'EOS'
        else:
            pre_word = X[i - 1].split("\t")[0]
            aft_word = X[i + 1].split("\t")[0]
        if pre_word =='\n':
            pre_word = 'BOS'
        if aft_word == '\n':
            aft_word = 'EOS'
        #print "pre_word,cur_word,aft_word are " ,pre_word,cur_word,aft_word
        low_item = 0
        up_item = 0
        index = 0
        word_position = int(dicX[cur_word]) + 1
        pre_position = int(dicX_pre[pre_word]) + 1 + len(dicX)
        aft_position = int(dicX_aft[aft_word]) + 1 + len(dicX) + len(dicX_pre)
        #print "this word's position is" ,word_position
        while index < len(thetaM):
            low_item_inner =  thetaM[index][0] + thetaM[index][word_position]  + thetaM[index][pre_position] + thetaM[index][aft_position]
            low_item = low_item + math.exp(low_item_inner)
            index = index + 1
        for k in range(len(thetaM)):
            up_item = math.exp(thetaM[k][0] + thetaM[k][word_position] +thetaM[k][pre_position] + thetaM[k][aft_position])
            #print up_item,thetaM[k][word_position],thetaM[k][0],low_item
            scalar = -(I(Y,k,i,Y_catgory) - up_item/low_item)
            #print "scalar is", scalar, "I is", I(Y,k,i,Y_catgory)
            j = 0
            while j < len(thetaM[k]):
                if j == word_position or j == 0 or j == pre_position or j == aft_position:
                    thetaM[k][j] = thetaM[k][j] - 0.5 * scalar
                j = j + 1
    #f.close()
    return thetaM

def iterate_M2(dicX,dicX_pre,dicX_aft,X,Y,thetaM,Y_catgory):
    for i in range(len(X)):
            thetaM = gradient_decent_k_M2(X,Y,dicX,dicX_pre,dicX_aft,Y_catgory,thetaM,i)            #print
    return thetaM

def negtive_likelihood_M2(X,Y,dicX,dicX_pre,dicX_aft,Y_catgory,thetaM):
    #print thetaM
    #print X
    l = 0
    for i in range(len(X)):
        if X[i] != '\n':
            for k in range(len(thetaM)):
                cur_word = X[i]
                if i == 0:
                    pre_word = 'BOS'
                    aft_word = X[i + 1]
                elif i == len(X) - 1:
                    pre_word = X[i - 1]
                    aft_word = 'EOS'
                else:
                    pre_word = X[i - 1]
                    aft_word = X[i + 1]

                if pre_word =='\n':
                    pre_word = 'BOS'
                if aft_word == '\n':
                    aft_word = 'EOS'
                index = 0
                low_item = 0
                up_item = 0
                word_position = int(dicX[cur_word]) + 1
                pre_position = int(dicX_pre[pre_word]) + 1 + len(dicX)
                aft_position = int(dicX_aft[aft_word]) + 1 + len(dicX) + len(dicX_pre)
                #print word_position,pre_position,aft_position,pre_word,cur_word,aft_word
                while index < len(thetaM):
                    low_item_inner =  thetaM[index][word_position]  + thetaM[index][0] + thetaM[index][pre_position] + thetaM[index][aft_position]
                    low_item = low_item + math.exp(low_item_inner)
                    index = index + 1
                up_item = math.exp(thetaM[k][word_position] + thetaM[k][0] + thetaM[k][pre_position] + thetaM[k][aft_position])
                #print "k is", k
                #print "up,lower are ",up_item,low_item
                l = l + I(Y,k,i,Y_catgory) * math.log(up_item/low_item)
                #print "l is",l
            #print "l I are ",l,I(Y,k,i,Y_catgory)
    X_copy = []
    for word in X:
        X_copy.append(word)
    for word in X_copy:
        if word == '\n':
            X_copy.remove('\n')
    likelihood = - l /(len(X_copy))
    return likelihood

def prediction_M2(X,dicX,dicX_pre,dicX_aft,thetaM,Y_catgory,i):
    # the ith word in the X matrix

    cur_word = X[i]
    if i == 0:
        pre_word = 'BOS'
        aft_word = X[i + 1]
    elif i == len(X) - 1:
        pre_word = X[i - 1]
        aft_word = 'EOS'
    else:
        pre_word = X[i - 1]
        aft_word = X[i + 1]
    if pre_word =='\n':
        pre_word = 'BOS'
    if aft_word == '\n':
        aft_word = 'EOS'
    word_position = int(dicX[cur_word]) + 1
    pre_position = int(dicX_pre[pre_word]) + 1 + len(dicX)
    aft_position = int(dicX_aft[aft_word]) + 1 + len(dicX) + len(dicX_pre)
    P = []
    for k in range(len(thetaM)):
        up_item = thetaM[k][0] + thetaM[k][word_position] + thetaM[k][pre_position] + thetaM[k][aft_position]
        P.append(up_item)
    #print P
    #print P.index(max(P))
    return P.index(max(P))

def output_labels_M2(dicX,dicX_pre,dicX_aft,X,thetaM,Y_catgory,test_filename,open_file_name):
    f0 = open(test_filename,'r')
    i = 0
    f1 = open(open_file_name,'wb')
    for line in f0:
        #print i,line
        if line != '\n':
            word = line.split("\t")[0]
            which_class = prediction_M2(X,dicX,dicX_pre,dicX_aft,thetaM,Y_catgory,i)
            #print 'the class is ',which_class,Y_catgory[which_class]
            f1.write(Y_catgory[which_class]+ '\n')
        else:
            f1.write('\n')
        i = i + 1
    f1.close()
    f0.close()


if __name__=="__main__":
    train_inputfile = sys.argv[1]
    validation_inputfile = sys.argv[2]
    test_inputfile  = sys.argv[3]
    train_outfile = sys.argv[4]
    test_outfile = sys.argv[5]
    maxtrice_outfile = sys.argv[6]
    num_epoch = sys.argv[7]
    feature_flag = sys.argv[8]
    if feature_flag == '1':
        dicX_vali,X_vali,Y_vali,thetaM_vali,Y_catgory_vali = create_dic_Y_thetaM(validation_inputfile)
        dicX_test,X_test,Y_test,thetaM_test,Y_catgory_test = create_dic_Y_thetaM(test_inputfile)
        dicX_tr,X_tr,Y_tr,thetaM_tr,Y_catgory_tr = create_dic_Y_thetaM(train_inputfile)
        f_out_maxtrice = open(maxtrice_outfile,'wb')
        ep = 1
        while ep <= int(num_epoch):
            thetaM_tr = iterate(dicX_tr,X_tr,Y_tr,thetaM_tr,Y_catgory_tr)
            likelihood_train = negtive_likelihood(X_tr,Y_tr,dicX_tr,Y_catgory_tr,thetaM_tr)
            likelihood_vali = negtive_likelihood(X_vali,Y_vali,dicX_tr,Y_catgory_tr,thetaM_tr)
            f_out_maxtrice.write('epoch=' + str(ep) + ' likelihood(train): ' + str(likelihood_train) + '\n')
            f_out_maxtrice.write('epoch=' + str(ep) + ' likelihood(validation): ' + str(likelihood_vali) + '\n')
            ep = ep + 1
        #thetaM = iterate(train_inputfile,int(num_epoch))
        output_labels(dicX_tr,X_tr,thetaM_tr,Y_catgory_tr,train_inputfile,train_outfile)
        errorrate_train = calculate_errorate(train_inputfile,train_outfile)
        f_out_maxtrice.write('error(train): '+ str(errorrate_train) + '\n')
        output_labels(dicX_tr,X_test,thetaM_tr,Y_catgory_tr,test_inputfile,test_outfile)
        errorrate_test = calculate_errorate(test_inputfile,test_outfile)
        f_out_maxtrice.write('error(test): '+ str(errorrate_test))
        f_out_maxtrice.close()

    elif feature_flag == '2':
        dicX_vali,dicX_pre_vali,dicX_aft_vali,X_vali,Y_vali,thetaM_vali,Y_catgory_vali =  create_dic_Y_thetaM_M2(validation_inputfile)
        dicX_t,dicX_pre_t,dicX_aft_t,X_t,Y_t,thetaM_t,Y_catgory_t =  create_dic_Y_thetaM_M2(train_inputfile)
        dicX_test,dicX_pre_test,dicX_aft_test,X_test,Y_test,thetaM_test,Y_catgory_test =  create_dic_Y_thetaM_M2(test_inputfile)
        f_out_maxtrice = open(maxtrice_outfile,'wb')
        ep = 1
        while ep <= int(num_epoch):
            thetaM_t = iterate_M2(dicX_t,dicX_pre_t,dicX_aft_t,X_t,Y_t,thetaM_t,Y_catgory_t)
            likelihood_vali = negtive_likelihood_M2(X_vali,Y_vali,dicX_t,dicX_pre_t,dicX_aft_t,Y_catgory_t,thetaM_t)
            likelihood_train = negtive_likelihood_M2(X_t,Y_t,dicX_t,dicX_pre_t,dicX_aft_t,Y_catgory_t,thetaM_t)
            f_out_maxtrice.write('epoch=' + str(ep) + ' likelihood(train): ' + str(likelihood_train) + '\n')
            f_out_maxtrice.write('epoch=' + str(ep) + ' likelihood(validation): ' + str(likelihood_vali) + '\n')
            ep = ep + 1

        #thetaM = iterate_M2(train_inputfile,int(num_epoch))
        output_labels_M2(dicX_t,dicX_pre_t,dicX_aft_t,X_t,thetaM_t,Y_catgory_t,train_inputfile,train_outfile)
        errorrate_train = calculate_errorate(train_inputfile,train_outfile)
        f_out_maxtrice.write('error(train): '+ str(errorrate_train) + '\n')
        output_labels_M2(dicX_t,dicX_pre_t,dicX_aft_t,X_test,thetaM_t,Y_catgory_t,test_inputfile,test_outfile)
        errorrate_test = calculate_errorate(test_inputfile,test_outfile)
        f_out_maxtrice.write('error(test): '+ str(errorrate_test))
        f_out_maxtrice.close()
        #print "x"
