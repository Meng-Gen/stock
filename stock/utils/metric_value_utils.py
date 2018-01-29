def normalize(metric_value):
    if metric_value == u'N/A':
        return 0
    else:
        return int(metric_value.replace(",", ""))