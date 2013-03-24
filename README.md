[Алгоритмы в биоинформатике] [bioinf]
============================

Структура репозитория
---------------------

```bash
.
└── README.md
└── lebedev
    └── pattern_matching
        └── kmp.py
        └── brute_force.py

```

Как измерить время работы алгоритма
----------------------------------

Чтобы **хорошо** измерить время работы алгоритма на некотором входе нужно
провести несколько измерений, исключить выбросы и посчитать среднее
оставшейся выборки. Ниже пример кода на Python, который иллюстрирует
данный подход:

```python
import time

import numpy as np


def measure(f, *args):
    num_iter = 1000
    timings = np.zeros(num_iter)

    for i in xrange(num_iter):
        tick = time.time()
        res = f(*args)  # Execute f.
        timings[i] = (time.time() - tick) * 1e6

        # Optionally check if ``res`` is correct.

    q1 = np.percentile(timings, 25)
    q3 = np.percentile(timings, 75)
    iqr = q3 - q1
    lo_extreme = q1 - 3 * iqr
    hi_extreme = q3 + 3 * iqr

    # Filter outliers and print mean execution time. See link for details:
    # http://www.itl.nist.gov/div898/handbook/prc/section1/prc16.htm
    mask = np.logical_and(timings >= lo_extreme, timings <= hi_extreme)
    solid = timings[mask]
    print("mean is {0} us ({1} solid timings, {2} outliers)"
          .format(solid.mean(), len(solid), num_iter - len(solid)))


if __name__ == "__main__":
    measure(lambda x: x**100500, 2)
```

Задание #1: pattern matching
----------------------------

* Реализовать четыре алгоритма поиска всех вхождений паттерна в текст:
   * brute-force
   * KMP (через prefix функцию)
   * KMP (через Z-функцию)
   * Rabin-Karp
* Написать программу (или скрипт), которая для заданных паттерна `P` и текста `T` выводит:
   * паттерн `P`
   * текст `T`
   * время работы каждого из алгоритмов на данном входе
* Для каждого алгоритма привести примеры входов, на котором он
   * лучше всех остальных
   * хуже всех остальных
   * (достаточно по одному на каждый случай)
   * (примеры входов должны быть поданы в формате результата выполнения вышеописанной программы или скрипта)


Задание #2: boyer-moore
-----------------------

* Добавить к четырём алгоритмам из предыдущего задания алгоритм Бойера-Мура.
  Реализовать эвристики:
   * bad character rule,
   * good suffix rule,
   * Galil rule.

  Освежить в памяти все эти словосочетания можно например в lecuture notes
  Дена [Гасфилда] [bm-gusfield] или в [Википедии] [bm-wiki]
* Найти (хотя бы один) пример на котором алгоритм Бойера-Мура работает
  быстрее чем KMP.

[bioinf]: http://bioinformaticsinstitute.ru/courses/bioalgo/2013/spring
[bm-gusfield]: http://www.cs.ucdavis.edu/~gusfield/cs224f09/bnotes.pdf
[bm-wiki]: http://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string_search_algorithm
