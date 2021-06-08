import argparse
from services import *
from serializations import *
import logging

parser = argparse.ArgumentParser()

parser.add_argument("type_of_serialization", choices=['json', 'pickle', 'toml', 'yaml', 'python'],
                    help='type of serialization', type=str)
parser.add_argument("type_of_source_serialization", choices=['json', 'pickle', 'toml', 'yaml', 'python'],
                    help='type of source serialization', type=str)
parser.add_argument("source_file", help="where get data", type=str)
parser.add_argument("result_file", help="where result", type=str)


args = parser.parse_args()
if args.type_of_source_serialization == args.type_of_serialization:
    with open(args.source_file, 'r') as source:
        with open(args.result_file, 'w') as result:
            result.write(source.read())
    logging.info('Same type of serializations')

else:
    # if args.type_of_source_serialization == 'pickle' and args.type_of_source_serialization == 'pickle'  :
    #     with open(args.source_file, 'rb') as source:
    #         with open(args.result_file, 'w') as result:

    with open(args.source_file, 'r') as source:
        with open(args.result_file, 'w') as result:
            sour = fabric.fabrica(args.type_of_source_serialization)
            if sour is not None:
                prep_obj = (sour.load(args.source_file))
            else:
                # емли питон
                prep_obj = eval(source.read())



            res = fabric.fabrica(args.type_of_serialization)
            # python if
            if res is None:
                result.write(str(prep_obj))
            else:
                prep_obj = ordinary_types.prepare_data(prep_obj)
                res.dump(prep_obj,args.result_file)
            logging.info('success')

