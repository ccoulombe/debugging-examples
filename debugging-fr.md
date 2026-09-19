

# Guide d'exemples de débogage avec Python

Vous trouverez une vue d'ensemble détaillée des exemples de débogage contenus dans ce dépôt. Il détaille le fonctionnement de chaque exemple, les problématiques illustrées, les commandes nécessaires pour les exécuter et la manière d'interagir avec les outils de débogage.

---

## Table des matières
1. [Outils de débogage](#outils-de-débogage)
2. [Exemples PDB (Débogueur interactif Python)](#exemples-pdb-débogueur-interactif-python)
   - [pdb-breakpoint.py — Points d'arrêt (breakpoint)](#1-pdb-breakpointpy--points-darrêt-breakpoint)
   - [pdb-set_trace.py — Méthode classique pdb.set_trace()](#2-pdb-set_tracepy--méthode-classique-pdbset_trace)
   - [pdb-average.py — Débogage en ligne de commande, pas-à-pas](#3-pdb-averagepy--débogage-en-ligne-de-commande-pas-à-pas)
   - [pdb-condition.py — Points d'arrêt conditionnels](#4-pdb-conditionpy--points-darrêt-conditionnels)
   - [pdb-data.py — Initialisation via ligne de commande (-c) et discordance de types](#5-pdb-datapy--initialisation-via-ligne-de-commande--c-et-discordance-de-types)
3. [Exemples Faulthandler (Diagnostics bas niveau)](#exemples-faulthandler-diagnostics-bas-niveau)
   - [faulthandler-hang.py — Détection de blocages et dépassement de délai (timeout)](#6-faulthandler-hangpy--détection-de-blocages-et-dépassement-de-délai-timeout)
   - [faulthandler-segfault.py — Erreurs de segmentation (SIGSEGV)](#7-faulthandler-segfaultpy--erreurs-de-segmentation-sigsegv)
   - [faulthandler-sigill.py — Activation en ligne de commande (-X faulthandler)](#8-faulthandler-sigillpy--activation-en-ligne-de-commande--x-faulthandler)
   - [faulthandler-sigusr.py — Inspection à la demande via signal et attachement de processus](#9-faulthandler-sigusrpy--inspection-à-la-demande-via-signal-et-attachement-de-processus)
4. [Exemples Jupyter (Notebooks)](#exemples-jupyter-notebooks)
   - [pdb-breakpoint.ipynb — Débogage interactif](#10-pdb-breakpointipynb--débogage-interactif)
   - [pdb-postmortem.ipynb — Débogage post-mortem avec %pdb](#11-pdb-postmortemipynb--débogage-post-mortem-avec-pdb)
   - [faulthandler-segfault.ipynb — Capture des plantages du noyau vers un fichier journal](#12-faulthandler-segfaultipynb--capture-des-plantages-du-noyau-vers-un-fichier-journal)
5. [Exemples concrets (supplémentaires)](#exemples-concrets-supplémentaires)
   - [hpc-slurm-sigterm.py — Boucle infinie](#13-hpc-slurm-sigtermpy--boucle-infinie)
   - [hpc-mpi-deadlock.py — Interblocages MPI](#14-hpc-mpi-deadlockpy--interblocages)
   - [hpc-io-watchdog.py — Bloquage I/O](#15-hpc-io-watchdogpy--bloquage-io)
   - [hpc-interactive-pdb.py — PDB interactif sur nœud de calcul](#16-hpc-interactive-pdbpy--pdb-interactif-sur-nœud-de-calcul)
6. [Aide-mémoire](#aide-mémoire)

---

## Outils de débogage

1. **`pdb` (Python Debugger)** :
   Le débogueur interactif de code source inclus dans la bibliothèque standard de Python. Il permet de poser des points d'arrêt, d'exécuter le code pas-à-pas (*step-by-step*), d'inspecter les cadres de la pile d'appels (*stack frames*) et de modifier des variables dynamiquement en cours d'exécution.
2. **`faulthandler`** :
   Introduit avec Python 3.3, ce module standard intercepte les signaux d'erreur bas niveau (tels que `SIGSEGV`, `SIGFPE`, `SIGABRT`, `SIGBUS` ou `SIGILL`) ainsi que les interblocages de threads. Comme ces plantages brutaux tuent le runtime Python avant même que les blocs `try...except` ne puissent agir, `faulthandler` écrit directement la pile d'appels Python sur la sortie d'erreur standard ou dans un fichier.
3. **Débogage IPython / Jupyter** :
   Les environnements interactifs intègrent `ipdb` (une version enrichie de PDB offrant coloration syntaxique et autocomplétion) via des commandes magiques comme `%pdb` ou `%debug`, ainsi que la fonction `set_trace()`.

---

## Exemples PDB (Débogueur interactif Python)

### 1. `pdb-breakpoint.py` — Points d'arrêt (`breakpoint`)

#### Description
Introduite avec Python 3.7 ([PEP 553](https://peps.python.org/pep-0553/)), la fonction native `breakpoint()` suspend l'exécution du programme et bascule directement vers le débogueur configuré (par défaut `pdb`).
Dans cet exemple, l'appel à `double(val)` rencontre immédiatement `breakpoint()`, interrompt le flux d'instructions et ouvre l'invite de commande `(Pdb)`.

```python
def double(x):
   breakpoint()
   return x * 2

val = 3
print(f"{val} * 2 is {double(val)}")
```

#### Exécution
```bash
python pdb-breakpoint.py
```

#### Déroulement
Dès le lancement, Python marque une pause à la ligne 2 (`breakpoint()`) :
```text
> pdb-breakpoint.py(2)double()
-> breakpoint()
(Pdb) ll
  1     def double(x):
  2  ->    breakpoint()
  3        return x * 2

(Pdb) n
> pdb-breakpoint.py(3)double()
-> return x * 2

(Pdb) p x
3

(Pdb) q
```
- `ll` (*long list*) : Affiche l'intégralité du code source de la fonction active, avec `->` indiquant la ligne courante.
- `n` (*next*) : Exécute la ligne courante et s'arrête à la ligne suivante (`return x * 2`).
- `p x` (*print*) : Affiche la valeur de l'argument `x` (`3`).
- `q` (*quit*) : Quitte le débogueur et interrompt le programme.

---

### 2. `pdb-set_trace.py` — Méthode classique `pdb.set_trace()`

#### Description
Illustre l'approche traditionnelle employée dans les versions de Python antérieures à 3.7 : l'import explicite du module `pdb` et l'appel à `pdb.set_trace()`. L'exemple met également en évidence la capacité du débogueur à évaluer directement des expressions Python à la volée.

```python
import pdb

def double(x):
   pdb.set_trace()
   return x * 2

val = 3
print(f"{val} * 2 is {double(val)}")
```

#### Exécution
```bash
python pdb-set_trace.py
```

#### Déroulement
```text
> pdb-set_trace.py(4)double()
-> pdb.set_trace()
(Pdb) ll
  3     def double(x):
  4  ->    pdb.set_trace()
  5        return x * 2

(Pdb) p x
3

(Pdb) x * 2
6

(Pdb) c
3 * 2 is 6
```
- `p x` : Affiche la variable `x`.
- `x * 2` : Évalue n'importe quelle expression Python valide dans le contexte du cadre local.
- `c` (*continue*) : Reprend l'exécution normale du programme jusqu'à la fin ou jusqu'au point d'arrêt suivant.

---

### 3. `pdb-average.py` — Débogage en ligne de commande, pas-à-pas

#### Description
Lance un script sous PDB sans modifier son code source grâce à l'option `-m pdb`.
La fonction calcule la moyenne d'une liste de nombres. Lorsqu'elle est invoquée avec une liste vide `[]`, une exception `ZeroDivisionError` est levée lors du calcul `total / len(nums)`.

```python
def average(nums):
    total = 0
    for n in nums:
        total += n
    return total / len(nums)

print(average([]))
```

#### Exécution

##### Exécution normale (reproduction de l'erreur) :
```bash
python pdb-average.py
```
Résultat :
```text
Traceback (most recent call last):
  File "pdb-average.py", line 7, in <module>
    print(average([]))
  File "pdb-average.py", line 5, in average
    return total / len(nums)
ZeroDivisionError: division by zero
```

##### Lancement sous PDB dès la première instruction :
```bash
python -m pdb pdb-average.py
```

#### Déroulement
```text
> pdb-average.py(1)<module>()
-> def average(nums):

(Pdb) n
> pdb-average.py(7)<module>()
-> print(average([]))

(Pdb) s
--Call--
> pdb-average.py(1)average()
-> def average(nums):

(Pdb) ll
  1  -> def average(nums):
  2         total = 0
  3         for n in nums:
  4             total += n
  5         return total / len(nums)

(Pdb) n
> pdb-average.py(2)average()
-> total = 0

(Pdb) n
> pdb-average.py(3)average()
-> for n in nums:

(Pdb) n
> pdb-average.py(5)average()
-> return total / len(nums)

(Pdb) args
nums = []

(Pdb) nums = [1]

(Pdb) n
--Return--
> pdb-average.py(5)average()->0.0
-> return total / len(nums)

(Pdb) n
0.0
--Return--
> pdb-average.py(7)<module>()->None
-> print(average([]))

(Pdb) q
```
- `s` (*step into*) : Descend à l'intérieur de l'appel de fonction `average()`.
- `args` : Affiche les arguments reçus par la fonction courante (`nums = []`).
- `nums = [1]` : Modification dynamique de l'état d'une variable directement dans le débogueur, évitant l'erreur de division par zéro et permettant de tester immédiatement le comportement du reste du code.

---

### 4. `pdb-condition.py` — Points d'arrêt conditionnels

#### Description
Présente la mise en place d'un point d'arrêt conditionnel qui n'interrompt le programme que lorsqu'une condition spécifique est satisfaite.
Dans cette boucle, la fonction parcourt des entiers et doit lever une `ValueError` dès qu'un nombre est négatif :

```python
def process(items):
    for i, x in enumerate(items):
        if x < 0:
            raise ValueError(f"Negative value at index {i}")
        print(i, x)

process([1, 2, 3, -1, 5])
```

#### Exécution
```bash
python -m pdb pdb-condition.py
```

#### Déroulement
```text
> pdb-condition.py(1)<module>()
-> def process(items):
(Pdb) ll
  1  -> def process(items):
  2         for i, x in enumerate(items):
  3             if x < 0:
  4                 raise ValueError(f"Negative value at index {i}")
  5             print(i, x)
  6     
  7     process([1, 2, 3, -1, 5])

(Pdb) b 3, x<0
Breakpoint 1 at pdb-condition.py:3

(Pdb) c
0 1
1 2
2 3
> pdb-condition.py(3)process()
-> if x < 0:

(Pdb) p x
-1

(Pdb) args
items = [1, 2, 3, -1, 5]
```
- `b 3, x<0` : Crée le point d'arrêt numéro 1 à la ligne 3 avec la condition `x < 0`.
- `c` (*continue*) : Le programme traite les valeurs positives (0, 1, 2) sans interruption, puis s'arrête exactement lors de l'itération où `x == -1`.

---

### 5. `pdb-data.py` — Initialisation via ligne de commande (`-c`) et discordance de types

#### Description
Illustre deux concepts clés :
1. Automatiser l'injection d'instructions de débogage dès le démarrage à l'aide du paramètre `-c`.
2. Diagnostiquer et corriger en mémoire une exception `TypeError` provoquée par une tentative d'addition entre une chaîne de caractères et un entier (`"12" + 5`).

```python
def load_data():
    return {"count": "12"}  # Bogue : count devrait être un entier

def compute_total():
    data = load_data()
    return data["count"] + 5  # TypeError

def main():
    compute_total()

main()
```

#### Exécution

##### Exécution classique :
```bash
python pdb-data.py
```

##### Débogage avec point d'arrêt automatique posé à la ligne 6 :
```bash
python -m pdb -c "b 6" pdb-data.py
```

#### Déroulement
```text
Breakpoint 1 at pdb-data.py:6
> pdb-data.py(1)<module>()
-> def load_data():

(Pdb) c
> pdb-data.py(6)compute_total()
-> return data["count"] + 5  # TypeError

(Pdb) p data
{'count': '12'}

(Pdb) type(data['count'])
<class 'str'>

(Pdb) data['count'] = 12

(Pdb) n
--Return--
> pdb-data.py(6)compute_total()->17
-> return data["count"] + 5  # TypeError

(Pdb) c
The program finished and will be restarted
> pdb-data.py(1)<module>()

(Pdb) q
```
- `-c "b 6"` : Définit le point d'arrêt à la ligne 6 dès le démarrage du débogueur.
- `type(...)` : Révèle que la valeur stockée sous la clé `'count'` est une chaîne (`str`).
- `data['count'] = 12` : Corrige la valeur en mémoire, permettant à l'addition de s'exécuter sans erreur et de retourner `17`.

---

## Exemples Faulthandler (Diagnostics bas niveau)

### 6. `faulthandler-hang.py` — Détection de blocages et dépassement de délai (*timeout*)

#### Description
Permet d'identifier les interblocages (*deadlocks*) ou les boucles infinies (*spinlocks*) à l'aide de `faulthandler.dump_traceback_later(timeout)`. Si le temps d'exécution dépasse le délai imparti (ici 3 secondes), `faulthandler` affiche la trace de tous les threads Python sur la sortie d'erreur (`sys.stderr`) sans interrompre le processus.

```python
import time
import faulthandler

faulthandler.dump_traceback_later(3)

time.sleep(10)
```

#### Exécution
```bash
python faulthandler-hang.py
```

#### Trace obtenue
Après exactement 3 secondes, la trace suivante est émise pendant que le script continue son sommeil jusqu'à atteindre 10 secondes :
```text
Timeout (0:00:03)!
Thread 0x00007f9a39ea6f00 [python] (most recent call first):
  File "faulthandler-hang.py", line 6 in <module>
```

---

### 7. `faulthandler-segfault.py` — Erreurs de segmentation (`SIGSEGV`)

#### Description
L'appel à `ctypes.string_at(0)` force un déréférencement de pointeur nul (`0x0`), ce qui déclenche immédiatement une violation d'accès mémoire (`SIGSEGV`).
Sans `faulthandler`, le système d'exploitation afficherait uniquement `Erreur de segmentation (core dumped)`. Grâce à `faulthandler.enable()`, la ligne de code Python responsable ainsi que la pile d'appels C sont intégralement affichées avant que le processus ne prenne fin.

```python
import faulthandler
faulthandler.enable()

print("About to crash...")

# Forcer un plantage mémoire via ctypes
import ctypes
ctypes.string_at(0)   # accès mémoire invalide → segfault
```

#### Exécution
```bash
python faulthandler-segfault.py
```

#### Trace obtenue
```text
About to crash...
Fatal Python error: Segmentation fault

Current thread 0x00007fb552718f00 [python] (most recent call first):
  File ".../ctypes/__init__.py", line 619 in string_at
  File "faulthandler-segfault.py", line 8 in <module>

Current thread's C stack trace (most recent call first):
...
[1]    273236 segmentation fault (core dumped)  python faulthandler-segfault.py
```

---

### 8. `faulthandler-sigill.py` — Activation en ligne de commande (`-X faulthandler`)

#### Description
Montre comment activer `faulthandler` au niveau de l'interpréteur Python sans modifier une seule ligne de code source, soit avec l'option CLI `-X faulthandler`, soit avec la variable d'environnement `PYTHONFAULTHANDLER=1`. Le script émet délibérément le signal d'instruction machine illégale (`SIGILL`).

```python
import signal

signal.raise_signal(signal.SIGILL)
```

#### Exécution

##### Exécution sans faulthandler (plantage brut sans contexte) :
```bash
python faulthandler-sigill.py
```
Sortie :
```text
illegal hardware instruction (core dumped)  python faulthandler-sigill.py
```

##### Exécution avec faulthandler activé en ligne de commande :
```bash
python -q -X faulthandler faulthandler-sigill.py
```
Ou alternativement :
```bash
PYTHONFAULTHANDLER=1 python faulthandler-sigill.py
```

#### Trace obtenue
```text
Fatal Python error: Illegal instruction

Current thread 0x00007f2c55b28f00 [python] (most recent call first):
  File "faulthandler-sigill.py", line 3 in <module>

Current thread's C stack trace (most recent call first):
  Binary file "/lib64/libpython3.14.so.1.0", at _Py_DumpStack+...
  ...
```

---

### 9. `faulthandler-sigusr.py` — Inspection à la demande via signal et attachement de processus

#### Description
Présente deux techniques avancées pour examiner un processus Python en cours ou bloqué :
1. Enregistrer un gestionnaire de signal avec `faulthandler.register(signal.SIGUSR1)`. Lors de la réception du signal `SIGUSR1`, le processus affiche immédiatement sa pile d'exécution sans s'arrêter.
2. Attacher un débogueur interactif PDB à un processus en cours d'exécution via la commande `python -m pdb -p <PID>`.

```python
import faulthandler
import signal
import time

faulthandler.register(signal.SIGUSR1)

print("Send SIGUSR1")

while True:
    time.sleep(2)
```

#### Exécution

##### Terminal 1 : Démarrage du script
```bash
python faulthandler-sigusr.py
```
Sortie :
```text
Send SIGUSR1
```

##### Terminal 2 (Option A) : Envoi du signal SIGUSR1
```bash
kill -USR1 $(pgrep -f faulthandler-sigusr.py)
```
Dans le Terminal 1, la trace d'appels instantanée apparaît immédiatement et la boucle continue son exécution :
```text
Current thread 0x00007fa455c49f00 [python] (most recent call first):
  File "faulthandler-sigusr.py", line 10 in <module>
```

##### Terminal 2 (Option B) : Attachement au processus
```bash
python -m pdb -p $(pgrep -f faulthandler-sigusr.py)
```
Sortie :
```text
> faulthandler-sigusr.py(10)<module>()
-> time.sleep(2)
(Pdb) 
```

---

## Exemples Jupyter (Notebooks)

### 10. `pdb-breakpoint.ipynb` — Débogage interactif

#### Description
Utilisation d'un point d'arrêt directement au cœur d'une cellule de *notebook* Jupyter en utilisant `IPython.core.debugger.set_trace()`. Lors de l'évaluation de la cellule, une invite interactive `ipdb` s'affiche directement dans la zone de sortie de la cellule.

#### Contenu :
- **Cellule 1** :
  ```python
  from IPython.core.debugger import set_trace

  def average(nums):
      total = 0
      set_trace() # Point d'arrêt ici
      for n in nums:
          total += n
      return total / len(nums)
  ```
- **Cellule 2** :
  ```python
  print(average([]))
  ```

#### Exécution
1. Démarrer Jupyter :
   ```bash
   jupyter lab
   ```
2. Ouvrir [`pdb-breakpoint.ipynb`](file:///workspace/pdb-breakpoint.ipynb).
3. Exécuter la cellule 1 pour charger la fonction.
4. Exécuter la cellule 2 : le flux s'arrête à `set_trace()` et l'invite `ipdb>` s'ouvre, prête à recevoir vos commandes (`n`, `p nums`, `q`).

---

### 11. `pdb-postmortem.ipynb` — Débogage post-mortem avec `%pdb`

#### Description
Utilisation du mode post-mortem automatique d'IPython via `%pdb on` (ou `%debug`). Lorsqu'une exception non interceptée survient (ici `TypeError: can only concatenate str (not "int") to str`), IPython bascule automatiquement dans `ipdb` à l'emplacement exact de la ligne fautive.

#### Contenu :
- **Cellule 1** :
  ```python
  def load_data():
      return {"count": "12"}  # Bogue : count devrait être un entier

  def compute_total():
      data = load_data()
      return data["count"] + 5  # TypeError

  def main():
      return compute_total()
  ```
- **Cellule 2** :
  ```python
  %pdb on
  main()

  # ou bien avec la commande magique %debug
  ```
- **Cellule 3** :
  ```python
  %pdb off
  ```

#### Exécution
1. Ouvrir [`pdb-postmortem.ipynb`](file:///workspace/pdb-postmortem.ipynb) dans Jupyter.
2. Exécuter la cellule 1.
3. Exécuter la cellule 2 : `%pdb on` active le débogueur automatique. Dès que `main()` lève l'exception `TypeError`, la session `ipdb>` s'active :
   ```text
   Automatic pdb calling has been turned ON
   TypeError: can only concatenate str (not "int") to str
   > compute_total()
   ----> 6 return data["count"] + 5
   ipdb> data["count"]
   '12'
   ipdb> type(data['count'])
   <class 'str'>
   ipdb> q
   ```
4. Exécuter la cellule 3 (`%pdb off`) pour désactiver l'ouverture automatique du débogueur.

---

### 12. `faulthandler-segfault.ipynb` — Capture des plantages du noyau vers un fichier journal

#### Description
Lorsqu'un notebook Jupyter subit une erreur fatale au niveau C (erreur de segmentation par exemple), le processus noyau (*kernel*) meurt subitement, entraînant souvent la perte des messages d'erreur standard dans l'interface web.
Cet exemple montre comment configurer `faulthandler.enable(open("faults.log", "w"))` pour rediriger la trace du crash vers un fichier journal persistant ([`faults.log`](file:///workspace/faults.log)).

#### Contenu :
- **Cellule 1** :
  ```python
  import faulthandler
  faulthandler.enable(open("faults.log", "w"))
  ```
- **Cellule 2** :
  ```python
  print("About to crash...")

  # Forcer un plantage mémoire via ctypes
  import ctypes
  ctypes.string_at(0)   # accès mémoire invalide → segfault
  ```

#### Exécution
1. Ouvrir [`faulthandler-segfault.ipynb`](file:///workspace/faulthandler-segfault.ipynb) dans Jupyter.
2. Exécuter la cellule 1 pour rediriger la sortie de `faulthandler` vers `faults.log`.
3. Exécuter la cellule 2 : le noyau Jupyter plante brutalement (*« Kernel died / restarting »*).
4. Consulter le fichier généré [`faults.log`](file:///workspace/faults.log) avec un éditeur ou dans un terminal :
   ```bash
   cat faults.log
   ```
   Vous constaterez que la pile d'appels complète a bien été enregistrée sur le disque, isolant précisément la fonction `ctypes/__init__.py` et la cellule incriminée !

---

## Exemples concrets (supplémentaires)

### 13. `hpc-slurm-sigterm.py` — Boucle infinie

#### Description
Dans un environnement de calcul haute performance (HPC), une tâche qui dépasse son temps limite (`#SBATCH --time=...`) car elle tourne infiniement. . En interceptant `SIGTERM` avec `faulthandler`, vous pouvez forcer l'affichage de la pile d'appels dans le fichier de sortie (`slurm-%j.out`) pour savoir exactement où la boucle infinie se produit.

```python
import faulthandler
import signal
import time

# Prints the trace in the Slurm output upon receiving SIGTERM
faulthandler.register(signal.SIGTERM)

def heavy_computation():
    print("Starting...")
    while True:
        time.sleep(1)

heavy_computation()
```

#### Exécution (Simulation)
```text
$ srun -c 2 --mem=10G python hpc-slurm-sigterm.py &
[1] 1663615
srun: job 3447846 queued and waiting for resources
srun: job 3447846 has been allocated resources
Starting...

$ scancel 3447846
srun: Job step aborted: Waiting up to 62 seconds for job step to finish.
slurmstepd: error: *** STEP 3447846.0 ON nc20142 CANCELLED AT 2026-09-19T16:52:24 DUE to SIGNAL Terminated ***
Current thread 0x0000150e66b84740 (most recent call first):
  File "hpc-slurm-sigterm.py", line 11 in heavy_computation
  File "hpc-slurm-sigterm.py", line 13 in <module>
```

---

### 14. `hpc-mpi-deadlock.py` — Interblocages MPI

#### Description
Lors de l'utilisation de `mpi4py` réparti sur plusieurs nœuds de calcul, un rang (processus) peut se bloquer en attendant indéfiniment un message. En associant un signal personnalisé (comme `SIGUSR1`) à `faulthandler` pour tous les threads, il est possible d'envoyer un signal à l'ensemble des processus via `scancel` pour afficher l'état de chaque rang.

```python
import faulthandler
import signal
from mpi4py import MPI

# Registers SIGUSR1 to print the trace of all threads
faulthandler.register(signal.SIGUSR1, all_threads=True)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    print("Rank 0 is waiting for rank 1...")
    # Bug: Rank 0 waits for a message that will never be sent
    data = comm.recv(source=1, tag=11)
else:
    print(f"Rank {rank} is busy...")
    import time
    while True:
        time.sleep(1)
```

#### Exécution
À l'intérieur d'une tâche:
```text
$ srun -n 2 python hpc-mpi-deadlock.py &
[1] 1663616
Rank 0 is waiting for rank 1...
Rank 1 is busy...

$ kill -USR1 $!
Current thread 0x0000150e66b84741 (most recent call first):
  File "hpc-mpi-deadlock.py", line 19 in <module>
Current thread 0x0000150e66b84740 (most recent call first):
  File "hpc-mpi-deadlock.py", line 14 in <module>
```
ou depuis un noeud de connexion
```text
$ srun -n 2 python hpc-mpi-deadlock.py &
[1] 1663617
srun: job 3447847 queued and waiting for resources
srun: job 3447847 has been allocated resources
Rank 0 is waiting for rank 1...
Rank 1 is busy...

$ scancel --signal=SIGUSR1 3447847
Current thread 0x0000150e66b84741 (most recent call first):
  File "hpc-mpi-deadlock.py", line 19 in <module>
Current thread 0x0000150e66b84740 (most recent call first):
  File "hpc-mpi-deadlock.py", line 14 in <module>
```


---

### 15. `hpc-io-watchdog.py` — Bloquage I/O

#### Description
Les systèmes de fichiers partagés HPC peuvent subir d'intenses pics, bloquant les opérations d'entrée/sortie (`np.load()`, lectures `h5py`) dans un état de sommeil ininterruptible. `faulthandler.dump_traceback_later()` permet de d'afficher la pile lorsque le temps est écoulé.

```python
import faulthandler
import time

# Starting a watchdog timer (here 3 seconds for demonstration)
faulthandler.dump_traceback_later(3)

try:
    print("Simulating reading file...")
    time.sleep(10) # Simulates a prolonged hang
finally:
    # Immediate cancellation upon success within the time limit
    faulthandler.cancel_dump_traceback_later()

print("I/O successfully completed.")
```

#### Exécution
```text
$ python hpc-io-watchdog.py
Simulating reading file...
Timeout (0:00:03)!
Thread 0x00007f9a39ea6f00 (most recent call first):
  File "hpc-io-watchdog.py", line 9 in <module>
I/O successfully completed.
```

---

### 16. `hpc-interactive-pdb.py` — PDB interactif sur nœud de calcul

#### Description
Insérer `breakpoint()` dans un script soumis via `sbatch` provoque un crash immédiat (`BdbQuit` ou `EOFError`) car la tâche en arrière-plan ne dispose d'aucun terminal (TTY) ou entrée standard pour interagir.
Pour utiliser PDB interactivement, il est indispensable de demander une session interactive (`salloc` ou `srun --pty`) afin de déboguer le tout.

```python
def heavy_computation_with_bug(matrix_size):
    print(f"Allocating a {matrix_size}x{matrix_size} matrix...")
    breakpoint()
    return matrix_size * 2

if __name__ == "__main__":
    result = heavy_computation_with_bug(10000)
    print(f"Result: {result}")
```

#### Exécution
Dans Slurm, on obtient d'abord un shell interactif :
```text
$ salloc -c 2 --mem=10G
salloc: Pending job allocation 3447848
salloc: job 3447848 queued and waiting for resources
salloc: job 3447848 has been allocated resources
salloc: Granted job allocation 3447848
salloc: Waiting for resource configuration
salloc: Nodes nc20142 are ready for job
```
Puis on lance le débogueur :
```text
$ python hpc-interactive-pdb.py
Allocating a 10000x10000 matrix...
> /workspace/hpc-interactive-pdb.py(4)heavy_computation_with_bug()
-> return matrix_size * 2
(Pdb) p matrix_size
10000
(Pdb) c
Result: 20000
```

---

## Aide-mémoire

### Commandes PDB indispensables

| Commande | Raccourci | Description |
| :--- | :--- | :--- |
| `next` | `n` | Pas principal (*step over*) : exécute la ligne courante sans entrer dans les sous-fonctions. |
| `step` | `s` | Pas détaillé (*step into*) : entre dans la fonction appelée à la ligne courante. |
| `continue` | `c` | Poursuit l'exécution jusqu'au prochain point d'arrêt ou jusqu'à la fin. |
| `return` | `r` | Poursuit l'exécution jusqu'au retour de la fonction courante. |
| `longlist` | `ll` | Affiche l'intégralité du code source de la fonction active. |
| `list` | `l` | Affiche 11 lignes de code autour de la ligne courante. |
| `print` | `p <expr>` | Évalue et affiche la valeur d'une variable ou d'une expression. |
| `pp` | `pp <expr>` | Affiche joliment (*pretty-print*) la structure d'une variable complexe. |
| `args` | `a` | Affiche la liste des arguments reçus par la fonction courante. |
| `break` | `b <ligne>` | Définit un point d'arrêt au numéro de ligne indiqué. |
| `break` (cond) | `b <ligne>, <cond>` | Définit un point d'arrêt conditionnel qui ne se déclenche que si `<cond>` est vraie. |
| `where` | `w` | Affiche la pile des appels (*stack trace*), le cadre le plus récent étant en bas. |
| `up` / `down` | `u` / `d` | Monte ou descend d'un niveau dans la pile des cadres d'exécution. |
| `quit` | `q` | Quitte le débogueur et met fin à l'exécution. |

### Commandes et options Faulthandler

| Contexte | Méthode / Option | Description |
| :--- | :--- | :--- |
| Dans le code | `faulthandler.enable(file=sys.stderr)` | Active la capture des signaux fatals (`SIGSEGV`, `SIGFPE`, `SIGABRT`, `SIGBUS`, `SIGILL`). |
| Dans le code | `faulthandler.dump_traceback_later(timeout)` | Écrit la trace de tous les threads après un délai d'attente de `timeout` secondes. |
| Dans le code | `faulthandler.register(signal)` | Écrit la trace dès la réception d'un signal système spécifique (ex. `SIGUSR1`). |
| Option à la ligne de commandes | `python -X faulthandler script.py` | Active le module `faulthandler` au démarrage de l'interpréteur sans modifier le script. |
| Variable d'environnement. | `export PYTHONFAULTHANDLER=1` | Active `faulthandler` de manière globale pour tous les processus Python de la session. |

### Commandes magiques IPython / Jupyter

| Commande magique | Description |
| :--- | :--- |
| `%pdb on` | Ouvre automatiquement `ipdb` dès qu'une exception non interceptée se produit. |
| `%pdb off` | Désactive l'ouverture automatique du débogueur post-mortem. |
| `%debug` | Ouvre `ipdb` en mode post-mortem sur la dernière exception non gérée. |
