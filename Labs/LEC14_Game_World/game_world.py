#게임 월드 리스트 초기화
world = [ [], [] ]  #객체들의 리스트, 빈 리스트

#객체들을 리스트에 추가하는 함수
def add_object(o, depth = 0):
    world[depth].append(o)

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return

#게임 로직
def update():
    for layer in world:
        for o in layer:
            o.update()  #객체들의 update() 호출

#게임 월드 렌더링
def render():
    for layer in world:
        for o in layer:
            o.draw()  #객체들의 draw() 호출