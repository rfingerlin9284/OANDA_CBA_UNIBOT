def reallocate_strategy_budget(strategy_stats):
    for strat, stats in strategy_stats.items():
        if stats['win_rate'] > 0.7:
            stats['alloc'] *= 1.2
        else:
            stats['alloc'] *= 0.8
    return strategy_stats
