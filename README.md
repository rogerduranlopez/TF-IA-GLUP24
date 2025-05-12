# GLUP24 ‑ Predicció de Glucosa (model offline)

Aquest projecte conté el codi, les dades i la documentació necessària per reproduir els resultats del treball final de l'assignatura d'intel·ligència artificial. En aquest traball s'han predit els nivells de glucosa a **+30 min** i **+60 min** per a sis pacients mitjançant un model *offline* basat en **Random Forest** del dataset **GLUP24**.

---

## Estructura de carpetes

```

TF_Roger_Duran
├── data/
│   ├── 559/ … 591/             # Dades train/test de cada pacient
│   ├── predicted/              # CSV de prediccions generats (offline_glucosa.ipynb o entrenament.py)
│   └── columns_description.txt # Descripció de les columnes
│
├── docs/
│   ├── GLUP24.pdf              # Enunciat del treball
│   └── TF_Roger_Duran.pdf      # Documentació del projecte
│
├── notebooks/                  # Notebooks d’anàlisi i modelatge
│   ├── EDA_GLUP24.ipynb        # Exploració i anàlisi prèvia de les dades
│   └── offline_glucosa.ipynb   # Preprocessament i predicció
│
├── resultats/                  # Figures extretes de l’exploració de dades
│
├── src/                        # Codi font
│   └── entrenament.py          # Script d’entrenament del model
│
└── README.md

```


---

## Requisits de programari
Ens hem d'assegurar de tenir intalats les seguents llibreries, per tal que el notebook pugui executarse correctament
```
pip install pandas numpy scikit-learn jupyter
```

---

## Com reproduir els resultats

1. **Obre** `notebooks/offline_glucosa.ipynb` amb VS Code.
2. **Executa** totes les cel·les.
3. Es crearan 12 fitxers de predicció a `data/predicted/` (per si es vol mirar els resultats de la predicció linea a linea) amb el format:
   * `pred<id_pacient>_30min.csv`
   * `pred<id_pacient>_60min.csv`
4. Al final del notebook s’imprimeix la taula de mètriques (RMSE i MAE)

Si es volgues fer la validació del model el que s'hauria d'afegir les dades de test i train tal i com es fa amb la resta de pacients, assignant un numero de pacient de validació i seguint la nomenclatura de forma estricte. 

### O bé...
Es pot **executar el codi des de la terminal fent**: `python src/entrenament.py` des de l'origen del projecte, s'obtindrà la mateixa taula de resultats obtinguda pel notebook.

---

## Format dels fitxers de predicció

Cada CSV de prediccions inclou dues columnes:

| Columna              | Descripció                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------ |
| `Index`              | Índex dins del fitxer de *test* original (després d’afegir +12 per saltar la primera hora) |
| `pred_glucosa_t+{h}` | Predicció de glucosa a +30 min o +60 min                                                   |

---

## Promig dels resultats obtinguts

| Horitzó | RMSE        | MAE         |
| ------- | ----------- | ----------- |
| 30 min  | 23 mg/dL    | 16.93 mg/dL |
| 60 min  | 37.02 mg/dL | 28.26 mg/dL |


---

## Comentaris sobre el codi

* **Model offline**: un únic entrenament per pacient, sense actualització en fase de test.
* **Les features no miren al futur**: les features només contenen informació fins a l’instant *t*; la target es genera amb `shift(-pas)` per fer el desplaçament de les files.
* **Imputació prudencial**: `forward‑fill` per a variables fisiològiques, però la glucosa queda sense imputar per evitar correlació artificial.
* **Repetibilitat**: `random_state=42` a l’estimador.


