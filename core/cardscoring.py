# coding: utf-8
import logging

from alfasense.calc.asense.cards.common.scoring_rules import score_key

LOGGER = logging.getLogger('python-alfasense.calc')


def cards_scoring(cards, scorer):
    for card in cards:
        try:
            card['score'] = scorer.score(card)
            if card['score']:
                LOGGER.debug(u"Scored card {}: score is {}".format(card['key'], card['score']))
        except:
            LOGGER.error('Error in scorer', exc_info=True)
            card['score'] = 0
        try:
            card['rule_based_score'] = scorer.score_by_rules(card)
            if card['rule_based_score']:
                LOGGER.debug("Scored by rules card {}: score is {}".format(card['key'], card['rule_based_score']))
        except:
            LOGGER.error('Error in rule_based_scorer', exc_info=True)
            card['rule_based_score'] = None
    return cards


def cards_ranking(cards, features):
    occupied_positions = set([card['rule_based_score'][0] for card in cards if card['rule_based_score']])
    cards_without_rule_scores = [card for card in cards if not card['rule_based_score']]
    cards_without_rule_scores.sort(key=lambda card: card['score'], reverse=True)

    position_number = len(cards_without_rule_scores) + len(occupied_positions)
    free_positions = [position for position in range(1, position_number + 1) if position not in occupied_positions]

    for card, position in zip(cards_without_rule_scores, free_positions):
        card['rule_based_score'] = (position, 0.0)

    cards.sort(key=lambda c: c['score'], reverse=True)
    cards.sort(key=lambda c: score_key(c['rule_based_score']), reverse=True)

    card_types_prefix_down = {
        'invite': ['blank', 'nearest_atm'],
        'uber': ['blank'],
        'pfm_month_advice': ['blank'],
    }

    # теперь нужно вручную поднять некоторые карточки выше бланков
    for up_card_type, prefixes in card_types_prefix_down.items():
        up_card_pos = None
        down_card_pos = None

        # ищем инверсии и позиции, на которые нужно сдвинуть
        # самую низкую позицию у up_card_type карточек и самую высокую у бланковых
        for pos, card in enumerate(cards):
            if card['type'] == up_card_type:
                # этого типа будем переопределять до тех пор, пока не перестанет встречаться -- останется самая низкая
                up_card_pos = pos
            elif any(card['type'].startswith(tp_prefix) for tp_prefix in prefixes) and down_card_pos is None:
                # бланковые проставим лишь однажды, останется самая высокая из всех
                down_card_pos = pos

        if up_card_pos is not None and down_card_pos is not None and up_card_pos > down_card_pos:
            # есть инверсия -- поднимем нашу карточку выше, остальные сдвинем
            up_card = cards[up_card_pos]
            for pos in xrange(up_card_pos, down_card_pos, -1):
                cards[pos] = cards[pos - 1]
            cards[down_card_pos] = up_card

    for pos, card in enumerate(cards):
        # Card score to give to front-end.
        # Human readable ('-' + str(pos) + '0.' + str(score)), negative, bigger is higher in ranking
        card['score'] = -card['score'] if card['score'] else 0
        card['score'] -= pos * 10

    return cards
