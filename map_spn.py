def get_spn(toponym):
    lower = toponym["boundedBy"]["Envelope"]["lowerCorner"].split()
    upper = toponym["boundedBy"]["Envelope"]["upperCorner"].split()

    delta_1 = str(float(upper[0]) - float(lower[0]))
    delta_2 = str(float(upper[1]) - float(lower[1]))

    return ','.join([delta_1, delta_2])