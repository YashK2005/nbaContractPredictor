import numpy as np
from database_setup import data_by_name
from data_visualizer import individual_input_output

''' w and b (using regulary salary, with normalized inputs (100,000 iterations))
[ 2935004.1726221   3260051.45000291  3894326.5545876  -5048306.39625757
 -3145781.18889619  6489313.06979566  5337976.61418766 -6502342.18458175
  -597606.62387763 -4005040.68316823  1433875.67877789 -3172759.42646885
    92974.62947959    75778.36198587 -4120343.26071334 -6108529.00941579
 17925877.75368398 -9533862.75547973  2463374.95152149 -3164422.76127016
  3404563.29875213   880358.48816297  2463539.16063948  5017861.07046103
  1900053.94121004  3652281.5967721  -2849632.98686238   833256.5211426 ]
  12767957.222222228
 ''' 

'''mu
 [5.10818713e+00 1.74301754e+03 3.10827193e+02 6.49578655e+02
 9.21292398e+01 2.52233333e+02 1.39598538e+02 1.76842398e+02
 8.53188889e+02 3.14397368e+02 1.89679532e+02 5.28073099e+01
 9.84324561e+01 2.29994152e+01 2.14880117e+01 2.81175941e+01
 4.99273360e+00 1.04629265e+01 1.47901488e+00 4.06584894e+00
 2.23004268e+00 2.83355608e+00 1.36802979e+01 5.08665937e+00
 3.04624684e+00 8.63059921e-01 1.59077256e+00 2.30240274e+00]
 
'''

'''sigma
 [3.71144786e+00 8.86789076e+02 2.14061435e+02 4.42314442e+02
 7.68486244e+01 2.01233265e+02 1.37926767e+02 1.67724471e+02
 6.02190145e+02 2.17888644e+02 1.67669777e+02 3.28900442e+01
 7.15549016e+01 7.00491053e+00 6.76102540e+00 1.01328330e+01
 2.99736218e+00 6.13297273e+00 1.10376077e+00 2.85531163e+00
 2.04685830e+00 2.47171065e+00 8.50315083e+00 2.87135252e+00
 2.46122434e+00 4.37184305e-01 1.02764150e+00 8.37650914e-01]
'''

w = np.array([
 2935004.1726221,   3260051.45000291,  3894326.5545876,  -5048306.39625757,
 -3145781.18889619,  6489313.06979566,  5337976.61418766, -6502342.18458175,
  -597606.62387763, -4005040.68316823,  1433875.67877789, -3172759.42646885,
    92974.62947959,    75778.36198587, -4120343.26071334, -6108529.00941579,
 17925877.75368398, -9533862.75547973,  2463374.95152149, -3164422.76127016,
  3404563.29875213,   880358.48816297,  2463539.16063948,  5017861.07046103,
  1900053.94121004,  3652281.5967721,  -2849632.98686238,   833256.5211426])

b = 12767957.222222228

mu = np.array([
      5.108187134502924, 1743.017543859649, 310.8271929824564, 649.5786549707602, 
      92.12923976608191, 252.23333333333326, 139.59853801169604, 176.84239766081856, 
      853.1888888888893, 314.39736842105253, 189.67953216374264, 52.807309941520465, 
      98.43245614035088, 22.999415204678378, 21.488011695906437, 28.11759405508588, 
      4.992733599703669, 10.462926534823785, 1.4790148782930845, 4.065848937826961,
      2.2300426788974033, 2.833556081405159, 13.68029788583521, 5.086659365397625, 
      3.0462468351033736, 0.8630599208523506, 1.5907725554085057, 2.302402737534365])

sigma = np.array([
         3.711447864584721, 886.7890759302849, 214.0614353875793, 442.3144421929493, 
         76.8486244174913, 201.23326547691607, 137.9267666230125, 167.72447065422364, 
         602.1901454524575, 217.88864361518844, 167.66977654614018, 32.890044163003004, 
         71.55490162524825, 7.004910533892563, 6.76102540061043, 10.132832993062944, 
         2.9973621793224425, 6.13297272862978, 1.103760770461535, 2.8553116285635904, 
         2.046858300477529, 2.471710645788755, 8.503150832430709, 2.871352517007864, 
         2.46122433578432, 0.43718430522316426, 1.0276414976143555, 0.8376509135226502]) 

def predictor(first_name, last_name, w=w, b=b, mu=mu, sigma=sigma):
    try:
        data = data_by_name(first_name, last_name)
        input, output = individual_input_output(data)
        input = (input - mu) / sigma
        salary_prediction = (np.dot(input, w) + b)
        print(first_name + " " + last_name + ":", end=" ")
        print(salary_prediction, output)
    except: print("ERROR")
predictor("Pascal", "Siakam", w, b, mu, sigma)
predictor("Stephen", "Curry")
predictor("Bradley", "Beal")
predictor("Fred", "VanVleet")
predictor("Malachi", "Flynn")
predictor("Joe", "Wieskamp")
predictor("LeBron", "James")
predictor("Nikola", "Jokic")
predictor("Joel", "Embiid")
predictor("Jose", "Alvarado")
predictor("DeAndre", "Jordan")
predictor("Marcus", "Smart")
predictor("Goga", "Bitadze")
predictor("Maxi", "Kleber")
predictor("Steven", "Adams")
predictor("Alex", "Len")
predictor("Kevin", "Love")
predictor("John", "Konchar")
predictor("Shaquille", "Harrison")