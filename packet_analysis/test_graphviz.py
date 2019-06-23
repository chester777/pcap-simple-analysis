from graphviz import Digraph

dot = Digraph(comment='The Round Table', format='png')

dot.node('A', 'King Arthur')
dot.node('A', 'King Arthur')
dot.node('B', '<<u>Sir Bedevere the Wise</u>>', URL="http://iamaman.tistory.com/", target="_blank")
dot.node('L', 'Sir Lancelot the Brave')

dot.edges(['AC', 'AL'])
dot.edge('B', 'L', constraint='false')

print(dot.source)  # doctest: +NORMALIZE_WHITESPACE
dot.render('round-table', view=True)
