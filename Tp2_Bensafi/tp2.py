# -*- coding: utf-8 -*-
"""TP2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OfWg2w0jJS3HQLopHkpncYohG6rbrltB

#                                                 Approches Neuronales – TP 2
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import re
import numpy as np
import random
import math
from scipy import linalg

"""En premier j'ai lu 49 données MINES pour train, puis j'ai lu 55 données Rocks puis j'au fussionner les deux et j'ai, créé les fichiers contennant les étiquettes M (49) ou R (55) selon la source de la donnée.

**Partie 0 : Lecture et normalisation des données**
"""

#Lecture des sonar.mines TRAIN #pour le test le test line[0]== 'C'

#Fonction pour mettre un des valeurs sur la même ligne
def grouper(n, A):
    it = iter(A)
    while True:
       nom = tuple(itertools.islice(it, n))
       if not nom:
           return
       yield nom

##lecture les données
Train=[]
Test=[]
i=0

'''
#Train
with open("/content/drive/MyDrive/M2Avignon/ApprocheNeuronales/Donnees/sonar.mines") as file:
    lines = file.readlines()
   
for line in lines:
    
    
    if line[0] == '*':
      for k in range(1,11):
       
           
          
          l = lines[i+k].split()
          if len(l) == 6:
           Train.extend(l)
           Train = [s.replace("}", "") for s in Train]
           Train = [s.replace("{", "") for s in Train]
          
    i=i+1

with open("/content/drive/MyDrive/M2Avignon/ApprocheNeuronales/Donnees/Train_MINES.txt", "w") as f:
  for chunk in grouper(60, Train):
    f.write(" ".join(str(x) for x in chunk) + "\n")
'''

#Test
#62 données pour mines test
with open("/content/drive/MyDrive/M2Avignon/ApprocheNeuronales/Donnees/sonar.mines") as file:
    lines = file.readlines()
   
for line in lines:
    
    
    if line[0] == 'C':
      for k in range(1,11):
       
           
          
          l = lines[i+k].split()
          if len(l) == 6:
           Test.extend(l)
           Test = [s.replace("}", "") for s in Test]
           Test = [s.replace("{", "") for s in Test]
          
    i=i+1

with open("/content/drive/MyDrive/M2Avignon/ApprocheNeuronales/Donnees/Test_MINES.txt", "w") as f:
  for chunk in grouper(60, Test):
    f.write(" ".join(str(x) for x in chunk) + "\n")

#Lecture des Train SONAR Rocks 
#pour le test le test line[0]== 'C'
#55 données pour rocks test
#42 données pour rocks test

def grouper(n, A):
    it = iter(A)
    while True:
       nom = tuple(itertools.islice(it, n))
       if not nom:
           return
       yield nom
Train=[]
Test=[]

'''
#Train
with open("/content/drive/MyDrive/M2Avignon/ApprocheNeuronales/Donnees/sonar.rocks") as file:
    lines = file.readlines()

i=0
k=0   
for line in lines:
    if line[0] == '*':
      for k in range(1,11):
          l = lines[i+k].split()
          if len(l) == 6:
           Train.extend(l)
           Train = [s.replace("}", "") for s in Train]
           Train = [s.replace("{", "") for s in Train]
          
    i=i+1

with open("/content/drive/MyDrive/M2Avignon/ApprocheNeuronales/Donnees/TrainRocks.txt", "w") as f:

 for chunk in grouper(60, Train):
    f.write(" ".join(str(x) for x in chunk) + "\n")
'''

#Test
with open("/content/drive/MyDrive/M2Avignon/ApprocheNeuronales/Donnees/sonar.rocks") as file:
    lines = file.readlines()

i=0
k=0   
for line in lines:
    if line[0] == 'C':
      for k in range(1,11):
          l = lines[i+k].split()
          if len(l) == 6:
           Train.extend(l)
           Train = [s.replace("}", "") for s in Train]
           Train = [s.replace("{", "") for s in Train]
          
    i=i+1

with open("/content/drive/MyDrive/M2Avignon/ApprocheNeuronales/Donnees/TestRocks.txt", "w") as f:

 for chunk in grouper(60, Train):
    f.write(" ".join(str(x) for x in chunk) + "\n")

"""# **Partie 1**"""

#Loader les données
#comme dans le TP précédant j'avais établie deux classes -1 et 1 mes deux classes seront alors 1=M et -1=R
TrainEtiq = np.genfromtxt('/content/drive/MyDrive/M2Avignon/ApprocheNeuronales/Donnees/etiqTrain.txt',dtype='str')
TrainData = np.loadtxt("/content/drive/MyDrive/M2Avignon/ApprocheNeuronales/Donnees/train.txt")


TestData = np.loadtxt("/content/drive/MyDrive/M2Avignon/ApprocheNeuronales/Donnees/test.txt")
TestEtiq = np.loadtxt("/content/drive/MyDrive/M2Avignon/ApprocheNeuronales/Donnees/etiq_test.txt")

#Les transformer en float
TrainEtiq = TrainEtiq.astype(np.int)
print(TrainEtiq)
print(TrainData)

"""# J'ai choisie la version Online
 Car le coût de calcul est plus faible en utilisant ONLINE puisque le nombre des itérations est toujours inférieure à ceux de la version BATCH
"""

#version online
def classeCorrectementVecteur(vect1,vect2):
  if np.array_equal(vect1,vect2):
    
      return True 
  return False


def versionOnline(W,alph,X,etiq):
  pred=np.ones(len(X))
  
  IT=0
  while not classeCorrectementVecteur(etiq, pred):
    i=random.randint(0, len(X) - 1)#car les vecteurs commence de 0 à n-1
    x_ = np.append(1, X[i])
    IT+=1
    Dw=0
    if np.transpose(W).dot(x_)> 0 :
       pred[i]=1
    else:
       pred[i]=-1
    if pred[i] != etiq[i] :
      Dw = x_.dot(alph*(etiq[i]-pred[i]))
    W=W+Dw
      
  print(IT)
  return W,pred

#Fonction pour  génerer le vecteur W 
def genererW(P, N):
    #si je n'effectue pas la normalisation mes algo ne s'arrete quasiment pas car beaucoup de valeurs après la virgule
    W = np.random.randint(-100,100,N+1)/100
    return   W

#pour tester l'apprentissage ce qui nous donne
def TrouverEtiquette(W,x):
  ones = np.ones((len(x),1))
  x_ = np.append(ones,x,axis=1)
  pred=np.ones(len(x_))
  res =x_.dot(W)
  #J'utilise np.sign ou lieu de faire une comparaison une par une
  etiq = np.sign(res)
  
  return  etiq

'''L'erreur de généralisation = l'erreur sur de nouvelles données
   comme par exemple : (Ea=10,8,6 fautes) alors on doit calculer combier y'a t'il de fautes.
'''
def Error(Etiq , predicted):

  return (Etiq != predicted).sum()

def generalisation(NBtot,NbErr) :
    NbBienClasse=NBtot-NbErr
    return NbBienClasse/NBtot

N = 60 #les colonnes
P = 104 #les lignes
alph = 0.01   
W_=genererW(P, N)


#1). Apprentissage  sur  « train »
W1 ,pred1 = versionOnline(W_,alph,TrainData,TrainEtiq)

print(W1)

#a.1) Ici nous allons trouver les etiquettes avec les Data d'apprentissage SUR lesquels il a appris
EtiquettePrediteTrain = TrouverEtiquette(W1,TrainData)
Ea = Error(TrainEtiq,EtiquettePrediteTrain)
print("Erreur d'apprentissage",Ea)

'''
Exemple :
Erreur d'apprentissage 2
'''

#a.2)
#Trouver etiquette avec les données de Test qui ne connais pas TESTER avec TEST
testPrediction=TrouverEtiquette(W1,TestData)

#Voir les deux
'''
print(TestEtiq)
print(testPrediction)'''

#Compter les erreurs gen
NbErr = Error(TestEtiq,testPrediction)
print(NbErr)
Eg=generalisation(P,NbErr)
print("Erreur de généralisation",Eg)

#b)afficher N+1 Weights
print("N+1 weights")
print(W1)

"""Stabilité

sachant Une grande stabilité positive assure une certaine robustesse de la réponse du neurone.(reference cours: APPRENTISSAGE ET GENERALISATION...)


![Capture.PNG](data:image/png;base64,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)
"""

#c)
def Stabilite(etiq,W,X):
    X = np.append(np.ones((len(X),1)),X,axis=1)
    enum=etiq*np.dot(X,W)
    return enum/linalg.norm(W)

#Calculer stabilité
j=Stabilite(TestEtiq,W1,TestData)
print("Stabilité")
print(j)

#d)
def plotstab(s):
    plt.hist(s, range=(-0.5, 0.5), bins=10, facecolor='red', alpha=0.5,edgecolor='blue')
    plt.show()
print("Plot de Stabilité")
plotstab(j)

#pour tester une autre figure
x = np.array(range(0, 104))
plt.title("stabilité")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.plot(x, j, color = "red", marker = "o", label = "valeur de stabilité")
plt.legend()
plt.show()

#2. Apprentissage sur « test »
W_test=genererW(P, N)
W2,pred2 = versionOnline(W_test,alph,TestData,TestEtiq)

#a.1)
#Ici nous allons trouver les etiquettes avec les Data TEST SUR lesquels il a appris
EtiquettePrediteTest = TrouverEtiquette(W2,TestData)
Ea_test = Error(TestEtiq,EtiquettePrediteTest)
print("Erreur d'apprentissage",Ea_test)



#Trouver etiquette avec les données de Train qui ne connais pas TESTER avec Train
trainPrediction_=TrouverEtiquette(W2,TrainData)


#a.2)
#Compter les erreurs generalz
NbErr=Error(TrainEtiq,trainPrediction_)
print(NbErr)
Eg=generalisation(P,NbErr)
print("Erreur de généralisation",Eg)




#b)Afficher W
print("N+1 weights")
print(W2)

#c) Calculer stabilité
j=Stabilite(TrainEtiq,W1,TrainData)
print("Stabilité",j)

#d)
def plotstab(s):
    plt.hist(s, range=(-0.5, 0.5), bins=10, facecolor='red', alpha=0.5,edgecolor='blue')
    plt.show()
print("Plot de Stabilité")
plotstab(j)

"""# **Partie 2 : Pocket**
1.   Notre nouvel algorithme Pocket depends de 2 parametre le nombre d'itérations et le nombre d'erreurs.
2.   Il garde le meilleur résultat de l’algorithme du perceptron en fonctions des itérations Nb d’erreurs prédéfini.
"""

#Algo pocket
def AlgorithmePocket(X, etiq, alph, N_it, N_Er,W):
  
  pred=np.ones(len(etiq))#mon tableau d'étiquettes que je vais prédir
  X = np.append(np.ones((len(X),1)),X,axis=1)
  Dw=0

  for i in range(N_it):
      res = X.dot(W)
      pred=np.sign(res)
      
      
      if  not classeCorrectementVecteur(etiq, pred) :
        Dw = np.transpose(X).dot(alph*(etiq-pred))
        W=W+Dw

      N_Er_Occured = Error(etiq,pred)

      if N_Er_Occured <= N_Er :
        break;

  
  return W

#Fonction pour RAMDON INITIALISATION et Hebb
def initialisation(X,N,etiq):
    #Random
    W_RA = np.random.randint(-100,100,N+1)/100
    
    
    #HEBB
    
    #Step 1 mettre en place les weights
    W_hebb = np.zeros((N+1))
    
    #Step 2  mettre en place input X
    X = np.append(np.ones((len(X),1)),X,axis=1)

    #Step 3  mettre en place pred
    pred=etiq

    for i in range(len(X)):
     
      #Step 4 w(nouveau) = w(vieux) + xi*yi  
      W_hebb=W_hebb+(X[i]*pred[i])

    
    W_hebb=W_hebb/100
      

    return W_RA,W_hebb

"""#APPRENTISSAGE TRAIN et Test avec 
- Alpha = 0.7 , 0.4 , 0.01
- Erreurlimit = 3, 6 , 8 , 10
- Et selon les deux initialisation
- nombre iteration = 8000
"""

####################################################### APPRENTISSAGE TRAIN ######################################################################

#Run Pocket with 2 initialisation    
W_RA,W_hebb = initialisation(TrainData,N,TrainEtiq)


####################################
print("alph=0.7 Ea_=3")
alph=0.7
Ea_=3

print("random")
#Initialisation Random
W_pocketRandom = AlgorithmePocket(TrainData, TrainEtiq, alph, 8000, Ea_, W_RA)

#-------------------------------------------------------------
EtiquettePredite_1 = TrouverEtiquette(W_pocketRandom,TrainData)
Ea_1 = Error(TrainEtiq,EtiquettePredite_1)
print("Erreur d'apprentissage",Ea_1)
#---
EtiquettePredite_2=TrouverEtiquette(W_pocketRandom,TestData)
Eg_1 = Error(TestEtiq,EtiquettePredite_2)
print("Erreur de généralisation",Eg_1)

#-------------------------------------------------------------


print("hebb")
#Initialisation Hebb
W_pocketHEBB = AlgorithmePocket(TrainData, TrainEtiq, alph, 8000, Ea_, W_hebb)

#-------------------------------------------------------------
EtiquettePredite_3 = TrouverEtiquette(W_pocketHEBB,TrainData)
Ea_2 = Error(TrainEtiq,EtiquettePredite_3)
print("Erreur d'apprentissage",Ea_2)
#---
EtiquettePredite_4=TrouverEtiquette(W_pocketHEBB,TestData)
Eg_2 = Error(TestEtiq,EtiquettePredite_4)
print("Erreur de généralisation",Eg_2)
#-------------------------------------------------------------



####################################
print("alph=0.4 Ea_=3")

alph=0.4
Ea_=3

print("random")
#Initialisation Random
W_pocketRandom = AlgorithmePocket(TrainData, TrainEtiq, alph, 8000, Ea_, W_RA)

#-------------------------------------------------------------
EtiquettePredite_9 = TrouverEtiquette(W_pocketRandom,TrainData)
Ea_5 = Error(TrainEtiq,EtiquettePredite_9 )
print("Erreur d'apprentissage",Ea_5)
#---
EtiquettePredite_10=TrouverEtiquette(W_pocketRandom,TestData)
Eg_5 = Error(TestEtiq,EtiquettePredite_10)
print("Erreur de généralisation",Eg_5)
#-------------------------------------------------------------

print("hebb")
#Initialisation Hebb
W_pocketHEBB = AlgorithmePocket(TrainData, TrainEtiq, alph, 8000, Ea_, W_hebb)

#-------------------------------------------------------------
EtiquettePredite_11 = TrouverEtiquette(W_pocketHEBB,TrainData)
Ea_6 = Error(TrainEtiq,EtiquettePredite_11)
print("Erreur d'apprentissage",Ea_6)
#---
EtiquettePredite_12=TrouverEtiquette(W_pocketHEBB,TestData)
Eg_6 = Error(TestEtiq,EtiquettePredite_12)
print("Erreur de généralisation",Eg_6)
#-------------------------------------------------------------


####################################
print("alph=0.01 Ea_=3")

alph=0.01
Ea_=3

print("random")
#Initialisation Random
W_pocketRandom = AlgorithmePocket(TrainData, TrainEtiq, alph, 8000, Ea_, W_RA)

#-------------------------------------------------------------
EtiquettePredite_5 = TrouverEtiquette(W_pocketRandom,TrainData)
Ea_3 = Error(TrainEtiq,EtiquettePredite_5 )
print("Erreur d'apprentissage",Ea_3)
#---
EtiquettePredite_6=TrouverEtiquette(W_pocketRandom,TestData)
Eg_3 = Error(TestEtiq,EtiquettePredite_6)
print("Erreur de généralisation",Eg_3)
#-------------------------------------------------------------

print("hebb")
#Initialisation Hebb
W_pocketHEBB = AlgorithmePocket(TrainData, TrainEtiq, alph, 8000, Ea_, W_hebb)

#-------------------------------------------------------------
EtiquettePredite_7 = TrouverEtiquette(W_pocketHEBB,TrainData)
Ea_4 = Error(TrainEtiq,EtiquettePredite_7)
print("Erreur d'apprentissage",Ea_4)
#---
EtiquettePredite_8=TrouverEtiquette(W_pocketHEBB,TestData)
Eg_4 = Error(TestEtiq,EtiquettePredite_8)
print("Erreur de généralisation",Eg_4)
#-------------------------------------------------------------

####################################################### APPRENTISSAGE sur TEST  ######################################################################

#Run Pocket with 2 initialisation    
W_RA,W_hebb = initialisation(TestData,N,TestEtiq)


####################################
print("alph=0.7 Ea_=3")
alph=0.7
Ea_=3

print("random")
#Initialisation Random
W_pocketRandom = AlgorithmePocket(TestData, TestEtiq, alph, 8000, Ea_, W_RA)

#-------------------------------------------------------------
EtiquettePredite_1 = TrouverEtiquette(W_pocketRandom,TestData)
Ea_1 = Error(TestEtiq,EtiquettePredite_1)
print("Erreur d'apprentissage",Ea_1)
#---
EtiquettePredite_2=TrouverEtiquette(W_pocketRandom,TrainData)
Eg_1 = Error(TrainEtiq,EtiquettePredite_2)
print("Erreur de généralisation",Eg_1)
#-------------------------------------------------------------


print("hebb")
#Initialisation Hebb
W_pocketHEBB = AlgorithmePocket(TestData, TestEtiq, alph, 8000, Ea_, W_hebb)

#-------------------------------------------------------------
EtiquettePredite_3 = TrouverEtiquette(W_pocketHEBB,TestData)
Ea_2 = Error(TestEtiq,EtiquettePredite_3)
print("Erreur d'apprentissage",Ea_2)
#---
EtiquettePredite_4=TrouverEtiquette(W_pocketHEBB,TrainData)
Eg_2 = Error(TrainEtiq,EtiquettePredite_4)
print("Erreur de généralisation",Eg_2)
#-------------------------------------------------------------



####################################
print("alph=0.4 Ea_=3")

alph=0.4
Ea_=3

print("random")
#Initialisation Random
W_pocketRandom = AlgorithmePocket(TestData, TestEtiq, alph, 8000, Ea_, W_RA)

#-------------------------------------------------------------
EtiquettePredite_9 = TrouverEtiquette(W_pocketRandom,TestData)
Ea_5 = Error(TestEtiq,EtiquettePredite_9 )
print("Erreur d'apprentissage",Ea_5)
#---
EtiquettePredite_10=TrouverEtiquette(W_pocketRandom,TrainData)
Eg_5 = Error(TrainEtiq,EtiquettePredite_10)
print("Erreur de généralisation",Eg_5)
#-------------------------------------------------------------

print("hebb")
#Initialisation Hebb
W_pocketHEBB = AlgorithmePocket(TestData, TestEtiq, alph, 8000, Ea_, W_hebb)

#-------------------------------------------------------------
EtiquettePredite_11 = TrouverEtiquette(W_pocketHEBB,TestData)
Ea_6 = Error(TestEtiq,EtiquettePredite_11)
print("Erreur d'apprentissage",Ea_6)
#---
EtiquettePredite_12=TrouverEtiquette(W_pocketHEBB,TrainData)
Eg_6 = Error(TrainEtiq,EtiquettePredite_12)
print("Erreur de généralisation",Eg_6)
#-------------------------------------------------------------


####################################
print("alph=0.01 Ea_=3")

alph=0.01
Ea_=3

print("random")
#Initialisation Random
W_pocketRandom = AlgorithmePocket(TestData, TestEtiq, alph, 8000, Ea_, W_RA)

#-------------------------------------------------------------
EtiquettePredite_5 = TrouverEtiquette(W_pocketRandom,TestData)
Ea_3 = Error(TestEtiq,EtiquettePredite_5 )
print("Erreur d'apprentissage",Ea_3)
#---
EtiquettePredite_6=TrouverEtiquette(W_pocketRandom,TrainData)
Eg_3 = Error(TrainEtiq,EtiquettePredite_6)
print("Erreur de généralisation",Eg_3)
#-------------------------------------------------------------

print("hebb")
#Initialisation Hebb
W_pocketHEBB = AlgorithmePocket(TestData, TestEtiq, alph, 8000, Ea_, W_hebb)

#-------------------------------------------------------------
EtiquettePredite_7 = TrouverEtiquette(W_pocketHEBB,TestData)
Ea_4 = Error(TestEtiq,EtiquettePredite_7)
print("Erreur d'apprentissage",Ea_4)
#---
EtiquettePredite_8=TrouverEtiquette(W_pocketHEBB,TrainData)
Eg_4 = Error(TrainEtiq,EtiquettePredite_8)
print("Erreur de généralisation",Eg_4)
#-------------------------------------------------------------

"""# Partie 3

Apprentissage  sur « train + test ».  Utiliser l’algorithme du perceptron pour  apprendre l’ensemble fusionné L = train + test (avec les classes tau)
L’ensemble L est LS ou pas LS ? Justifier votre réponse en fonction des calculs de vos programmes
"""

TrainTestData = np.loadtxt("/content/drive/MyDrive/M2Avignon/ApprocheNeuronales/Donnees/train_test.txt")
TrainTestTestEtiq = np.loadtxt("/content/drive/MyDrive/M2Avignon/ApprocheNeuronales/Donnees/train_test_Etiq.txt")

#2. Apprentissage Version Online et Pocket
P_All=208
alph=0.1

W_TrainTest=genererW(P_All, N)

w_all,predAll=versionOnline(W_TrainTest,alph,TrainTestData,TrainTestTestEtiq)


#c'est à dire on ne tolère aucune erreur pour qu'il soit linéairement séparable
W_pocketAllData = AlgorithmePocket(TrainTestData, TrainTestTestEtiq, alph, 8000, 0, W_TrainTest)

print(predAll)


print(w_all)


print(W_pocketAllData)

#Calculer stabilité
S=Stabilite( TrainTestTestEtiq,w_all,TrainTestData)
print("Stabilité",S)

def plotstab(s):
    plt.hist(s, range=(-0.5, 0.5), bins=10, facecolor='red', alpha=0.5,edgecolor='blue')
    plt.show()
print("Plot de Stabilité")
plotstab(S)

"""sources :

https://www.geeksforgeeks.org/hebbian-learning-rule-with-implementation-of-and-gate/


http://webcache.googleusercontent.com/search?q=cache:vu5HrFkOBGcJ:www.info2.uqam.ca/~boukadoum_m/DIC9310/Notes/4-5-DIC9310%2520RNA.doc+&cd=3&hl=fr&ct=clnk&gl=fr


https://tel.archives-ouvertes.fr/tel-00390069/file/these_torres_presentation.pdf


"""