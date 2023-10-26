import pandas as pd
import random

def train(data):
    index = ['Температура', 'Кашель', 'Одышка', 'Боли в горле',
             'Ринит', 'Головная боль', 'Диарея', 'Боли в животе', 'Зима', 'Весна', 'Лето', 'Осень']
    columns = ['Грипп', 'РС', 'Адено', 'Бока']
    prob = pd.DataFrame(columns=columns, index=index)
    weights_winter = [0.675, 0.195, 0.083, 0.047]
    weights_spring = [0.675, 0.195, 0.083, 0.047]
    weights_summer = [0.675, 0.195, 0.083, 0.047]
    weights_autumn = [0.675, 0.195, 0.083, 0.047]
    prob_infl = [0.789, 0.744, 0.400, 0.169, 0.301, 0.181, 0.111, 0.091]
    prob_rs = [0.716, 0.874, 0.601, 0.115, 0.616, 0.012, 0.135, 0.082]
    prob_adeno = [0.892, 0.844, 0.228, 0.700, 0.375, 0.684, 0.166, 0.165]
    prob_boca = [0.615, 0.918, 0.557, 0.077, 0.808, 0.443, 0.819]

    prob['Грипп'] = prob_infl + [weights_winter[0]] + [weights_spring[0]] + [weights_summer[0]] + [weights_autumn[0]]
    prob['РС'] = prob_rs + [weights_winter[1]] + [weights_spring[1]] + [weights_summer[1]] + [weights_autumn[1]]
    prob['Адено'] = prob_adeno + [weights_winter[2]] + [weights_spring[2]] + [weights_summer[2]] + [weights_autumn[2]]
    prob['Бока'] = prob_boca[0:5] + ['-'] + prob_boca[5:] + [weights_winter[3]] + [weights_spring[3]] + [
        weights_summer[3]] + [weights_autumn[3]]
    ans_probs = pd.DataFrame(columns=['Грипп', 'РС', 'Адено', 'Бока'],
                             index=range(0, 40000))
    ans = []
    values_boca = ['Температура', 'Кашель', 'Одышка', 'Боли в горле',
                   'Ринит', 'Диарея', 'Боли в животе']
    values = ['Температура', 'Кашель', 'Одышка', 'Боли в горле',
              'Ринит', 'Головная боль', 'Диарея', 'Боли в животе']
    for i in range(0, 40000):
        # print(i)
        znam_1 = znam_2 = znam_3 = znam_4 = 1
        # values_boca.append(data.loc[i]['Сезон'])
        for j in range(0, len(values_boca)):
            if data.loc[i][values_boca[j]] != 0:
                znam_1 *= prob.loc[values_boca[j]]['Грипп']
                znam_2 *= prob.loc[values_boca[j]]['РС']
                znam_3 *= prob.loc[values_boca[j]]['Адено']
                znam_4 *= prob.loc[values_boca[j]]['Бока']
            else:
                znam_1 *= (1 - prob.loc[values_boca[j]]['Грипп'])
                znam_2 *= (1 - prob.loc[values_boca[j]]['РС'])
                znam_3 *= (1 - prob.loc[values_boca[j]]['Адено'])
                znam_4 *= (1 - prob.loc[values_boca[j]]['Бока'])
        znam_1 *= prob.loc[data.loc[i]['Сезон']]['Грипп']
        znam_2 *= prob.loc[data.loc[i]['Сезон']]['РС']
        znam_3 *= prob.loc[data.loc[i]['Сезон']]['Адено']
        znam_4 *= prob.loc[data.loc[i]['Сезон']]['Бока']
        znam = znam_1 + znam_2 + znam_3 + znam_4

        if data.loc[i]['Головная боль'] == '–':
            '''
            надо типа конец алгоритма, вероятности получены по этим знам
            '''
            prob_infl = znam_1 / znam
            prob_rc = znam_2 / znam
            prob_adeno = znam_3 / znam
            prob_boca = znam_4 / znam
        else:
            prob_boca = znam_4 / znam
            prob_g1 = 1 - prob_boca
            znam_1 = znam_2 = znam_3 = 1
            for j in range(0, len(values)):
                if data.loc[i][values[j]] != 0:
                    znam_1 *= prob.loc[values[j]]['Грипп']
                    znam_2 *= prob.loc[values[j]]['РС']
                    znam_3 *= prob.loc[values[j]]['Адено']
                else:
                    znam_1 *= (1 - prob.loc[values[j]]['Грипп'])
                    znam_2 *= (1 - prob.loc[values[j]]['РС'])
                    znam_3 *= (1 - prob.loc[values[j]]['Адено'])
            znam_1 *= prob.loc[data.loc[i]['Сезон']]['Грипп']
            znam_2 *= prob.loc[data.loc[i]['Сезон']]['РС']
            znam_3 *= prob.loc[data.loc[i]['Сезон']]['Адено']
            znam = znam_1 + znam_2 + znam_3
            prob_infl = prob_g1 * znam_1 / znam
            prob_rc = prob_g1 * znam_2 / znam
            prob_adeno = prob_g1 * znam_3 / znam
        ans_probs.loc[i] = [prob_infl, prob_rc, prob_adeno, prob_boca]
        maxim = max(prob_infl, prob_rc, prob_adeno, prob_boca)
        if prob_infl == maxim:
            ans.append('Грипп')
        elif prob_rc == maxim:
            ans.append('РС')
        elif prob_adeno == maxim:
            ans.append('Адено')
        elif prob_boca == maxim:
            ans.append('Бока')
    return ans_probs, ans
