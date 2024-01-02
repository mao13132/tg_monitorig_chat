# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------

sep_list = ['\n', ' ', ',', ';']


async def scrap_stop_words(stop_word_list):
    for _sep in sep_list:
        if _sep in stop_word_list:
            temp_list = [x for x in stop_word_list.split(_sep) if x != '']
            return set(temp_list)

    return [stop_word_list]
