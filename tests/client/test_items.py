import json

import pytest
from six.moves import range

from scrapinghub.hubstorage.serialization import mpdecode


def _add_test_items(job):
    for i in range(3):
        job.items.write({'id': i, 'data': 'data' + str(i)})
    job.items.flush()
    job.items.close()


def test_items_iter(spider):
    job = spider.jobs.schedule(meta={'state': 'running'})
    _add_test_items(job)

    o = job.items.iter()
    assert next(o) == {'id': 0, 'data': 'data0'}
    assert next(o) == {'id': 1, 'data': 'data1'}
    next(o)
    with pytest.raises(StopIteration):
        next(o)

    o = job.items.iter(offset=2)
    assert next(o) == {'id': 2, 'data': 'data2'}
    with pytest.raises(StopIteration):
        next(o)

    o = job.items.iter_raw_json(offset=2)
    item = json.loads(next(o))
    assert item['id'] == 2
    assert item['data'] == 'data2'
    with pytest.raises(StopIteration):
        next(o)

    msgpacked_o = job.items.iter_raw_msgpack(offset=2)
    o = mpdecode(msgpacked_o)
    assert item['id'] == 2
    assert item['data'] == 'data2'


def test_items_list(spider):
    job = spider.jobs.schedule(meta={'state': 'running'})
    _add_test_items(job)

    o = job.items.list()
    assert isinstance(o, list)
    assert len(o) == 3
    assert o[0] == {'id': 0, 'data': 'data0'}
    assert o[1] == {'id': 1, 'data': 'data1'}
    assert o[2] == {'id': 2, 'data': 'data2'}
