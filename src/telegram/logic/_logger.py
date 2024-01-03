# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import logging
import sys
import traceback


def logger_msg(message):
    _msg = f'Logger: ' \
           f'{message}'

    logging.warning(f"{''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))}"
                    f"\n"
                    f"{_msg}")

    print(_msg)
