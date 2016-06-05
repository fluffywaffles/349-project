import json

nominal_headers = [ 'developer', 'publisher', 'appid', 'name' ]

def run ():
    with open("./unwrapped-data.json") as json_file:
        json_data = json.load(json_file)

    headers   = json_data[0].keys()
    game_data = [ game.values() for game in json_data ]

    nominal_values = [
        set([ process(game[nominal]) for game in json_data ]) for nominal in nominal_headers
    ]

    attributes = {}

    for header in headers:
        nominal = nominal_headers.index(header) if header in nominal_headers else False
        attributes[header] = {
            'type': 'nominal' if nominal is not False else 'numeric',
            'data': sorted(nominal_values[nominal]) if nominal is not False else set()
        }

    with open("out.arff", 'w') as out:
        out.write('@RELATION fuckinarff\n\n')

        for name, info in attributes.items():
            type, attr_data = info['type'], info['data']
            possible = '{ ' + ','.join(attr_data) + '}'

            decl = [ '@ATTRIBUTE', process(name) ]
            if attr_data:
                decl.append(possible)
            else:
                decl.append(type)

            out.write(' '.join(decl))
            out.write('\n')

        game_data_processed = sorted([
            process_game(game) for game in game_data
        ])

        data = '\n'.join(game_data_processed)

        out.write('\n')
        out.write('@DATA\n')
        out.write(data)


def process (field):
    sf = ''.join(str(field).replace(',', '').replace('\'', '').lower())
    if sf == '':
        return '?'
    else:
        return sf if type(field) is not str else "'" + sf + "'"

def process_game (game_datum):
    processed = [ process(item) for item in game_datum ]
    return ','.join(processed)

if __name__ == '__main__':
    run()

