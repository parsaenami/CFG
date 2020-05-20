terminals = []
variables = []
graph = dict()
adjacent = []
out = []


def filling():
    for n in range(97, 123):
        terminals.append(chr(n))
    for m in range(65, 91):
        variables.append(chr(m))


def read_data():
    grammar_count = int(input('***NOTICE: Consider "$" As λ***\nPlease Enter The Number Of Rules: '))
    rules = dict()

    while grammar_count != 0:
        grammar_in = input()
        left_variable, right_variables = grammar_in.split('->')[0], grammar_in.split('->')[1].split('|')

        if left_variable in rules.keys():
            rules[left_variable] += right_variables
        else:
            rules[left_variable] = right_variables

        grammar_count -= 1

    return rules


def lambda_finder(rule, v):
    tmp = rule
    if rule == '':
        return

    if terminal_finder(rule):
        out.append(rule)

    for i in v:
        if i in rule:
            if tmp not in out:
                out.append(tmp)

            if tmp[:tmp.index(i)] + tmp[tmp.index(i) + 1:] not in out:
                out.append(tmp[:tmp.index(i)] + tmp[tmp.index(i) + 1:])
                lambda_finder(tmp[:tmp.index(i)] + tmp[tmp.index(i) + 1:], v)

        else:
            out.append(rule)


def lambda_removal2(rules_in):
    rules = dict(rules_in)
    v = []
    qualified = True
    outs = []
    null = []
    rules_out = dict()

    for r1 in rules:
        if '$' in rules[r1]:
            v.append(r1)

    if len(v) == 0:
        return rules_in

    for r2 in rules:
        for i in range(len(rules[r2])):
            qualified = True
            for j in range(len(rules[r2][i])):
                if rules[r2][i][j] not in v:
                    qualified = False

        if qualified:
            v.append(r2)

    if len(v) == 0:
        return rules_in

    for x in rules_in:
        for y in rules_in[x]:
            lambda_finder(y, v)
            outs = list(set().union(outs, out))

        if outs:
            rules_out[x] = outs.copy()
        else:
            rules_out[x] = rules_in[x]

        outs.clear()
        out.clear()

    for z in rules_out:
        for t in rules_out[z]:
            if t == '' or t == '$':
                rules_out[z].remove(t)

    for m in rules_out:
        if not rules_out[m]:
            null.append(m)
            for n in rules_out:
                for p in rules_out[n]:
                    if m in p:
                        cur = p.replace(m, '')
                        rules_out[n].remove(p)
                        if cur not in rules_out[n]:
                            rules_out[n].append(cur)

    for z1 in rules_out:
        for t1 in rules_out[z1]:
            if t1 == '' or t1 == '$':
                rules_out[z1].remove(t1)

    for nu in null:
        rules_out.pop(nu)

    return rules_out


def dfs(v, rules):
    visited = dict()
    adj = []

    for r in rules:
        graph[r] = []
        visited[r] = False

        for k in rules[r]:
            if k in variables:
                graph[r].append(k)

    dfs_util(v, visited, adj)

    adjacent.append(adj)


def dfs_util(v, visited, adj):
    visited[v] = True
    adj.append(v)

    for i in graph[v]:
        if not visited[i]:
            dfs_util(i, visited, adj)


def unit_removal(rules_in):
    rules_prime = dict()
    rules_out = dict()

    for r0 in rules_in:
        rules_prime[r0] = []
        rules_out[r0] = []

    for r1 in rules_in:
        for k1 in rules_in[r1]:
            if k1 not in variables:
                rules_prime[r1].append(k1)
                rules_out[r1].append(k1)

    for r2 in rules_in:
        dfs(r2, rules_in)

    for a1 in range(len(adjacent)):
        for a2 in range(1, len(adjacent[a1])):
            rules_out[adjacent[a1][0]] += rules_prime[adjacent[a1][a2]]

    adjacent.clear()
    graph.clear()

    return rules_out


def terminal_finder(_list):
    for w in _list:
        flag = True
        for c in w:
            if c not in terminals:
                flag = False

        if flag:
            return True

    return False


def generating_finder(s, dic):
    for i in dic[s]:
        if i in terminals:
            return True
        else:
            return generating_finder(i, dic)

    return False


def useless_removal(rules_in):
    delete = []
    left = []
    right = []

    for r2 in rules_in:
        flag = False
        for r3 in rules_in[r2]:
            for r4 in r3:
                if r4 == r2:
                    flag = True
                elif r4 in variables and r4 != r2:
                    flag = False

        if terminal_finder(rules_in[r2]):
            flag = False

        if flag:
            delete.append(r2)

    for r5 in delete:
        rules_in.pop(r5)
        for r6 in rules_in:
            for r7 in rules_in[r6]:
                if r5 in r7:
                    rules_in[r6].remove(r7)

        delete.clear()

    for r8 in rules_in:
        left.append(r8)
        right += rules_in[r8]

    for r9 in left:
        for r10 in right:
            if r9 in r10:
                break
            if r9 not in r10 and r9 != 'S' and 'S' not in r10:
                for i in r10:
                    if (i in variables or terminal_finder(i)) and (r9 not in delete):
                        delete.append(r9)

    for r11 in delete:
        rules_in.pop(r11)
        for r12 in rules_in:
            for r13 in rules_in[r12]:
                if r11 in r13:
                    rules_in[r12].remove(r13)

    return rules_in


def printing(dic):
    for k in dic:
        _out = ''
        for v in dic[k]:
            _out += v + '|'
        print(f'{k}->{_out[:-1]}')


if __name__ == '__main__':
    filling()
    _read = read_data()
    _lambda = lambda_removal2(_read)
    _unit = unit_removal(_lambda)
    _useless = useless_removal(_unit)
    print()
    printing(_useless)
