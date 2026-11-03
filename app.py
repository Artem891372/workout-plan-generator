import streamlit as st
import pandas as pd
import math
from collections import defaultdict
import io

# -------------------- CONFIG --------------------
EXERCISES = {
    "Жим лёжа": {
        "muscles": {
            "Грудь": 1.0, "Трицепс": 0.6, "Передняя дельта": 0.4, "Средняя дельта": 0.2, "Бицепс": 0.2
        },
        "type": "compound",
        "tut": (2, 4)
    },
    "Жим лёжа в наклоне": {
        "muscles": {
            "Грудь": 1.0, "Трицепс": 0.4, "Передняя дельта": 0.6, "Средняя дельта": 0.2, "Бицепс": 0.2
        },
        "type": "compound",
        "tut": (3, 5)
    },
    "Отжимания на брусьях": {
        "muscles": {
            "Грудь": 0.8, "Трицепс": 1.0, "Передняя дельта": 0.5, "Бицепс": 0.3
        },
        "type": "compound",
        "tut": (2, 4)
    },
    "Тяга в наклоне": {
        "muscles": {
            "Трапеция": 1.0, "Широчайшие": 0.3, "Задняя дельта": 0.3, "Плечелучевая": 0.3, "Разгибатели спины": 0.2, "Пресс":0.2
        },
        "type": "compound",
        "tut": (2, 4)
    },
    "Тяга вертикального блока": {
        "muscles": {
            "Широчайшие": 1.0, "Плечелучевая": 0.3, "Задняя дельта": 0.2
        },
        "type": "compound",
        "tut": (2, 4)
    },
    "Подтягивания": {
        "muscles": {
            "Широчайшие": 1.0, "Плечелучевая": 0.6, "Задняя дельта": 0.3, "Бицепс": 0.2
        },
        "type": "compound",
        "tut": (3, 5)
    },
    "Румынская тяга": {
        "muscles": {
            "Ягодицы": 1.0, "Бедра задняя": 0.8, "Разгибатели спины": 0.3, "Пресс": 0.3, "Косые": 0.1
        },
        "type": "compound",
        "tut": (3, 5)
    },
    "Присед": {
        "muscles": {
            "Квадрицепс": 1.0, "Ягодицы": 0.6, "Бедра задняя": 0.3, "Разгибатели спины": 0.3, "Пресс": 0.3, "Икроножные": 0.2, "Косые": 0.1
        },
        "type": "compound",
        "tut": (3, 5)
    },
    "Фронтальный присед": {
        "muscles": {
            "Квадрицепс": 1.0, "Ягодицы": 0.5, "Разгибатели спины": 0.2, "Пресс": 0.4, "Косые": 0.1
        },
        "type": "compound",
        "tut": (3, 5)
    },
    "Жим ногами": {
        "muscles": {
            "Квадрицепс": 1.0, "Ягодицы": 0.7, "Бедра задняя": 0.3, "Икроножные": 0.1
        },
        "type": "compound",
        "tut": (3, 5)
    },
    "Жим гантелей сидя": {
        "muscles": {
            "Передняя дельта": 1.0, "Средняя дельта": 0.4, "Трицепс": 0.3
        },
        "type": "compound",
        "tut": (2, 4)
    },
    "Жим стоя": {
        "muscles": {
            "Передняя дельта": 1.0, "Грудь": 0.4, "Средняя дельта": 0.2, "Трицепс": 0.4, "Разгибатели спины": 0.2, "Пресс": 0.2, "Косые": 0.1
        },
        "type": "compound",
        "tut": (3, 5)
    },
    "Становая тяга": {
        "muscles": {
            "Ягодицы": 1.0, "Бедра задняя": 0.9, "Трапеция": 0.4, "Разгибатели спины": 0.4, "Пресс": 0.4, "Косые": 0.2
        },
        "type": "compound",
        "tut": (3, 5)
    },
    "Жим штанги лежа узким хватом": {
        "muscles": {
            "Трицепс": 1.0, "Грудь": 0.6, "Передняя дельта": 0.4, "Бицепс": 0.2
        },
        "type": "compound",
        "tut": (2, 4)
    },
    "Сгибания на бицепс": {
        "muscles": {
            "Бицепс": 1.0, "Сгибатель предплечья": 0.3, "Плечелучевая": 0.2
        },
        "type": "isolation",
        "tut": (1, 3)
    },
    "Сгибания на бицепс с гантелями": {
        "muscles": {
            "Бицепс": 1.0, "Сгибатель предплечья": 0.2, "Плечелучевая": 0.3
        },
        "type": "isolation",
        "tut": (1, 3)
    },
    "Разгибания рук на блоке": {
        "muscles": {
            "Трицепс": 1.0, "Разгибатель предплечья": 0.2
        },
        "type": "isolation",
        "tut": (1, 3)
    },
    "Французский жим": {
        "muscles": {
            "Трицепс": 1.0, "Разгибатель предплечья": 0.2
        },
        "type": "isolation",
        "tut": (1, 3)
    },
    "Подъем на носки стоя": {
        "muscles": {
            "Икроножные": 1.0, "Большеберцовая": 0.3
        },
        "type": "isolation",
        "tut": (2, 5)
    },
    "Подъем на носки сидя": {
        "muscles": {
            "Икроножные": 1.0, "Большеберцовая": 0.2
        },
        "type": "isolation",
        "tut": (2, 5)
    },
    "Подъем на носки в тренажере": {
        "muscles": {
            "Икроножные": 1.0, "Большеберцовая": 0.3
        },
        "type": "isolation",
        "tut": (2, 5)
    },
    "Обратные сгибания стопы": {
        "muscles": {
            "Большеберцовая": 1.0
        },
        "type": "isolation",
        "tut": (1, 3)
    },
    "Тяга к лицу": {
        "muscles": {
            "Задняя дельта": 1.0, "Трапеция": 0.2
        },
        "type": "isolation",
        "tut": (1, 3)
    },
    "Разведения гантелей в наклоне": {
        "muscles": {
            "Задняя дельта": 1.0, "Трапеция": 0.2
        },
        "type": "isolation",
        "tut": (1, 3)
    },
    "Сгибания запястий со штангой": {
        "muscles": {
            "Сгибатель предплечья": 1.0
        },
        "type": "isolation",
        "tut": (1, 3)
    },
    "Разгибания запястий со штангой": {
        "muscles": {
            "Разгибатель предплечья": 1.0
        },
        "type": "isolation",
        "tut": (1, 3)
    },
    "Подъем штанги на бицепс обратным хватом": {
        "muscles": {
            "Разгибатель предплечья": 1.0, "Плечелучевая": 0.5
        },
        "type": "isolation",
        "tut": (1, 3)
    },
    "Фронтальный подъем гантелей": {
        "muscles": {
            "Передняя дельта": 1.0
        },
        "type": "isolation",
        "tut": (2, 4)
    },
    "Медиальный подъем гантелей": {
        "muscles": {
            "Средняя дельта": 1.0
        },
        "type": "isolation",
        "tut": (2, 4)
    },
    "Разгибания ног в тренажере": {
        "muscles": {
            "Квадрицепс": 1.0
        },
        "type": "isolation",
        "tut": (2, 4)
    },
    "Сгибания ног в тренажере": {
        "muscles": {
            "Бедра задняя": 1.0
        },
        "type": "isolation",
        "tut": (2, 4)
    },
    "Планка": {
        "muscles": {
            "Разгибатели спины": 0.2, "Пресс": 1, "Косые": 0.4
        },
        "type": "isolation",
        "tut": (30, 60)
    },
    "Скручивания": {
        "muscles": {
            "Пресс": 1, "Косые": 0.1
        },
        "type": "isolation",
        "tut": (2, 4)
    },
    "Подъем ног в висе": {
        "muscles": {
            "Пресс": 1, "Косые": 0.1
        },
        "type": "isolation",
        "tut": (2, 4)
    },
    "Разведения гантелей лёжа": {
        "muscles": {"Грудь": 1.0, "Передняя дельта": 0.2},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Разведения гантелей на наклонной скамье": {
        "muscles": {"Грудь": 1.0, "Передняя дельта": 0.4},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Кроссовер": {
        "muscles": {"Грудь": 1.0, "Передняя дельта": 0.2},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Отжимания от пола": {
        "muscles": {"Грудь": 1.0, "Трицепс": 0.5, "Передняя дельта": 0.4},
        "type": "compound",
        "tut": (3, 5)
    },
    "Тяга Т-грифа": {
        "muscles": {"Трапеция": 1.0, "Широчайшие": 0.5, "Задняя дельта": 0.3, "Разгибатели спины": 0.2, "Пресс":0.1},
        "type": "compound",
        "tut": (2, 4)
    },
    "Тяга гантели в наклоне": {
        "muscles": {"Широчайшие": 0.5, "Трапеция": 1, "Задняя дельта": 0.3},
        "type": "compound",
        "tut": (2, 4)
    },
    "Гиперэкстензия": {
        "muscles": {"Бедра задняя": 0.7, "Ягодицы": 1, "Разгибатели спины": 0.5},
        "type": "compound",
        "tut": (3, 5)
    },
    "Пуловер с гантелью": {
        "muscles": {"Трицепс": 1.0, "Широчайшие": 0.5},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Пуловер с верхнего блока": {
        "muscles": {"Широчайшие": 1.0, "Трицепс": 0.5},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Выпады": {
        "muscles": {"Квадрицепс": 1.0, "Ягодицы": 0.8, "Бедра задняя": 0.4, "Пресс": 0.3, "Косые": 0.3},
        "type": "compound",
        "tut": (3, 5)
    },
    "Болгарские выпады": {
        "muscles": {"Квадрицепс": 1.0, "Ягодицы": 0.8, "Бедра задняя": 0.2, "Пресс": 0.2, "Косые": 0.2},
        "type": "compound",
        "tut": (3, 5)
    },
    "Подъем таза (мостик)": {
        "muscles": {"Ягодицы": 1.0, "Бедра задняя": 0.5, "Пресс": 0.2},
        "type": "isolation",
        "tut": (2, 5)
    },
    "Жим Арнольда": {
        "muscles": {"Передняя дельта": 1.0, "Средняя дельта": 0.5, "Трицепс": 0.3},
        "type": "compound",
        "tut": (2, 4)
    },
    "Обратные махи в тренажёре (пек-дек)": {
        "muscles": {"Задняя дельта": 1.0, "Трапеция": 0.2},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Жим гантелей стоя": {
        "muscles": {"Передняя дельта": 1.0, "Средняя дельта": 0.5, "Трицепс": 0.3, "Разгибатели спины": 0.2, "Пресс": 0.2, "Косые": 0.1},
        "type": "compound",
        "tut": (2, 4)
    },
    "Молотковые сгибания": {
        "muscles": {"Плечелучевая": 1.0, "Бицепс": 0.6, "Разгибатель предплечья": 0.3},
        "type": "isolation",
        "tut": (1, 3)
    },
    "Русские повороты": {
        "muscles": {"Пресс": 1.0, "Косые": 0.5},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Велосипед": {
        "muscles": {"Пресс": 1.0, "Косые": 0.6},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Подъем корпуса на римском стуле": {
        "muscles": {"Пресс": 1.0, "Косые": 0.2},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Шраги": {
        "muscles": {"Трапеция": 1.0},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Жим в тренажере (Смит)": {
        "muscles": {"Грудь": 1.0, "Передняя дельта": 0.2, "Трицепс": 0.5},
        "type": "compound",
        "tut": (2, 4)
    },
    "Жим гантелей лёжа": {
        "muscles": {"Грудь": 1.0, "Трицепс": 0.6, "Передняя дельта": 0.2},
        "type": "compound",
        "tut": (2, 4)
    },
    "Жим гантелей на наклонной скамье": {
        "muscles": {"Грудь": 1.0, "Трицепс": 0.4, "Передняя дельта": 0.4, "Бицепс": 0.2},
        "type": "compound",
        "tut": (2, 4)
    },
    "Тяга горизонтального блока": {
        "muscles": {"Широчайшие": 0.4, "Трапеция": 1, "Задняя дельта": 0.3},
        "type": "compound",
        "tut": (2, 4)
    },
    "Подтягивания обратным хватом": {
        "muscles": {"Широчайшие": 1.0, "Бицепс": 0.5, "Сгибатель предплечья":0.3, "Плечелучевая": 0.2},
        "type": "compound",
        "tut": (3, 5)
    },
    "Тяга верхнего блока обратным хватом": {
        "muscles": {"Широчайшие": 1.0, "Бицепс": 0.4, "Сгибатель предплечья":0.2},
        "type": "compound",
        "tut": (2, 4)
    },
    "Гуд монинг": {
        "muscles": {"Бедра задняя": 0.8, "Ягодицы": 1, "Разгибатели спины": 0.6},
        "type": "compound",
        "tut": (3, 5)
    },
    "Становая на прямых ногах": {
        "muscles": {"Бедра задняя": 1.0, "Ягодицы": 0.8, "Разгибатели спины": 0.4},
        "type": "compound",
        "tut": (3, 5)
    },
    "Приседания в Смите": {
        "muscles": {"Квадрицепс": 1.0, "Ягодицы": 0.7, "Бедра задняя": 0.3},
        "type": "compound",
        "tut": (3, 5)
    },
    "Гакк-приседания": {
        "muscles": {"Квадрицепс": 1.0, "Ягодицы": 0.5},
        "type": "compound",
        "tut": (3, 5)
    },
    "Разгибания ног одной ногой": {
        "muscles": {"Квадрицепс": 1.0},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Сгибания ног лёжа": {
        "muscles": {"Бедра задняя": 1.0},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Тяга штанги к подбородку": {
        "muscles": {"Средняя дельта": 1.0, "Трапеция": 0.5, "Передняя дельта": 0.3},
        "type": "compound",
        "tut": (2, 4)
    },
    "Подъём гантелей через стороны в наклоне": {
        "muscles": {"Задняя дельта": 1.0, "Трапеция": 0.3},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Подъём одной гантели перед собой": {
        "muscles": {"Передняя дельта": 1.0},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Отжимания узким хватом": {
        "muscles": {"Трицепс": 1.0, "Грудь": 0.6, "Передняя дельта": 0.3},
        "type": "compound",
        "tut": (2, 4)
    },
    "Разгибания руки с гантелью из-за головы": {
        "muscles": {"Трицепс": 1.0},
        "type": "isolation",
        "tut": (1, 3)
    },
    "Разгибания одной рукой на блоке": {
        "muscles": {"Трицепс": 1.0},
        "type": "isolation",
        "tut": (1, 3)
    },
    "Сгибания с EZ-грифом": {
        "muscles": {"Бицепс": 1.0, "Сгибатель предплечья":0.3, "Плечелучевая": 0.3},
        "type": "isolation",
        "tut": (1, 3)
    },
    "Сгибания концентрированные (сидя)": {
        "muscles": {"Бицепс": 1.0, "Сгибатель предплечья":0.1},
        "type": "isolation",
        "tut": (1, 3)
    },
    "Скручивания на фитболе": {
        "muscles": {"Пресс": 1.0},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Скручивания на блоке (Молитва)": {
        "muscles": {"Пресс": 1.0},
        "type": "isolation",
        "tut": (2, 4)
    },
    "Боковая планка": {
        "muscles": {"Пресс": 1.0, "Косые": 0.6},
        "type": "isolation",
        "tut": (30, 60)
    },
    "Подъем коленей в упоре": {
        "muscles": {"Пресс": 1.0},
        "type": "isolation",
        "tut": (2, 4)
    },
    

}

DEFAULT_TARGET_VOLUME_MG = {
    "Грудь": {"min": 10.0, "max": 12.0, "category": "upper"},
    "Трапеция": {"min": 10.0, "max": 12.0, "category": "upper"},
    "Сгибатель предплечья": {"min": 8.0, "max": 10.0, "category": "upper"},
    "Разгибатель предплечья": {"min": 8.0, "max": 10.0, "category": "upper"},
    "Плечелучевая": {"min": 8.0, "max": 10.0, "category": "upper"},
    "Трицепс": {"min": 8.0, "max": 10.0, "category": "upper"},
    "Передняя дельта": {"min": 8.0, "max": 12.0, "category": "upper"},
    "Средняя дельта": {"min": 8.0, "max": 10.0, "category": "upper"},
    "Задняя дельта": {"min": 8.0, "max": 10.0, "category": "upper"},
    "Широчайшие": {"min": 10.0, "max": 12.0, "category": "upper"},
    "Бицепс": {"min": 8.0, "max": 10.0, "category": "upper"},
    "Ягодицы": {"min": 10.0, "max": 12.0, "category": "lower"},
    "Бедра задняя": {"min": 10.0, "max": 12.0, "category": "lower"},
    "Квадрицепс": {"min": 10.0, "max": 12.0, "category": "lower"},
    "Пресс": {"min": 5.0, "max": 15.0, "category": "core"},
    "Разгибатели спины": {"min": 5.0, "max": 15.0, "category": "core"},
    "Косые": {"min": 5.0, "max": 15.0, "category": "core"},
    "Икроножные": {"min": 8.0, "max": 10.0, "category": "lower"},
    "Большеберцовая": {"min": 6.0, "max": 8.0, "category": "lower"}
}

CARDIO = {"Бег": 2.0, "Ходьба": 1.0, "Велотренажер": 1.5, "Эллипсоид": 1.2}
STIM_FACTORS = {'light': 0.5, 'medium': 1.0, 'heavy': 1.5}
RPE_BY_TYPE = {'light': '3–5', 'medium': '6–7', 'heavy': '8–9'}
GOAL = 'hypertrophy'
GOAL_TUT = {
    'strength': (0.0, 15.0),
    'hypertrophy': (15.0, 40.0),
    'endurance': (40.0, 180.0)
}

# Ограничения, чтобы неделя не превращалась в 70 подходов за тренировку.
MAX_SETS_PER_DAY = 25
MAX_SETS_PER_EXERCISE_PER_DAY = 6
MAX_WEEKLY_SETS_PER_EXERCISE = 12
MAX_WEEKLY_SETS_PER_ISOLATION = 9

# Категории мышц для выбора упражнений и порядка в тренировке.
UPPER_MUSCLES = {mg for mg, data in DEFAULT_TARGET_VOLUME_MG.items() if data.get('category') == 'upper'}
LOWER_MUSCLES = {mg for mg, data in DEFAULT_TARGET_VOLUME_MG.items() if data.get('category') == 'lower'}
CORE_MUSCLES = {mg for mg, data in DEFAULT_TARGET_VOLUME_MG.items() if data.get('category') == 'core'}

PUSH_MUSCLES = {'Грудь', 'Трицепс', 'Передняя дельта', 'Средняя дельта'}
PULL_MUSCLES = {'Широчайшие', 'Трапеция', 'Задняя дельта', 'Бицепс',
                'Сгибатель предплечья', 'Разгибатель предплечья', 'Плечелучевая'}
LEGS_MUSCLES = LOWER_MUSCLES

# Крупные мышцы получают базовое (многосуставное) движение,
# мелкие — изолирующее на конкретную активацию.
LARGE_MUSCLES = {
    'Квадрицепс', 'Бедра задняя', 'Ягодицы', 'Широчайшие', 'Грудь',
    'Передняя дельта', 'Средняя дельта', 'Задняя дельта', 'Трапеция'
}
SMALL_MUSCLES = set(DEFAULT_TARGET_VOLUME_MG.keys()) - LARGE_MUSCLES
# Предплечья и большеберцовая — не приоритет для общего набора,
# добавляем их только если осталось место после базовых и основных изоляций.
LOW_PRIORITY_ACCESSORY = {
    'Сгибатель предплечья', 'Разгибатель предплечья', 'Плечелучевая', 'Большеберцовая'
}

MUSCLE_PRIORITY = [
    'Квадрицепс', 'Бедра задняя', 'Ягодицы', 'Широчайшие', 'Грудь',
    'Передняя дельта', 'Средняя дельта', 'Задняя дельта', 'Трапеция',
    'Бицепс', 'Трицепс', 'Икроножные', 'Пресс', 'Косые',
    'Разгибатели спины', 'Плечелучевая', 'Сгибатель предплечья',
    'Разгибатель предплечья', 'Большеберцовая'
]

# Разумный стартовый набор: крупные группы + руки + пресс.
# Пользователь может выбрать больше групп вручную.
DEFAULT_SELECTED_MUSCLES = [
    'Грудь', 'Широчайшие', 'Квадрицепс', 'Бедра задняя', 'Ягодицы',
    'Передняя дельта', 'Средняя дельта', 'Бицепс', 'Трицепс', 'Пресс'
]

# -------------------- UTILITY FUNCTIONS --------------------
def primary_muscle(ex_name, exercises=None):
    """Основная мышца упражнения (максимальный коэффициент вовлечённости)."""
    ex = (exercises or EXERCISES)[ex_name]
    return max(ex['muscles'], key=lambda mg: ex['muscles'][mg])

def display_exercise_name(ex_name):
    """Убирает скобки из названия для выгрузки: «(сидя)» → «— сидя»."""
    if '(' in ex_name:
        return ex_name.replace(' (', ' — ').replace(')', '')
    return ex_name

def muscle_sort_key(mg):
    """Порядок мышц: сначала крупные базовые, потом мелкие/изолирующие."""
    try:
        return MUSCLE_PRIORITY.index(mg)
    except ValueError:
        return len(MUSCLE_PRIORITY)

def weekly_set_cap(ex_name, ex_to_days, exercises):
    """Сколько подходов в неделю разумно давать одному упражнению."""
    days = len(ex_to_days.get(ex_name, []))
    if days == 0:
        return 0
    is_compound = exercises[ex_name]['type'] == 'compound'
    per_day = MAX_SETS_PER_EXERCISE_PER_DAY if is_compound else MAX_SETS_PER_EXERCISE_PER_DAY - 1
    weekly = MAX_WEEKLY_SETS_PER_EXERCISE if is_compound else MAX_WEEKLY_SETS_PER_ISOLATION
    return max(days, min(days * per_day, weekly))

def mg_volume_from_allocation(allocation, exercises, target_volume_mg):
    """Объём считается по рабочим подходам (базовые подходы × вовлечённость)."""
    volume = {mg: 0.0 for mg in target_volume_mg}
    for ex_name, sets in allocation.items():
        for mg, coefficient in exercises[ex_name]['muscles'].items():
            if mg in volume:
                volume[mg] += sets * coefficient
    return volume

def split_set_types(total_sets):
    """Делит подходы на тяжёлые/средние/лёгкие так, чтобы средний стимул был ~1.0."""
    if total_sets <= 0:
        return []
    heavy = total_sets // 3
    light = total_sets // 3
    medium = total_sets - heavy - light
    result = []
    if heavy:
        result.append(('heavy', heavy))
    if medium:
        result.append(('medium', medium))
    if light:
        result.append(('light', light))
    return result

def order_day_items(items, exercises):
    """Сначала базовые движения, затем изолирующие на конкретную активацию."""
    grouped = {}
    for item in items:
        grouped.setdefault(item[0], []).append(item)

    for ex_name in grouped:
        grouped[ex_name].sort(key=lambda x: {'heavy': 0, 'medium': 1, 'light': 2}[x[2]])

    compounds = [ex for ex in grouped if exercises[ex]['type'] == 'compound']
    isolations = [ex for ex in grouped if exercises[ex]['type'] != 'compound']

    def sort_key(ex_name):
        return (
            muscle_sort_key(primary_muscle(ex_name, exercises)),
            -sum(item[1] for item in grouped[ex_name])
        )

    compounds.sort(key=sort_key)
    isolations.sort(key=sort_key)

    ordered = []
    for ex_name in compounds + isolations:
        ordered.extend(grouped[ex_name])
    return ordered

def week_intensity_pct(week, progression_type):
    """Ориентир нагрузки в %1ПМ: плавно растёт, в волне есть разгрузка."""
    if progression_type == 'wave':
        cycle = week // 3
        cycle_week = week % 3
        return min(85.0, 65.0 + cycle * 1.5 + cycle_week * 5.0)
    return min(85.0, 65.0 + week * 2.0)

def set_load_pct(week, progression_type, set_type):
    base = week_intensity_pct(week, progression_type)
    if set_type == 'heavy':
        return min(95.0, base + 5.0)
    if set_type == 'light':
        return max(50.0, base - 10.0)
    return base

def is_deload_week(week, progression_type):
    return progression_type == 'wave' and week > 0 and week % 3 == 0


def make_week_schedule(train_days: int, pattern: str = 'consecutive'):
    if pattern == 'cycle_2on2off' and train_days == 4:
        return [True, True, False, False, True, True, False]
    return [True if i < train_days else False for i in range(7)]

def list_training_days(schedule):
    return [i for i, t in enumerate(schedule) if t]

def group_exercises_by_muscle():
    mg_to_exs = defaultdict(list)
    for ex_name, ex in EXERCISES.items():
        for mg, c in ex['muscles'].items():
            if c == 1.0:
                mg_to_exs[mg].append(ex_name)
    return mg_to_exs

def analyze_volume_shortfalls(mg_total_volume, target_volume_mg, exercises, ex_week_sets, ex_to_days):
    """
    Анализирует причины недостижения целевых объемов по мышечным группам
    """
    shortfall_analysis = {}
    
    for mg, actual_volume in mg_total_volume.items():
        if mg not in target_volume_mg:
            continue
            
        min_target = target_volume_mg[mg]['min']
        max_target = target_volume_mg[mg]['max']
        
        if actual_volume < min_target:
            # Анализируем причины недостаточного объема
            reasons = []
            
            # 1. Ищем упражнения, которые затрагивают эту МГ
            relevant_exercises = []
            for ex_name, ex_data in exercises.items():
                if mg in ex_data['muscles']:
                    involvement = ex_data['muscles'][mg]
                    weekly_sets = ex_week_sets.get(ex_name, 0)
                    if weekly_sets > 0:
                        relevant_exercises.append({
                            'exercise': ex_name,
                            'involvement': involvement,
                            'weekly_sets': weekly_sets,
                            'days': ex_to_days.get(ex_name, [])
                        })
            
            # 2. Анализируем ограничения
            if not relevant_exercises:
                reasons.append("⚠️ В выбранном наборе нет упражнения с прямой нагрузкой на эту группу")
            else:
                total_potential = sum(ex['involvement'] * ex['weekly_sets'] for ex in relevant_exercises)
                
                if total_potential < min_target:
                    reasons.append(f"❌ Недостаточно общего объема: {total_potential:.1f} из {min_target:.1f}")
                    capped = [
                        ex for ex in relevant_exercises
                        if ex['weekly_sets'] >= weekly_set_cap(ex['exercise'], ex_to_days, exercises)
                    ]
                    if len(capped) == len(relevant_exercises):
                        reasons.append("ℹ️ Упражнения уже на пределе недельного объёма — дальше прогрессия идёт за счёт нагрузки (%1ПМ)")
                    else:
                        reasons.append("ℹ️ Объём можно добрать подходами на уже выбранных упражнениях — добавлять новые упражнения не нужно")
                
                # Проверяем ограничения по дням тренировок
                training_days_with_mg = set()
                for ex in relevant_exercises:
                    training_days_with_mg.update(ex['days'])
                
                if len(training_days_with_mg) < 2 and min_target > 8:
                    reasons.append(f"⚠️ Ограниченное количество тренировочных дней: {len(training_days_with_mg)}")
                
                # Проверяем эффективность упражнений
                high_involvement_exercises = [ex for ex in relevant_exercises if ex['involvement'] >= 0.8]
                if not high_involvement_exercises:
                    reasons.append("⚠️ Прямая вовлечённость низкая: объём набирается второстепенными движениями")
                
                # Детали по упражнениям
                exercise_details = []
                for ex in relevant_exercises:
                    contribution = ex['involvement'] * ex['weekly_sets']
                    exercise_details.append(
                        f"{display_exercise_name(ex['exercise'])} — "
                        f"{contribution:.1f} через {ex['weekly_sets']} подходов"
                    )
                
                reasons.append(f"📊 Вклад упражнений: {', '.join(exercise_details)}")
            
            shortfall_analysis[mg] = {
                'actual_volume': actual_volume,
                'min_target': min_target,
                'max_target': max_target,
                'reasons': reasons,
                'relevant_exercises': relevant_exercises
            }
    
    return shortfall_analysis

def _pick_session_exercises(session_muscles, cap, exercises):
    """
    Подбирает упражнения на одну тренировочную сессию.

    Сначала выбираются базовые движения под крупные мышцы, затем — изолирующие
    упражнения на конкретную активацию. Ничего не добавляется «из пула» сверх
    лимита: набор остаётся компактным, а объём потом распределяется по нему.
    """
    session_muscles = set(session_muscles)
    if not session_muscles or cap <= 0:
        return []

    chosen = []
    used_primary_compounds = set()

    def covered(mg):
        return any(exercises[e]['muscles'].get(mg, 0.0) >= 0.8 for e in chosen)

    def has_isolation(mg):
        return any(
            exercises[e]['type'] == 'isolation' and exercises[e]['muscles'].get(mg, 0.0) >= 0.8
            for e in chosen
        )

    def add(ex_name):
        chosen.append(ex_name)
        if exercises[ex_name]['type'] == 'compound':
            used_primary_compounds.add(primary_muscle(ex_name, exercises))

    # Этап 1. По одному базовому движению на каждую крупную мышцу.
    max_compounds = max(2, math.ceil(cap * 0.6))
    max_compounds = min(max_compounds, max(1, cap - 1))
    for mg in [m for m in MUSCLE_PRIORITY if m in session_muscles and m in LARGE_MUSCLES]:
        if len(chosen) >= max_compounds:
            break
        if covered(mg):
            continue
        best = None
        best_score = 0.0
        for ex_name, ex_data in exercises.items():
            if ex_name in chosen or ex_data['type'] != 'compound':
                continue
            coefficient = ex_data['muscles'].get(mg, 0.0)
            if coefficient < 0.8:
                continue
            if primary_muscle(ex_name, exercises) in used_primary_compounds:
                continue
            if not any(m in session_muscles for m in ex_data['muscles']):
                continue
            score = coefficient * 5.0
            if primary_muscle(ex_name, exercises) == mg:
                score += 3.0
            score += sum(v for m, v in ex_data['muscles'].items() if m in session_muscles) * 0.4
            if score > best_score:
                best_score = score
                best = ex_name
        if best:
            add(best)

    # Этап 2. Добираем базовые движения, которые закрывают ещё не закрытые мышцы.
    while len(chosen) < max_compounds:
        best = None
        best_score = 0.0
        for ex_name, ex_data in exercises.items():
            if ex_name in chosen or ex_data['type'] != 'compound':
                continue
            if primary_muscle(ex_name, exercises) in used_primary_compounds:
                continue
            if not any(m in session_muscles for m in ex_data['muscles']):
                continue
            # Базовыми движениями закрываем только крупные мышцы.
            # Мелкие (руки, икры, пресс) добираем изоляцией — так меньше лишних упражнений.
            new_coverage = sum(
                coefficient for mg, coefficient in ex_data['muscles'].items()
                if mg in session_muscles and mg in LARGE_MUSCLES
                and coefficient >= 0.8 and not covered(mg)
            )
            if new_coverage <= 0:
                continue
            score = new_coverage * 2.0 + sum(
                v for m, v in ex_data['muscles'].items() if m in session_muscles
            )
            if score > best_score:
                best_score = score
                best = ex_name
        if not best:
            break
        add(best)

    # Этап 3. Изолирующие упражнения: сначала на незакрытые крупные мышцы,
    # затем на мелкие, затем — на конкретную активацию уже закрытых мышц.
    priorities = []
    for mg in [m for m in MUSCLE_PRIORITY if m in session_muscles and m in LARGE_MUSCLES]:
        if not covered(mg):
            priorities.append((0, mg))
    for mg in [m for m in MUSCLE_PRIORITY if m in session_muscles and m in SMALL_MUSCLES
               and m not in LOW_PRIORITY_ACCESSORY]:
        if not covered(mg):
            priorities.append((1, mg))
    for mg in [m for m in MUSCLE_PRIORITY if m in session_muscles and m in LARGE_MUSCLES]:
        if not has_isolation(mg):
            priorities.append((2, mg))
    for mg in [m for m in MUSCLE_PRIORITY if m in session_muscles and m in SMALL_MUSCLES
               and m not in LOW_PRIORITY_ACCESSORY]:
        if not has_isolation(mg):
            priorities.append((3, mg))
    # Предплечья/большеберцовая — только если осталось место.
    for mg in [m for m in MUSCLE_PRIORITY if m in session_muscles and m in LOW_PRIORITY_ACCESSORY]:
        if not has_isolation(mg):
            priorities.append((4, mg))

    seen = set()
    for _, mg in priorities:
        if len(chosen) >= cap:
            break
        if mg in seen:
            continue
        seen.add(mg)
        if has_isolation(mg):
            continue
        best = None
        best_score = 0.0
        for ex_name, ex_data in exercises.items():
            if ex_name in chosen or ex_data['type'] != 'isolation':
                continue
            coefficient = ex_data['muscles'].get(mg, 0.0)
            if coefficient < 0.8:
                continue
            total_involvement = sum(ex_data['muscles'].values()) or 1.0
            specificity = coefficient / total_involvement
            score = coefficient * 5.0 + specificity * 2.0
            if primary_muscle(ex_name, exercises) == mg:
                score += 3.0
            score += sum(v for m, v in ex_data['muscles'].items() if m in session_muscles) * 0.15
            if score > best_score:
                best_score = score
                best = ex_name
        if best:
            add(best)

    # Этап 4. Если осталось место и крупная мышца всё ещё без прямого движения.
    for mg in [m for m in MUSCLE_PRIORITY if m in session_muscles and m in LARGE_MUSCLES]:
        if len(chosen) >= cap:
            break
        if covered(mg):
            continue
        best = None
        best_score = 0.0
        for ex_name, ex_data in exercises.items():
            if ex_name in chosen or ex_data['type'] != 'compound':
                continue
            coefficient = ex_data['muscles'].get(mg, 0.0)
            if coefficient < 0.8:
                continue
            if primary_muscle(ex_name, exercises) in used_primary_compounds:
                continue
            score = coefficient * 5.0 + sum(
                v for m, v in ex_data['muscles'].items() if m in session_muscles
            ) * 0.3
            if score > best_score:
                best_score = score
                best = ex_name
        if best:
            add(best)

    return chosen

def select_balanced_exercises(selected_muscles, split, train_days, exercises):
    """Компактный сбалансированный набор упражнений под выбранный сплит."""
    selected = set(selected_muscles)
    if not selected:
        return {}

    sessions = []
    if split == 'full_body':
        cap = min(9, max(4, len(selected) + 1))
        sessions.append((selected, cap))
    elif split == 'upper_lower':
        upper = selected & UPPER_MUSCLES
        lower = selected & LOWER_MUSCLES
        core = selected & CORE_MUSCLES
        cap_upper = min(7, max(3, len(upper) + 1))
        cap_lower = min(6, max(3, len(lower) + len(core) + 1))
        sessions.append((upper, cap_upper))
        sessions.append((lower | core, cap_lower))
    else:  # push_pull_legs
        push = selected & PUSH_MUSCLES
        pull = selected & PULL_MUSCLES
        legs = selected & LEGS_MUSCLES
        cap_push = min(5, max(3, len(push) + 1))
        cap_pull = min(5, max(3, len(pull) + 1))
        cap_legs = min(5, max(3, len(legs) + 1))
        sessions.append((push, cap_push))
        sessions.append((pull, cap_pull))
        sessions.append((legs, cap_legs))

    chosen = []
    for muscles, cap in sessions:
        for ex_name in _pick_session_exercises(muscles, cap, exercises):
            if ex_name not in chosen:
                chosen.append(ex_name)

    # Кор на PPL не образует отдельный день — добавляем 1–2 упражнения,
    # они будут стоять во все тренировочные дни как активация.
    if split == 'push_pull_legs':
        core = selected & CORE_MUSCLES
        if core:
            for ex_name in _pick_session_exercises(core, min(2, max(1, len(core))), exercises):
                if ex_name not in chosen:
                    chosen.append(ex_name)

    return {ex_name: exercises[ex_name] for ex_name in chosen}

def select_exercises_interactively(selected_muscles, use_custom_selection=False,
                                   split='full_body', train_days=3):
    if use_custom_selection and st.session_state.get('selected_exercises_custom'):
        # Используем кастомный выбор упражнений, если он реально задан
        return st.session_state.selected_exercises_custom

    # Автоматический выбор: не «по упражнению на каждую мышцу из пула»,
    # а компактный набор «базовое движение + изоляция на активацию».
    return select_balanced_exercises(selected_muscles, split, train_days, EXERCISES)

def allocate_weekly_sets(exercises, target_volume_mg, train_days_idx, ex_to_days,
                         prev_allocation=None, max_changes=None):
    """
    Распределяет недельный объём по упражнениям.

    Ключевые отличия от старого алгоритма:
    - не раздаёт всем упражнениям по подходу на каждый день «просто так»;
    - начинает с 1 подхода на запланированный день (чтобы упражнение не исчезло);
    - добирает подходы туда, где реально есть дефицит объёма;
    - за одну неделю меняет ограниченное число подходов, поэтому нет скачков.
    """
    if not exercises:
        return {}, {mg: 0.0 for mg in target_volume_mg}

    days_count = {ex: len(ex_to_days.get(ex, [])) for ex in exercises}
    baseline = {ex: days_count[ex] for ex in exercises}

    if prev_allocation is None:
        allocation = dict(baseline)
    else:
        allocation = {
            ex: max(0, int(prev_allocation.get(ex, baseline[ex])))
            for ex in exercises
        }

    caps = {ex: weekly_set_cap(ex, ex_to_days, exercises) for ex in exercises}
    weekly_capacity = MAX_SETS_PER_DAY * max(1, len(train_days_idx))
    volume = mg_volume_from_allocation(allocation, exercises, target_volume_mg)
    changes = 0
    change_limit = max_changes if max_changes is not None else 10 ** 9

    # Сначала убираем лишнее, если цель снизилась (например, разгрузочная неделя).
    if prev_allocation is not None:
        while changes < change_limit:
            over = {mg: max(0.0, volume[mg] - target_volume_mg[mg]['max']) for mg in target_volume_mg}
            if not any(value > 0.01 for value in over.values()):
                break
            best = None
            best_score = 0.0
            for ex_name, sets in allocation.items():
                if sets <= baseline[ex_name]:
                    continue
                benefit = 0.0
                penalty = 0.0
                for mg, coefficient in exercises[ex_name]['muscles'].items():
                    if mg not in target_volume_mg:
                        continue
                    if over[mg] > 0:
                        benefit += min(over[mg], coefficient)
                    if volume[mg] - coefficient < target_volume_mg[mg]['min']:
                        penalty += min(target_volume_mg[mg]['min'] - (volume[mg] - coefficient), coefficient)
                score = benefit - 2.0 * penalty
                if score > best_score:
                    best_score = score
                    best = ex_name
            if best is None:
                break
            allocation[best] -= 1
            volume = mg_volume_from_allocation(allocation, exercises, target_volume_mg)
            changes += 1

    # Затем добираем подходы до минимальных целей.
    while changes < change_limit:
        deficits = {
            mg: max(0.0, target_volume_mg[mg]['min'] - volume[mg])
            for mg in target_volume_mg
        }
        if not any(value > 0.01 for value in deficits.values()):
            break
        if sum(allocation.values()) >= weekly_capacity:
            break

        best = None
        best_score = 0.0
        for ex_name, sets in allocation.items():
            if sets >= caps[ex_name]:
                continue
            gain = 0.0
            overflow = 0.0
            for mg, coefficient in exercises[ex_name]['muscles'].items():
                if mg not in target_volume_mg:
                    continue
                gain += min(deficits[mg], coefficient)
                overflow += max(0.0, volume[mg] + coefficient - target_volume_mg[mg]['max'])
            # Небольшой штраф за перекос: не отдаём все подходы одному упражнению.
            diminishing = 1.0 + 0.08 * max(0, sets - days_count[ex_name])
            score = gain / diminishing - 3.0 * overflow
            if exercises[ex_name]['type'] == 'compound':
                score *= 1.08
            if score > best_score:
                best_score = score
                best = ex_name
        if best is None:
            break
        allocation[best] += 1
        volume = mg_volume_from_allocation(allocation, exercises, target_volume_mg)
        changes += 1

    return allocation, volume

def force_progress_step(allocation, volume, target_volume_mg, exercises, ex_to_days,
                        train_days_idx):
    """Гарантирует один новый подход за неделю, если есть реальный дефицит объёма."""
    if sum(allocation.values()) >= MAX_SETS_PER_DAY * max(1, len(train_days_idx)):
        return allocation, volume

    deficits = {
        mg: max(0.0, target_volume_mg[mg]['min'] - volume[mg])
        for mg in target_volume_mg
    }
    if not any(value > 0.01 for value in deficits.values()):
        return allocation, volume

    caps = {ex: weekly_set_cap(ex, ex_to_days, exercises) for ex in exercises}
    best = None
    best_score = 0.0
    for ex_name, sets in allocation.items():
        if sets >= caps[ex_name]:
            continue
        gain = 0.0
        overflow = 0.0
        for mg, coefficient in exercises[ex_name]['muscles'].items():
            if mg not in target_volume_mg:
                continue
            gain += min(deficits[mg], coefficient)
            overflow += max(0.0, volume[mg] + coefficient - target_volume_mg[mg]['max'])
        if gain <= 0:
            continue
        score = gain / (1.0 + 0.08 * max(0, sets - len(ex_to_days.get(ex_name, [])))) - 3.0 * overflow
        if exercises[ex_name]['type'] == 'compound':
            score *= 1.08
        if score > best_score:
            best_score = score
            best = ex_name
    if best:
        allocation[best] += 1
        volume = mg_volume_from_allocation(allocation, exercises, target_volume_mg)
    return allocation, volume

def assign_exercise_days_by_split(exercises, train_days_idx, split):
    ex_to_days = {}

    if split == 'full_body':
        for ex in exercises.keys():
            ex_to_days[ex] = list(train_days_idx)

    elif split == 'upper_lower':
        for ex, data in exercises.items():
            primary_mg = primary_muscle(ex, exercises)
            if primary_mg in UPPER_MUSCLES:
                days = [train_days_idx[i] for i in range(0, len(train_days_idx), 2)]
            elif primary_mg in LOWER_MUSCLES or primary_mg in CORE_MUSCLES:
                days = [train_days_idx[i] for i in range(1, len(train_days_idx), 2)]
            else:
                days = list(train_days_idx)
            ex_to_days[ex] = days or list(train_days_idx)

    elif split == 'push_pull_legs':
        for ex, data in exercises.items():
            primary_mg = primary_muscle(ex, exercises)
            if primary_mg in PUSH_MUSCLES:
                days = [train_days_idx[i] for i in range(0, len(train_days_idx), 3)]
            elif primary_mg in PULL_MUSCLES:
                days = [train_days_idx[i] for i in range(1, len(train_days_idx), 3)]
            elif primary_mg in LEGS_MUSCLES:
                days = [train_days_idx[i] for i in range(2, len(train_days_idx), 3)]
            elif primary_mg in CORE_MUSCLES:
                # Кор — активация на каждой тренировке.
                days = list(train_days_idx)
            else:
                days = list(train_days_idx)
            # Для 2 тренировочных дней PPL ноги могут не получить свой день.
            ex_to_days[ex] = days or [train_days_idx[-1]]

    return ex_to_days

def _session_day_groups(train_days_idx, split):
    if split == 'upper_lower' and len(train_days_idx) >= 2:
        return [train_days_idx[0::2], train_days_idx[1::2]]
    if split == 'push_pull_legs':
        return [[d] for d in train_days_idx]
    return [list(train_days_idx)]

def _balance_group(per_day, group, ex_to_days):
    """Выравнивает подходы между однотипными днями (например, двумя верхами)."""
    for _ in range(200):
        totals = {d: sum(per_day[d].values()) for d in group}
        high_day = max(group, key=lambda d: totals[d])
        low_day = min(group, key=lambda d: totals[d])
        if totals[high_day] - totals[low_day] <= 1:
            break

        candidates = [
            (ex, sets) for ex, sets in per_day[high_day].items()
            if sets > 0 and low_day in ex_to_days.get(ex, [])
        ]
        if not candidates:
            break
        ex_name, _ = max(candidates, key=lambda item: item[1])
        per_day[high_day][ex_name] -= 1
        if per_day[high_day][ex_name] == 0:
            del per_day[high_day][ex_name]
        per_day[low_day][ex_name] = per_day[low_day].get(ex_name, 0) + 1

def _trim_day_caps(per_day, train_days_idx, exercises):
    """Страховка от 30+ подходов в один день: убираем лишнее с изоляции."""
    for day in train_days_idx:
        while sum(per_day[day].values()) > MAX_SETS_PER_DAY:
            candidates = [
                (ex, sets) for ex, sets in per_day[day].items() if sets > 0
            ]
            if not candidates:
                break
            ex_name, _ = max(
                candidates,
                key=lambda item: (exercises[item[0]]['type'] == 'isolation', item[1])
            )
            per_day[day][ex_name] -= 1
            if per_day[day][ex_name] == 0:
                del per_day[day][ex_name]

def _equalize_day_totals(per_day, train_days_idx, exercises, ex_to_days):
    """
    Выравнивает общий объём между днями.

    Для верх/низ и PPL это важно: иначе верх получается на 25 подходов,
    а низ — на 15. Переносим часть подходов с перегруженного дня на недогруженный,
    не меняя общий недельный объём.
    """
    if len(train_days_idx) <= 1:
        return

    caps = {ex: weekly_set_cap(ex, ex_to_days, exercises) for ex in exercises}
    for _ in range(200):
        totals = {day: sum(per_day[day].values()) for day in train_days_idx}
        high_day = max(train_days_idx, key=lambda day: totals[day])
        low_day = min(train_days_idx, key=lambda day: totals[day])
        if totals[high_day] - totals[low_day] <= 2:
            break

        # Сначала пробуем перенести подход того же упражнения на другой день.
        moved = False
        for ex_name, sets in sorted(per_day[high_day].items(), key=lambda item: -item[1]):
            if sets > 0 and low_day in ex_to_days.get(ex_name, []):
                per_day[high_day][ex_name] -= 1
                if per_day[high_day][ex_name] == 0:
                    del per_day[high_day][ex_name]
                per_day[low_day][ex_name] = per_day[low_day].get(ex_name, 0) + 1
                moved = True
                break
        if moved:
            continue

        # Если упражнения не пересекаются по дням — переносим объём между
        # упражнениями: снимаем с изоляции перегруженного дня, добавляем
        # упражнению недогруженного дня, у которого есть запас по лимиту.
        donors = []
        for ex_name, sets in per_day[high_day].items():
            if sets <= 0:
                continue
            weekly_sets = sum(per_day[day].get(ex_name, 0) for day in train_days_idx)
            min_weekly = max(1, min(2, len(ex_to_days.get(ex_name, []))))
            if weekly_sets - 1 >= min_weekly:
                donors.append((ex_name, sets))
        if not donors:
            break
        donor, _ = max(
            donors,
            key=lambda item: (exercises[item[0]]['type'] == 'isolation', item[1])
        )

        recipients = []
        for ex_name in per_day[low_day]:
            weekly_sets = sum(per_day[day].get(ex_name, 0) for day in train_days_idx)
            room = caps.get(ex_name, 0) - weekly_sets
            if room > 0:
                recipients.append((ex_name, room))
        if not recipients:
            break
        recipient, _ = max(
            recipients,
            key=lambda item: (item[1], exercises[item[0]]['type'] == 'isolation')
        )

        per_day[high_day][donor] -= 1
        if per_day[high_day][donor] == 0:
            del per_day[high_day][donor]
        per_day[low_day][recipient] = per_day[low_day].get(recipient, 0) + 1

def distribute_weekly_sets(allocation, ex_to_days, train_days_idx, exercises, split, week=0):
    """Равномерно раскладывает недельные подходы по тренировочным дням."""
    per_day = {d: {} for d in train_days_idx}

    ordered_exercises = sorted(
        allocation.items(),
        key=lambda item: (muscle_sort_key(primary_muscle(item[0], exercises)), item[0])
    )
    for index, (ex_name, total_sets) in enumerate(ordered_exercises):
        days = ex_to_days.get(ex_name, [])
        if total_sets <= 0 or not days:
            continue
        n = len(days)
        base_sets = total_sets // n
        remainder = total_sets % n
        start = (week + index) % n
        for position, day in enumerate(days):
            sets = base_sets + (1 if (position - start) % n < remainder else 0)
            if sets > 0:
                per_day[day][ex_name] = per_day[day].get(ex_name, 0) + sets

    for group in _session_day_groups(train_days_idx, split):
        if len(group) > 1:
            _balance_group(per_day, group, ex_to_days)

    _equalize_day_totals(per_day, train_days_idx, exercises, ex_to_days)
    _trim_day_caps(per_day, train_days_idx, exercises)
    return per_day

def build_days_info(per_day, exercises, target_volume_mg):
    """Собирает описание дней и считает объём по рабочим подходам."""
    days_info = {}
    mg_total_volume = {mg: 0.0 for mg in target_volume_mg}

    for day in sorted(per_day.keys()):
        items = []
        set_types = {'light': 0, 'medium': 0, 'heavy': 0}

        for ex_name, total_sets in per_day[day].items():
            if total_sets <= 0:
                continue
            for set_type, count in split_set_types(total_sets):
                perf = round(count * STIM_FACTORS[set_type])
                items.append((ex_name, count, set_type, perf))
                set_types[set_type] += count

            for mg, coefficient in exercises[ex_name]['muscles'].items():
                if mg in mg_total_volume:
                    mg_total_volume[mg] += total_sets * coefficient

        items = order_day_items(items, exercises)
        days_info[day] = {
            'items': items,
            'total_stim': sum(item[3] for item in items),
            'set_types': set_types
        }

    return days_info, mg_total_volume

EXERCISE_TYPE_LABELS = {
    'compound': 'Базовое',
    'isolation': 'Изолирующее'
}
SET_TYPE_LABELS = {
    'heavy': 'Тяжёлый',
    'medium': 'Средний',
    'light': 'Лёгкий'
}
VOLUME_STATUS_LABELS = {
    'ok': 'В норме',
    'low': 'Ниже цели',
    'high': 'Выше цели'
}

EXPORT_COLUMNS = [
    'День', 'Упражнение', 'Тип упражнения', 'Тип подхода', 'Подходы',
    'RPE', 'Повторения', 'Диапазон повторений', 'Целевой TUT, с',
    'Нагрузка, %1ПМ', 'Стимул, усл. ед.'
]
SUMMARY_COLUMNS = [
    'Неделя', 'Всего подходов', 'Лёгкие', 'Средние', 'Тяжёлые',
    'Интенсивность, %1ПМ', 'Разгрузка', 'Примечание'
]
VOLUME_COLUMNS = [
    'Мышечная группа', 'Объём', 'Целевой минимум',
    'Целевой максимум', 'Статус'
]
SET_TYPE_COLUMNS = [
    'День', 'Лёгкие подходы', 'Средние подходы',
    'Тяжёлые подходы', 'Всего подходов', 'Общая стимуляция'
]

def build_export_dataframe(days_info, exercises, week, progression_type):
    """Русская таблица для выгрузки: без скобок, диапазоны через тире."""
    rows = []
    for day in sorted(days_info.keys()):
        for ex_name, sets, set_type, perf in days_info[day]['items']:
            rec = recommend_reps_for_exercise(ex_name, exercises, GOAL)
            if rec['est_reps'] is not None:
                reps = rec['est_reps']
                low, high = rec['range']
                rep_range = f"{low}–{high}"
            else:
                reps = "—"
                hold_low, hold_high = rec['hold_time_s']
                rep_range = f"{hold_low:g}–{hold_high:g} с"

            rows.append({
                'День': day + 1,
                'Упражнение': display_exercise_name(ex_name),
                'Тип упражнения': EXERCISE_TYPE_LABELS.get(
                    exercises[ex_name]['type'], exercises[ex_name]['type']
                ),
                'Тип подхода': SET_TYPE_LABELS.get(set_type, set_type),
                'Подходы': sets,
                'RPE': RPE_BY_TYPE[set_type],
                'Повторения': reps,
                'Диапазон повторений': rep_range,
                'Целевой TUT, с': rec['target_tut_s'],
                'Нагрузка, %1ПМ': set_load_pct(week, progression_type, set_type),
                'Стимул, усл. ед.': perf
            })

    return pd.DataFrame(rows, columns=EXPORT_COLUMNS)

def get_export_dataframe(plan, exercises):
    """Возвращает русскую таблицу даже для старых планов без export_df."""
    export_df = plan.get('export_df')
    if export_df is None:
        export_df = build_export_dataframe(
            plan['days_info'], exercises, plan['week'] - 1,
            plan.get('progression_type', 'linear')
        )
    return export_df

def _excel_title(ws, title, subtitle, ncols):
    from openpyxl.styles import Alignment, Font

    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncols)
    cell = ws.cell(row=1, column=1, value=title)
    cell.font = Font(bold=True, size=16, color='1F4E78')
    cell.alignment = Alignment(horizontal='left', vertical='center')
    ws.row_dimensions[1].height = 26

    if subtitle:
        ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
        cell = ws.cell(row=2, column=1, value=subtitle)
        cell.font = Font(size=10, color='666666')
        cell.alignment = Alignment(horizontal='left', vertical='center')
    ws.row_dimensions[2].height = 18
    ws.row_dimensions[3].height = 6

def _excel_style_table(ws, header_row, data_start, data_end, ncols,
                       day_col=None, exercise_col=None, status_col=None,
                       left_cols=None, widths=None):
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.properties import PageSetupProperties

    left_cols = left_cols or set()
    header_fill = PatternFill('solid', fgColor='1F4E78')
    header_font = Font(bold=True, color='FFFFFF', size=11)
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    thin_side = Side(style='thin', color='B4C6E7')
    medium_side = Side(style='medium', color='1F4E78')
    thin_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
    fill_white = PatternFill('solid', fgColor='FFFFFF')
    fill_blue = PatternFill('solid', fgColor='EAF1FB')

    for col in range(1, ncols + 1):
        cell = ws.cell(row=header_row, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
        cell.border = Border(
            left=thin_side, right=thin_side, top=medium_side, bottom=medium_side
        )
    ws.row_dimensions[header_row].height = 34

    ws.freeze_panes = f'A{header_row + 1}'
    ws.auto_filter.ref = f'A{header_row}:{get_column_letter(ncols)}{data_end}'
    ws.print_title_rows = f'{header_row}:{header_row}'
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = 'landscape'
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)

    current_day = None
    group_index = 0
    for row in range(data_start, data_end + 1):
        if day_col is not None:
            day_value = ws.cell(row=row, column=day_col).value
            if day_value != current_day:
                current_day = day_value
                group_index += 1
            fill = fill_blue if group_index % 2 == 1 else fill_white
        else:
            fill = fill_blue if (row - data_start) % 2 == 0 else fill_white

        for col in range(1, ncols + 1):
            cell = ws.cell(row=row, column=col)
            cell.fill = fill
            cell.border = thin_border
            cell.font = Font(size=10)
            cell.alignment = Alignment(
                horizontal='left' if col in left_cols else 'center',
                vertical='center',
                wrap_text=col in left_cols
            )

        if day_col is not None:
            day_cell = ws.cell(row=row, column=day_col)
            day_cell.font = Font(bold=True, size=10)
            day_cell.alignment = Alignment(horizontal='center', vertical='center')

        if status_col is not None:
            status_cell = ws.cell(row=row, column=status_col)
            if status_cell.value == 'В норме':
                status_cell.fill = PatternFill('solid', fgColor='C6EFCE')
                status_cell.font = Font(bold=True, color='006100', size=10)
            elif status_cell.value == 'Ниже цели':
                status_cell.fill = PatternFill('solid', fgColor='FFEB9C')
                status_cell.font = Font(bold=True, color='9C6500', size=10)
            elif status_cell.value == 'Выше цели':
                status_cell.fill = PatternFill('solid', fgColor='FFC7CE')
                status_cell.font = Font(bold=True, color='9C0006', size=10)

        ws.row_dimensions[row].height = 24

    # Разделители: пунктир между упражнениями, толстая линия между днями.
    if day_col is not None or exercise_col is not None:
        for row in range(data_start, data_end):
            day_changed = (
                day_col is not None
                and ws.cell(row=row, column=day_col).value
                != ws.cell(row=row + 1, column=day_col).value
            )
            exercise_changed = (
                exercise_col is not None
                and ws.cell(row=row, column=exercise_col).value
                != ws.cell(row=row + 1, column=exercise_col).value
            )
            if not day_changed and not exercise_changed:
                continue
            bottom_side = medium_side if day_changed else Side(
                style='dashed', color='8EA9DB'
            )
            for col in range(1, ncols + 1):
                cell = ws.cell(row=row, column=col)
                cell.border = Border(
                    left=thin_side, right=thin_side, top=thin_side, bottom=bottom_side
                )

    # Нижняя граница таблицы.
    for col in range(1, ncols + 1):
        cell = ws.cell(row=data_end, column=col)
        cell.border = Border(
            left=thin_side, right=thin_side, top=thin_side, bottom=medium_side
        )

    if widths:
        for col, width in widths.items():
            ws.column_dimensions[get_column_letter(col)].width = width

def build_excel_export(progression_plans, exercises):
    """Собирает читаемый Excel: русские листы, заголовки и оформление."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        # Сводка по неделям — первая и самая полезная для быстрого просмотра.
        summary_rows = []
        previous_total = None
        for week_number, plan in enumerate(progression_plans, 1):
            total_light = total_medium = total_heavy = 0
            for day_info in plan['days_info'].values():
                set_types = day_info.get('set_types', {'light': 0, 'medium': 0, 'heavy': 0})
                total_light += set_types['light']
                total_medium += set_types['medium']
                total_heavy += set_types['heavy']
            total_sets = total_light + total_medium + total_heavy
            if plan.get('is_deload'):
                note = 'разгрузка'
            elif previous_total is not None and total_sets == previous_total:
                note = 'без прироста подходов — прогресс в нагрузке'
            else:
                note = ''
            summary_rows.append({
                'Неделя': week_number,
                'Всего подходов': total_sets,
                'Лёгкие': total_light,
                'Средние': total_medium,
                'Тяжёлые': total_heavy,
                'Интенсивность, %1ПМ': round(plan.get('intensity_pct', 65.0), 1),
                'Разгрузка': 'да' if plan.get('is_deload') else '',
                'Примечание': note
            })
            previous_total = total_sets

        summary_df = pd.DataFrame(summary_rows, columns=SUMMARY_COLUMNS)
        summary_sheet = 'Сводка'
        summary_df.to_excel(writer, sheet_name=summary_sheet, startrow=3, index=False)
        ws = writer.sheets[summary_sheet]
        _excel_title(
            ws, 'Сводка по неделям',
            'Плавная прогрессия объёма и нагрузки', len(summary_df.columns)
        )
        _excel_style_table(
            ws, 4, 5, 4 + len(summary_df), len(summary_df.columns),
            left_cols={1},
            widths={1: 10, 2: 16, 3: 12, 4: 12, 5: 12, 6: 18, 7: 12, 8: 50}
        )

        for week_number, plan in enumerate(progression_plans, 1):
            # Основная программа недели.
            export_df = get_export_dataframe(plan, exercises)
            sheet_name = f'Неделя {week_number}'
            export_df.to_excel(writer, sheet_name=sheet_name, startrow=3, index=False)
            ws = writer.sheets[sheet_name]
            subtitle = f"Ориентир интенсивности: {plan.get('intensity_pct', 65.0):.1f}% 1ПМ"
            if plan.get('is_deload'):
                subtitle += ' · разгрузочная неделя'
            _excel_title(
                ws, f'Неделя {week_number} — программа тренировок',
                subtitle, len(export_df.columns)
            )
            _excel_style_table(
                ws, 4, 5, 4 + len(export_df), len(export_df.columns),
                day_col=1, exercise_col=2, left_cols={2},
                widths={
                    1: 8, 2: 44, 3: 18, 4: 16, 5: 10, 6: 8,
                    7: 12, 8: 22, 9: 16, 10: 16, 11: 16
                }
            )

            # Объёмы по мышечным группам.
            volume_rows = []
            for mg, volume in sorted(plan['mg_total_volume'].items()):
                min_volume = plan['target_volume_mg'][mg]['min']
                max_volume = plan['target_volume_mg'][mg]['max']
                if min_volume <= volume <= max_volume:
                    status_key = 'ok'
                elif volume < min_volume:
                    status_key = 'low'
                else:
                    status_key = 'high'
                volume_rows.append({
                    'Мышечная группа': mg,
                    'Объём': round(volume, 1),
                    'Целевой минимум': round(min_volume, 1),
                    'Целевой максимум': round(max_volume, 1),
                    'Статус': VOLUME_STATUS_LABELS[status_key]
                })

            volume_df = pd.DataFrame(volume_rows, columns=VOLUME_COLUMNS)
            volume_sheet = f'Объём {week_number}'
            volume_df.to_excel(writer, sheet_name=volume_sheet, startrow=3, index=False)
            ws = writer.sheets[volume_sheet]
            _excel_title(
                ws, f'Объём по мышечным группам — неделя {week_number}',
                'Рабочие подходы с учётом вовлечённости мышц', len(volume_df.columns)
            )
            _excel_style_table(
                ws, 4, 5, 4 + len(volume_df), len(volume_df.columns),
                left_cols={1}, status_col=5,
                widths={1: 26, 2: 12, 3: 16, 4: 16, 5: 16}
            )

            # Типы подходов по дням.
            set_type_rows = []
            for day in sorted(plan['days_info'].keys()):
                day_info = plan['days_info'][day]
                set_types = day_info.get('set_types', {'light': 0, 'medium': 0, 'heavy': 0})
                set_type_rows.append({
                    'День': day + 1,
                    'Лёгкие подходы': set_types['light'],
                    'Средние подходы': set_types['medium'],
                    'Тяжёлые подходы': set_types['heavy'],
                    'Всего подходов': (
                        set_types['light'] + set_types['medium'] + set_types['heavy']
                    ),
                    'Общая стимуляция': day_info['total_stim']
                })

            set_type_df = pd.DataFrame(set_type_rows, columns=SET_TYPE_COLUMNS)
            set_type_sheet = f'Подходы {week_number}'
            set_type_df.to_excel(writer, sheet_name=set_type_sheet, startrow=3, index=False)
            ws = writer.sheets[set_type_sheet]
            set_type_subtitle = f"Ориентир интенсивности: {plan.get('intensity_pct', 65.0):.1f}% 1ПМ"
            if plan.get('is_deload'):
                set_type_subtitle += ' · разгрузочная неделя'
            _excel_title(
                ws, f'Типы подходов по дням — неделя {week_number}',
                set_type_subtitle, len(set_type_df.columns)
            )
            _excel_style_table(
                ws, 4, 5, 4 + len(set_type_df), len(set_type_df.columns),
                widths={1: 8, 2: 16, 3: 16, 4: 16, 5: 16, 6: 18}
            )

    buffer.seek(0)
    return buffer

def recommend_reps_for_exercise(ex_name, exercises, goal):
    ex = exercises[ex_name]
    tut_min, tut_max = ex.get('tut', (2.0, 3.0))
    tut_lo, tut_hi = GOAL_TUT[goal]
    target_tut = (tut_lo + tut_hi) / 2.0
    avg_tut = (tut_min + tut_max) / 2.0

    if ex['type'] == 'isolation' and ex_name in ["Планка", "Подъем ног в висе"]:
        return {'est_reps': None, 'range': None, 'target_tut_s': target_tut, 'hold_time_s': (tut_min, tut_max)}
    
    est_reps = target_tut / avg_tut
    reps = int(round(max(1, min(30, est_reps))))
    reps_min = max(1, int(math.floor(target_tut / tut_max)))
    reps_max = max(reps_min, int(math.ceil(target_tut / tut_min)))
    return {'est_reps': reps, 'range': (reps_min, reps_max), 'target_tut_s': target_tut}

def generate_progression_plan(base_target_volume_mg, exercises, train_days_idx, ex_to_days, split, schedule, progression_type='linear', compound_step=0.5, isolation_step=0.3, weeks=9):
    progression_plans = []
    previous_allocation = None
    previous_total = None

    for week in range(weeks):
        # Плавно меняем целевой объём: без «двух недель без изменений и потом скачка».
        target_volume_mg = {}
        for mg, values in base_target_volume_mg.items():
            step = compound_step if values.get('min', 0) >= 10.0 else isolation_step
            if progression_type == 'wave':
                cycle = week // 3
                cycle_week = week % 3
                addition = cycle * step * 0.5 + cycle_week * step
            else:
                addition = step * week
            target_volume_mg[mg] = {
                'min': values['min'] + addition,
                'max': values['max'] + addition,
                'category': values.get('category')
            }

        if previous_allocation is None:
            max_changes = None
        elif is_deload_week(week, progression_type):
            # В разгрузочную неделю волны объём должен снизиться заметнее.
            max_changes = max(6, round(previous_total * 0.25))
        else:
            max_changes = max(3, round(previous_total * 0.08))

        allocation, mg_volume = allocate_weekly_sets(
            exercises, target_volume_mg, train_days_idx, ex_to_days,
            prev_allocation=previous_allocation, max_changes=max_changes
        )

        total_sets = sum(allocation.values())
        if (previous_total is not None and total_sets == previous_total
                and not is_deload_week(week, progression_type)):
            allocation, mg_volume = force_progress_step(
                allocation, mg_volume, target_volume_mg, exercises, ex_to_days, train_days_idx
            )
            total_sets = sum(allocation.values())

        per_day = distribute_weekly_sets(
            allocation, ex_to_days, train_days_idx, exercises, split, week
        )

        # После выравнивания по дням и обрезки лимитов пересчитываем фактические подходы.
        ex_week_sets_int = {
            ex: sum(per_day[day].get(ex, 0) for day in train_days_idx)
            for ex in exercises
        }
        ex_week_sets = {ex: float(sets) for ex, sets in ex_week_sets_int.items()}
        days_info, mg_total_volume = build_days_info(per_day, exercises, target_volume_mg)
        export_df = build_export_dataframe(days_info, exercises, week, progression_type)

        plan = {
            'week': week + 1,
            'target_volume_mg': target_volume_mg,
            'ex_week_sets': ex_week_sets,
            'ex_week_sets_int': ex_week_sets_int,
            'days_info': days_info,
            'mg_total_volume': mg_total_volume,
            'export_df': export_df,
            'progression_type': progression_type,
            'intensity_pct': week_intensity_pct(week, progression_type),
            'is_deload': is_deload_week(week, progression_type)
        }

        plan['volume_analysis'] = analyze_volume_shortfalls(
            plan['mg_total_volume'],
            plan['target_volume_mg'],
            exercises,
            plan['ex_week_sets_int'],
            ex_to_days
        )
        progression_plans.append(plan)
        # Для следующей недели берём фактическое распределение после
        # выравнивания по дням, а не промежуточный результат аллокатора.
        previous_allocation = ex_week_sets_int
        previous_total = sum(ex_week_sets_int.values())

    return progression_plans

def build_plan_streamlit(selected_muscles, split, train_days, progression_type, compound_step, isolation_step, selected_cardio, use_custom_settings=False):
    # Используем кастомные или стандартные настройки
    if use_custom_settings and 'custom_volumes' in st.session_state:
        target_volume_mg = {}
        for mg in selected_muscles:
            if mg in st.session_state.custom_volumes:
                target_volume_mg[mg] = st.session_state.custom_volumes[mg].copy()
            elif mg in DEFAULT_TARGET_VOLUME_MG:
                target_volume_mg[mg] = DEFAULT_TARGET_VOLUME_MG[mg].copy()
    else:
        target_volume_mg = {}
        for mg in selected_muscles:
            if mg in DEFAULT_TARGET_VOLUME_MG:
                # Копируем все данные включая категорию
                target_volume_mg[mg] = DEFAULT_TARGET_VOLUME_MG[mg].copy()
    
    if not target_volume_mg:
        st.error("Не выбраны корректные мышечные группы!")
        return None, None, None
    
    schedule = make_week_schedule(train_days, 'consecutive')
    train_days_idx = list_training_days(schedule)
    
    # Используем кастомные или автоматически выбранные упражнения
    selected_exercises = select_exercises_interactively(
        selected_muscles,
        use_custom_selection=use_custom_settings,
        split=split,
        train_days=train_days
    )
    
    if not selected_exercises:
        st.error("Не удалось подобрать упражнения для выбранных мышечных групп!")
        return None, None, None
        
    ex_to_days = assign_exercise_days_by_split(selected_exercises, train_days_idx, split)
    
    progression_plans = generate_progression_plan(
        target_volume_mg, selected_exercises, train_days_idx, ex_to_days, split, schedule, 
        progression_type, compound_step, isolation_step
    )
    
    return progression_plans, selected_exercises, selected_cardio

# -------------------- STREAMLIT INTERFACE --------------------
def reset_custom_selection_on_muscle_change():
    """При смене мышечных групп старый ручной выбор упражнений больше не актуален."""
    st.session_state.selected_exercises_custom = None
    st.session_state.selected_exercises_by_muscle = {}

def main():
    st.set_page_config(page_title="Программа тренировок", layout="wide", page_icon="💪")
    
    st.title("💪 Генератор программы тренировок")
    st.markdown("Создайте персонализированную программу тренировок на основе выбранных мышечных групп")
    
    # Инициализация session state
    if 'progression_plans' not in st.session_state:
        st.session_state.progression_plans = None
    if 'selected_exercises' not in st.session_state:
        st.session_state.selected_exercises = None
    if 'selected_cardio' not in st.session_state:
        st.session_state.selected_cardio = {}
    
    # Вкладки
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏋️ Конфигурация", "🎯 Упражнения", "📊 Программа", "📈 Просмотр", "💾 Выгрузка"])
    
    with tab1:
        st.header("Настройка параметров тренировки")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Мышечные группы")
            all_muscles = list(DEFAULT_TARGET_VOLUME_MG.keys())
            selected_muscles = st.multiselect(
                "Выберите мышечные группы для тренировки:",
                all_muscles,
                default=[mg for mg in DEFAULT_SELECTED_MUSCLES if mg in all_muscles],
                on_change=reset_custom_selection_on_muscle_change
            )
            
            st.subheader("Тип сплита")
            split = st.selectbox(
                "Выберите тип сплита:",
                ['full_body', 'upper_lower', 'push_pull_legs'],
                format_func=lambda x: {
                    'full_body': 'Фулбади (все тело)',
                    'upper_lower': 'Верх/Низ',
                    'push_pull_legs': 'Толкать/Тянуть/Ноги'
                }[x]
            )
            
            st.subheader("Кардио")
            selected_cardio = st.multiselect(
                "Выберите кардио упражнения:",
                list(CARDIO.keys()),
                default=['Велотренажер']
            )
            
        with col2:
            st.subheader("Параметры тренировки")
            train_days = st.slider("Количество тренировочных дней в неделю:", 2, 6, 3)
            
            st.subheader("Тип прогрессии")
            progression_type = st.selectbox(
                "Выберите тип прогрессии:",
                ['linear', 'wave'],
                format_func=lambda x: {
                    'linear': 'Линейная',
                    'wave': 'Волнообразная'
                }[x]
            )
            
            st.subheader("Шаги прогрессии")
            compound_step = st.number_input("Шаг для базовых упражнений:", min_value=0.1, max_value=2.0, value=0.5, step=0.1)
            isolation_step = st.number_input("Шаг для изолирующих упражнений:", min_value=0.1, max_value=2.0, value=0.3, step=0.1)
        
        # Добавьте перед кнопкой генерации
        use_custom_settings = st.checkbox(
            "Использовать настройки упражнений и объёмов",
            value=True,
            help=(
                "Если отмечено и на вкладке «Упражнения» применён выбор — "
                "используется он. Иначе работает компактный автоподбор."
            )
        )

        if st.button("Сгенерировать программу", type="primary"):
            if not selected_muscles:
                st.error("Пожалуйста, выберите хотя бы одну мышечную группу!")
                return
                
            cardio_dict = {cardio: 1.0 for cardio in selected_cardio}
            result = build_plan_streamlit(
                selected_muscles, split, train_days, progression_type, compound_step, 
                isolation_step, cardio_dict, use_custom_settings
            )
            
            if result[0] is not None:
                progression_plans, selected_exercises, _ = result
                st.session_state.progression_plans = progression_plans
                st.session_state.selected_exercises = selected_exercises
                st.session_state.selected_cardio = cardio_dict
                st.success("Программа успешно сгенерирована! Перейдите на вкладку 'Программа' для просмотра.")
            else:
                st.error("Не удалось сгенерировать программу. Проверьте настройки.")
    
    with tab2:
        st.header("Настройка упражнений и объемов")
        
        # Инициализация session state
        if 'custom_exercises' not in st.session_state:
            st.session_state.custom_exercises = EXERCISES.copy()
        if 'custom_volumes' not in st.session_state:
            st.session_state.custom_volumes = DEFAULT_TARGET_VOLUME_MG.copy()
        if 'selected_exercises_by_muscle' not in st.session_state:
            st.session_state.selected_exercises_by_muscle = {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Настройка целевых объемов")
            st.markdown("Установите минимальный и максимальный объем для каждой мышечной группы:")
        
            volume_data = []
            for mg, targets in st.session_state.custom_volumes.items():
                category = targets.get('category', 'не указана')
                volume_data.append({
                    'Мышечная группа': mg,
                    'Категория': category,
                    'Мин объем': targets['min'],
                    'Макс объем': targets['max']
                })
            
            volume_df = pd.DataFrame(volume_data)
            edited_volume_df = st.data_editor(
                volume_df,
                column_config={
                    "Мышечная группа": st.column_config.TextColumn("Мышечная группа", disabled=True),
                    "Категория": st.column_config.TextColumn("Категория", disabled=True),
                    "Мин объем": st.column_config.NumberColumn("Мин объем", min_value=0.0, max_value=50.0, step=0.5),
                    "Макс объем": st.column_config.NumberColumn("Макс объем", min_value=0.0, max_value=50.0, step=0.5)
                },
                width='stretch',
                num_rows="fixed"
            )
            
            if st.button("💾 Сохранить настройки объемов"):
                new_volumes = {}
                for _, row in edited_volume_df.iterrows():
                    new_volumes[row['Мышечная группа']] = {
                        'min': float(row['Мин объем']),
                        'max': float(row['Макс объем'])
                    }
                st.session_state.custom_volumes = new_volumes
                st.success("Настройки объемов сохранены!")
        
        with col2:
            st.subheader("Выбор упражнений по мышечным группам")
            
            # Группируем упражнения по мышечным группам
            mg_to_exs = group_exercises_by_muscle()
            
            # Инициализируем выбор тем же компактным набором, который строит
            # автоматический алгоритм: базовое движение + изоляция на активацию.
            compact_default = select_balanced_exercises(
                selected_muscles, split, train_days, EXERCISES
            )
            for mg in mg_to_exs.keys():
                if mg not in st.session_state.selected_exercises_by_muscle:
                    st.session_state.selected_exercises_by_muscle[mg] = [
                        ex for ex in compact_default if ex in mg_to_exs[mg]
                    ][:2]
            
            # Показываем все мышечные группы сразу для выбора упражнений
            st.markdown("**Выберите упражнения для каждой мышечной группы:**")

            for mg in mg_to_exs.keys():
                available_exercises = mg_to_exs[mg]
                if available_exercises:
                    with st.expander(f"📌 {mg}", expanded=False):
                        # Мультиселект для каждой мышечной группы
                        selected_exercises = st.multiselect(
                            f"Упражнения для {mg}:",
                            options=available_exercises,
                            default=st.session_state.selected_exercises_by_muscle[mg],
                            key=f"ex_select_{mg}"
                        )
                        
                        # Сохраняем выбранные упражнения сразу
                        st.session_state.selected_exercises_by_muscle[mg] = selected_exercises
                        
                        # Показываем детали выбранных упражнений
                        if selected_exercises:
                            st.markdown("**Выбрано:**")
                            for ex_name in selected_exercises:
                                ex_data = st.session_state.custom_exercises[ex_name]
                                primary_muscles = [m for m, w in ex_data['muscles'].items() if w == 1.0]
                                secondary_muscles = [m for m, w in ex_data['muscles'].items() if w < 1.0 and w > 0]
                                
                                st.write(f"• **{ex_name}**")
                                st.write(f"  Тип: {ex_data['type']}")
                                if primary_muscles:
                                    st.write(f"  Основные: {', '.join(primary_muscles)}")
                                if secondary_muscles:
                                    st.write(f"  Второстепенные: {', '.join(secondary_muscles)}")
            
            # Кнопка для подтверждения выбора
            if st.button("💾 Применить выбор упражнений", type="primary"):
                # Собираем все выбранные упражнения
                all_selected_exercises = {}
                for mg, exercises_list in st.session_state.selected_exercises_by_muscle.items():
                    for ex_name in exercises_list:
                        all_selected_exercises[ex_name] = st.session_state.custom_exercises[ex_name]
                
                if all_selected_exercises:
                    st.session_state.selected_exercises_custom = all_selected_exercises
                    st.success(f"Успешно выбрано {len(all_selected_exercises)} упражнений!")
                    
                    # Показываем сводку
                    st.subheader("Сводка по выбранным упражнениям:")
                    for mg in mg_to_exs.keys():
                        exercises_for_mg = st.session_state.selected_exercises_by_muscle[mg]
                        if exercises_for_mg:
                            st.write(f"**{mg}:** {', '.join(exercises_for_mg)}")
                else:
                    st.warning("Не выбрано ни одного упражнения!")

            # Кнопка сброса
            # В tab2 при сбросе к значениям по умолчанию:
            if st.button("🔄 Сбросить к упражнениям по умолчанию"):
                st.session_state.custom_exercises = EXERCISES.copy()
                st.session_state.custom_volumes = DEFAULT_TARGET_VOLUME_MG.copy()  # Теперь с категориями
                st.session_state.selected_exercises_by_muscle = {}
                st.session_state.selected_exercises_custom = None
                st.success("Настройки сброшены к значениям по умолчанию!")
                st.rerun()

            # Показываем текущий статус
            if 'selected_exercises_custom' in st.session_state and st.session_state.selected_exercises_custom:
                st.info(f"✅ Текущий выбор: {len(st.session_state.selected_exercises_custom)} упражнений")
   
    with tab3:
        st.header("Ваша программа тренировок")
        
        if st.session_state.progression_plans is None:
            st.info("Сначала настройте параметры на вкладке 'Конфигурация' и сгенерируйте программу.")
        else:
            selected_week = st.selectbox(
                "Выберите неделю для просмотра:",
                options=list(range(1, 10)),
                format_func=lambda x: f"Неделя {x}"
            )
            
            plan = st.session_state.progression_plans[selected_week - 1]
            
            st.subheader(f"Программа тренировок - Неделя {selected_week}")
            intensity_note = f"Ориентир интенсивности: {plan.get('intensity_pct', 65.0):.1f}% 1ПМ"
            if plan.get('is_deload'):
                intensity_note += " · разгрузочная неделя"
            st.caption(intensity_note)
            
            # Отображение программы по дням
            for day in sorted(plan['days_info'].keys()):
                with st.expander(f"День {day + 1}", expanded=True):
                    day_data = plan['days_info'][day]
                    
                    if not day_data['items']:
                        st.write("Отдых")
                        continue
                    
                    # Показываем сводку по типам подходов
                    set_types = day_data.get('set_types', {'light': 0, 'medium': 0, 'heavy': 0})
                    total_day_sets = sum(set_types.values())
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.metric("Тяжёлые подходы", set_types['heavy'] or "-")
                    with col2:
                        st.metric("Средние подходы", set_types['medium'] or "-")
                    with col3:
                        st.metric("Лёгкие подходы", set_types['light'] or "-")
                    with col4:
                        st.metric("Всего подходов", total_day_sets)
                    with col5:
                        st.metric("Общая стимуляция", f"{day_data['total_stim']:.1f}")

                    # Порядок уже задан в build_days_info:
                    # сначала базовые движения, затем изолирующие на активацию.
                    day_df = get_export_dataframe(plan, st.session_state.selected_exercises)
                    day_df = day_df[day_df['День'] == day + 1].drop(columns=['День'])
                    if not day_df.empty:
                        st.dataframe(day_df, width='stretch')
    
    with tab4:
        st.header("Обзор программы")
        
        if st.session_state.progression_plans is None:
            st.info("Сначала настройте параметры на вкладке 'Конфигурация' и сгенерируйте программу.")
        else:

            # Выбор недели для детального просмотра
            selected_week = st.selectbox(
                "Выберите неделю для детального просмотра:",
                options=list(range(1, 10)),
                format_func=lambda x: f"Неделя {x}",
                key="detail_week"
            )
            
            plan = st.session_state.progression_plans[selected_week - 1]

            # Показываем, что объём меняется плавно, а не «неделю стоим — потом скачок».
            st.subheader("📈 Динамика объёма по неделям")
            progression_rows = []
            previous_total = None
            for week_number, week_plan in enumerate(st.session_state.progression_plans, 1):
                total_sets = sum(week_plan['ex_week_sets_int'].values())
                if week_plan.get('is_deload'):
                    note = "разгрузка"
                elif previous_total is not None and total_sets == previous_total:
                    note = "без прироста подходов — прогресс в нагрузке"
                else:
                    note = ""
                progression_rows.append({
                    'Неделя': week_number,
                    'Всего подходов': total_sets,
                    'Изменение': "-" if previous_total is None else f"{total_sets - previous_total:+d}",
                    'Интенсивность, %1ПМ': f"{week_plan.get('intensity_pct', 65.0):.1f}",
                    'Разгрузка': "да" if week_plan.get('is_deload') else "",
                    'Примечание': note
                })
                previous_total = total_sets
            progression_df = pd.DataFrame(progression_rows)
            st.dataframe(progression_df, width='stretch')
            st.caption(
                "Если подходы упираются в лимит по дню или упражнению, прогрессия "
                "продолжается за счёт нагрузки: ориентир «%1ПМ» растёт каждую неделю."
            )

            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Объем по мышечным группам")
                volume_data = []
                for mg, vol in sorted(plan['mg_total_volume'].items()):
                    min_vol = plan['target_volume_mg'][mg]['min']
                    max_vol = plan['target_volume_mg'][mg]['max']
                    status = "✅" if min_vol <= vol <= max_vol else "⚠️" if vol < min_vol else "🔴"
                    
                    volume_data.append({
                        'Мышечная группа': mg,
                        'Объем': f"{vol:.1f}",
                        'Целевой минимум': f"{min_vol:.1f}",
                        'Целевой максимум': f"{max_vol:.1f}",
                        'Статус': status
                    })
                
                volume_df = pd.DataFrame(volume_data)
                st.dataframe(volume_df, width='stretch')
            
            with col2:
                st.subheader("Выбранные упражнения")
                exercises_list = list(st.session_state.selected_exercises.keys())
                for i, ex in enumerate(exercises_list, 1):
                    st.write(f"{i}. {display_exercise_name(ex)}")
                
                st.subheader("Кардио")
                total_cardio = 0.0
                for cardio, factor in st.session_state.selected_cardio.items():
                    val = CARDIO.get(cardio, factor) * factor
                    st.write(f"• {cardio}: {val:.2f} мг-эквивалентов/неделя")
                    total_cardio += val
                
                st.metric("Общий кардио объем", f"{total_cardio:.2f} мг-эквивалентов/неделя")
            # Добавляем раздел анализа недостатков объема
            st.subheader("🔍 Анализ достижения целевых объемов")
            
            volume_analysis = plan.get('volume_analysis', {})
            
            if not volume_analysis:
                st.info("Все целевые объемы достигнуты! ✅")
            else:
                for mg, analysis in volume_analysis.items():
                    with st.expander(f"📊 {mg} - {analysis['actual_volume']:.1f} из {analysis['min_target']:.1f} (недостаточно)", expanded=False):
                        st.write(f"**Текущий объем:** {analysis['actual_volume']:.1f}")
                        st.write(f"**Целевой минимум:** {analysis['min_target']:.1f}")
                        st.write(f"**Целевой максимум:** {analysis['max_target']:.1f}")
                        
                        st.write("**Причины недостаточного объема:**")
                        for reason in analysis['reasons']:
                            st.write(f"• {reason}")
                        
                        # Рекомендации по улучшению: не «добавить упражнения»,
                        # а перераспределить объём по уже выбранному набору.
                        st.write("**💡 Рекомендации:**")
                        recommendations = []
                        reasons_text = " ".join(analysis['reasons']).lower()

                        if "нет упражнения с прямой нагрузкой" in reasons_text or "нет упражнений" in reasons_text:
                            recommendations.append("В пуле уже есть подходящее упражнение — замените менее целевое на вкладке «Упражнения»")
                        if "недостаточно общего объема" in reasons_text:
                            if "пределе недельного объёма" not in reasons_text:
                                recommendations.append("Увеличьте количество подходов на уже выбранных упражнениях, затрагивающих эту группу")
                            recommendations.append("Перераспределите подходы на дни, где эта группа уже нагружается")
                        if "пределе недельного объёма" in reasons_text:
                            recommendations.append("Подходы уже на лимите — прогрессируйте нагрузку (%1ПМ), технику и качество повторений")
                        if "ограниченное количество тренировочных дней" in reasons_text:
                            recommendations.append("Добавьте тренировочный день или перенесите часть объёма на другой день")
                        if "прямая вовлечённость низкая" in reasons_text:
                            recommendations.append("Замените одно из выбранных упражнений на более целевое из пула")
                        if not recommendations:
                            recommendations.append("Немного увеличьте число подходов на упражнениях, которые уже нагружают эту группу")

                        for rec in recommendations:
                            st.write(f"• {rec}")

    with tab5:
        st.header("Выгрузка данных")
        
        if st.session_state.progression_plans is None:
            st.info("Сначала настройте параметры на вкладке 'Конфигурация' и сгенерируйте программу.")
        else:
            # Добавляем сводку по типам подходов для всех недель
            st.subheader("Сводка по типам подходов")
            
            set_type_summary = []
            for week, plan in enumerate(st.session_state.progression_plans, 1):
                total_light = 0
                total_medium = 0
                total_heavy = 0
                
                for day_info in plan['days_info'].values():
                    set_types = day_info.get('set_types', {'light': 0, 'medium': 0, 'heavy': 0})
                    total_light += set_types['light']
                    total_medium += set_types['medium']
                    total_heavy += set_types['heavy']
                
                set_type_summary.append({
                    'Неделя': week,
                    'Лёгкие подходы': total_light,
                    'Средние подходы': total_medium,
                    'Тяжёлые подходы': total_heavy,
                    'Всего подходов': total_light + total_medium + total_heavy,
                    'Интенсивность, %1ПМ': f"{plan.get('intensity_pct', 65.0):.1f}",
                    'Разгрузка': "да" if plan.get('is_deload') else ""
                })
            
            set_type_df = pd.DataFrame(set_type_summary)
            st.dataframe(set_type_df, width='stretch')

            st.subheader("Экспорт в Excel")
            
            # Создаем Excel файл со всеми неделями.
            buffer = build_excel_export(
                st.session_state.progression_plans,
                st.session_state.selected_exercises
            )

            st.download_button(
                label="📥 Скачать полную программу (Excel)",
                data=buffer,
                file_name="Программа_тренировок.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            # Отдельные выгрузки по неделям
            st.subheader("Экспорт по неделям")
            selected_week_export = st.selectbox(
                "Выберите неделю для экспорта:",
                options=list(range(1, 10)),
                format_func=lambda x: f"Неделя {x}",
                key="export_week"
            )
            
            plan = st.session_state.progression_plans[selected_week_export - 1]
            
            col1, col2 = st.columns(2)
            
            with col1:
                # CSV выгрузка программы — тот же русский формат, что и в Excel.
                export_df = get_export_dataframe(
                    plan, st.session_state.selected_exercises
                )
                csv_program = export_df.to_csv(
                    index=False, encoding='utf-8-sig'
                ).encode('utf-8-sig')
                st.download_button(
                    label=f"📥 Скачать программу недели {selected_week_export} (CSV)",
                    data=csv_program,
                    file_name=f"Программа_неделя_{selected_week_export}.csv",
                    mime="text/csv"
                )

            with col2:
                # CSV выгрузка объёмов.
                volume_data = []
                for mg, vol in sorted(plan['mg_total_volume'].items()):
                    min_vol = plan['target_volume_mg'][mg]['min']
                    max_vol = plan['target_volume_mg'][mg]['max']
                    if min_vol <= vol <= max_vol:
                        status_key = 'ok'
                    elif vol < min_vol:
                        status_key = 'low'
                    else:
                        status_key = 'high'
                    volume_data.append({
                        'Мышечная группа': mg,
                        'Объём': round(vol, 1),
                        'Целевой минимум': round(min_vol, 1),
                        'Целевой максимум': round(max_vol, 1),
                        'Статус': VOLUME_STATUS_LABELS[status_key]
                    })

                volume_df = pd.DataFrame(volume_data, columns=VOLUME_COLUMNS)
                csv_volume = volume_df.to_csv(
                    index=False, encoding='utf-8-sig'
                ).encode('utf-8-sig')
                st.download_button(
                    label=f"📥 Скачать объёмы недели {selected_week_export} (CSV)",
                    data=csv_volume,
                    file_name=f"Объёмы_неделя_{selected_week_export}.csv",
                    mime="text/csv"
                )
                
if __name__ == "__main__":
    main()