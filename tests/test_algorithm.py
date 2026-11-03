import io
import math

import openpyxl

import app


def build_plan(split='full_body', days=3, progression='linear', selected=None):
    selected = selected or app.DEFAULT_SELECTED_MUSCLES
    exercises = app.select_exercises_interactively(selected, split=split, train_days=days)
    schedule = app.make_week_schedule(days)
    train_days = app.list_training_days(schedule)
    ex_to_days = app.assign_exercise_days_by_split(exercises, train_days, split)
    targets = {mg: app.DEFAULT_TARGET_VOLUME_MG[mg].copy() for mg in selected}
    plans = app.generate_progression_plan(
        targets, exercises, train_days, ex_to_days, split, schedule,
        progression, 0.5, 0.3, 9
    )
    return plans, exercises, train_days, ex_to_days


def test_default_full_body_progresses_without_plateaus():
    plans, _, _, _ = build_plan('full_body', 3)
    totals = [sum(plan['ex_week_sets_int'].values()) for plan in plans]

    assert all(totals[i] >= totals[i - 1] for i in range(1, len(totals)))
    assert all(totals[i] - totals[i - 1] <= 5 for i in range(1, len(totals)))
    assert not any(totals[i] == totals[i - 1] for i in range(1, len(totals)))


def test_auto_selection_is_compact_and_has_both_types():
    exercises = app.select_exercises_interactively(
        app.DEFAULT_SELECTED_MUSCLES, split='full_body', train_days=3
    )
    types = {app.EXERCISES[ex]['type'] for ex in exercises}

    assert len(exercises) <= 9
    assert 'compound' in types
    assert 'isolation' in types


def test_day_limits_and_compound_before_isolation():
    plans, exercises, _, _ = build_plan('full_body', 3)

    for plan in plans:
        for day_info in plan['days_info'].values():
            day_sets = sum(item[1] for item in day_info['items'])
            assert day_sets <= app.MAX_SETS_PER_DAY

            types = [exercises[item[0]]['type'] for item in day_info['items']]
            if 'compound' in types and 'isolation' in types:
                last_compound = max(i for i, t in enumerate(types) if t == 'compound')
                first_isolation = min(i for i, t in enumerate(types) if t == 'isolation')
                assert last_compound < first_isolation


def test_ppl_forearm_exercises_are_assigned_to_pull_day():
    exercises = app.select_exercises_interactively(
        list(app.DEFAULT_TARGET_VOLUME_MG.keys()), split='push_pull_legs', train_days=3
    )
    schedule = app.make_week_schedule(3)
    train_days = app.list_training_days(schedule)
    ex_to_days = app.assign_exercise_days_by_split(exercises, train_days, 'push_pull_legs')

    for ex_name, days in ex_to_days.items():
        primary = app.primary_muscle(ex_name, exercises)
        if primary in app.PULL_MUSCLES:
            assert days == [train_days[1]], (ex_name, days)


def test_wave_progression_has_deload_weeks():
    plans, _, _, _ = build_plan('full_body', 3, 'wave')

    assert plans[3]['is_deload']
    assert plans[6]['is_deload']
    assert plans[3]['intensity_pct'] < plans[2]['intensity_pct']
    assert plans[6]['intensity_pct'] < plans[5]['intensity_pct']


def test_set_type_split_keeps_average_stimulus_equal_to_sets():
    for total_sets in range(1, 20):
        parts = app.split_set_types(total_sets)
        stimulus = sum(app.STIM_FACTORS[set_type] * count for set_type, count in parts)
        assert math.isclose(stimulus, total_sets)


def test_export_dataframe_is_russian_and_without_extra_parentheses():
    plans, _, _, _ = build_plan('full_body', 3)
    export_df = plans[0]['export_df']

    assert list(export_df.columns) == app.EXPORT_COLUMNS
    assert 'Повторения' in export_df.columns
    assert 'Диапазон повторений' in export_df.columns

    for value in export_df['Диапазон повторений']:
        assert '(' not in str(value)
        assert ')' not in str(value)
        assert '–' in str(value)

    for value in export_df['Упражнение']:
        assert '(' not in str(value)
        assert ')' not in str(value)

    assert set(export_df['Тип упражнения']) <= {'Базовое', 'Изолирующее'}
    assert set(export_df['Тип подхода']) <= {'Тяжёлый', 'Средний', 'Лёгкий'}


def test_excel_export_has_russian_sheets_and_separating_style():
    plans, exercises, _, _ = build_plan('full_body', 3)
    buffer = app.build_excel_export(plans, exercises)
    workbook = openpyxl.load_workbook(io.BytesIO(buffer.getvalue()))

    assert workbook.sheetnames[0] == 'Сводка'
    assert 'Неделя 1' in workbook.sheetnames
    assert 'Объём 1' in workbook.sheetnames
    assert 'Подходы 1' in workbook.sheetnames

    sheet = workbook['Неделя 1']
    assert sheet.freeze_panes == 'A5'
    assert sheet['A4'].font.bold
    assert sheet['A4'].fill.fgColor.rgb.endswith('1F4E78')

    # Между днями должна быть заметная разделительная линия.
    for row in range(5, sheet.max_row):
        if sheet.cell(row=row, column=1).value != sheet.cell(row=row + 1, column=1).value:
            assert sheet.cell(row=row, column=1).border.bottom.style == 'medium'
            break
    else:
        raise AssertionError('Не найден разделитель между днями')
