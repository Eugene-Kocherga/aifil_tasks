from collections import defaultdict

def mean(values):
    return sum(values)/len(values)


def global_uniform_metric(values):
    l = len(values)
    if l <= 1:
        return 0
    m = mean(values)
    if m <= 0:
        return 0
    mse = mean([(v-m)**2 for v in values])**0.5
    normed_mse = mse/m/(l-1)**0.5
    return normed_mse


def uniform_metric_groups(normed_mse):
    limits = [0.2, 0.5]
    for i, v in enumerate(limits):
        if normed_mse < v:
            return i
    return len(limits)


def trinary_check(left, right, thresold):
    if left * thresold > right:
        return 0
    if left < right * thresold:
        return 2
    return 1


def even_scenario_big(outcome_history, income_history):
    return ('even_scenario_big', outcome_history[0], mean(outcome_history[1:]))


def even_scenario_small(outcome_history, income_history):
    return ('even_scenario_small', outcome_history[0], mean(outcome_history[1:]))


def even_scenario_normal(outcome_history, income_history):
    outcome = outcome_history[0]
    income = income_history[0]
    return {
        0: ('even_scenario_normal_negative', outcome - income),
        2: ('even_scenario_normal_positive', (income - outcome)*6),
        1: ('even_scenario_normal_neutral')
    }[trinary_check(outcome, income, 0.95)]


def first_panel_even_scenario(outcome_history, income_history):
    def last_month_behavior(outcome_history):
        return min(outcome_history[1:]) <= outcome_history[0],  outcome_history[0] <= max(outcome_history[1:])
    scenario = {
        (True, True): even_scenario_normal,
        (True, False): even_scenario_big,
        (False, True): even_scenario_small,
    }
    return scenario[last_month_behavior(outcome_history)](outcome_history, income_history)


def first_panel_uneven_scenario(current_month, prev_month):
    return {
        0: ('uneven_scenario_negative', current_month, prev_month),
        2: ('uneven_scenario_positive', current_month, prev_month),
        1: ('uneven_scenario_neutral')
    }[trinary_check(current_month, prev_month, 0.9)]    


def pfm_first_panel_info(current_month_num, by_month_outcome, by_month_income, months=3):
    outcome_history = [by_month_outcome.get(current_month_num - m, 0) for m in range(months+1)]
    previous_even_group = uniform_metric_groups(global_uniform_metric(outcome_history[1:]))
    if previous_even_group == 0:
        income_history = [by_month_income.get(current_month_num - m, 0) for m in range(months+1)]
        return first_panel_even_scenario(outcome_history, income_history)
    else:
        return first_panel_uneven_scenario(outcome_history[0], outcome_history[1])


def usage_example(operations, acc_to_cus):
    month_grouped = defaultdict(lambda : defaultdict(lambda : dict({'i': 0, 'o': 0})))
    for op in operations:
        cus = acc_to_cus[op['account']['$oid']]
        date = op['dte']
        month_num = date.year*12+date.month
        neg = op['neg']
        if neg not in {'C', 'D'}:
            continue
        direction = {'C':'i', 'D':'o'}[neg]
        if op['subtype'] in {'self_transfer'}:
            continue
        month_grouped[cus][month_num][direction] += int(op['ama'])
    scenarious = {cus: pfm_first_panel_info(max(m_slice),
                                            {k:v['o'] for k, v in m_slice.items()},
                                            {k:v['i'] for k, v in m_slice.items()},
                                            )
                  for cus, m_slice in month_grouped.items()}
    return scenarious