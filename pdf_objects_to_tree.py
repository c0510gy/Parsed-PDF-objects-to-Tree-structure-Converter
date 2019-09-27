import pickle
import re

class pdf_to_tree(object):

    class Vertex(object):

        def __init__(self, type):
            self.type = type # 1: obj, 2: item, 3: dict, 4: arr
            if type == 1:
                self.child = dict()
            elif type == 2:
                self.child = None
            elif type == 3:
                self.child = dict()
            elif type == 4:
                self.child = []
            '''
            1: child를 사전으로 가지고 있다.
            2: child를 가지고 있지 않다.
            3: child를 사전으로 가지고 있다.
            4: child를 리스트로 가지고 있다.
            '''
            self.name = ''

        def add_child(self, idx, edge=''):
            if self.type == 4:
                self.child.append(idx)
            else:
                self.child[edge] = idx

        def set_name(self, name):
            self.name = name

    def run(self, path):
        # path = 'pdfsample.txt' # pdf의 파싱된 문자열이 저장된 위치
        f = open(path, 'r')
        par_pdf = f.read()
        f.close()

        par_pdf = re.sub(r'([0-9]+) 0 R', r' OBJ\1 ', par_pdf) # obj를 가리키는 문자열 OBJ{번호} 로 치환

        arr = re.split('obj [0-9]+ 0', par_pdf)
        objs_names = re.findall('obj [0-9]+ 0', par_pdf)
        objs = []
        max_id = 0
        for i in range(len(objs_names)):
            objs_id = int(objs_names[i].split()[1])
            max_id = max(max_id, objs_id)
            if '\n  <<' not in arr[i + 1]: # 사전이 아닌경우
                continue
            info = arr[i + 1].split('\n  <<')[1] # 오브젝트의 헤더 제거
            objs.append([objs_id, info])

        print(objs)
        print(len(objs), max_id)

        for i in range(len(objs)):
            objs[i][1] = self.parse_dict(objs[i][1], 4)
            print(objs[i][0], ':', objs[i][1]) # 각 object에 대한 parsing된 상태 출력


        # get tree
        G = [self.Vertex(1) for _ in range(max_id + 1)] # tree structure을 저장

        for obj in objs:
            for k in obj[1]:
                if k == '/Parent': # 오브젝트를 가리키지 않게 처리
                    G[obj[0]].add_child(self.make_vertex(G, obj[1][k], True), k)
                else:
                    G[obj[0]].add_child(self.make_vertex(G, obj[1][k]), k)
        
        print('number of vertices:', len(G))

        return G

    def parse_arr(self, s):
        ret = []

        s = re.sub(r'[\s]+', ' ', s) # 연속된 white space -> single space

        b = 0 # 남아 있는 여는 괄호
        t = '' # 배열 원소
        for c in s:
            if c == '[':
                if b == 1 and len(t) > 0:
                    ret.append(t)
                    t = ''
                b += 1
                if b > 1:
                    t += c
            elif c == ']':
                if b > 1:
                    t += c
                b -= 1
                if (b == 0 or b == 1) and len(t) > 0:
                    ret.append(t)
                    t = ''
            else:
                if c == ' ':
                    if b == 1 and len(t) > 0:
                        ret.append(t)
                        t = ''
                    elif b > 1:
                        t += c
                else:
                    t += c

        return ret


    def parse_dict(self, s, inden):
        ret = dict()

        s = s.split('\n' + ' ' * (inden - 2) + '>>')[0] # 마지막 >> 제거

        keyreg = r'[\n][\s]{' + re.escape(str(inden))  + r'}[\/][\S]*[\s]'
        keys = re.findall(keyreg, s)
        items = re.split(keyreg, s)

        for i in range(len(keys)):
            k = keys[i].strip()
            item = items[i + 1].strip()

            if item[0] == '[': # 배열인 경우
                ret[k] = self.parse_arr(item)
            elif item[0] == '<': # 사전인 경우
                ret[k] = self.parse_dict(item, inden + 4)
            else:
                ret[k] = item # 오브젝트, 정수형, 등등

        return ret

    def make_vertex(self, G, data, ign=False):
        v = None
        if isinstance(data, str):
            if not ign and data[:3] == 'OBJ' and data[3:].isdigit(): # 오브젝트일 경우 (/Parent 등에서 ign = True)
                return int(data[3:])
            v = self.Vertex(2)
            v.set_name(data)
        elif isinstance(data, list):
            v = self.Vertex(4)
            for i in data:
                v.add_child(self.make_vertex(G, i))
        elif isinstance(data, dict):
            v = self.Vertex(3)
            for k in data:
                v.add_child(self.make_vertex(G, data[k]), k)
        
        G.append(v)
        return len(G) - 1

if __name__ == '__main__':
    pdftot = pdf_to_tree()
    pdftot.run('./test1.txt')