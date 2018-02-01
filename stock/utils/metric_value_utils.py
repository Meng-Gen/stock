def normalize(metric_value):
    if metric_value == u'N/A':
        return 0
    else:
        return float(metric_value.replace(",", ""))
