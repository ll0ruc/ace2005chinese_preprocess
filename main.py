import os
import copy
from parser import Parser
import json
import argparse
from tqdm import tqdm


def get_data_paths(ace2005_path):
    test_files, dev_files, train_files = [], [], []

    with open('./data_list.csv', mode='r') as csv_file:
        rows = csv_file.readlines()
        for row in rows[1:]:
            items = row.replace('\n', '').split(',')
            data_type = items[0]
            name = items[1]

            path = os.path.join(ace2005_path, name)
            if data_type == 'test':
                test_files.append(path)
            elif data_type == 'dev':
                dev_files.append(path)
            elif data_type == 'train':
                train_files.append(path)
    return test_files, dev_files, train_files

def find_all(sub, s):
    index_list = []
    index = s.find(sub)
    while index != -1:
        index_list.append(index)
        index = s.find(sub, index + 1)

    if len(index_list) > 0:
        return index_list
    else:
        return [-1]


def find_token_index(tokens, start_pos, end_pos, phrase):
    start_idx, end_idx = start_pos, end_pos
    token = tokens[start_idx: end_idx]
    if token != phrase:
        # print(tokens)
        pos = find_all(phrase, tokens)
        if pos[0] == -1:
            start_idx, end_idx = -10, -10
            print(tokens)
        elif len(pos) == 1:
            start_idx = pos[0]
            end_idx = start_idx + len(phrase)
        else:
            rela = [abs(a - start_idx) for a in pos]
            start_idx = pos[rela.index(min(rela))]
            end_idx = start_idx + len(phrase)

    return start_idx, end_idx


def preprocessing(data_type, files):
    result = []
    event_count, entity_count, sent_count = 0, 0, 0
    event_count_2 = 0

    print('-' * 20)
    print('[preprocessing] type: ', data_type)
    for file in tqdm(files):
        parser = Parser(path=file)

        entity_count += len(parser.entity_mentions)
        event_count += len(parser.event_mentions)
        sent_count += len(parser.sents_with_pos)

        for item in parser.get_data():

            data = dict()
            data['sentence'] = item['sentence']
            data['golden-entity-mentions'] = []
            data['golden-event-mentions'] = []
            tokens = item['sentence']

            sent_start_pos = item['position'][0]

            #由parser预处理的文件进一步处理，得到entity_mention在句子中的相对位置
            for entity_mention in item['golden-entity-mentions']:
                position = entity_mention['position']
                start_idx, end_idx = find_token_index(
                    tokens=tokens,
                    start_pos=position[0] - sent_start_pos,
                    end_pos=position[1] - sent_start_pos + 1,
                    phrase=entity_mention['text'],
                )

                entity_mention['start'] = start_idx
                entity_mention['end'] = end_idx

                del entity_mention['position']

                data['golden-entity-mentions'].append(entity_mention)

            # 由parser预处理的文件进一步处理，得到event_mention在句子中的相对位置
            for event_mention in item['golden-event-mentions']:
                # same event mention cab be shared
                event_mention = copy.deepcopy(event_mention)
                position = event_mention['trigger']['position']
                start_idx, end_idx = find_token_index(
                    tokens=tokens,
                    start_pos=position[0] - sent_start_pos,
                    end_pos=position[1] - sent_start_pos + 1,
                    phrase=event_mention['trigger']['text'],
                )
                event_mention['trigger']['start'] = start_idx
                event_mention['trigger']['end'] = end_idx
                del event_mention['trigger']['position']
                del event_mention['position']

                # 由parser预处理的文件进一步处理，得到arguments在句子中的相对位置
                arguments = []
                for argument in event_mention['arguments']:
                    position = argument['position']
                    start_idx, end_idx = find_token_index(
                        tokens=tokens,
                        start_pos=position[0] - sent_start_pos,
                        end_pos=position[1] - sent_start_pos + 1,
                        phrase=argument['text'],
                    )
                    argument['start'] = start_idx
                    argument['end'] = end_idx
                    del argument['position']

                    arguments.append(argument)

                event_mention['arguments'] = arguments
                data['golden-event-mentions'].append(event_mention)

            
            result.append(data)

    print('sent_count :', sent_count)
    print('event_count :', event_count)
    print('entity_count :', entity_count)


    with open('output/{}.json'.format(data_type), 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help="Path of ACE2005 English data", default='./data/ace_2005_td_v7/data/Chinese')
    args = parser.parse_args()
    test_files, dev_files, train_files = get_data_paths(args.data)

    preprocessing('test', test_files)
    preprocessing('dev', dev_files)
    preprocessing('train', train_files)


