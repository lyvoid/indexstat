from utils.tool import *
from dao.models import *


logging.basicConfig(level=logging.INFO)
date_today = get_today_date()
# get yesterday value
date_yest = get_yest_date(date_today)
date_yy = get_yest_date(date_yest)
sz_values_yy = SZIndexStat()
if not sz_values_yy.load({'date': str(date_yy)}):
    logging.error('cannot get index value of the day before yesterday')
    exit(0)

sz_values_y = SZIndexStat()
if sz_values_y.load({'date': str(date_yest)}):
    logging.info(
        'yesterday sz index value is exist. value: %s' %
        sz_values_y.today_index_value)
else:
    # if yesterday index value is not in database, update new average date
    # in this case, i don't care whether yesterday is trade day or not
    # save yesterday index value to database
    sz_values_y.date = str(date_yest)
    sz_values_y.today_index_value = get_yest_sz_index()
    # calculate new average of 30 90 180 days' value
    sz_values_tail = SZIndexStat()
    sz_values_head = SZIndexStat()

    sz_values_tail.load({'date': str(get_next_n_date(date_yest, -30 + 15))})
    # need delete, -1 more
    sz_values_head.load({'date': str(get_next_n_date(date_yest, -30 - 15 - 1))})
    sz_values_y.avg_30_index = (
                                   sz_values_yy.avg_30_index * 31 +
                                   sz_values_tail.today_index_value -
                                   sz_values_head.today_index_value
                               ) / 31

    sz_values_tail.load({'date': str(get_next_n_date(date_yest, - 90 + 15))})
    sz_values_head.load({'date': str(get_next_n_date(date_yest, - 90 - 15 - 1))})
    sz_values_y.avg_90_index = (
                                   sz_values_yy.avg_90_index * 31 +
                                   sz_values_tail.today_index_value -
                                   sz_values_head.today_index_value
                               ) / 31

    sz_values_tail.load({'date': str(get_next_n_date(date_yest, - 180 + 15))})
    sz_values_head.load({'date': str(get_next_n_date(date_yest, - 180 - 15 - 1))})
    sz_values_y.avg_180_index = (
                                    sz_values_yy.avg_180_index * 31 +
                                    sz_values_tail.today_index_value -
                                    sz_values_head.today_index_value
                                ) / 31

    sz_values_y.commit()


cur_30_rate = sz_values_y.today_index_value / sz_values_y.avg_30_index - 1
cur_90_rate = sz_values_y.today_index_value / sz_values_y.avg_90_index - 1
cur_180_rate = sz_values_y.today_index_value / sz_values_y.avg_180_index - 1

send_email(
    '735600970@qq.com',
    '统计信息',
    'yesterday:%s\n'
    'avg30:%s\navg90:%s\navg180:%s\n--------\n'
    'avg30rate:%s\navg90rate:%s\navg180rate:%s' %
    (sz_values_y.today_index_value, sz_values_y.avg_30_index,
     sz_values_y.avg_90_index, sz_values_y.avg_180_index,
     cur_30_rate, cur_90_rate, cur_180_rate)
)
