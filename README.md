# GLUP24 ‑ Predicció de Glucosa (model offline)

Aquest repositori conté el codi, les dades i la documentació necessària per reproduir els resultats del treball final de l'assignatura: **"GLUP24"**. En aquest traball s'han predit els nivells de glucosa a **+30 min** i **+60 min** per a sis pacients mitjançant un model *offline* basat en **Random Forest**.

---

## Estructura de carpetes

```

TF_Roger_Duran
├── data/                       # Dades originals i csv de prediccions
│   ├── 559/ … 591/             # Dades train/test de cada pacient
│   ├── predicted/              # CSV de prediccions generats pel notebook (offline_glucosa.ipynb)
│   └── columns_description.txt
│
├── docs/
│   └── GLUP24.pdf              # Enunciat del treball
│
├── notebooks/
│   ├── EDA_GLUP24.ipynb        # Exploració i anàlisi prèvia de les dades
│   └── offline_glucosa.ipynb   # Notebook principal de preprocessament i predicció
│
└── README.md
```


---

## Requisits de programari
Ens hem d'assegurar de tenir intalats les seguents llibreries, per tal que el codi pugui executarse correctament
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
4. Al final del notebook s’imprimeix la taula de mètriques (RMSE i MAE) i es desa una còpia a `resultats/`.

---

## Format dels fitxers de predicció

Cada CSV inclou dues columnes:

| Columna              | Descripció                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------ |
| `Index`              | Índex dins del fitxer de *test* original (després d’afegir +12 per saltar la primera hora) |
| `pred_glucosa_t+{h}` | Predicció de glucosa a +30 min o +60 min                                                   |

---

## Promig dels resultats obtinguts

| Horitzó | RMSE        | MAE         |
| ------- | ----------- | ----------- |
| 30 min  | 22.63 mg/dL | 16.42 mg/dL |
| 60 min  | 36.05 mg/dL | 27.43 mg/dL |


---

## Comentaris sobre el codi

* **Model offline**: un únic entrenament per pacient, sense actualització en fase de test.
* **Les features no miren al futur**: les features només contenen informació fins a l’instant *t*; la target es genera amb `shift(-pas)`.
* **Imputació prudencial**: `forward‑fill` per a variables fisiològiques, però la glucosa queda sense imputar per evitar correlació artificial.
* **Repetibilitat**: `np.random.seed(42)` i `random_state=42` a l’estimador.


