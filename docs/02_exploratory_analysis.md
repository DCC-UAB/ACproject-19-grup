# Comprensió de les dades
En aquest arxiu, farem un anàlisi general del dataset i respondrem les preguntes de la **setmana 1**. Comprovarem que inclou tant dades sobre la contaminació com dades sobre salut mental. A més, realitzarem una exploració inicial per entendre el conjunt de dades (tipus de variables, missing values, outliers, etc.).
Les comandes executades per obtenir la informació exposada es troba en l'arxiu `csv_to_dataset.py`.

---

## Característiques:
El dataset té 3348 files (instàncies) i 95 columnes (característiques). Les dades són numèriques, categòriques i temporals. 

1. **Dades temporals:**
    year, month, day, hour, dayoftheweek: Informació útil per analitzar variacions temporals en la contaminació o en la salut mental.
2. **Indicadors de salut mental:**
    occurrence_mental, bienestar, energia, estres, sueno: Dades reportades pels participants que poden servir com a variables dependents per predir l’impacte de la contaminació.
3. **Contaminació ambiental:**
    no2bcn_24h, no2bcn_12h, pm25bcn: Concentracions de contaminants atmosfèrics.
    BCμg: Black Carbon, rellevant per a la salut respiratòria i mental.
    sec_noise55_day, sec_noise65_day: Exposició al soroll.
    hours_greenblue_day: Temps d'exposició a espais verds/blaus.
4. **Dades demogràfiques i personals:**
    age_yrs, gender, education, district: Context de l’individu per estudiar efectes diferenciats segons la població.
5. **Factors relacionats amb la COVID-19:**
    covid_work, covid_mood, covid_sleep: Canvis de comportament durant la pandèmia.
6. **Condicions meteorològiques:**
    tmean_24h, humi_24h, pressure_24h, precip_24h: Factors climàtics que poden influir en la salut mental.
7. **Exposició espacial i temporal:**
    min_gps, hour_gps, access_greenbluespaces_300mbuff: Dades de localització i accés a espais verds/blaus.


---

## Valors null:
Hi ha 3348 valors null en tot el dataset. Observem que es distribueixen de manera dispersa i no afecta a una columna en concret. És a dir, no hi ha cap columna amb tot de valors null, per tant, d'entrada no és pot eliminar cap columna sencera.

Tot i això, hem analitzat la distribució de valors null per columna. Observem que les distribucions amb <5% són columnes amb pocs nulls on la pèrdua d'informació és petita. Les columnes amb <5% i >10%, la proporció no és massa alta i encara és pot gestionar de la mateixa manera que els de <5%: substituint per els valors de les columnes null per la mitjana (var. numèriques) o per la moda (var. categòriques). En canvi, quan la proporció és >10%, els valors null són alts i pot haver-hi una mancança d'informació. Després de plantejar-nos l'eliminació d'aquestes característiques "poc valioses" a priori, decidim mantenir-les fins analitzar l'impacte de cada una en el model.
1. **Característiques amb <5% valors null:** ['ID_Zenodo', 'date_all', 'year', 'month', 'day', 'dayoftheweek', 'hour', 'mentalhealth_survey', 'occurrence_mental', 'bienestar', 'energia', 'sueno', 'horasfuera', 'actividadfisica', 'ordenador', 'dieta', 'alcohol', 'drogas', 'bebida', 'enfermo', 'otrofactor', 'stroop_test', 'no2bcn_24h', 'no2bcn_12h', 'no2bcn_12h_x30', 'no2bcn_24h_x30', 'min_gps', 'hour_gps', 'pm25bcn', 'tmean_24h', 'tmean_12h', 'humi_24h', 'humi_12h', 'pressure_24h', 'pressure_12h', 'precip_24h', 'precip_12h', 'precip_12h_binary', 'precip_24h_binary', 'maxwindspeed_24h', 'maxwindspeed_12h', 'gender', 'district', 'covid_work'].
2. **Característiques amb >5% i <10% valors null:** ['estres', 'occurrence_stroop', 'mean_incongruent', 'correct', 'response_duration_ms', 'performance', 'mean_congruent', 'inhib_control', 'z_performance', 'z_mean_incongruent', 'z_inhib_control', 'no2gps_24h', 'no2gps_12h', 'no2gps_12h_x30', 'no2gps_24h_x30', 'BCμg', 'noise_total_LDEN_55', 'access_greenbluespaces_300mbuff', 'µgm3', 'incidence_cat', 'start_day', 'start_month', 'start_year', 'start_hour', 'end_day', 'end_month', 'end_year', 'end_hour', 'Totaltime', 'Totaltime_estimated', 'Houron', 'Houroff', 'age_yrs', 'yearbirth', 'education', 'covid_mood', 'covid_sleep', 'covid_espacios', 'covid_aire', 'covid_motor', 'covid_electric', 'covid_bikewalk', 'covid_public_trans'].
3. **Característiques amb >10% valors null:**  ['sec_noise55_day', 'sec_noise65_day', 'sec_greenblue_day', 'hours_noise_55_day', 'hours_noise_65_day', 'hours_greenblue_day', 'smoke', 'psycho'].

---

## Outliers: 
Els outliers (valors atípics) són dades que es troben molt lluny de la resta de valors en un conjunt de dades. Aquests poden ser resultats d’errors de mesura, errors de registre, anomalies reals, o simplement punts inusuals en el conjunt de dades. Hi ha diverses tècniques per analitzar els outliers d'un dataset. Es poden identificar amb tècniques visuals (boxplots, scatterplots) o estadístiques (IQR, desviació estàndard). Per últim, el tractament dels outliers depèn del context: es poden eliminar, transformar o analitzar com a casos especials.

En el nostre projecte, farem servir la **tècnica visual boxplot**. L’ús de **boxplots** és ideal perquè permet una visualització clara i ràpida dels **outliers** i de la distribució de les dades. Aquesta tècnica destaca els valors atípics d’una manera intuïtiva gràcies als **bigotis** i als punts fora del rang esperat, sense necessitat de càlculs complexos. A més, facilita la comparació entre múltiples variables numèriques de manera simultània. Tot i que hi ha tècniques alternatives (IQR, desviació estàndard), els boxplots són més comprensibles visualment i eficients per a una anàlisi inicial.

Si cerquem l'apartat d'outliers en el codi `csv_to_dataset.py`, observem que hem generat els diferents gràfics per a les variables numèriques que poden tenir valors anòmals. A continuació, s'explica les observacions realitzades a partir d'aquests:
1. `age_yrs`: les enquestes s'han realitzat a persones d'entre 18 i 76 anys. La mitjana d'edat és 37.82 anys.
2. `BCµg`: el valor mitjà és de 0.9478µg. Es consideren 3 outliers, els quals >2µg. Doncs, la contaminació sol prendre valors baixos.
3. `bienestar`: la mesura de benestar comprèn el rang [0, 10]. El valor mitjà és de 7.22. Es consideren 3 outliers, els quals <3. Doncs, el benestar és bastant alt en general.
4. `µgm3`: el valor mitjà és 28.15 µg/m³. Existeixen diversos valors atípics (<10 y >50), indicant variabilitat en els nivells de contaminació.
5. `correct`: Els valors correctes estan entre 9 i 11 amb una mitjana de 10.47. Es consideren outliers els valors inferiors a 8 i superiors a 12.
6. `date_all` : Les dates registrades varien dins del rang [22,200, 22,250], amb una mitjana de 2 i 230.48. Es detecten outliers en dates posteriors a 22 i 300, que poden correspondre a registres anòmals.
7. `day`: Els dies registrats comprenen el rang [1, 31]. La mitjana és de 15.45 i la mediana de 15.00. No es detecten outliers en aquesta variable.
8. `dayoftheweek`: Els valors comprenen el rang [0, 6], representant els dies de la setmana. La mitjana és de 3.21. No hi ha outliers.
9. `end_day`: Els dies finals comprenen el rang [1, 31], amb una mitjana de 15.58. No es detecten valors atípics en aquesta variable.
10. `end_hour`: Les hores finals varien entre les 10 i les 20 hores, amb una mitjana de 14.82 hores. No es detecten outliers.
11. `end_month`: Els valors mes estan concentrats en els mesos finals de l'any (9-12). La mediana és 10.00 i la mitjana és 9.8. S'han detectat alguns outliers en mesos anteriors al 5, possiblement errors o dades menys representatives.
12. `end_year`: La majoria dels registres corresponen a l'any 2020 amb una mediana i mitjana de 2020.0. Hi ha un outlier a l'any 2021, que podria indicar un registre anòmal.
13. `inhib_control`: Els valors principals estan propers a 0, amb una mediana de 0.05 i una mitjana de -0.12. S'han detectat molts outliers a bandes negatives (< -2000) i positives (> 2000), indicant variabilitat alta en aquest indicador.
14. `maxwindspeed_12h`: Els valors típics són baixos (0-5 m/s), amb una mediana de 1.2 m/s i una mitjana de 2.0 m/s. Els outliers es troben per sobre de 10 m/s, representant vents atípics o extrems.
15. `occurrence_mental`: Les puntuacions es distribueixen entre 2 i 12 amb una mediana de 7.0 i una mitjana de 7.3. No s'han detectat outliers significatius.
16. `occurrence_stroop`: La distribució és similar a la variable anterior, amb una mitjana de 7.1. No hi ha valors extrems destacats.
17. `start_day`: Els dies estan distribuïts uniformement entre 1 i 30, amb una mitjana de 15.3. No s'han detectat outliers.
18. `start_hour`: Els valors centrals són entre 8 i 12, amb una mediana de 10.0 i una mitjana de 9.8. Els outliers es troben abans de les 5 i després de les 20 hores, probablement per activitats irregulars.
19. `z_mean_incongruent`: Els valors centrals estan propers a 0, amb una mitjana de 0.02. Els outliers van des de -2.0 fins a més de 10.0, indicant dispersió important.
20. `z_performance`: La mediana és 0.00 i la mitjana és 0.05. S'han detectat outliers a ambdues bandes (< -3 i > 3), però la major part de les dades es troben en un rang ajustat.
21. `energia`: Els valors estan principalment entre 6 i 8, amb una mediana de 7.5 i una mitjana de 7.3. Hi ha 3 outliers amb valors inferiors a 3, representant una baixa energia.
22. `estres`: Els nivells d'estrès es distribueixen entre 2 i 8, amb una mediana de 5.0 i una mitjana de 5.1. No es detecten outliers destacats.
23. `horasfuera`: Les hores fora varien entre 0 i 10, amb una mitjana de 4.8. Hi ha diversos outliers amb valors superiors a 15 hores, sent un valor màxim de 35 hores.
24. `hour`: Els registres d'hores es concentren entre 15 i 21, amb una mediana de 19.0 i una mitjana de 18.7. S'han detectat outliers abans de les 10 hores, indicant activitats poc freqüents en aquest horari.
25. `hour_gps`: Els valors es distribueixen uniformement entre 0 i 24 hores, amb una mediana de 12.0 i una mitjana de 12.1. No hi ha valors extrems destacats.
26. `hours_greenblue_day`: Les hores en espais verds i blaus són generalment inferiors a 5, amb una mediana de 1.0 i una mitjana de 2.3. S'han detectat diversos outliers superiors a 20 hores.
27. `hours_noise_55_day`: La majoria dels valors es troben entre 0 i 5 hores, amb una mediana de 2.0 i una mitjana de 2.7. S'han identificat outliers amb més de 15 hores d'exposició al soroll de 55 dB.
28. `hours_noise_65_day`: La distribució és similar a `hours_noise_55_day`, amb una mitjana de 1.9. Els outliers superen les 15 hores d'exposició al soroll de 65 dB.
29. `humi_12h`: Els valors d'humitat relativa oscil·len entre 50% i 80%, amb una mitjana de 66.3%. No es detecten outliers significatius.
30. `humi_24h`: Les dades d'humitat de 24 hores tenen un comportament similar a `humi_12h`, amb una mitjana de 66.8%. Els valors estan dins del rang esperat.
31 . `maxwindspeed_24h`: la velocitat màxima del vent en 24 hores comprèn valors entre 0 i 25 m/s. El valor mitjà és de 2.34 m/s. Es consideren outliers els valors superiors a 10 m/s. Doncs, la velocitat del vent sol ser baixa la major part del temps.
32. `mean_congruent`: el temps mitjà de resposta congruent varia entre 0 i 8000 ms. El valor mitjà és de 1312.45 ms. Es consideren outliers els valors >3000 ms. Doncs, la majoria de respostes congruents es donen ràpidament.
33. `mean_incongruent`: el temps mitjà de resposta incongruent comprèn el rang de 0 a 6000 ms. El valor mitjà és de 1452.89 ms. Es consideren outliers els valors superiors a 4000 ms. Doncs, les respostes incongruents solen requerir més temps que les congruents.
34. `min_gps`: el valor mínim de GPS (distància o temps segons la variable) oscil·la entre 0 i 1400 unitats. El valor mitjà és de 623.11 unitats. No s’identifiquen outliers evidents en aquesta variable.
35. `month`: la distribució mensual indica que les observacions es concentren sobretot a la tardor (setembre, octubre, novembre). El valor mitjà és de 9.12 (corresponent a setembre). Es consideren outliers els mesos de gener, febrer i març.
36. `no2bcn_12h`: la concentració de NO2 en 12 hores varia entre 10 i 80 µg/m³. El valor mitjà és de 34.67 µg/m³. Es consideren outliers els valors >60 µg/m³, que corresponen a episodis d’alta contaminació.
37. `no2bcn_24h` la concentració de NO2 en 24 hores té un rang similar, amb un valor mitjà de 33.45 µg/m³. Els outliers també es consideren per sobre dels 60 µg/m³.
38. `no2gps_12h`: el valor mitjà de NO2 mesurat per GPS en 12 hores és de 38.12 µg/m³. Es detecten diversos outliers >70 µg/m³, que podrien indicar zones amb alta densitat de trànsit o fonts de contaminació puntuals.
39. `no2gps_24h`: la concentració mitjana en 24 hores és similar a la de 12 hores, amb un valor mitjà de 37.78 µg/m³. Els outliers també superen els 70 µg/m³.
40. `noise_total_LDEN_55`: la mesura de soroll total (LDEN >55 dB) varia entre 0 i 1 (indicador binari). El valor mitjà és de 0.78, el que implica que en la majoria de casos es superen els 55 dB. Només s'identifiquen pocs casos amb valors propers a 0.
41. `performance`: Aquesta variable mostra un rang de valors d'aproximadament 20 a 80. La mitjana del rendiment és de 50.32. Es consideren valors atípics aquells que són inferiors a 20 o superiors a 80.
42. `pm25bcn`: Els nivells de PM2.5 a Barcelona es troben principalment entre 10 i 20, amb una mitjana de 15.48. S'observen valors atípics significatius per sobre de 25, que reflecteixen episodis puntuals de contaminació.
43. `precip_12h`: Les precipitacions acumulades en 12 hores són generalment baixes, amb una mitjana de 3.24 mm. No obstant això, s'identifiquen valors atípics per sobre de 30 mm, que representen episodis de pluja intensa.
44. `precip_24h`: Les precipitacions acumulades en 24 hores tenen una mitjana de 5.68 mm. S'observen valors atípics per sobre de 40 mm, coincidint amb episodis de pluja intensa.
45. `pressure_12h`: La pressió atmosfèrica en 12 hores varia entre 990 i 1030 hPa, amb una mitjana de 1012.78 hPa. Els valors inferiors a 990 hPa es consideren atípics i podrien estar associats a sistemes meteorològics significatius.
46. `pressure_24h`: Aquesta variable segueix un patró semblant al de 12 hores, amb una mitjana de 1013.02 hPa i valors atípics similars.
47. `response_duration_ms`: El temps de resposta varia àmpliament amb una mitjana de 15,482.32 ms. Els valors atípics es concentren a partir de 40,000 ms, indicant possibles problemes tècnics o interrupcions.
48. `sec_greenblue_day`: Aquesta variable mostra el nombre de segons diaris exposats a zones verdes o blaves, amb una mitjana de 5,432 segons (1.5 hores). Els valors superiors a 20,000 segons es consideren atípics, representant exposicions molt altes.
49. `sec_noise55_day`: Les exposicions diàries a nivells de soroll superiors a 55 dB tenen una mitjana de 7,890 segons (2.2 hores). Els valors atípics es troben a partir de 20,000 segons.
50. `sec_noise65_day`: El temps diari en soroll intens (65 dB) és més limitat, amb una mitjana de 3,102 segons (0.86 hores). Els valors atípics superen els 10,000 segons, reflectint exposicions prolongades a entorns sorollosos.
51. start_month: Els valors oscil·len entre 2 i 12, amb la mediana al mes 10 i una concentració notable entre setembre i desembre. Valors atípics detectats als mesos 2 i 3.
52. `start_year`: Dades principalment concentrades al 2020. Valors atípics identificats el 2021.
53. `sueno`: La mitjana és de 7.12 hores, amb la majoria de valors entre 6 i 8. Valors atípics inferiors a 3 hores indiquen possibles casos d'insomni sever.
53. `tmean_12h`: Les temperatures mitjanes de 12 hores oscil·len entre 10 °C i 25 °C, amb una mitjana de 17.4 °C. Valors atípics detectats per sobre de 27 °C.
54. `tmean_24h`: Temperatures mitjanes de 24 hores concentrades entre 15 °C i 20 °C, amb una mitjana de 17.8 °C. Valors atípics inferiors a 10 °C i superiors a 25 °C.
55. `Totaltime`: Temps total entre 100 i 400 minuts, amb una mitjana de 175.3 minuts. Valors atípics per sobre de 300 minuts.
56. `year`: Observacions principalment del 2020. Valors atípics detectats el 2021.
57. `z_inhib_control`: Els valors oscil·len entre -10 i 10, centrats a 0. Valors atípics identificats fora d’aquest rang.

---

## Proporció dels registres de mental health. 

Hem pogut generar un gràfic en el que hem escollit les variables 'Bienestar', 'mentalhealth_survey' i 'occurrence_mental', que són relacionades ammb la salut mental.En aquest gràfic hem torbat que el problema principal és que les categories de cadascun dels conjunts de dades no són coherents entre elles, fet que dificulta la comparació. És a dir, 'mentalhealth_survey' es compon per dades categòriques ('Yes', 'No'), i en canvi les altres dues són números del 1 al 10. Per tant, no podem trobar una proporció clara dels registres de mentalhealth. 
És a dir,trobem que hi ha un desbalanç cap als malalts, ja que només hi ha 13 registres classificats com a malalts en comparació amb 3335 registres classificats com a sans. Això representa una proporció extremadament petita de malalts respecte als sans, la qual cosa pot complicar qualsevol anàlisi o model que es vulgui construir més endavant. Aquest desbalanç té diverses implicacions importants:

- **Falta de representació del grup minoritari**: El grup de malalts és tan petit que pot ser difícil extreure conclusions fiables sobre les seves característiques.
- **Esbiaix en resultats futurs**: Qualsevol model o anàlisi podria estar esbiaixat cap al grup majoritari (els sans), ja que tindrà més pes en els càlculs estadístics.
- **Dificultat en la generalització**: Les dades actuals no permeten generalitzar fàcilment conclusions sobre els malalts perquè no representen adequadament aquest grup.
    
---

## Correlació i redundància entre variables
Per tal d'evaluar la correlació i redundància entre variables, hem creat una matriu de correlació (heatmap). Doncs, en aquest apartat explicarem les variables amb correlació moderada o alta (positiva o negativa) que ens han cridat l'atenció, així com aquelles que poden tenir una rellevància important.

1. **Salut mental i contaminació**:
   - Variables salut mental: `estres`, `bienestar`, `energia`.
   - Variables contaminació: `no2bcn_24h`, `no2gps_24h`, `pm25bcn`.
   - Observem una correlació moderada (positiva) entre `estres` i `no2bcn_24h`. Això podria suggerir que l’exposició a nivells més alts de NO₂ durant 24 hores està associada a majors nivells d’estrès.
   - Observem una correlació moderada (negativa) entre `bienestar` i `no2bcn_24h`.  Aquesta relació indica que majors nivells de NO₂ podrien estar associats amb un sentiment de benestar reduït. Destaquem que la variable `energia` segueix una tendència similar amb NO₂, amb correlacions negatives.
   - Observem una correlació moderada (positiva) entre les variables `sec_noise55_day` i `sec_noise65_day` amb `estres`. Aquesta associació és coherent amb estudis que relacionen el soroll ambiental amb l’augment de l’estrès.
     
2. **Hores de son i estrès**
    -  Variables: `son` i `estres`.
    -  Observem una correlació negativa entre `sueno` i `estres`. Doncs, menys hores de son estan associades a majors nivells d’estrès. Aquesta relació és consistent amb la literatura sobre els efectes de la privació del son en la salut mental.
    -  També s’observa una correlació lleu (positiva) entre `sueno` i `bienestar`, la qual cosa indica que més hores de son es relacionen amb un major benestar.

3. **Meteorologia i salut**
    - Variables meteorològiques: `tmean_24h`, `pressure_24h`.
    - Variables de salut mental: `estres`, `bienestar`, `energia`.
    - Observem una correlació lleu amb `tmean_24h` i `estres`. Per tant, dies amb temperatures extremes podrien influir negativament en l’estrès, tot i que cal un anàlisi més profund. En canvi,  `tmean_24h` i `energia` és lleument positiva, suggerint que temperatures moderades podrien estar associades amb nivells més alts d’energia.
    - Observem una correlació lleu negativa amb `pressure_24h` i `bienestar`, la qual  indica que variacions en la pressió poden influir en el sentiment de benestar. Això pot estar relacionat amb efectes fisiològics de la pressió en el cos humà.

4. **Relacions entre variables de contaminació**
    - `no2bcn_24h` i `no2gps_24h` mostren una correlació gairebé perfecta (valors propers a 1), indicant que són pràcticament redundants. Doncs, potser es pot simplificar en 1 variable.
    - La correlació entre `no2bcn_24h` i `pm25bcn` és moderada, la qual cosa és esperable, ja que ambdós són contaminants atmosfèrics comuns però amb fonts i dinàmiques diferents.
      
5. **Impacte del sorol ambiental**
    - Variables de soroll: `sec_noise55_day`, `sec_noise65_day`, `hours_noise_55_day`.
    - Variables de salut mental: `estres`.
    - Observem una correlació positiva moderada entre `estres` amb `sec_noise55_day` i `sec_noise65_day`. Això indica que una exposició prolongada a sorolls per sobre de 55 dB i 65 dB està associada amb majors nivells d’estrès.
    - La variable `hours_noise_55_day` també mostra una tendència similar, suggerint que tant la intensitat com la durada del soroll són factors importants.
      
6. **Variables temporals**
    - Variables temporals: `day`, `hour`, `month`.
    - Variable de salut mental: `estres`, `bienestar`.
    - L’anàlisi temporal mostra que el mes (`month`) pot tenir un efecte en variables com `estres` i `bienestar`, probablement per factors estacionals (per exemple, estiu amb més contaminació o soroll).
    - La variable `hour` pot influir en variables com `sueno`, reflectint diferències en la qualitat del descans segons l’hora del dia.

---

## **Hipòtesi inicial sobre les relacions entre variables**
1. **Salut mental i contaminació**:
   - Existeix una relació moderada entre contaminació (NO₂) i estrès/benestar.
   - Els nivells alts de soroll ambiental augmenten l’estrès.

2. **Son i estrès**:
   - Hores de son més baixes estan associades amb majors nivells d’estrès.

3. **Meteorologia i salut**:
   - La temperatura i la pressió poden influir en el benestar i l’energia.

4. **Relacions dins de la contaminació**:
   - Les variables de NO₂ estan altament correlacionades entre elles i moderadament amb PM2.5.

