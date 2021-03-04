import random
from collections import defaultdict
import math
import copy
import pandas as pd

with open("DatasetS.txt", "r") as f1:
    positive = f1.read().splitlines()

with open("not_afp560147.txt", "r") as f2:
    negative = f2.read().splitlines()

random.seed(0)
negative2 = random.sample(negative, len(negative))
negative3 = negative2[0:len(positive)]
negative3.extend(positive)
array = negative3

amino = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
dipeptide = ['AA', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AK', 'AL', 'AM', 'AN', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AV', 'AW', 'AY', 'CA', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CV', 'CW', 'CY', 'DA', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DK', 'DL', 'DM', 'DN', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DV', 'DW', 'DY', 'EA', 'EC', 'ED', 'EE', 'EF', 'EG', 'EH', 'EI', 'EK', 'EL', 'EM', 'EN', 'EP', 'EQ', 'ER', 'ES', 'ET', 'EV', 'EW', 'EY', 'FA', 'FC', 'FD', 'FE', 'FF', 'FG', 'FH', 'FI', 'FK', 'FL', 'FM', 'FN', 'FP', 'FQ', 'FR', 'FS', 'FT', 'FV', 'FW', 'FY', 'GA', 'GC', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GK', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GV', 'GW', 'GY', 'HA', 'HC', 'HD', 'HE', 'HF', 'HG', 'HH', 'HI', 'HK', 'HL', 'HM', 'HN', 'HP', 'HQ', 'HR', 'HS', 'HT', 'HV', 'HW', 'HY', 'IA', 'IC', 'ID', 'IE', 'IF', 'IG', 'IH', 'II', 'IK', 'IL', 'IM', 'IN', 'IP', 'IQ', 'IR', 'IS', 'IT', 'IV', 'IW', 'IY', 'KA', 'KC', 'KD', 'KE', 'KF', 'KG', 'KH', 'KI', 'KK', 'KL', 'KM', 'KN', 'KP', 'KQ', 'KR', 'KS', 'KT', 'KV', 'KW', 'KY', 'LA', 'LC', 'LD', 'LE', 'LF', 'LG', 'LH', 'LI', 'LK', 'LL', 'LM', 'LN', 'LP', 'LQ', 'LR', 'LS', 'LT', 'LV', 'LW', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MI', 'MK', 'ML', 'MM', 'MN', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MV', 'MW', 'MY', 'NA', 'NC', 'ND', 'NE', 'NF', 'NG', 'NH', 'NI', 'NK', 'NL', 'NM', 'NN', 'NP', 'NQ', 'NR', 'NS', 'NT', 'NV', 'NW', 'NY', 'PA', 'PC', 'PD', 'PE', 'PF', 'PG', 'PH', 'PI', 'PK', 'PL', 'PM', 'PN', 'PP', 'PQ', 'PR', 'PS', 'PT', 'PV', 'PW', 'PY', 'QA', 'QC', 'QD', 'QE', 'QF', 'QG', 'QH', 'QI', 'QK', 'QL', 'QM', 'QN', 'QP', 'QQ', 'QR', 'QS', 'QT', 'QV', 'QW', 'QY', 'RA', 'RC', 'RD', 'RE', 'RF', 'RG', 'RH', 'RI', 'RK', 'RL', 'RM', 'RN', 'RP', 'RQ', 'RR', 'RS', 'RT', 'RV', 'RW', 'RY', 'SA', 'SC', 'SD', 'SE', 'SF', 'SG', 'SH', 'SI', 'SK', 'SL', 'SM', 'SN', 'SP', 'SQ', 'SR', 'SS', 'ST', 'SV', 'SW', 'SY', 'TA', 'TC', 'TD', 'TE', 'TF', 'TG', 'TH', 'TI', 'TK', 'TL', 'TM', 'TN', 'TP', 'TQ', 'TR', 'TS', 'TT', 'TV', 'TW', 'TY', 'VA', 'VC', 'VD', 'VE', 'VF', 'VG', 'VH', 'VI', 'VK', 'VL', 'VM', 'VN', 'VP', 'VQ', 'VR', 'VS', 'VT', 'VV', 'VW', 'VY', 'WA', 'WC', 'WD', 'WE', 'WF', 'WG', 'WH', 'WI', 'WK', 'WL', 'WM', 'WN', 'WP', 'WQ', 'WR', 'WS', 'WT', 'WV', 'WW', 'WY', 'YA', 'YC', 'YD', 'YE', 'YF', 'YG', 'YH', 'YI', 'YK', 'YL', 'YM', 'YN', 'YP', 'YQ', 'YR', 'YS', 'YT', 'YV', 'YW', 'YY']

vector = [[] for i in range(len(array))]

for j,k in enumerate(array):
    for l in amino:
        x = k.count(l)/len(k)
        vector[j].append(x)

for m,n in enumerate(array):
    for o in dipeptide:
        y = n.count(o)/len(n)
        vector[m].append(y)

for p,q in enumerate(array):
    for r in dipeptide:
        count=0
        for s in range(len(q)-2):
            if q[s]==r[0] and q[s+2]==r[1]:
                count+=1
        vector[p].append(count/len(q))

_DisorderPropensity = {'1':'ARSQEGKP','2':'ILNCFYVW', '3':'DHMT'}
_Hydrophobicity = {'1':'RKEDQN','2':'GASTPHY','3':'CLVIMFW'}
_Polarity = {'1':'LIFWCMVY','2':'PATGS','3':'HQRKNED'}
_Polarizability = {'1':'GASDT','2':'CPNVEQIL','3':'KMHFRYW'}
_Charge = {'1':'KR','2':'ANCQGHILMFPSTWYV','3':'DE'}
_SecondaryStr = {'1':'EALMQKRH','2':'VIYCWFT','3':'GNPSD'} #Orig
_NormalizedVDWV = {'1':'GASTPDC','2':'NVEQIL','3':'MHKFRYW'}
_SolventAccessibility = {'1':'ALFCGIVW','2':'RKQEND','3':'MPSTHY'}


AAG_Properties=[_Hydrophobicity, _NormalizedVDWV, _Polarity, _Charge,_SecondaryStr, _SolventAccessibility, _Polarizability, _DisorderPropensity]

AAG_Names=['Hydrophobicity', 'Normalized VDWV', 'Polarity','Charge', 'Secondary Str', 'Solvent Accessibility', 'Polarizability', 'Disorder Propensity']


def StringtoNum(ProteinSequence,AAProperty):

    hardProteinSequence=copy.deepcopy(ProteinSequence)
    for k,m in AAProperty.items():
      # print ("AAProperty: %s" %(AAProperty))
      # print ("AAProperty.items(): %s" %(AAProperty.items()))
      # print ("k,m = %s,%s, in AAProperty.items() " % (k,m))
      for index in m:
          # print ("index in m: %s" %(index))
          hardProteinSequence=str.replace(hardProteinSequence,index,k)

    return hardProteinSequence


def CalculateCTD(ProteinSequence,ctd_call='CTD'):

    result=defaultdict(float)

    get_C = True
    get_T = True
    get_D = True
    ctd_call = ctd_call.lower()
    if 'c' not in ctd_call:
        get_C=False
    if 't' not in ctd_call:
        get_T=False
    if 'd' not in ctd_call:
        get_D=False

    for i in range(len(AAG_Names)):
        AAProperty=AAG_Properties[i]
        AAPName = AAG_Names[i]
        if get_C:
            result.update(CalculateComposition(ProteinSequence, AAProperty, AAPName))
        if get_T:
            result.update(CalculateTransition(ProteinSequence, AAProperty, AAPName))
        if get_D:
            result.update(CalculateDistribution(ProteinSequence, AAProperty, AAPName))

    return result


def CalculateComposition(ProteinSequence,AAProperty,AAPName):

    TProteinSequence=StringtoNum(ProteinSequence,AAProperty)
    Result={}
    Num=len(TProteinSequence)
    Result[AAPName +' Composition:'+'1']=round(float(TProteinSequence.count('1'))/Num,3)
    Result[AAPName +' Composition:'+'2']=round(float(TProteinSequence.count('2'))/Num,3)
    Result[AAPName +' Composition:'+'3']=round(float(TProteinSequence.count('3'))/Num,3)
    return Result

def CalculateTransition(ProteinSequence,AAProperty,AAPName):

    TProteinSequence=StringtoNum(ProteinSequence,AAProperty)
    # Result={}
    Result=defaultdict(float)
    Num=len(TProteinSequence)
    CTD=TProteinSequence
    Result[AAPName +' Transitions:'+'12']=round(float(CTD.count('12')+CTD.count('21'))/(Num-1),3)
    Result[AAPName +' Transitions:'+'13']=round(float(CTD.count('13')+CTD.count('31'))/(Num-1),3)
    Result[AAPName +' Transitions:'+'23']=round(float(CTD.count('23')+CTD.count('32'))/(Num-1),3)

    return Result


def CalculateDistribution(ProteinSequence,AAProperty,AAPName):

    TProteinSequence=StringtoNum(ProteinSequence,AAProperty)
    # Result={}
    Result=defaultdict(float)
    Num=len(TProteinSequence)
    temp=('1','2','3')
    for i in temp:
        num=TProteinSequence.count(i)
        ink=1
        indexk=0
        cds=[]
        while ink<=num:
            indexk=str.find(TProteinSequence,i,indexk)+1
            cds.append(indexk)
            ink=ink+1

        if cds==[]:
            Result[AAPName +' Distribution'+i+'001']=0
            Result[AAPName +' Distribution'+i+'025']=0
            Result[AAPName +' Distribution'+i+'050']=0
            Result[AAPName +' Distribution'+i+'075']=0
            Result[AAPName +' Distribution'+i+'100']=0
        else:

            Result[AAPName +' Distribution'+i+'001']=round(float(cds[0])/Num*100,3)
            Result[AAPName +' Distribution'+i+'025']=round(float(cds[int(math.floor(num*0.25))-1])/Num*100,3)
            Result[AAPName +' Distribution'+i+'050']=round(float(cds[int(math.floor(num*0.5))-1])/Num*100,3)
            Result[AAPName +' Distribution'+i+'075']=round(float(cds[int(math.floor(num*0.75))-1])/Num*100,3)
            Result[AAPName +' Distribution'+i+'100']=round(float(cds[-1])/Num*100,3)

    return Result


def CalculateCompositionHydrophobicity(ProteinSequence):
    result=CalculateComposition(ProteinSequence,_Hydrophobicity,'_Hydrophobicity')
    return result


def CalculateCompositionNormalizedVDWV(ProteinSequence):
    result=CalculateComposition(ProteinSequence,_NormalizedVDWV,'_NormalizedVDWV')
    return result


def CalculateCompositionPolarity(ProteinSequence):
    result=CalculateComposition(ProteinSequence,_Polarity,'_Polarity')
    return result


def CalculateCompositionCharge(ProteinSequence):
    result=CalculateComposition(ProteinSequence,_Charge,'_Charge')
    return result


def CalculateCompositionSecondaryStr(ProteinSequence):
    result=CalculateComposition(ProteinSequence,_SecondaryStr,'_SecondaryStr')
    return result


def CalculateCompositionSolventAccessibility(ProteinSequence):
    result=CalculateComposition(ProteinSequence,_SolventAccessibility,'_SolventAccessibility')
    return result


def CalculateCompositionPolarizability(ProteinSequence):
    result=CalculateComposition(ProteinSequence,_Polarizability,'_Polarizability')
    return result


def CalculateTransitionHydrophobicity(ProteinSequence):
    result=CalculateTransition(ProteinSequence,_Hydrophobicity,'_Hydrophobicity')
    return result


def CalculateTransitionNormalizedVDWV(ProteinSequence):
    result=CalculateTransition(ProteinSequence,_NormalizedVDWV,'_NormalizedVDWV')
    return result


def CalculateTransitionPolarity(ProteinSequence):
    result=CalculateTransition(ProteinSequence,_Polarity,'_Polarity')
    return result


def CalculateTransitionCharge(ProteinSequence):
    result=CalculateTransition(ProteinSequence,_Charge,'_Charge')
    return result


def CalculateTransitionSecondaryStr(ProteinSequence):
    result=CalculateTransition(ProteinSequence,_SecondaryStr,'_SecondaryStr')
    return result


def CalculateTransitionSolventAccessibility(ProteinSequence):
    result=CalculateTransition(ProteinSequence,_SolventAccessibility,'_SolventAccessibility')
    return result


def CalculateTransitionPolarizability(ProteinSequence):
    result=CalculateTransition(ProteinSequence,_Polarizability,'_Polarizability')
    return result


def CalculateDistributionHydrophobicity(ProteinSequence):
    result=CalculateDistribution(ProteinSequence,_Hydrophobicity,'_Hydrophobicity')
    return result


def CalculateDistributionNormalizedVDWV(ProteinSequence):
    result=CalculateDistribution(ProteinSequence,_NormalizedVDWV,'_NormalizedVDWV')
    return result


def CalculateDistributionPolarity(ProteinSequence):
    result=CalculateDistribution(ProteinSequence,_Polarity,'_Polarity')
    return result


def CalculateDistributionCharge(ProteinSequence):
    result=CalculateDistribution(ProteinSequence,_Charge,'_Charge')
    return result


def CalculateDistributionSecondaryStr(ProteinSequence):
    result=CalculateDistribution(ProteinSequence,_SecondaryStr,'_SecondaryStr')
    return result


def CalculateDistributionSolventAccessibility(ProteinSequence):
    result=CalculateDistribution(ProteinSequence,_SolventAccessibility,'_SolventAccessibility')
    return result


def CalculateDistributionPolarizability(ProteinSequence):
    result=CalculateDistribution(ProteinSequence,_Polarizability,'_Polarizability')
    return result



def CalculateC(ProteinSequence):

    result={}
    for i in range(len(AAG_Names)):
        AAProperty=AAG_Properties[i]
        AAPName = AAG_Names[i]
        result.update(CalculateComposition(ProteinSequence, AAProperty, AAPName))

    return result



def CalculateT(ProteinSequence):

    result={}
    for i in range(len(AAG_Names)):
        AAProperty=AAG_Properties[i]
        AAPName = AAG_Names[i]
        result.update(CalculateTransition(ProteinSequence, AAProperty, AAPName))

    return result



def CalculateD(ProteinSequence):

    result={}
    for i in range(len(AAG_Names)):
        AAProperty=AAG_Properties[i]
        AAPName = AAG_Names[i]
        result.update(CalculateDistribution(ProteinSequence, AAProperty, AAPName))

    return result


vector_CTD=[]
for protein in array:
    vector_CTD.append(list(CalculateCTD(protein).values()))

for i in range(len(vector)):
    vector[i].extend(vector_CTD[i])

class_vector = []
for i in range(len(array)//2):
    class_vector.append([0])
for j in range(len(array)//2):
    class_vector.append([1])

for k in range(len(array)):
    class_vector[k].extend(vector[k])

title = ['class']
for i in range(len(vector[0])):
    title.append('f'+str(i+1))

df = pd.DataFrame(class_vector, columns=title)
df.to_csv('all_OS.csv', index=False)