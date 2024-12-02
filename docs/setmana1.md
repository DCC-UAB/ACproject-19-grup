# Comprensió de les dades
En aquest arxiu, farem un anàlisi general del dataset i respondrem les preguntes de la **setmana 1**. Comprovarem que inclou tant dades sobre la contaminació com dades sobre salut mental. A més, realitzarem una exploració inicial per entendre el conjunt de dades (tipus de variables, missing values, outliers, etc.).
Les comandes executades per obtenir la informació exposada es troba en l'arxiu `csv_to_dataset.py`.

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

## Valors null:
Hi ha 3348 valors null en tot el dataset. Observem que es distribueixen de manera dispersa i no afecta a una columna en concret. És a dir, no hi ha cap columna amb tot de valors null, per tant, d'entrada no és pot eliminar cap columna sencera.

Tot i això, hem analitzat la distribució de valors null per columna. Observem que les distribucions amb <5% són columnes amb pocs nulls on la pèrdua d'informació és petita. Les columnes amb <5% i >10%, la proporció no és massa alta i encara és pot gestionar de la mateixa manera que els de <5%: substituint per els valors de les columnes null per la mitjana (var. numèriques) o per la moda (var. categòriques). En canvi, quan la proporció és >10%, els valors null són alts i pot haver-hi una mancança d'informació. Després de plantejar-nos l'eliminació d'aquestes característiques "poc valioses" a priori, decidim mantenir-les fins analitzar l'impacte de cada una en el model.
1. **Característiques amb <5% valors null:** ['ID_Zenodo', 'date_all', 'year', 'month', 'day', 'dayoftheweek', 'hour', 'mentalhealth_survey', 'occurrence_mental', 'bienestar', 'energia', 'sueno', 'horasfuera', 'actividadfisica', 'ordenador', 'dieta', 'alcohol', 'drogas', 'bebida', 'enfermo', 'otrofactor', 'stroop_test', 'no2bcn_24h', 'no2bcn_12h', 'no2bcn_12h_x30', 'no2bcn_24h_x30', 'min_gps', 'hour_gps', 'pm25bcn', 'tmean_24h', 'tmean_12h', 'humi_24h', 'humi_12h', 'pressure_24h', 'pressure_12h', 'precip_24h', 'precip_12h', 'precip_12h_binary', 'precip_24h_binary', 'maxwindspeed_24h', 'maxwindspeed_12h', 'gender', 'district', 'covid_work'].
2. **Característiques amb >5% i <10% valors null:** ['estres', 'occurrence_stroop', 'mean_incongruent', 'correct', 'response_duration_ms', 'performance', 'mean_congruent', 'inhib_control', 'z_performance', 'z_mean_incongruent', 'z_inhib_control', 'no2gps_24h', 'no2gps_12h', 'no2gps_12h_x30', 'no2gps_24h_x30', 'BCμg', 'noise_total_LDEN_55', 'access_greenbluespaces_300mbuff', 'µgm3', 'incidence_cat', 'start_day', 'start_month', 'start_year', 'start_hour', 'end_day', 'end_month', 'end_year', 'end_hour', 'Totaltime', 'Totaltime_estimated', 'Houron', 'Houroff', 'age_yrs', 'yearbirth', 'education', 'covid_mood', 'covid_sleep', 'covid_espacios', 'covid_aire', 'covid_motor', 'covid_electric', 'covid_bikewalk', 'covid_public_trans'].
3. **Característiques amb >10% valors null:**  ['sec_noise55_day', 'sec_noise65_day', 'sec_greenblue_day', 'hours_noise_55_day', 'hours_noise_65_day', 'hours_greenblue_day', 'smoke', 'psycho'].

## Outliers: 
Els outliers (valors atípics) són dades que es troben molt lluny de la resta de valors en un conjunt de dades. Aquests poden ser resultats d’errors de mesura, errors de registre, anomalies reals, o simplement punts inusuals en el conjunt de dades. Hi ha diverses tècniques per analitzar els outliers d'un dataset. Es poden identificar amb tècniques visuals (boxplots, scatterplots) o estadístiques (IQR, desviació estàndard). Per últim, el tractament dels outliers depèn del context: es poden eliminar, transformar o analitzar com a casos especials.

En el nostre projecte, farem servir la **tècnica visual boxplot**. L’ús de **boxplots** és ideal perquè permet una visualització clara i ràpida dels **outliers** i de la distribució de les dades. Aquesta tècnica destaca els valors atípics d’una manera intuïtiva gràcies als **bigotis** i als punts fora del rang esperat, sense necessitat de càlculs complexos. A més, facilita la comparació entre múltiples variables numèriques de manera simultània. Tot i que hi ha tècniques alternatives (IQR, desviació estàndard), els boxplots són més comprensibles visualment i eficients per a una anàlisi inicial.

Si cerquem l'apartat d'outliers en el codi `csv_to_dataset.py`, observem que hem generat els diferents gràfics per a les variables numèriques que poden tenir valors anòmals. A continuació, s'explica les observacions realitzades a partir d'aquests:
1. `age_yrs`: les enquestes s'han realitzat a persones d'entre 18 i 76 anys. La mitjana d'edat és 37.82 anys.
2. `BCµg`: el valor mitjà és de 0.9478µg. Es consideren 3 outliers, els quals >2µg. Doncs, la contaminació sol prendre valors baixos.
3. `bienestar`: la mesura de benestar comprèn el rang [0, 10]. El valor mitjà és de 7.22. Es consideren 3 outliers, els quals <3. Doncs, el benestar és bastant alt en general.
4. **por hacer!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!**

## Gestió dels valors null:
**esto va en preprocessament de les dades!!!!!!!!!!!!!!!!!!!!**
1. **Eliminació de les files / columnes amb valors null:** és una manera ràpida i senzilla, només ens asseguraria treballar amb dades completes, ja que no afegim informació artificial. Però, com els valors null estan dispersos entre les files i columnes, això podria reduir significativament els registres disponibles per entrenar el model, afectant a la capacitat de generalitzar. D'altra banda, si els registres amb valors null tenen característiques diferents als complets, eliminar-los significaria introduir un biaix, ja que el model no representaria correctament les dades. Doncs, no farem servir aquesta tècnica per no disminuir la mostra del model. A més, perquè no seria correcte, ja que es recomanable eliminar registres quan la proporció de files amb null és <5% o quan es perd un 10% de la mostra original. En el nostre cas, la meitat dels registres (52.38%) contenen almenys un valor null, per tant, no seria adhient. Pel que respecta a les columnes, no sabem si les característiques són significatives, per tant, preferim mantenir-les per averiguar la seva importància en el model.

2. Imputació simple (mitjana/moda): **por hacer!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!**

3. Models predictius per imputar els nulls: **por hacer!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!**

4. Crear variables indicadores: **por hacer!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!**

## Gestió dels outliers:
**por hacer????????????????????**

## Proporció dels registres de mentalhealth 
per veure si Les variables de salut mental estan equilibrades? Hi ha molts més malalts que sans? En cas que sí, hem de tenir alguna cosa en compte en crear? --> **por hacer!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!**

# Preguntes:
***por hacer!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*
