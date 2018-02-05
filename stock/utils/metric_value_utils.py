def normalize(metric_value):
    if metric_value in [u'N/A', u'--']:
        return 0
    elif metric_value.endswith("%"):
        return float(metric_value.replace(",", "").replace("%", ""))
    else:
        return float(metric_value.replace(",", ""))
