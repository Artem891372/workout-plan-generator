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
RPE_BY_TYPE = {'light': '3-5', 'medium': '6-7', 'heavy': '8-9'}
GOAL = 'hypertrophy'
GOAL_TUT = {
    'strength': (0.0, 15.0),
    'hypertrophy': (15.0, 40.0),
    'endurance': (40.0, 180.0)
}

# -------------------- UTILITY FUNCTIONS --------------------
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
                reasons.append("❌ Нет упражнений, нацеленных на эту мышечную группу")
            else:
                total_potential = sum(ex['involvement'] * ex['weekly_sets'] for ex in relevant_exercises)
                
                if total_potential < min_target:
                    reasons.append(f"❌ Недостаточно общего объема: {total_potential:.1f} из {min_target:.1f}")
                
                # Проверяем ограничения по дням тренировок
                training_days_with_mg = set()
                for ex in relevant_exercises:
                    training_days_with_mg.update(ex['days'])
                
                if len(training_days_with_mg) < 2 and min_target > 8:
                    reasons.append(f"⚠️ Ограниченное количество тренировочных дней: {len(training_days_with_mg)}")
                
                # Проверяем эффективность упражнений
                high_involvement_exercises = [ex for ex in relevant_exercises if ex['involvement'] >= 0.8]
                if not high_involvement_exercises:
                    reasons.append("⚠️ Нет упражнений с высокой вовлеченностью этой МГ")
                
                # Детали по упражнениям
                exercise_details = []
                for ex in relevant_exercises:
                    contribution = ex['involvement'] * ex['weekly_sets']
                    exercise_details.append(f"{ex['exercise']} ({contribution:.1f} через {ex['weekly_sets']} подходов)")
                
                reasons.append(f"📊 Вклад упражнений: {', '.join(exercise_details)}")
            
            shortfall_analysis[mg] = {
                'actual_volume': actual_volume,
                'min_target': min_target,
                'max_target': max_target,
                'reasons': reasons,
                'relevant_exercises': relevant_exercises
            }
    
    return shortfall_analysis

def select_exercises_interactively(selected_muscles, use_custom_selection=False):
    mg_to_exs = group_exercises_by_muscle()
    selected_exercises = {}
    
    if use_custom_selection and 'selected_exercises_custom' in st.session_state:
        # Используем кастомный выбор упражнений
        return st.session_state.selected_exercises_custom
    
    # Автоматический выбор: по одному упражнению для каждой выбранной мышечной группы
    for mg in selected_muscles:
        if mg in mg_to_exs and mg_to_exs[mg]:
            # Выбираем первое упражнение для каждой группы мышц
            selected_ex = mg_to_exs[mg][0]
            selected_exercises[selected_ex] = EXERCISES[selected_ex]
    
    return selected_exercises

def allocate_sets_per_exercise(exercises, target_volume_mg, train_days_idx, ex_to_days):
    mg_to_exs = defaultdict(list)
    for ex_name, ex in exercises.items():
        primary_mg = max(ex['muscles'], key=lambda mg: ex['muscles'][mg])
        for mg, c in ex['muscles'].items():
            if c > 0:
                mg_to_exs[mg].append((ex_name, c, ex['type'], primary_mg))

    big_mgs = {mg for mg, targets in target_volume_mg.items() if targets['min'] >= 10.0}
    compound_exs = [ex for ex, data in exercises.items() if data['type'] == 'compound']
    isolation_exs = [ex for ex, data in exercises.items() if data['type'] == 'isolation']

    # Инициализация подходов
    ex_sets_per_day = {ex: {d: 1 for d in ex_to_days.get(ex, [])} for ex in exercises}
    mg_vol = {mg: 0.0 for mg in target_volume_mg}
    for ex, day_sets in ex_sets_per_day.items():
        for d, s in day_sets.items():
            for mg, c in exercises[ex]['muscles'].items():
                mg_vol[mg] += s * c * STIM_FACTORS['light']

    # Этап 1: Увеличиваем подходы для базовых упражнений
    max_iterations = 100
    iteration = 0
    while iteration < max_iterations:
        needs_increase = {mg for mg in big_mgs if mg_vol[mg] < target_volume_mg[mg]['min']}
        if not needs_increase:
            break
        for ex in compound_exs:
            days = sorted(ex_to_days.get(ex, []))
            if not days:
                continue
            n = len(days)
            order = []
            left, right = 0, n - 1
            while left <= right:
                order.append(left)
                if left != right:
                    order.append(right)
                left += 1
                right -= 1
            order = [days[i] for i in order]
            for d in order:
                temp_vol = {mg: mg_vol[mg] + exercises[ex]['muscles'].get(mg, 0.0) * STIM_FACTORS['light'] for mg in target_volume_mg}
                if any(temp_vol[mg] > target_volume_mg[mg]['max'] for mg in target_volume_mg):
                    continue
                ex_sets_per_day[ex][d] = ex_sets_per_day[ex].get(d, 0) + 1
                mg_vol = temp_vol
        iteration += 1

    # Этап 2: Увеличиваем подходы для изолирующих упражнений
    iteration = 0
    while iteration < max_iterations:
        needs_increase = {mg for mg in target_volume_mg if mg_vol[mg] < target_volume_mg[mg]['min']}
        if not needs_increase:
            break
        for mg in needs_increase:
            iso_exs = [(e[0], e[1]) for e in mg_to_exs[mg] if e[2] == 'isolation' and e[3] == mg and e[1] >= 0.8]
            if not iso_exs:
                iso_exs = [(e[0], e[1]) for e in mg_to_exs[mg] if e[2] == 'isolation']
            for ex, c in iso_exs:
                days = sorted(ex_to_days.get(ex, []))
                if not days:
                    continue
                n = len(days)
                order = []
                left, right = 0, n - 1
                while left <= right:
                    order.append(left)
                    if left != right:
                        order.append(right)
                    left += 1
                    right -= 1
                order = [days[i] for i in order]
                while mg_vol[mg] < target_volume_mg[mg]['min']:
                    for d in order:
                        temp_vol = {m: mg_vol[m] + exercises[ex]['muscles'].get(m, 0.0) * STIM_FACTORS['light'] for m in target_volume_mg}
                        if any(temp_vol[m] > target_volume_mg[m]['max'] for m in target_volume_mg):
                            break
                        ex_sets_per_day[ex][d] = ex_sets_per_day[ex].get(d, 0) + 1
                        mg_vol = temp_vol
                    else:
                        continue
                    break
                break
        iteration += 1

    # Подсчет недельных подходов
    ex_week_sets = {ex: sum(day_sets.values()) for ex, day_sets in ex_sets_per_day.items()}
    return ex_week_sets, ex_sets_per_day

def assign_exercise_days_by_split(exercises, train_days_idx, split):
    ex_to_days = {}
    
    # Определяем категории мышечных групп
    upper_mgs = {mg for mg, data in DEFAULT_TARGET_VOLUME_MG.items() if data.get('category') == 'upper'}
    lower_mgs = {mg for mg, data in DEFAULT_TARGET_VOLUME_MG.items() if data.get('category') == 'lower'}
    core_mgs = {mg for mg, data in DEFAULT_TARGET_VOLUME_MG.items() if data.get('category') == 'core'}
    
    if split == 'full_body':
        for ex in exercises.keys():
            ex_to_days[ex] = list(train_days_idx)
            
    elif split == 'upper_lower':
        for ex, data in exercises.items():
            ex_mgs = data['muscles']
            # Находим основную мышечную группу по максимальному вовлечению
            primary_mg = max(ex_mgs, key=lambda mg: ex_mgs[mg])
            
            # Определяем категорию упражнения по основной мышечной группе
            if primary_mg in upper_mgs:
                # Верх: дни 0, 2, 4... (четные индексы)
                ex_to_days[ex] = [train_days_idx[i] for i in range(0, len(train_days_idx), 2)]
            elif primary_mg in lower_mgs:
                # Низ: дни 1, 3, 5... (нечетные индексы)
                ex_to_days[ex] = [train_days_idx[i] for i in range(1, len(train_days_idx), 2)]
            elif primary_mg in core_mgs:
                # Кор: дни 1, 3, 5... (нечетные индексы)
                ex_to_days[ex] = [train_days_idx[i] for i in range(1, len(train_days_idx), 2)]
            else:
                # Если категория не определена, распределяем равномерно
                ex_to_days[ex] = list(train_days_idx)
                
    elif split == 'push_pull_legs':
        # Определяем толкающие, тянущие и ножные мышечные группы
        push_mgs = {'Грудь', 'Трицепс', 'Передняя дельта', 'Средняя дельта'}
        pull_mgs = {'Трапеция', 'Широчайшие', 'Задняя дельта', 'Бицепс'}
        legs_mgs = lower_mgs  # Используем уже определенные нижние группы
        
        for ex, data in exercises.items():
            ex_mgs = data['muscles']
            primary_mg = max(ex_mgs, key=lambda mg: ex_mgs[mg])
            
            if primary_mg in push_mgs:
                # Толкающие: дни 0, 3, 6...
                ex_to_days[ex] = [train_days_idx[i] for i in range(0, len(train_days_idx), 3)]
            elif primary_mg in pull_mgs:
                # Тянущие: дни 1, 4, 7...
                ex_to_days[ex] = [train_days_idx[i] for i in range(1, len(train_days_idx), 3)]
            elif primary_mg in legs_mgs:
                # Ноги: дни 2, 5, 8...
                ex_to_days[ex] = [train_days_idx[i] for i in range(2, len(train_days_idx), 3)]
            elif primary_mg in core_mgs:
                # Кор на все дни
                ex_to_days[ex] = list(train_days_idx)
            else:
                # Если категория не определена, распределяем равномерно
                ex_to_days[ex] = list(train_days_idx)
    
    return ex_to_days

def distribute_sets_to_days_int(ex_week_sets, ex_sets_per_day, ex_to_days, schedule, exercises, target_volume_mg):
    train_days_idx = list_training_days(schedule)
    days_info = {d: {'items': [], 'total_stim': 0.0, 'set_types': {'light': 0, 'medium': 0, 'heavy': 0}} for d in train_days_idx}
    mg_total_volume = {mg: 0.0 for mg in target_volume_mg}
    max_sets_per_day = 25

    # Этап 1: Проверяем и корректируем распределение подходов
    for ex, day_sets in ex_sets_per_day.items():
        total_sets = sum(day_sets.values())
        if total_sets != ex_week_sets.get(ex, 0):
            days = sorted(ex_to_days.get(ex, []))
            if not days:
                continue
            sets_per_day = {d: 0 for d in days}
            remaining_sets = ex_week_sets.get(ex, 0)
            n = len(days)
            order = []
            left, right = 0, n - 1
            while left <= right:
                order.append(left)
                if left != right:
                    order.append(right)
                left += 1
                right -= 1
            order = [days[i] for i in order]
            i = 0
            while remaining_sets > 0 and i < len(order):
                d = order[i % len(order)]
                if sum(sets_per_day[d] for d in sets_per_day) < max_sets_per_day:
                    sets_per_day[d] += 1
                    remaining_sets -= 1
                i += 1
            ex_sets_per_day[ex] = {d: s for d, s in sets_per_day.items() if s > 0}

    # Этап 2: Распределение подходов по типам интенсивности
    for ex, day_sets in ex_sets_per_day.items():
        days = sorted(day_sets.keys())
        for d in days:
            total_sets = day_sets[d]
            if total_sets == 0:
                continue
            
            # Определяем распределение по типам подходов
            if total_sets % 3 == 0:
                heavy_sets = total_sets // 3
                medium_sets = 0
                light_sets = 0

            elif total_sets % 2 == 0:
                heavy_sets = 0
                medium_sets = total_sets //2
                light_sets = 0

            else:
                light_sets = 1
                total_sets_1 = total_sets - 1

                if total_sets_1 % 3 == 0:
                    heavy_sets = total_sets_1 // 3
                    medium_sets = 0

                elif total_sets_1 % 2 == 0:
                    heavy_sets = 0
                    medium_sets = total_sets_1 //2
            
            # Добавляем подходы каждого типа
            if heavy_sets > 0:
                perf_heavy = round(heavy_sets * STIM_FACTORS['heavy'])
                days_info[d]['items'].append((ex, heavy_sets, 'heavy', perf_heavy))
                days_info[d]['set_types']['heavy'] += heavy_sets
                
            if medium_sets > 0:
                perf_medium = round(medium_sets * STIM_FACTORS['medium'])
                days_info[d]['items'].append((ex, medium_sets, 'medium', perf_medium))
                days_info[d]['set_types']['medium'] += medium_sets
                
            if light_sets > 0:
                perf_light = round(light_sets * STIM_FACTORS['light'])
                days_info[d]['items'].append((ex, light_sets, 'light', perf_light))
                days_info[d]['set_types']['light'] += light_sets

    # НОВЫЙ КОД: Сортировка упражнений в днях
    for d in days_info:
        # Сначала разделяем на базовые и изолирующие
        compound_exercises = []
        isolation_exercises = []
        
        for item in days_info[d]['items']:
            ex_name, base, ex_type, perf = item
            if exercises[ex_name]['type'] == 'compound':
                compound_exercises.append(item)
            else:
                isolation_exercises.append(item)
        
        # Сортируем упражнения по "тяжести и объемности" - сначала те, у которых больше тяжелых подходов
        def exercise_weight(items):
            """Вычисляет вес упражнения на основе типов подходов"""
            weight = 0
            for item in items:
                ex_name, base, ex_type, perf = item
                if ex_type == 'heavy':
                    weight += base * 3
                elif ex_type == 'medium':
                    weight += base * 2
                else:  # light
                    weight += base * 1
            return weight
        
        # Группируем подходы по упражнениям
        compound_by_exercise = {}
        for item in compound_exercises:
            ex_name = item[0]
            if ex_name not in compound_by_exercise:
                compound_by_exercise[ex_name] = []
            compound_by_exercise[ex_name].append(item)
        
        isolation_by_exercise = {}
        for item in isolation_exercises:
            ex_name = item[0]
            if ex_name not in isolation_by_exercise:
                isolation_by_exercise[ex_name] = []
            isolation_by_exercise[ex_name].append(item)
        
        # Сортируем упражнения по весу (убывание) - сначала более тяжелые и объемные
        sorted_compound = sorted(compound_by_exercise.items(), key=lambda x: exercise_weight(x[1]), reverse=True)
        sorted_isolation = sorted(isolation_by_exercise.items(), key=lambda x: exercise_weight(x[1]), reverse=True)
        
        # Восстанавливаем список items с правильным порядком
        new_items = []
        
        # Добавляем базовые упражнения (от самых тяжелых к легким)
        for ex_name, items in sorted_compound:
            # Внутри каждого упражнения сортируем подходы: light -> medium -> heavy
            items.sort(key=lambda x: {'light': 0, 'medium': 1, 'heavy': 2}[x[2]])
            new_items.extend(items)
        
        # Добавляем изолирующие упражнения (от самых тяжелых к легким)
        for ex_name, items in sorted_isolation:
            # Внутри каждого упражнения сортируем подходы: light -> medium -> heavy
            items.sort(key=lambda x: {'light': 0, 'medium': 1, 'heavy': 2}[x[2]])
            new_items.extend(items)
        
        days_info[d]['items'] = new_items

    # Рассчитываем итоговый объем
    for d in days_info:
        total_stim = 0.0
        for ex, base, ex_type, perf in days_info[d]['items']:
            total_stim += perf
            for mg, c in exercises[ex]['muscles'].items():
                mg_total_volume[mg] += base * c * STIM_FACTORS[ex_type]
        days_info[d]['total_stim'] = total_stim

    return days_info, mg_total_volume

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
    
    for week in range(weeks):
        target_volume_mg = {mg: {'min': v['min'], 'max': v['max']} for mg, v in base_target_volume_mg.items()}
        
        if progression_type == 'linear':
            for mg in target_volume_mg:
                step = compound_step if mg in {'Грудь', 'Трапеция', 'Широчайшие', 'Ягодицы', 'Бедра задняя', 'Квадрицепс'} else isolation_step
                target_volume_mg[mg]['min'] += step * week
                target_volume_mg[mg]['max'] += step * week
        elif progression_type == 'wave':
            cycle_week = week % 3
            cycle = week // 3
            for mg in target_volume_mg:
                step = compound_step if mg in {'Грудь', 'Трапеция', 'Широчайшие', 'Ягодицы', 'Бедра задняя', 'Квадрицепс'} else isolation_step
                if cycle_week == 0:
                    target_volume_mg[mg]['min'] = base_target_volume_mg[mg]['min'] + (cycle * step * 0.5)
                    target_volume_mg[mg]['max'] = base_target_volume_mg[mg]['max'] + (cycle * step * 0.5)
                else:
                    target_volume_mg[mg]['min'] = base_target_volume_mg[mg]['min'] + (cycle * step * 0.5) + (cycle_week * step)
                    target_volume_mg[mg]['max'] = base_target_volume_mg[mg]['max'] + (cycle * step * 0.5) + (cycle_week * step)

        ex_week_sets, ex_sets_per_day = allocate_sets_per_exercise(exercises, target_volume_mg, train_days_idx, ex_to_days)
        ex_week_sets_int = {ex: math.ceil(v) for ex, v in ex_week_sets.items()}
        days_info, mg_total_volume = distribute_sets_to_days_int(ex_week_sets_int, ex_sets_per_day, ex_to_days, schedule, exercises, target_volume_mg)

        rows = []
        for d in sorted(days_info.keys()):
            # Группируем подходы по упражнениям для правильной сортировки
            exercise_groups = {}
            for ex, base, ex_type, perf in days_info[d]['items']:
                if ex not in exercise_groups:
                    exercise_groups[ex] = []
                exercise_groups[ex].append({
                    'type': ex_type,
                    'sets': base,
                    'perf': perf
                })
            
            # Вычисляем вес упражнения для сортировки
            def get_exercise_weight(approaches):
                weight = 0
                for approach in approaches:
                    if approach['type'] == 'heavy':
                        weight += approach['sets'] * 3
                    elif approach['type'] == 'medium':
                        weight += approach['sets'] * 2
                    else:  # light
                        weight += approach['sets'] * 1
                return weight
            
            # Сортируем упражнения: сначала базовые, потом изолирующие, внутри по весу (убывание)
            compound_exercises = []
            isolation_exercises = []
            
            for ex_name, approaches in exercise_groups.items():
                exercise_data = {
                    'name': ex_name,
                    'type': exercises[ex_name]['type'],
                    'approaches': approaches,
                    'weight': get_exercise_weight(approaches)
                }
                if exercises[ex_name]['type'] == 'compound':
                    compound_exercises.append(exercise_data)
                else:
                    isolation_exercises.append(exercise_data)
            
            # Сортируем базовые упражнения по весу (убывание)
            compound_exercises.sort(key=lambda x: x['weight'], reverse=True)
            # Сортируем изолирующие упражнения по весу (убывание)
            isolation_exercises.sort(key=lambda x: x['weight'], reverse=True)
            
            # Собираем все упражнения в правильном порядке
            sorted_exercises = compound_exercises + isolation_exercises
            
            # Добавляем данные в таблицу
            for exercise_data in sorted_exercises:
                ex_name = exercise_data['name']
                # Сортируем подходы внутри упражнения: light -> medium -> heavy
                exercise_data['approaches'].sort(key=lambda x: {'light': 0, 'medium': 1, 'heavy': 2}[x['type']])
                
                for approach in exercise_data['approaches']:
                    rpe = RPE_BY_TYPE[approach['type']]
                    rec = recommend_reps_for_exercise(ex_name, exercises, GOAL)
                    reps = f"{rec['est_reps']} (range {rec['range']})" if rec['est_reps'] is not None else f"hold time: {rec['hold_time_s']}s"
                    
                    rows.append({
                        'Day': d + 1,  # +1 для удобства чтения (День 1, День 2...)
                        'Exercise': ex_name,
                        'Exercise Type': exercises[ex_name]['type'],
                        'Set Type': approach['type'],
                        'Sets': approach['sets'],
                        'RPE': rpe,
                        'Performed Stimulus': approach['perf'],
                        'Reps': reps,
                        'Target TUT (s)': rec['target_tut_s']
                    })

        df = pd.DataFrame(rows)
        
        # Дополнительная сортировка для гарантии правильного порядка
        df['Exercise_Type_Order'] = df['Exercise Type'].map({'compound': 0, 'isolation': 1})
        df['Set_Type_Order'] = df['Set Type'].map({'light': 0, 'medium': 1, 'heavy': 2})
        
        # Создаем порядок упражнений внутри дня
        exercise_order = {}
        current_order = 0
        for ex_name in df[df['Day'] == (sorted(days_info.keys())[0] + 1)]['Exercise'].unique():
            exercise_order[ex_name] = current_order
            current_order += 1
        
        df['Exercise_Order'] = df['Exercise'].map(exercise_order)
        
        df = df.sort_values(['Day', 'Exercise_Type_Order', 'Exercise_Order', 'Set_Type_Order'], 
                           ascending=[True, True, True, True])
        
        df = df.drop(['Exercise_Type_Order', 'Set_Type_Order', 'Exercise_Order'], axis=1)

        plan = {
            'week': week + 1,
            'target_volume_mg': target_volume_mg,
            'ex_week_sets': ex_week_sets,
            'ex_week_sets_int': ex_week_sets_int,
            'days_info': days_info,
            'mg_total_volume': mg_total_volume,
            'df': df
        }

        volume_analysis = analyze_volume_shortfalls(
            plan['mg_total_volume'], 
            plan['target_volume_mg'],
            exercises,
            plan['ex_week_sets_int'],
            ex_to_days
        )
        plan['volume_analysis'] = volume_analysis
        progression_plans.append(plan)

    return progression_plans

def build_plan_streamlit(selected_muscles, split, train_days, progression_type, compound_step, isolation_step, selected_cardio, use_custom_settings=False):
    # Используем кастомные или стандартные настройки
    if use_custom_settings and 'custom_volumes' in st.session_state:
        target_volume_mg = {}
        for mg in selected_muscles:
            if mg in st.session_state.custom_volumes:
                target_volume_mg[mg] = st.session_state.custom_volumes[mg].copy()
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
        use_custom_selection=use_custom_settings
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
                default=all_muscles  # Первые 6 по умолчанию
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
            "Использовать кастомные настройки упражнений и объемов", 
            value=False,
            help="Если отмечено, будут использоваться настройки из вкладки 'Упражнения'"
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
                use_container_width=True,
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
            
            # Инициализируем выбранные упражнения для всех мышечных групп
            for mg in mg_to_exs.keys():
                if mg not in st.session_state.selected_exercises_by_muscle:
                    # По умолчанию выбираем первое упражнение для каждой группы
                    st.session_state.selected_exercises_by_muscle[mg] = mg_to_exs[mg][:1] if mg_to_exs[mg] else []
            
            # Показываем все мышечные группы сразу для выбора упражнений
            st.markdown("**Выберите упражнения для каждой мышечной группы:**")
            
            all_exercises_selected = {}
            
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
            
            # Отображение программы по дням
            for day in sorted(plan['days_info'].keys()):
                with st.expander(f"День {day + 1}", expanded=True):
                    day_data = plan['days_info'][day]
                    
                    if not day_data['items']:
                        st.write("Отдых")
                        continue
                    
                    # Показываем сводку по типам подходов
                    set_types = day_data.get('set_types', {'light': 0, 'medium': 0, 'heavy': 0})
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Тяжелые подходы", set_types['heavy'] or "-")
                    with col2:
                        st.metric("Средние подходы", set_types['medium'] or "-")
                    with col3:
                        st.metric("Легкие подходы", set_types['light'] or "-")
                    with col4:
                        st.metric("Общая стимуляция", f"{day_data['total_stim']:.1f}")
                    
                    # Группируем подходы по упражнениям для лучшего отображения
                    exercise_groups = {}
                    for ex, base, ex_type, perf in day_data['items']:
                        if ex not in exercise_groups:
                            exercise_groups[ex] = []
                        exercise_groups[ex].append({
                            'type': ex_type,
                            'sets': base,
                            'perf': perf
                        })
                    
                    # Создаем таблицу для дня
                    day_df_data = []
                    for ex_name in exercise_groups.keys():
                        # Получаем тип упражнения
                        exercise_type = st.session_state.selected_exercises[ex_name]['type']
                        
                        # Для каждого типа подхода в упражнении
                        for approach in exercise_groups[ex_name]:
                            rec = recommend_reps_for_exercise(ex_name, st.session_state.selected_exercises, GOAL)
                            if rec['est_reps'] is not None:
                                reps_info = f"{rec['est_reps']} (диапазон {rec['range']})"
                            else:
                                reps_info = f"удержание: {rec['hold_time_s']}с"
                            
                            day_df_data.append({
                                'Упражнение': ex_name,
                                'Тип упражнения': exercise_type,
                                'Тип подхода': approach['type'],
                                'Подходы': approach['sets'],
                                'RPE': RPE_BY_TYPE[approach['type']],
                                'Повторения': reps_info,
                                'Выполнено': approach['perf']
                            })
                    
                    if day_df_data:
                        day_df = pd.DataFrame(day_df_data)
                        # Сортируем: сначала базовые, потом изолирующие, внутри по упражнениям
                        day_df['Type_Order'] = day_df['Тип упражнения'].map({'compound': 0, 'isolation': 1})
                        day_df['Exercise_Order'] = day_df.groupby('Упражнение')['Тип подхода'].transform(
                            lambda x: x.map({'light': 0, 'medium': 1, 'heavy': 2}).max()
                        )
                        day_df = day_df.sort_values(['Type_Order', 'Exercise_Order', 'Тип подхода'], 
                                                ascending=[True, False, True])
                        day_df = day_df.drop(['Type_Order', 'Exercise_Order'], axis=1).sort_index()
                        
                        st.dataframe(day_df, use_container_width=True)
                        st.metric("Общая стимуляция дня", f"{day_data['total_stim']:.1f}")
    
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
                st.dataframe(volume_df, use_container_width=True)
            
            with col2:
                st.subheader("Выбранные упражнения")
                exercises_list = list(st.session_state.selected_exercises.keys())
                for i, ex in enumerate(exercises_list, 1):
                    st.write(f"{i}. {ex}")
                
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
                        
                        # Рекомендации по улучшению
                        st.write("**💡 Рекомендации:**")
                        recommendations = []
                        
                        if "Нет упражнений" in analysis['reasons'][0]:
                            recommendations.append("Добавьте упражнения, нацеленные на эту мышечную группу")
                        
                        if "Недостаточно общего объема" in analysis['reasons'][0]:
                            recommendations.append("Увеличьте количество подходов для существующих упражнений")
                            recommendations.append("Добавьте дополнительные упражнения для этой группы")
                        
                        if "Ограниченное количество тренировочных дней" in analysis['reasons'][0]:
                            recommendations.append("Распределите нагрузку на большее количество тренировочных дней")
                        
                        if "Нет упражнений с высокой вовлеченностью" in analysis['reasons'][0]:
                            recommendations.append("Добавьте упражнения с высокой вовлеченностью этой МГ")
                        
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
                    'Легкие подходы': total_light,
                    'Средние подходы': total_medium,
                    'Тяжелые подходы': total_heavy,
                    'Всего подходов': total_light + total_medium + total_heavy
                })
            
            set_type_df = pd.DataFrame(set_type_summary)
            st.dataframe(set_type_df, use_container_width=True)

            st.subheader("Экспорт в Excel")
            
            # Создаем Excel файл со всеми неделями
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                for week, plan in enumerate(st.session_state.progression_plans, 1):
                    # Основная программа
                    plan['df'].to_excel(writer, sheet_name=f'Week_{week}', index=False)
                    
                    # Добавляем лист с объемами
                    volume_data = []
                    for mg, vol in sorted(plan['mg_total_volume'].items()):
                        min_vol = plan['target_volume_mg'][mg]['min']
                        max_vol = plan['target_volume_mg'][mg]['max']
                        volume_data.append({
                            'Мышечная группа': mg,
                            'Объем': vol,
                            'Целевой минимум': min_vol,
                            'Целевой максимум': max_vol,
                            'Статус': 'OK' if min_vol <= vol <= max_vol else 'LOW' if vol < min_vol else 'HIGH'
                        })
                    
                    volume_df = pd.DataFrame(volume_data)
                    volume_df.to_excel(writer, sheet_name=f'Volumes_Week_{week}', index=False)
                    
                    # Добавляем лист со сводкой по типам подходов
                    set_type_data = []
                    for day in sorted(plan['days_info'].keys()):
                        day_info = plan['days_info'][day]
                        set_types = day_info.get('set_types', {'light': 0, 'medium': 0, 'heavy': 0})
                        set_type_data.append({
                            'День': day + 1,
                            'Легкие подходы': set_types['light'],
                            'Средние подходы': set_types['medium'],
                            'Тяжелые подходы': set_types['heavy'],
                            'Всего подходов': set_types['light'] + set_types['medium'] + set_types['heavy'],
                            'Общая стимуляция': day_info['total_stim']
                        })
                    
                    set_type_day_df = pd.DataFrame(set_type_data)
                    set_type_day_df.to_excel(writer, sheet_name=f'Set_Types_Week_{week}', index=False)
                
            buffer.seek(0)
            
            st.download_button(
                label="📥 Скачать полную программу (Excel)",
                data=buffer,
                file_name="training_program.xlsx",
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
                # CSV выгрузка программы
                csv_program = plan['df'].to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                st.download_button(
                    label=f"📥 Скачать программу недели {selected_week_export} (CSV)",
                    data=csv_program,
                    file_name=f"training_week_{selected_week_export}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # CSV выгрузка объемов
                volume_data = []
                for mg, vol in sorted(plan['mg_total_volume'].items()):
                    min_vol = plan['target_volume_mg'][mg]['min']
                    max_vol = plan['target_volume_mg'][mg]['max']
                    volume_data.append({
                        'Мышечная группа': mg,
                        'Объем': vol,
                        'Целевой минимум': min_vol,
                        'Целевой максимум': max_vol
                    })
                
                volume_df = pd.DataFrame(volume_data)
                csv_volume = volume_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                st.download_button(
                    label=f"📥 Скачать объемы недели {selected_week_export} (CSV)",
                    data=csv_volume,
                    file_name=f"volumes_week_{selected_week_export}.csv",
                    mime="text/csv"
                )
                
if __name__ == "__main__":
    main()