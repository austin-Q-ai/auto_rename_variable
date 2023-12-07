import string
from parser.changeVar import changeVar
from parser.parse import parse


def check_variable(methodStr, oldVar, newVar):
    new_method = changeVar(methodStr, oldVar, newVar)
    try:
        parse(new_method)
        return True
    except:
        return False

def filter_result(predictions, methodStr, variables, old_var, top_nums):
    special_characters = set(string.punctuation)

    # Filtering out single-character words
    words = list(set([word for sublist in predictions for word in sublist if word not in variables]))

    filtered_words = [word for word in words if not any(char in special_characters for char in word)]
    vaild_variables = [word for word in filtered_words if check_variable(methodStr, old_var, word)]
    default_value = 0


    # Create a new dictionary with keys from the list and all values set to the default value
    rank_dict = {key: default_value for key in vaild_variables}

    for ele in predictions:
        for i, var in enumerate(ele):
            if var in vaild_variables:
                rank_dict[var] += top_nums - i

    # print(rank_dict)
    return dict(sorted(rank_dict.items(), key=lambda item: item[1], reverse=True))


methodStr = '''
async def main(args: argparse.Namespace):
    logger.info("starting scan...")

    if args.address:
        device = await BleakScanner.find_device_by_address(
            args.address, cb=dict(use_bdaddr=args.macos_use_bdaddr)
        )
        if device is None:
            logger.error("could not find device with address '%s'", args.address)
            return
    else:
        device = await BleakScanner.find_device_by_name(
            args.name, cb=dict(use_bdaddr=args.macos_use_bdaddr)
        )
        if device is None:
            logger.error("could not find device with name '%s'", args.name)
            return

    logger.info("connecting to device...")

    async with BleakClient(
        device,
        services=args.services,
    ) as client:
        logger.info("connected")

        for service in client.services:
            logger.info("[Service] %s", service)

            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = await client.read_gatt_char(char.uuid)
                        logger.info(
                            "  [Characteristic] %s (%s), Value: %r",
                            char,
                            ",".join(char.properties),
                            value,
                        )
                    except Exception as e:
                        logger.error(
                            "  [Characteristic] %s (%s), Error: %s",
                            char,
                            ",".join(char.properties),
                            e,
                        )

                else:
                    logger.info(
                        "  [Characteristic] %s (%s)", char, ",".join(char.properties)
                    )

                for descriptor in char.descriptors:
                    try:
                        value = await client.read_gatt_descriptor(descriptor.handle)
                        logger.info("    [Descriptor] %s, Value: %r", descriptor, value)
                    except Exception as e:
                        logger.error("    [Descriptor] %s, Error: %s", descriptor, e)

        logger.info("disconnecting...")

    logger.info("disconnected")
'''

# print(check_variable(methodStr, 'return'))
# predictions = [['handler', 'def', 'return', ')', 'appl??ication'], ['products', 'p', 'server', 'c', ')'], ['handler', '.', ')', 'route', 'app']]
# print(filter_result(predictions, methodStr, 5))