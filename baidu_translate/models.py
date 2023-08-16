import abc
import json


class AbstractResult(abc.ABC):
    _raw: dict

    def __init__(self, raw: dict) -> None:
        self._raw = raw

    def get_errors(self):
        if 'error' in self._raw:
            return self._raw['error'], self._raw['errmsg']

    @abc.abstractmethod
    def __str__(self):
        return NotImplemented


class V2TransapiResult(AbstractResult):
    def __str__(self):
        dst = []
        for row in self._raw['trans_result']['data']:
            dst.append(row['dst'])

        return '\n'.join(dst)


class TransapiSentenceResult(AbstractResult):
    def __str__(self):
        return '\n'.join(dst['dst'] for dst in self._raw['data'])


class TransapiWordResult(AbstractResult):
    def __str__(self):
        data = json.loads(self._raw['result'])
        try:
            data = json.loads(self._raw['result'])
            dst = (data['voice'][0]['en_phonic'])

            for entry in data['content'][0]['mean']:
                dst+=' '+entry['pre']+' '
                for mean in entry['cont'].keys():
                    if dst[-1] != ' ':
                        dst+='；'
                    dst+=mean
            # default return one result
            return dst
        except:
            dst = []

            for entry in data['content'][0]['mean']:
                dst += entry['cont'].keys()
            # default return one result
            return dst[0]
